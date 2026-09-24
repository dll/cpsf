# -*- coding: utf-8 -*-
"""
verify_console.py —— 证明「中文乱码」真的被解决了

原理：
  Windows 中文版控制台默认代码页是 936(GBK)，而我们的源码是 UTF-8，
  两边对不上就乱码。程序里调用 SetConsoleOutputCP(CP_UTF8) 之后，
  控制台代码页应当变成 65001。

本脚本做的事：
  1. 强行把当前控制台代码页设回 936，模拟「没修好的环境」
  2. 运行各讲程序（stdout 丢掉，只看它对控制台做了什么）
  3. 读回代码页：65001 = 修复生效；936 = 没生效，仍会乱码
  4. 顺带演示：同一串 UTF-8 字节按 GBK 解释会长什么样（乱码对比）

用法：python tools/verify_console.py
"""
import ctypes
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
k = ctypes.windll.kernel32

EXES = [
    (2, "02_控制结构/src/atm_menu.exe"),
    (5, "05_指针/src/pointer_atm.exe"),
    (9, "09_静态库/src/atm_static.exe"),
    (11, "11_运行时加载/src/host.exe"),
    (12, "12_接口抽象/src/plugin_atm.exe"),
    (13, "13_插件框架/src/plugin_framework.exe"),
    (14, "14_完整项目/src/atm_framework.exe"),
]

STDIN = {
    2: "1\n2\n500\n0\n",
    5: "1\n0\n",
    9: "6\n0\n",
    13: "1\n500\n0\n",
    14: "1\n500\n9\n0\n",
}


def main():
    if k.GetConsoleOutputCP() == 0:
        k.AllocConsole()
    before = k.GetConsoleOutputCP()
    print("当前控制台代码页: %s（Windows 中文版默认 936 = GBK）" % before)

    print("\n== 1. 证明：UTF-8 字节被 GBK 解释 = 乱码 ==")
    s = "欢迎使用 ATM 系统"
    print("   原本（UTF-8 正确显示）: %s" % s)
    garbled = s.encode("utf-8").decode("gbk", errors="replace")
    print("   同一串字节按 GBK 读取  : %s   <-- 这就是乱码" % garbled)

    print("\n== 2. 把控制台设回 936，再运行各讲程序 ==")
    allok = True
    for num, rel in EXES:
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            print("   %-34s 缺产物" % rel)
            allok = False
            continue
        src = os.path.dirname(path)
        k.SetConsoleOutputCP(936)          # 模拟未修复的环境
        start = k.GetConsoleOutputCP()
        try:
            subprocess.run([path], cwd=src,
                           input=STDIN.get(num, "").encode("utf-8"),
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=30)
        except subprocess.TimeoutExpired:
            pass
        after = k.GetConsoleOutputCP()
        ok = (after == 65001)
        allok = allok and ok
        print("   %-34s %4d -> %-5d %s" % (rel, start, after,
                                           "UTF-8 ✓ 中文正常" if ok else "仍是 GBK ✗ 会乱码"))

    k.SetConsoleOutputCP(before)
    print("\n结论: %s" % ("全部已切换到 UTF-8，控制台中文不再乱码" if allok else "存在未切换的程序，需要检查"))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
