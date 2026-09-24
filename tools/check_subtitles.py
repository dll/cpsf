# -*- coding: utf-8 -*-
"""
check_subtitles.py —— 字幕质检：找出"念稿痕迹"没被还原干净的地方

念稿里允许出现的中文读法（美元问号、星号p、方括号…）在**字幕**里一律不该出现，
否则投影出来的字幕和页面上的真实代码对不上，学生看不懂。

用法：
    python tools/check_subtitles.py            # 全 14 讲
    python tools/check_subtitles.py 05 06      # 只看指定讲
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from subtitle_text import show_text          # noqa: E402

# 字幕里不该出现的读法痕迹
BAD = [
    (r'美元问号', '应为 $?'),
    (r'星号', '应为 *'),
    (r'方括号', '应为 []'),
    (r'反斜杠', '应为 \\'),
    # "取地址a" 这种紧跟标识符的必须还原成 &a；
    # 单独说"取地址"这个操作名是正常中文，不算问题
    (r'取地址[A-Za-z_]', '应为 &'),
    (r'\d+\s*加\s*-', '应为 - 参数'),
    (r'[A-Za-z0-9]\s*加加', '应为 ++'),
    (r'[A-Za-z_][A-Za-z_0-9]*\s*点\s*[A-Za-z_]', '应为 .'),
    (r'[A-Za-z_][A-Za-z_0-9]*\s*箭头\s*[A-Za-z_]', '应为 ->'),
    (r'(void|int|char|double|float)\s+星号', '应为 void *'),
]


def scan(lecture):
    d = sorted(glob.glob(os.path.join(ROOT, lecture + '_*')))[0]
    script = json.load(open(os.path.join(d, 'video', '讲解脚本.json'), encoding='utf-8'))
    issues = []
    for i, entry in enumerate(script, 1):
        sub = show_text(entry)
        for pat, why in BAD:
            for m in re.finditer(pat, sub):
                a, b = max(0, m.start() - 14), min(len(sub), m.end() + 14)
                issues.append((i, m.group(0), why, sub[a:b]))
    return d, issues


def main():
    keys = sys.argv[1:] or ['%02d' % n for n in range(1, 15)]
    total = 0
    for k in keys:
        d, issues = scan(k)
        if not issues:
            print('✅ %s  字幕干净' % d)
            continue
        print('⚠️  %s  命中 %d 处' % (d, len(issues)))
        for i, hit, why, ctx in issues:
            print('    段%02d  「%s」 %s\n           …%s…' % (i, hit, why, ctx))
        total += len(issues)
    print('-' * 60)
    print('合计待处理：%d 处' % total)
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
