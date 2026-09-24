# -*- coding: utf-8 -*-
"""为 14 讲生成统一格式的顶层 README.md（讲次导读）。

读取：docs/课件.md（标题 + 本讲目标）、src/ 真实文件清单、video/讲解.mp4（时长）
输出：<讲目录>/README.md
"""
import os
import re
import subprocess
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFPROBE = r"D:\development\ffmpeg-8.0.1-full_build\bin\ffprobe.exe"

LECTURES = [
    ("01_你好世界", "你好世界", "程序骨架", "从一个 printf 出发，看清 C 程序的骨架与编译运行全流程。"),
    ("02_控制结构", "控制结构", "程序骨架", "用 ATM 菜单把顺序、分支、循环串成一段真正能跑的逻辑。"),
    ("03_函数封装", "函数封装", "函数", "把 main 里的长代码拆成函数，第一次尝到复用的甜头。"),
    ("04_多文件编程", "多文件编程", "模块", "代码按职责分文件，用头文件声明契约，迈出模块化的第一步。"),
    ("05_指针", "指针", "数据结构", "地址即一切：理解指针是打通后面所有关卡的钥匙。"),
    ("06_数组", "数组", "数据结构", "连续内存 + 下标运算，看清数组与指针的同与不同。"),
    ("07_结构体", "结构体", "数据结构", "把相关数据打包成一个整体，从散装变量走向数据建模。"),
    ("08_链表", "链表", "数据结构", "用指针把节点串起来，获得运行期可增长的数据结构。"),
    ("09_静态库", "静态库", "库", "把通用代码打包成 .a，编译期链接，第一次交付一个真正的库。"),
    ("10_动态库", "动态库", "库", "把库变成 .dll/.so，运行期共享，多个程序共用一份代码。"),
    ("11_运行时加载", "运行时加载", "插件", "不链接也能调用：dlopen/LoadLibrary 在运行期把代码装进来。"),
    ("12_接口抽象", "接口抽象", "插件", "用函数指针表定义契约，宿主与实现彻底解耦。"),
    ("13_插件框架", "插件框架", "框架", "框架定骨架、插件填血肉，控制反转让框架来调用你。"),
    ("14_完整项目", "完整项目", "框架", "把十四讲的零件装成一台能跑的机器，并收回整条演进路线。"),
]


