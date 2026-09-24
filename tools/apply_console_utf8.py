# -*- coding: utf-8 -*-
"""
apply_console_utf8.py —— 把 console_utf8.h 接入每一讲的 main 入口

做什么：
  1. 把 tools/console_utf8.h 复制到 <讲>/src/console_utf8.h
  2. 在含 main 的那个 .c 里
       - 最后一个 #include 之后插入  #include "console_utf8.h"
       - main 函数体的第一行插入    console_utf8_init();
  3. 幂等：已经注入过的会跳过

用法（在仓库根目录执行）：
    python tools/apply_console_utf8.py          # 处理全部 14 讲
    python tools/apply_console_utf8.py 02 09    # 只处理指定讲次（前两位数字）
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HDR_SRC = os.path.join(ROOT, "tools", "console_utf8.h")

MAIN_RE = re.compile(r"^int\s+main\s*\([^;{]*\)", re.M)


def find_main_file(src_dir):
    """找到定义 main 的 .c（排除插件 dll 的源文件）"""
    hits = []
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith(".c"):
            continue
        path = os.path.join(src_dir, name)
        try:
            text = open(path, "r", encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        if MAIN_RE.search(text):
            hits.append((path, text))
    if not hits:
        return None, None
    # 有多个时优先 main.c / host.c
    for path, text in hits:
        base = os.path.basename(path).lower()
        if base in ("main.c", "host.c"):
            return path, text
    return hits[0]


def inject(path, text):
    changed = False

    # ---- 1) 插入 #include "console_utf8.h" ----
    if 'console_utf8.h' not in text:
        incs = list(re.finditer(r'^[ \t]*#include[^\n]*\n', text, re.M))
        if incs:
            pos = incs[-1].end()
            # 关键：最后一条 #include 可能落在 #ifdef/#else 分支里，
            # 必须把它后面的 #endif / #else 都跨过去，插到条件编译块之外。
            rest = text[pos:]
            m = re.match(r'(?:[ \t]*#[ \t]*(?:endif|else|elif)[^\n]*\n)+', rest)
            if m:
                pos += m.end()
            text = text[:pos] + '#include "console_utf8.h"\n' + text[pos:]
        else:
            text = '#include "console_utf8.h"\n' + text
        changed = True

    # ---- 2) 在 main 函数体开头插入 console_utf8_init(); ----
    if "console_utf8_init" not in text.split("int main")[0] + text.split("int main")[-1] or True:
        m = MAIN_RE.search(text)
        if m:
            brace = text.find("{", m.end())
            if brace != -1:
                after = text[brace + 1:brace + 200]
                if "console_utf8_init()" not in after:
                    indent = "    "
                    text = (text[:brace + 1]
                            + "\n" + indent + "console_utf8_init();   /* 解决中文乱码：切换到 UTF-8 控制台 */"
                            + text[brace + 1:])
                    changed = True

    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    return changed


def main():
    args = [a for a in sys.argv[1:] if a.strip()]
    want = set()
    for a in args:
        m = re.match(r"^(\d{1,2})", a)
        if m:
            want.add(int(m.group(1)))

    if not os.path.isfile(HDR_SRC):
        print("缺少 tools/console_utf8.h")
        return 1

    lectures = []
    for name in sorted(os.listdir(ROOT)):
        full = os.path.join(ROOT, name)
        if os.path.isdir(full) and os.path.isdir(os.path.join(full, "src")):
            m = re.match(r"^(\d{2})_", name)
            if m:
                lectures.append((int(m.group(1)), name, os.path.join(full, "src")))

    for num, name, src_dir in lectures:
        if want and num not in want:
            continue
        shutil.copyfile(HDR_SRC, os.path.join(src_dir, "console_utf8.h"))
        path, text = find_main_file(src_dir)
        if path is None:
            print("  %-16s 未找到含 main 的源文件，已放置头文件" % name)
            continue
        ok = inject(path, text)
        print("  %-16s %-22s %s" % (name, os.path.basename(path), "已注入" if ok else "已存在，跳过"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
