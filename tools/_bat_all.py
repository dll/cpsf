# -*- coding: utf-8 -*-
"""
_bat_all.py —— 用真实的 cmd 跑一遍每讲的 build.bat

验证三件事：
  1. 批处理在 Windows 的 cmd 里能跑通（不是只在 Git Bash 里能跑）
  2. 控制台代码页是 GBK(936) 时，bat 自己 echo 的中文也不乱码
  3. 构建产物确实被生成出来

用法：python tools/_bat_all.py
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 需要传 build 参数（否则会运行演示 / 结尾 pause）的讲次
BUILD_ARG = {1, 2, 3, 5, 6, 7, 8, 12}
# 每讲构建完应当出现的产物
EXPECT = {
    1: ["hello.exe"],
    2: ["atm_menu.exe"],
    3: ["atm_func.exe"],
    4: ["atm_multi.exe"],
    5: ["pointer_atm.exe"],
    6: ["array_atm.exe"],
    7: ["struct_atm.exe"],
    8: ["linked_atm.exe"],
    9: ["libaccount.a", "atm_static.exe"],
    10: ["account.dll", "atm_dynamic.exe"],
    11: ["host.exe", "deposit_plugin.dll", "plugins/query_plugin.dll"],
    12: ["plugin_atm.exe"],
    13: ["plugin_framework.exe"],
    14: ["atmcore.dll", "atm_framework.exe", "plugins/deposit_plugin.dll"],
}


def main():
    rows = []
    for name in sorted(os.listdir(ROOT)):
        src = os.path.join(ROOT, name, "src")
        m = re.match(r"^(\d{2})_", name)
        if not m or not os.path.isdir(src):
            continue
        num = int(m.group(1))
        bat = os.path.join(src, "build.bat")
        if not os.path.isfile(bat):
            rows.append((name, "缺 build.bat", ""))
            continue
        arg = "build" if num in BUILD_ARG else ""
        cmdline = "chcp 936 >nul && build.bat" + (" " + arg if arg else "")
        try:
            p = subprocess.run(["cmd", "/c", cmdline], cwd=src,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               timeout=180)
            out = p.stdout.decode("utf-8", "replace")
            rc = p.returncode
        except subprocess.TimeoutExpired:
            out, rc = "", -9

        problems = []
        if rc != 0:
            problems.append("rc=%d" % rc)
        if "\ufffd" in out:
            problems.append("输出含非法 UTF-8")
        if "不是内部或外部命令" in out or "is not recognized" in out:
            idx = max(out.find("不是内部或外部命令"), out.find("is not recognized"))
            problems.append("命令未找到: ...%s..." % out[max(0, idx - 60):idx + 30].replace("\r\n", " "))
        for f in EXPECT.get(num, []):
            if not os.path.isfile(os.path.join(src, f)):
                problems.append("缺产物 " + f)
        han = len(re.findall(r"[\u4e00-\u9fff]", out))
        if han < 5:
            problems.append("中文提示过少 %d" % han)

        rows.append((name, "OK" if not problems else " / ".join(problems),
                     "中文 %d 字 / rc=%d" % (han, rc)))

    print("=" * 76)
    for name, flag, info in rows:
        print("  %-16s %-30s %s" % (name, flag, info))
    print("=" * 76)
    bad = [r for r in rows if r[1] != "OK"]
    print("通过 %d / %d" % (len(rows) - len(bad), len(rows)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
