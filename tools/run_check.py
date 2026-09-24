# -*- coding: utf-8 -*-
"""
run_check.py —— 逐讲构建 + 运行 + 中文显示体检

做什么：
  1. 按每讲的构建配方调用 gcc，产出 exe / dll / .a
  2. 用一串预设输入喂给程序，把输出存成 <讲>/src/运行示例.txt
  3. 体检：退出码、是否超时（死循环）、UTF-8 能否解码、中文是否成形

用法（仓库根目录）：
    python tools/run_check.py            # 全部 14 讲
    python tools/run_check.py 09 10      # 只跑指定讲次
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# (讲次, exe 相对 src 的路径, 输入序列, 超时秒)
# 输入序列设计原则：走完主要菜单分支，最后一定以 0 退出
RUN = {
    1:  ("hello.exe", "", 15),
    2:  ("atm_menu.exe", "1\n2\n500\n3\n200\n4\n100\n2002\n9\n0\n", 20),
    3:  ("atm_func.exe", "1\n2\n500\n3\n200\n4\n100\n2002\n9\n0\n", 20),
    4:  ("atm_multi.exe", "1\n2\n500\n3\n200\n4\n100\n2002\n0\n", 20),
    5:  ("pointer_atm.exe", "1\n2\n500\n3\n200\n4\n100\n2002\n0\n", 20),
    6:  ("array_atm.exe", "1001\n1\n2\n500\n3\n200\n5\n6\n0\n", 20),
    7:  ("struct_atm.exe", "1001\n1\n2\n500\n3\n200\n5\n6\n0\n", 20),
    8:  ("linked_atm.exe", "1001\n1\n2\n500\n3\n200\n5\n7\n0\n", 20),
    9:  ("atm_static.exe", "1\n赵六\n800\n2\n1\n500\n5\n1\n6\n7\n1\n0\n", 25),
    10: ("atm_dynamic.exe", "1\n赵六\n800\n2\n1\n500\n5\n1\n6\n7\n1\n0\n", 25),
    11: ("host.exe", "", 25),
    12: ("plugin_atm.exe", "", 25),
    13: ("plugin_framework.exe", "1\n500\n2\n200\n3\n0\n4\n300\n0\n", 25),
    14: ("atm_framework.exe", "1\n500\n2\n200\n3\n0\n4\n1002\n100\n9\n0\n", 30),
}


def run(cmd, cwd, timeout=120):
    try:
        p = subprocess.run(cmd, cwd=cwd, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout)
        return p.returncode, p.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return -1, ""


def build(num, src):
    """按讲次构建，返回 (是否成功, 日志)"""
    if num == 1:
        c = "gcc -Wall -O2 -o hello.exe hello.c"
    elif num == 2:
        c = "gcc -Wall -O2 -o atm_menu.exe atm_menu.c"
    elif num == 3:
        c = "gcc -Wall -O2 -o atm_func.exe atm_func.c"
    elif num == 4:
        c = "gcc -Wall -O2 -o atm_multi.exe main.c menu.c account.c utils.c"
    elif num == 5:
        c = "gcc -Wall -O2 -o pointer_atm.exe pointer_atm.c"
    elif num == 6:
        c = "gcc -Wall -O2 -o array_atm.exe array_atm.c"
    elif num == 7:
        c = "gcc -Wall -O2 -o struct_atm.exe struct_atm.c"
    elif num == 8:
        c = "gcc -Wall -O2 -o linked_atm.exe linked_atm.c"
    elif num == 9:
        c = ("gcc -Wall -Wextra -g -c account.c -o account.o && "
             "gcc -Wall -Wextra -g -c transaction.c -o transaction.o && "
             "gcc -Wall -Wextra -g -c main.c -o main.o && "
             "ar rcs libaccount.a account.o transaction.o && "
             "gcc -Wall -Wextra -g -o atm_static.exe main.o -L. -laccount")
    elif num == 10:
        c = ("gcc -Wall -Wextra -g -shared -o account.dll account.c transaction.c "
             "-Wl,--out-implib,libaccount.dll.a -DACCOUNT_EXPORTS -DTRANSACTION_EXPORTS && "
             "gcc -Wall -Wextra -g -o atm_dynamic.exe main.c -L. -laccount")
    elif num == 11:
        c = ("for %%P in (deposit withdraw query broken) do "
             "gcc -Wall -Wextra -g -shared -o %%P_plugin.dll %%P_plugin.c && "
             "gcc -Wall -Wextra -g -o host.exe host.c && "
             "if not exist plugins mkdir plugins && "
             "copy /Y *_plugin.dll plugins\\ >nul")
        c = c.replace("%%", "%")
    elif num == 12:
        c = "gcc -Wall -O2 -o plugin_atm.exe plugin_atm.c"
    elif num == 13:
        c = ("gcc -Wall -O2 -o plugin_framework.exe framework.c atm_state.c "
             "plugin_deposit.c plugin_withdraw.c plugin_query.c plugin_transfer.c main.c")
    elif num == 14:
        c = ("gcc -Wall -O2 -shared -o atmcore.dll account.c transaction.c "
             "-Wl,--out-implib,libatmcore.a -DATMCORE_BUILD && "
             "if not exist plugins mkdir plugins && "
             "(for %%P in (deposit withdraw query transfer) do "
             "gcc -Wall -O2 -shared -DPLUGIN_DLL -o plugins\\%%P_plugin.dll "
             "plugins\\%%P_plugin.c -I. -Iplugins -L. -latmcore) && "
             "gcc -Wall -O2 -o atm_framework.exe main.c framework.c dynamic_loader.c "
             "plugins\\deposit_plugin.c plugins\\withdraw_plugin.c plugins\\query_plugin.c "
             "plugins\\transfer_plugin.c -I. -Iplugins -L. -latmcore").replace("%%", "%")
    else:
        return False, "未知讲次"
    rc, out = run(c, src, timeout=180)
    return rc == 0, out


def main():
    want = set()
    for a in sys.argv[1:]:
        m = re.match(r"^(\d{1,2})$", a.strip())
        if m:
            want.add(int(m.group(1)))

    rows = []
    for name in sorted(os.listdir(ROOT)):
        full = os.path.join(ROOT, name)
        m = re.match(r"^(\d{2})_", name)
        if not m or not os.path.isdir(os.path.join(full, "src")):
            continue
        num = int(m.group(1))
        if want and num not in want:
            continue
        src = os.path.join(full, "src")
        exe, stdin, timeout = RUN.get(num, (None, "", 20))

        ok, blog = build(num, src)
        status = []
        if not ok:
            status.append("构建失败")
            rows.append((name, "构建失败", blog[-400:]))
            continue

        # ---- 运行 ----
        exe_path = os.path.join(src, exe)
        if not os.path.isfile(exe_path):
            rows.append((name, "缺产物 " + exe, ""))
            continue
        try:
            p = subprocess.run([exe_path], cwd=src, input=stdin.encode("utf-8"),
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               timeout=timeout)
            rc, raw = p.returncode, p.stdout
        except subprocess.TimeoutExpired:
            rc, raw = -9, b""

        text = raw.decode("utf-8", "replace")
        bad = text.count("\ufffd")
        han = len(re.findall(r"[\u4e00-\u9fff]", text))
        min_han = 0 if num == 1 else 20   # 第1讲只打印英文 Hello World，豁免
        if rc == -9:
            status.append("超时(疑似死循环)")
        if bad:
            status.append("UTF-8 解码异常 %d 处" % bad)
        if han < min_han:
            status.append("中文过少 %d 字" % han)

        # 保存运行示例
        sample = os.path.join(src, "运行示例.txt")
        with open(sample, "w", encoding="utf-8", newline="\n") as f:
            f.write("$ %s\n" % exe)
            if stdin:
                f.write("$ 输入: %s\n" % stdin.replace("\n", " "))
            f.write("-" * 60 + "\n")
            f.write(text)
            f.write("\n" + "-" * 60 + "\n")
            f.write("退出码: %d\n" % rc)

        flag = "OK" if not status else " / ".join(status)
        rows.append((name, flag, "%d 行 / 中文 %d 字 / rc=%d" % (text.count("\n"), han, rc)))

    print("=" * 78)
    for name, flag, info in rows:
        print("  %-16s %-28s %s" % (name, flag, info))
    print("=" * 78)
    bad_rows = [r for r in rows if r[1] != "OK"]
    print("通过 %d / %d" % (len(rows) - len(bad_rows), len(rows)))
    return 1 if bad_rows else 0


if __name__ == "__main__":
    sys.exit(main())
