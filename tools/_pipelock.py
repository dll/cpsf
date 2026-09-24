# -*- coding: utf-8 -*-
"""
_pipelock.py —— 流水线互斥锁（防止"上一轮会话的残留循环"和新任务抢同一批文件）

背景：课件流水线里，克隆音 / PPT / 视频三件事一旦被两个进程同时做，
      轻则互相覆盖产物，重则把 Voicebox 的服务端拖死（并发两个任务会让它长时间无产出）。
      所以任何"会写产物"的工具，开工前先拿到这把锁。

锁文件：<项目根>/.pipeline.<tool>.lock，内容是一行 JSON：{"pid":…, "tool":…, "at":…}
    · 锁不存在            → 拿锁
    · 锁里的 pid 已不存在  → 视为陈旧锁，接管
    · 锁是别的活进程持有   → 拒绝，工具直接退出（退出码 3）
退出时自动释放（atexit）；被 kill 掉也能靠"pid 不存在"自愈。

按工具分别加锁（clone 一把、video 一把），这样"补克隆音"和"合成视频"
可以并行推进，只把**同一种任务**限制成单飞。
"""
import atexit
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lock_path(tool):
    return os.path.join(ROOT, '.pipeline.%s.lock' % tool)


def _alive(pid):
    try:
        import psutil
        return psutil.pid_exists(pid)
    except Exception:
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False


def _holder(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def acquire(tool='unknown'):
    path = _lock_path(tool)
    h = _holder(path)
    if h:
        pid = h.get('pid')
        if pid and pid != os.getpid() and _alive(pid):
            print('[锁] 已有同类任务在跑：%s (pid=%s, 起于 %s)，本次 %s 退出以免互相覆盖'
                  % (h.get('tool'), pid, h.get('at'), tool))
            return False
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'pid': os.getpid(), 'tool': tool,
                       'at': time.strftime('%Y-%m-%d %H:%M:%S')}, f)
    except Exception as e:
        print('[锁] 写入失败（忽略，继续跑）：%s' % e)
        return True
    atexit.register(lambda: release(tool))
    return True


def release(tool='unknown'):
    path = _lock_path(tool)
    h = _holder(path)
    if h and h.get('pid') == os.getpid():
        try:
            os.remove(path)
        except Exception:
            pass
