# -*- coding: utf-8 -*-
"""
voicebox_clone.py —— 用本机 Voicebox 克隆音色批量生成讲解音频（可断点续跑 · 绝不重复提交）

【三条铁律（吸取上一轮的教训）】
  1) 本地已有音频 → 直接跳过，绝不再生成
  2) Voicebox 里已有同一段文字的"已完成"任务 → 直接导出复用，绝不重新生成
  3) 已有"进行中"的任务 → 只等它，**绝不再提交一份**（CPU 模式单段可能要十几分钟，
     上一版因为"等超时就重试"导致 Voicebox 里堆出多份重复任务）
  4) 同一时刻只允许**一个**在跑：CPU 后端并发会把每个任务拖到十几倍慢，甚至整个队列卡死。
     本脚本启动时会先做"去重/清队"（同文本只留最早的一个进行中任务，其余取消）。

用法（命令行只传 ASCII 编号，避免 Git Bash 中文乱码）：
    python tools/voicebox_clone.py 02            # 第2讲，缺哪段补哪段
    python tools/voicebox_clone.py 13 1 18       # 第13讲，指定 1~18 段
也可以用 tools/run_clone.py 串起多讲：
    python tools/run_clone.py 02 13 14
"""
import glob
import json
import os
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from _audiohash import is_fresh, write_stamp      # noqa: E402

API = 'http://127.0.0.1:17493'
PROFILE_ID = '6a1f7579-b2e1-4ec9-98da-febeaa7f325a'   # 声纹：刘东良（克隆）
ENGINE = 'qwen'
MODEL = '0.6B'
MIN_BYTES = 200 * 1024          # 小于 200KB 视为无效
POLL = 15
MAX_WAIT = 2400                 # 单段最多等 40 分钟（CPU 模式够用），超时不重提交
STALL_WARN = 1500               # 超过这个秒数还没动静就提示（正常单段 5~15 分钟）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE_STATES = ('generating', 'queued', 'pending', 'processing')


def log(m):
    print(m, flush=True)


def health():
    try:
        return requests.get(f'{API}/health', timeout=8).status_code == 200
    except Exception:
        return False


def history():
    try:
        r = requests.get(f'{API}/history', params={'limit': 60}, timeout=30)
        return r.json().get('items', [])
    except Exception:
        return []


def cancel(gid):
    try:
        requests.post(f'{API}/generate/{gid}/cancel', timeout=30)
        return True
    except Exception:
        return False


def find_by_text(items, text):
    """在历史里找同一段文字的任务，返回 (已完成列表, 进行中列表)，按时间升序。"""
    same = [i for i in items if (i.get('text') or '') == text]
    same.sort(key=lambda x: x.get('created_at') or '')
    done = [i for i in same if i.get('status') == 'completed']
    live = [i for i in same if i.get('status') in LIVE_STATES]
    return done, live


def resolve_lecture(key):
    """
    按 ASCII 编号解析讲次目录（中文命令行参数在 Git Bash 下会乱码）。
    同名编号可能有历史遗留目录，优先取带 video/讲解脚本.json 的那个。
    """
    key = str(key).strip()
    if os.path.isdir(key):
        return os.path.abspath(key)
    cand = os.path.join(ROOT, key)
    if os.path.isdir(cand):
        return cand
    num = key.zfill(2)[:2] if key.isdigit() or key[:2].isdigit() else key
    num = key.zfill(2) if key.isdigit() else key[:2]
    hits = [d for d in glob.glob(os.path.join(ROOT, '%s_*' % num)) if os.path.isdir(d)]
    hits = [d for d in hits if os.path.basename(d)[:2] == num]
    if not hits:
        return None
    for probe in ('video/讲解脚本.json', 'docs/课件.pptx'):
        good = [h for h in hits if os.path.exists(os.path.join(h, probe))]
        if good:
            return sorted(good)[0]
    return sorted(hits)[0]


def export(gid, out_path):
    r = requests.get(f'{API}/history/{gid}/export-audio', timeout=180)
    if r.status_code != 200 or len(r.content) < MIN_BYTES:
        return False
    with open(out_path, 'wb') as f:
        f.write(r.content)
    return os.path.getsize(out_path) >= MIN_BYTES


def submit(text):
    r = requests.post(f'{API}/generate', json={
        'profile_id': PROFILE_ID, 'text': text, 'language': 'zh',
        'model_size': MODEL, 'engine': ENGINE, 'personality': False, 'normalize': True,
    }, timeout=90)
    r.raise_for_status()
    return r.json().get('id')


def wait_for(gid, label):
    """等一个已存在的任务完成。超时返回 None（调用方不得重提交）。"""
    waited = 0
    warned = False
    while waited < MAX_WAIT:
        time.sleep(POLL)
        waited += POLL
        for it in history():
            if it.get('id') == gid:
                st = it.get('status')
                if st == 'completed':
                    log('      ✅ %s 完成（等待 %ds）' % (label, waited))
                    return it
                if st in ('failed', 'cancelled'):
                    log('      ❌ %s 状态 %s' % (label, st))
                    return None
                break
        if waited % 120 == 0:
            log('      等待中… %ds（该段较长属正常，不要重提交）' % waited)
        if waited >= STALL_WARN and not warned:
            warned = True
            log('      ⚠️ 已等待 %ds 仍无产出 —— 若超过 %ds，请检查 Voicebox 应用是否还在响应'
                % (waited, MAX_WAIT))
    log('      ⏱ 等待超时（%ds）——保持原样，下次运行会继续等这一个' % MAX_WAIT)
    return None


