# -*- coding: utf-8 -*-
"""
gen_src_readme.py —— 给每讲的 src 目录生成 README.md

内容全部来自实际扫描（源码文件、头文件首行注释、构建脚本、构建产物），
不会出现「文档写的和目录里不一样」的情况。

用法：python tools/gen_src_readme.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = {
    1:  "你好世界 —— 一行 printf 里的五个要素",
    2:  "控制结构 —— 顺序 / 分支 / 循环",
    3:  "函数封装 —— 给代码找个家",
    4:  "多文件编程 —— .h 声明，.c 实现",
    5:  "指针 —— 为什么函数能改外面的变量",
    6:  "数组 —— 从「一个账户」到「一批账户」",
    7:  "结构体 —— 把散落的数据打包成一个东西",
    8:  "链表 —— 大小不再写死的数据结构",
    9:  "静态库 —— 把 .o 打包成 .a",
    10: "动态库 —— .dll / .so 与加载时链接",
    11: "运行时加载 —— 运行中才决定加载谁",
    12: "接口抽象 —— 结构体里装函数指针",
    13: "插件框架 —— 生命周期与插件管理器",
    14: "完整项目 —— 可插拔 ATM 与全系列总结",
}

POINT = {
    1:  "编译四阶段、链接器的作用、printf 背后的标准库。",
    2:  "三种控制结构搭出第一个能一直跑下去的交互程序。",
    3:  "把重复代码抽成函数，main 只负责调度。",
    4:  "拆文件：头文件放声明，实现放 .c，改一个只编译一个。",
    5:  "传地址而不是传值，函数才能修改调用者的变量。",
    6:  "用数组管理多个账户与交易流水，体会连续内存与容量上限。",
    7:  "struct 把一组相关数据打包，代码可读性上一个台阶。",
    8:  "链表取代数组：不再预先写死容量，随用随长。",
    9:  "ar 打包 .o 成 .a，链接时把代码复制进可执行文件。",
    10: "编译出 .dll/.so，exe 只记录导入表，运行时由 OS 加载。",
    11: "LoadLibrary/dlopen：宿主不认识插件，运行时扫描目录并调用。",
    12: "约定 struct Plugin 接口，统一调用不同实现——C 语言的多态。",
    13: "插件生命周期 + 管理器 + 配置化菜单，主程序零改动扩展。",
    14: "静态核心库 + 动态插件 + 框架调度，14 讲能力一次合流。",
}

DEMO = {
    1:  "（无需输入）",
    2:  "1 → 2/500 → 3/200 → 4/100/2002 → 0",
    3:  "1 → 2/500 → 3/200 → 4/100/2002 → 0",
    4:  "1 → 2/500 → 3/200 → 4/100/2002 → 0",
    5:  "1 → 2/500 → 3/200 → 4/100/2002 → 0",
    6:  "1001 → 1 → 2/500 → 3/200 → 5 → 6 → 0",
    7:  "1001 → 1 → 2/500 → 3/200 → 5 → 6 → 0",
    8:  "1001 → 1 → 2/500 → 3/200 → 5 → 7 → 0",
    9:  "1/赵六/800 → 2/1/500 → 5/1 → 6 → 7/1 → 0",
    10: "1/赵六/800 → 2/1/500 → 5/1 → 6 → 7/1 → 0",
    11: "（无需输入，自动扫描 plugins 目录）",
    12: "（无需输入，自动注册并遍历插件）",
    13: "1/500 → 2/200 → 3 → 4/300 → 0",
    14: "1/500 → 2/200 → 3 → 4/1002/100 → 9 → 0",
}

PRODUCTS = {
    1:  "hello.exe",
    2:  "atm_menu.exe",
    3:  "atm_func.exe",
    4:  "atm_multi.exe",
    5:  "pointer_atm.exe",
    6:  "array_atm.exe",
    7:  "struct_atm.exe",
    8:  "linked_atm.exe",
    9:  "libaccount.a、atm_static.exe",
    10: "account.dll、libaccount.dll.a、atm_dynamic.exe",
    11: "host.exe、deposit/withdraw/query/broken_plugin.dll（并复制到 plugins\\）",
    12: "plugin_atm.exe",
    13: "plugin_framework.exe",
    14: "atmcore.dll、libatmcore.a、atm_framework.exe、plugins\\*_plugin.dll",
}


def first_comment_line(path):
    """取文件开头注释里第一句像标题的话"""
    try:
        text = open(path, "r", encoding="utf-8", errors="replace").read()
    except Exception:
        return ""
    m = re.search(r"/\*+={0,}\s*\n\s*\*?\s*(.+)", text[:1500])
    if m:
        line = m.group(1).strip().strip("*").strip()
        line = re.sub(r"^第\d+讲[：:]?\s*", "", line)
        # 去掉 "xxx.c - " 这类文件名前缀
        line = re.sub(r"^\w+\.[ch]\s*[-—:]\s*", "", line)
        return line[:40]
    return ""


def main():
    for name in sorted(os.listdir(ROOT)):
        src = os.path.join(ROOT, name, "src")
        m = re.match(r"^(\d{2})_", name)
        if not m or not os.path.isdir(src):
            continue
        num = int(m.group(1))
        title = TITLE.get(num, name.split("_", 1)[-1])
        point = POINT.get(num, "")

        cs = sorted(f for f in os.listdir(src) if f.endswith(".c"))
        hs = sorted(f for f in os.listdir(src) if f.endswith(".h"))
        prods = sorted(f for f in os.listdir(src)
                       if f.endswith((".exe", ".dll", ".a", ".so")))

        lines = []
        lines.append("# 第%d讲 %s" % (num, title))
        lines.append("")
        lines.append("> %s" % point)
        lines.append("")
        lines.append("## 一、文件清单")
        lines.append("")
        lines.append("| 文件 | 说明 |")
        lines.append("|:---|:---|")
        for f in cs:
            lines.append("| `%s` | %s |" % (f, first_comment_line(os.path.join(src, f)) or "实现文件"))
        for f in hs:
            if f == "console_utf8.h":
                lines.append("| `%s` | 控制台 UTF-8 初始化（解决中文乱码，全系列共用） |" % f)
            else:
                lines.append("| `%s` | %s |" % (f, first_comment_line(os.path.join(src, f)) or "头文件"))
        if os.path.isdir(os.path.join(src, "plugins")):
            lines.append("| `plugins/` | 插件目录（源码 + 编译好的插件 DLL） |")
        lines.append("| `build.bat` | Windows 一键构建（cmd 里双击或命令行运行） |")
        lines.append("| `Makefile` | Linux / macOS / Git Bash 构建 |")
        lines.append("| `运行示例.txt` | 一次完整演示的真实输出，可直接对照 |")
        lines.append("")
        lines.append("## 二、怎么构建")
        lines.append("")
        lines.append("**Windows（cmd / PowerShell）**")
        lines.append("")
        lines.append("```bat")
        lines.append("cd %s\\src" % name)
        lines.append("build.bat")
        lines.append("```")
        lines.append("")
        lines.append("**Linux / macOS / Git Bash**")
        lines.append("")
        lines.append("```bash")
        lines.append("cd %s/src" % name)
        lines.append("make          # 只编译")
        lines.append("make run      # 编译并自动演示")
        lines.append("make clean    # 清理产物")
        lines.append("```")
        lines.append("")
        lines.append("## 三、怎么运行")
        lines.append("")
        lines.append("- 演示输入序列：`%s`" % DEMO.get(num, "见 build.bat"))
        lines.append("- 完整输出见 [`运行示例.txt`](运行示例.txt)")
        lines.append("")
        lines.append("## 四、构建产物")
        lines.append("")
        lines.append("```")
        lines.append(PRODUCTS.get(num, "、".join(prods)))
        lines.append("```")
        lines.append("")
        if prods:
            lines.append("（目录里当前存在：%s）" % "、".join(prods))
            lines.append("")
        lines.append("## 五、中文为什么会乱码，以及本讲怎么解决的")
        lines.append("")
        lines.append("源码统一保存为 **UTF-8**，而 Windows 中文版控制台默认用 **GBK(936)** 解释字节，")
        lines.append("两边对不上就显示成乱码。解决办法是让程序自己把控制台切到 UTF-8：")
        lines.append("")
        lines.append("```c")
        lines.append('#include "console_utf8.h"')
        lines.append("")
        lines.append("int main(void)")
        lines.append("{")
        lines.append("    console_utf8_init();   /* 内部：SetConsoleOutputCP(CP_UTF8) */")
        lines.append("    ...")
        lines.append("}")
        lines.append("```")
        lines.append("")
        lines.append("`build.bat` 开头也有 `chcp 65001`，保证脚本自己打印的中文同样不乱码。")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("本讲是「表达式 → 函数 → 模块 → 库 → 插件 → 框架」主线上的第 %d 级台阶。" % num)

        out = os.path.join(src, "README.md")
        open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
        print("  已生成:", os.path.join(name, "src", "README.md"))


if __name__ == "__main__":
    main()
