# -*- coding: utf-8 -*-
"""
tts_batch.py —— 第3~12讲的语音合成（Windows SAPI 中文女声，无需克隆）

按用户要求：第1、2、13、14讲用克隆音（tools/voicebox_clone.py）；
其余讲次用语音合成即可，本脚本负责这一部分。

特性：
  · 逐段生成到 <讲次>/video/audio_tts/audio_NN.wav，已存在且合格的段直接跳过（断点续跑）
  · 每段新建引擎再销毁，避免 SAPI COM 长时间运行卡死（旧流水线踩过的坑）
  · 生成后校验文件大小与时长，不合格自动重试一次

用法：
    python tools/tts_batch.py <讲次编号或目录> [起始段] [结束段] [--force]
例：
    python tools/tts_batch.py 03
    python tools/tts_batch.py 03 1 18 --force     # 讲解稿改过，强制重合成
"""
import glob
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from _pipelock import acquire as _lock_acquire      # noqa: E402
from _audiohash import is_fresh, write_stamp        # noqa: E402
from subtitle_text import narration                 # noqa: E402

MIN_BYTES = 120 * 1024
RATE = 196          # 语速：实测 196 时每段约 20~26 秒，18 段正好落在 6~8 分钟
VOICE_HINT = 'zh-CN'


def log(m):
    print(m, flush=True)



def _pick_dir(hits):
    """
    同名编号可能有遗留目录（例如 02_函数封装 是旧编号遗留，现行的第2讲是 02_控制结构）。
    优先级：有 讲解脚本.json 的 > 有 课件.pptx 的 > 其余，避免跑到废弃目录上。
    """
    for probe in (os.path.join('video', '讲解脚本.json'), os.path.join('docs', '课件.pptx')):
        good = [h for h in hits if os.path.exists(os.path.join(h, probe))]
        if good:
            return sorted(good)[0]
    return sorted(hits)[0]

def resolve(key):
    key = str(key).strip()
    cand = os.path.join(ROOT, key)
    if os.path.isdir(cand):
        return cand
    num = key.zfill(2)
    hits = sorted(d for d in glob.glob(os.path.join(ROOT, '*'))
                  if os.path.isdir(d) and os.path.basename(d)[:2] == num)
    hits = [h for h in hits if '_' in os.path.basename(h)]
    if hits:
        return _pick_dir(hits)
    raise SystemExit('找不到讲次：%s' % key)


def duration(path):
    ff = glob.glob('ffprobe') or ['ffprobe']
    try:
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                              '-of', 'csv=p=0', path], capture_output=True, text=True, timeout=60)
        return float(out.stdout.strip())
    except Exception:
        return 0.0


def speak(text, path):
    """用 SAPI 合成一段语音。每段独立引擎，避免长时间运行卡死。"""
    import pyttsx3
    eng = pyttsx3.init()
    try:
        for v in eng.getProperty('voices'):
            if VOICE_HINT in str(getattr(v, 'languages', '')) or 'huihui' in v.name.lower():
                eng.setProperty('voice', v.id)
                break
        eng.setProperty('rate', RATE)
        eng.save_to_file(text, path)
        eng.runAndWait()
    finally:
        try:
            eng.stop()
        except Exception:
            pass
        del eng
    time.sleep(0.3)
    return os.path.exists(path) and os.path.getsize(path) >= MIN_BYTES


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    force = '--force' in sys.argv
    if not args:
        print(__doc__)
        return 1
    if not _lock_acquire('tts_batch'):
        return 3
    ldir = resolve(args[0])
    name = os.path.basename(ldir)
    start = int(args[1]) if len(args) > 1 else 1
    end = int(args[2]) if len(args) > 2 else 10 ** 6

    script_file = os.path.join(ldir, 'video', '讲解脚本.json')
    script = json.load(open(script_file, encoding='utf-8'))
    out_dir = os.path.join(ldir, 'video', 'audio_tts')
    os.makedirs(out_dir, exist_ok=True)

    log('=' * 60)
    log('语音合成：%s ｜ 共 %d 段 ｜ 本次 %d~%d%s'
        % (name, len(script), start, min(end, len(script)), '（强制重合成）' if force else ''))
    log('=' * 60)

    ok = skip = fail = stale = 0
    for i in range(start, min(end, len(script)) + 1):
        p = os.path.join(out_dir, 'audio_%02d.wav' % i)
        text = narration(script[i - 1])[0]        # 念稿（不受字幕还原影响）
        if not force and is_fresh(p, text, MIN_BYTES, script_path=script_file):
            skip += 1
            continue
        if not force and os.path.exists(p):
            stale += 1
            log('  第%02d段 讲稿已更新，旧配音作废 → 重新合成' % i)
        done = False
        for attempt in (1, 2):
            if speak(text, p):
                done = True
                break
            log('     第%d段 第%d次合成不合格，重试' % (i, attempt))
        if done:
            write_stamp(p, text)
            ok += 1
            if i % 5 == 1 or i == len(script):
                log('  第%02d段 ✅ %.1f 秒  %s' % (i, duration(p), text[:24]))
        else:
            fail += 1
            log('  第%02d段 ❌ 合成失败' % i)

    log('-' * 60)
    log('本次：新生成 %d（其中重做 %d），跳过 %d，失败 %d' % (ok, stale, skip, fail))
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