def video_duration(path):
    if not os.path.exists(path):
        return None
    try:
        out = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration",
             "-of", "json", path],
            capture_output=True, timeout=60)
        sec = float(json.loads(out.stdout)["format"]["duration"])
        return "%d 分 %02d 秒" % (int(sec // 60), int(sec % 60))
    except Exception:
        return None


def course_title_and_goals(docs_md):
    """从课件.md 提取标题与本讲目标前几条。"""
    title, goals = None, []
    if os.path.exists(docs_md):
        text = open(docs_md, encoding="utf-8", errors="replace").read()
        m = re.search(r"^#\s+(.+)$", text, re.M)
        if m:
            title = m.group(1).strip()
        # 本讲目标区块
        m = re.search(r"##\s*.*?本讲目标.*?\n(.*?)(?=\n##\s|\Z)", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                line = line.strip()
                if line.startswith("- "):
                    g = line[2:].strip()
                    g = re.sub(r"`([^`]+)`", r"\1", g)
                    if len(g) > 4:
                        goals.append(g)
    return title, goals[:4]


def src_tree(src_dir, indent=""):
    """列出 src 下的源码（跳过产物与说明文件）。"""
    rows = []
    if not os.path.isdir(src_dir):
        return rows
    names = []
    for name in sorted(os.listdir(src_dir)):
        p = os.path.join(src_dir, name)
        if os.path.isdir(p):
            sub = [f for f in sorted(os.listdir(p)) if f.endswith((".c", ".h"))]
            if sub:
                names.append(name + "/")
                names.extend("    " + f for f in sub[:6])
        elif name.endswith((".c", ".h")):
            names.append(name)
    for n in names:
        mark = "" if n.startswith("    ") else "├── "
        rows.append(indent + mark + n)
    return rows


def build(idx, folder, topic, stage, summary):
    num = idx + 1
    docs_md = os.path.join(ROOT, folder, "docs", "课件.md")
    src_dir = os.path.join(ROOT, folder, "src")
    mp4 = os.path.join(ROOT, folder, "video", "讲解.mp4")

    md_title, goals = course_title_and_goals(docs_md)
    heading = md_title or ("第%d讲：%s" % (num, topic))
    dur = video_duration(mp4) or "—"

    prev_row = ("| ⬅️ 上一讲 | [%s](../%s/) | %s |" %
                (LECTURES[idx - 1][1], LECTURES[idx - 1][0], LECTURES[idx - 1][3])
                if idx > 0 else "| ⬅️ 上一讲 | —— | 这是起点 |")
    next_row = ("| ➡️ 下一讲 | [%s](../%s/) | %s |" %
                (LECTURES[idx + 1][1], LECTURES[idx + 1][0], LECTURES[idx + 1][3])
                if idx < len(LECTURES) - 1 else "| ➡️ 下一讲 | —— | 全系列收官 |")

    goal_lines = "\n".join("- %s" % g for g in goals) if goals else "- %s" % summary
    tree_lines = "\n".join(src_tree(src_dir, "│   ")) or "│   （见 src 目录）"

    return """# %s

> **从程序员到架构师 · C语言插件框架演进之旅**
>
> 第%d讲 / 共14讲 ｜ 视频时长：%s

---

## 📋 本讲概览

| 项目 | 内容 |
|:---:|---|
| **讲次** | %02d / 14 |
| **主题** | %s |
| **关键词** | %s |
| **视频** | `video/讲解.mp4`（%s，含硬字幕） |
| **课件** | `docs/课件.pptx`（18 页） ｜ `docs/课件.md` |
| **代码** | `src/`（可直接编译运行） |

---

## 🎯 本讲目标

%s

---

## 📁 目录结构

```
%s/
├── src/
%s
│   ├── build.bat      # Windows 编译脚本（双击即可）
│   ├── Makefile       # 跨平台构建（make / make run）
│   └── 运行示例.txt    # 一次完整演示的真实输出
├── docs/
│   ├── 课件.md        # Markdown 课件
│   ├── 课件.pptx      # 投影用课件（由 generate_ppt.py 生成）
│   └── generate_ppt.py
├── video/
│   ├── 讲解.mp4       # 讲解视频（硬字幕 + 鼠标同步）
│   ├── 讲解.srt       # 字幕
│   └── 讲解脚本.json   # 18 段口播稿
├── 思考题.md
└── README.md
```

---

## 🚀 快速开始

```bash
cd src
build.bat          # Windows：双击或命令行执行（chcp 65001，中文不乱码）
# 或
make run           # Linux / Git Bash：编译并自动演示
```

---

## 📖 学习路径

1. **看视频**（%s）→ `video/讲解.mp4`
2. **读课件**（20 分钟）→ `docs/课件.md`
3. **跑代码**（15 分钟）→ `src/`，照着 `运行示例.txt` 复现一遍
4. **做思考题**（5 分钟）→ `思考题.md`（课件与视频内均含答案）

---

## 🔗 前后衔接

| 方向 | 讲次 | 内容 |
|:---:|:---|:---|
%s
%s

---

*主线位置：表达式 → 函数 → 模块 → 库 → 插件 → 框架*
""" % (heading, num, dur, num, topic,
       "%s · %s" % (topic, stage),
       dur, goal_lines, folder, tree_lines, dur, prev_row, next_row)


def main():
    for idx, (folder, topic, stage, summary) in enumerate(LECTURES):
        path = os.path.join(ROOT, folder, "README.md")
        content = build(idx, folder, topic, stage, summary)
        open(path, "w", encoding="utf-8", newline="\n").write(content)
        print("%-14s README.md  %d 字" % (folder, len(content)))


if __name__ == "__main__":
    main()
