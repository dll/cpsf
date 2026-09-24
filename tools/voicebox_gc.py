# -*- coding: utf-8 -*-
"""
voicebox_gc.py —— 清理 Voicebox 里的重复/多余生成任务（保守、只取消、不删除已完成的）

【为什么需要它】
CPU 模式下单段克隆可能要十几分钟。如果调用方"等超时就重新提交"，
Voicebox 里就会堆出多份同样的任务，既占 CPU 又让每一份都变慢。
这个工具把重复清掉：
  · 同一段文字有多个"进行中"的任务 → 只保留最早提交的那一个，其余取消
  · 该段文字本地已经有音频文件了 → 它的所有"进行中"任务全部取消（不需要了）
  · 已完成的任务一律保留（直接复用，避免重复克隆）

用法：
    python tools/voicebox_gc.py                       # 全局去重
    python tools/voicebox_gc.py <讲解脚本.json> <音频目录>   # 结合本地文件判断哪些不需要了
"""
import json
import os
import sys

import requests

API = 'http://127.0.0.1:17493'
TERMINAL = ('completed', 'failed', 'cancelled')
LIVE = ('generating', 'queued', 'pending', 'processing')


def fetch_history(limit=60):
    r = requests.get(f'{API}/history', params={'limit': limit}, timeout=30)
    r.raise_for_status()
    return r.json().get('items', [])


def cancel(gid):
    try:
        r = requests.post(f'{API}/generate/{gid}/cancel', timeout=20)
        return r.status_code < 400
    except Exception:
        return False


def main():
    have = {}          # text -> 本地是否已有音频
    if len(sys.argv) >= 3:
        script = json.load(open(sys.argv[1], encoding='utf-8'))
        adir = sys.argv[2]
        for i, t in enumerate(script, 1):
            p = os.path.join(adir, 'audio_%02d.wav' % i)
            have[t] = os.path.exists(p) and os.path.getsize(p) > 200 * 1024
        print('本地已有音频的段数：%d / %d' % (sum(have.values()), len(have)))

    items = fetch_history()
    live = [i for i in items if i.get('status') in LIVE]
    print('历史条目 %d，其中进行中 %d' % (len(items), len(live)))

    by_text = {}
    for it in live:
        by_text.setdefault(it.get('text', ''), []).append(it)

    cancelled, kept = [], 0
    for text, group in by_text.items():
        group.sort(key=lambda x: x.get('created_at') or '')
        if have.get(text):
            # 本地已经有了，进行中的全部取消
            for it in group:
                if cancel(it['id']):
                    cancelled.append(it['id'])
        else:
            for it in group[1:]:
                if cancel(it['id']):
                    cancelled.append(it['id'])
            kept += 1

    print('已取消 %d 个重复/多余任务，保留 %d 个进行中的任务' % (len(cancelled), kept))
    for c in cancelled:
        print('  - cancelled', c)
    if have:
        missing = [i for i, t in enumerate(have, 1) if not have[t]]
        print('仍未完成（需继续等待或重跑）的段号：', missing)
    return 0


if __name__ == '__main__':
    sys.exit(main())
