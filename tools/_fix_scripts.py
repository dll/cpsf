# -*- coding: utf-8 -*-
"""
_fix_scripts.py —— 统一构建脚本的「编码 + 换行 + 代码页」

三件事（幂等，可反复运行）：
  1. build.bat 统一成 UTF-8 无 BOM + CRLF（Windows cmd 对纯 LF 的批处理容易出错）
  2. build.bat 第二行补 chcp 65001，否则 bat 自己 echo 的中文会乱码
  3. Makefile 顶部补一条 chcp 65001，否则 make 输出的中文提示会乱码
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def escape_echo_gt(text):
    """
    cmd 里 echo 一行中的裸 > 会被当成输出重定向。
    典型事故：echo   -> account.o 生成成功   会把 "  -" 写进 account.o。
    这里把 echo 行里没转义的 > 补上 ^（>nul / 2>&1 这类真重定向保留原样）。
    """
    out = []
    for line in text.split("\n"):
        low = line.lstrip().lower()
        if not (low.startswith("echo") or " echo " in line):
            out.append(line)
            continue
        # 先把已经转义过的 ^> / ^^> 统一收敛成一个 ^>，避免重复转义
        line = re.sub(r"\^+>", "^>", line)
        # 保护真正的重定向写法
        line = line.replace(">nul", "\x01").replace(">>", "\x02")
        line = re.sub(r"\d>&\d", lambda m: m.group(0).replace(">", "\x03"), line)
        # 只转义「前面没有 ^ 的 >」，避免 ^> 被反复加成 ^^>
        line = re.sub(r"(?<!\^)>", "^>", line)
        line = line.replace("\x01", ">nul").replace("\x02", ">>").replace("\x03", ">")
        out.append(line)
    return "\n".join(out)


def fix_bat(path):
    raw = open(path, "rb").read()
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    text = raw.decode("utf-8", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = escape_echo_gt(text)

    if "chcp 65001" not in text:
        lines = text.split("\n")
        # 插到 @echo off 之后；没有就插到最前面
        pos = 0
        for i, ln in enumerate(lines[:3]):
            if ln.strip().lower().startswith("@echo off"):
                pos = i + 1
                break
        lines.insert(pos, "chcp 65001 >nul 2>&1")
        text = "\n".join(lines)
        changed = True
    else:
        changed = False

    # Windows cmd 对纯 LF 的批处理容易出问题，统一写回 CRLF
    out = text.replace("\n", "\r\n").encode("utf-8")
    if open(path, "rb").read() != out:
        changed = True
    if changed:
        open(path, "wb").write(out)
    return changed


def fix_makefile(path):
    text = open(path, "r", encoding="utf-8", errors="replace").read()
    if "chcp 65001" in text:
        return False
    banner = (
        "# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：\n"
        "# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。\n"
        "ifeq ($(OS),Windows_NT)\n"
        "$(shell chcp 65001 >nul)\n"
        "endif\n\n"
    )
    open(path, "w", encoding="utf-8", newline="\n").write(banner + text)
    return True


def main():
    for name in sorted(os.listdir(ROOT)):
        src = os.path.join(ROOT, name, "src")
        if not (os.path.isdir(src) and re.match(r"^\d{2}_", name)):
            continue
        for fn in sorted(os.listdir(src)):
            p = os.path.join(src, fn)
            if fn.lower() == "build.bat":
                print("  bat  %-22s %s" % (name, "已修正" if fix_bat(p) else "无需改动"))
            elif fn.lower().startswith("makefile"):
                print("  mk   %-22s %s" % (name, "已修正" if fix_makefile(p) else "无需改动"))


if __name__ == "__main__":
    main()