def cleanup_queue(keep_texts=()):
    """
    队列体检：CPU 后端不适合并发。
      · 同一文本有多个进行中 → 只留最早的一个，其余取消
      · 文本已在 keep_texts（本地已有音频）→ 其所有进行中任务全部取消
    返回取消数量。
    """
    items = history()
    live = [i for i in items if i.get('status') in LIVE_STATES]
    live.sort(key=lambda x: x.get('created_at') or '')
    by_text = {}
    for it in live:
        by_text.setdefault(it.get('text') or '', []).append(it)
    killed = 0
    for text, group in by_text.items():
        if text in keep_texts:
            for it in group:
                if cancel(it['id']):
                    killed += 1
            continue
        for it in group[1:]:
            if cancel(it['id']):
                killed += 1
    if killed:
        log('[队列体检] 取消 %d 个重复/多余的进行中任务（同文本只保留最早一个）' % killed)
    return killed


def run(lecture, start=1, end=10 ** 6):
    # 流水线互斥：克隆音只允许一个进程在跑。
    # 并发提交两个任务时，Voicebox（CPU 后端）会长时间无产出，
    # 上一轮会话的残留进程正是这样把队列拖死的。
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _pipelock import acquire as _lock_acquire
    if not _lock_acquire('voicebox_clone'):
        return 3
    ldir = resolve_lecture(lecture)
    if not ldir:
        log('[错误] 找不到讲次目录：%s' % lecture)
        return 2
    script_path = os.path.join(ldir, 'video', '讲解脚本.json')
    audio_dir = os.path.join(ldir, 'video', 'audio_clone')
    name = os.path.basename(ldir.rstrip('\\/'))

    scripts = json.load(open(script_path, encoding='utf-8'))
    os.makedirs(audio_dir, exist_ok=True)
    end = min(end, len(scripts))

    log('=' * 60)
    log('克隆音：%s ｜ 共 %d 段 ｜ 本次处理 %d~%d' % (name, len(scripts), start, end))
    log('输出：%s' % audio_dir)
    log('=' * 60)
    if not health():
        log('[错误] Voicebox 未就绪，请先打开 Voicebox 应用')
        return 2

    # 本地已有音频的文本，其进行中任务（若有）应当清掉，避免占住 CPU
    have = set()
    for idx in range(1, len(scripts) + 1):
        out = os.path.join(audio_dir, 'audio_%02d.wav' % idx)
        if is_fresh(out, scripts[idx - 1], MIN_BYTES):
            have.add(scripts[idx - 1])
    cleanup_queue(have)

    ok = skip = reuse = fail = stale = 0
    for idx in range(start, end + 1):
        text = scripts[idx - 1]
        out = os.path.join(audio_dir, 'audio_%02d.wav' % idx)

        if is_fresh(out, text, MIN_BYTES):
            log('第%02d段 本地已有音频且与讲稿一致，跳过' % idx)
            skip += 1
            continue
        if os.path.exists(out) and os.path.getsize(out) >= MIN_BYTES:
            stale += 1
            log('第%02d段 讲稿已更新，旧克隆音作废 → 重新生成' % idx)

        items = history()
        done, live = find_by_text(items, text)

        if done:
            gid = done[-1]['id']
            log('第%02d段 Voicebox 已有完成记录，直接导出复用（不重新生成）' % idx)
            if export(gid, out):
                write_stamp(out, text)
                reuse += 1
                log('      ✅ 导出 %dKB' % (os.path.getsize(out) // 1024))
            else:
                fail += 1
                log('      ❌ 导出失败')
            continue

        if live:
            gid = live[0]['id']
            log('第%02d段 发现进行中的任务，只等待、不重复提交' % idx)
            # 同一文本多余的进行中任务先取消，避免并发拖慢
            for extra in live[1:]:
                cancel(extra['id'])
            if wait_for(gid, '第%02d段' % idx) and export(gid, out):
                write_stamp(out, text)
                ok += 1
                log('      ✅ 下载 %dKB' % (os.path.getsize(out) // 1024))
            else:
                fail += 1
            continue

        log('第%02d段 提交新任务：%s…' % (idx, text[:24]))
        try:
            gid = submit(text)
        except Exception as e:
            log('      提交失败：%s（跳过，下次再试）' % e)
            fail += 1
            continue
        if wait_for(gid, '第%02d段' % idx) and export(gid, out):
            write_stamp(out, text)
            ok += 1
            log('      ✅ 下载 %dKB' % (os.path.getsize(out) // 1024))
        else:
            fail += 1

    log('-' * 60)
    log('本次：新生成 %d，复用已有 %d，跳过 %d，未完成 %d（其中因讲稿更新重做 %d）'
        % (ok, reuse, skip, fail, stale))
    return 0 if fail == 0 else 1


def main():
    if len(sys.argv) < 2:
        log(__doc__)
        return 2
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
    return run(sys.argv[1], start, end)


if __name__ == '__main__':
    sys.exit(main())
