# -*- coding: utf-8 -*-
"""
run_clone.py —— 串行跑多讲的克隆音（ASCII 编号传参，规避 Git Bash 中文乱码）

用法：
    python tools/run_clone.py 02 13 14          # 依次补第2、13、14讲的克隆音
    python tools/run_clone.py 02:11-18          # 只做第2讲 11~18 段

CPU 后端同一时刻只适合跑一个任务，所以这里**严格串行**。
日志写到 clone_batch.log（工作区里，别写 /tmp）。
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import voicebox_clone as vc   # noqa: E402


def parse(spec):
    """'02' -> (lecture, 1, inf)；'02:11-18' -> (lecture, 11, 18)"""
    if ':' in spec:
        lec, rng = spec.split(':', 1)
        if '-' in rng:
            a, b = rng.split('-', 1)
            return lec, int(a), int(b)
        return lec, int(rng), int(rng)
    return spec, 1, 10 ** 6


def main():
    specs = sys.argv[1:]
    if not specs:
        print(__doc__)
        return 2
    log_path = os.path.join(ROOT, 'clone_batch.log')
    logf = open(log_path, 'a', encoding='utf-8')

    def tee(msg):
        print(msg, flush=True)
        logf.write(msg + '\n')
        logf.flush()

    tee('\n' + '#' * 64)
    tee('批量克隆开始 %s ｜ 目标：%s' % (time.strftime('%Y-%m-%d %H:%M:%S'), ' '.join(specs)))
    rc = 0
    for spec in specs:
        lec, a, b = parse(spec)
        ldir = vc.resolve_lecture(lec)
        tee('\n>>> 第 %s 讲 %s 段 %s~%s' % (lec, os.path.basename(ldir or '?'), a, b))
        try:
            r = vc.run(lec, a, b)
        except Exception as e:
            tee('    [异常] %s' % e)
            r = 1
        rc = rc or r
    tee('\n批量克隆结束 %s ｜ rc=%d' % (time.strftime('%Y-%m-%d %H:%M:%S'), rc))
    logf.close()
    return rc


if __name__ == '__main__':
    sys.exit(main())
