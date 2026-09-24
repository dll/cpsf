# -*- coding: utf-8 -*-
"""为综合篇生成 Markdown 讲义与 README（从讲解脚本 + PPTX 页标题提取）。

用法：python tools/gen_summary_docs.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from subtitle_text import show_text  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LECTURE_DIR = os.path.join(ROOT, "15_综合篇")

# 页标题与讲解脚本一一对应（取自 课件.pptx 每页首行）
PAGE_TITLES = [
    "封面：从程序员到架构师",
    "整条路线：六级台阶",
    "第1讲 表达式：一行代码里的骨架",
    "第2讲 控制结构：程序活了",
    "第3讲 函数封装：给逻辑起名字",
    "第4讲 多文件模块：按职责分家",
    "第5讲 指针：全系列的分水岭",
    "第6讲 数组：一段连续内存",
    "第7讲 结构体：把数据打包",
    "第8讲 链表：随时能长的数据结构",
    "第9讲 静态库：复用做到了",
    "第10讲 动态库：共享做到了",
    "第11讲 运行时加载：不链接也能调用",
    "第12讲 接口抽象：定一份契约",
    "第13讲 插件框架：控制反转",
    "第14讲 完整项目：零件装成机器",
    "六次跃迁：变化被挪到了哪里",
    "同一件事的四种写法",
    "十四讲沉淀的三条原则",
    "运行演示：机器真的转起来了",
    "思考题 ①②",
    "解答 ①②",
    "思考题 ③④",
    "解答 ③④ 与全系列总结",
]


def build_script_md(script):
    lines = [
        "# 综合篇 · 讲解稿（24 段）",
        "",
        "> 与《从表达式到框架 · 14讲综合篇》视频逐段对应：",
        "> 第 N 段 = 课件第 N 页 = 视频第 N 个镜头。",
        "> 全文 %d 字，片长约 11 分钟。" % sum(len(x) for x in script),
        "",
        "---",
        "",
    ]
    for i, seg in enumerate(script, 1):
        lines.append("## 第 %d 页 · %s" % (i, PAGE_TITLES[i - 1]))
        lines.append("")
        lines.append(show_text(seg).strip())
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_本文件由 `tools/gen_summary_docs.py` 从 `video/讲解脚本.json` 自动生成，")
    lines.append("_改稿后重跑该脚本即可同步。_")
    return "\n".join(lines)


README = """# 综合篇：从表达式到框架

> 一节课把 14 讲串成一条线 —— 从一行 `printf` 走到可插拔的插件框架。

| 项目 | 内容 |
|---|---|
| 定位 | 全系列总复习 / 导学（可单独看，也可学完 14 讲后回看） |
| 时长 | 约 11 分钟（24 页 ↔ 24 段配音 ↔ 140 条硬字幕） |
| 成片 | 项目根目录 `从表达式到框架 · 14讲综合篇.mp4` |
| 课件 | `docs/课件.pptx`（24 页，同时复制一份到项目根目录与视频同名） |
| 配音 | SAPI 合成（Voicebox 未就绪时的兜底方案，成片完整） |

## 目录

```
15_综合篇/
├── README.md              本文件
├── 讲解稿.md              24 段讲解全文（Markdown，便于阅读与检索）
├── docs/
│   ├── 课件.pptx          24 页课件（ppt_kit 生成，逐页质检）
│   └── generate_ppt.py    课件生成脚本（可复现、可改稿重生成）
└── video/
    ├── 讲解脚本.json      24 段口播稿（配音与字幕的唯一数据源）
    └── video_meta.json    鼠标锚点、演示段配置
```

## 内容结构

| 页码 | 内容 |
|---|---|
| P1–2 | 封面 + 六级台阶主线地图（表达式 → 函数 → 模块 → 库 → 插件 → 框架） |
| P3–16 | 14 讲逐讲要点：每讲一页「痛点 → 解法 → 遗留问题 + 关键代码」 |
| P17–18 | 六次跃迁对比表 + 同一存款功能的四种写法（代码演进） |
| P19 | 三条设计原则：解耦 / 契约先行 / 开闭原则 |
| P20 | 运行演示：终端打字动画展示插件扫描、注册、优雅降级 |
| P21–24 | 思考题 ①②③④ + 解答 + 全系列总结 |

## 怎么重新生成

```bash
# 1. 课件
python 15_综合篇/docs/generate_ppt.py

# 2. 渲染幻灯片
python tools/render_slides.py "15_综合篇/docs/课件.pptx" "15_综合篇/video/_work/v6images" 1920

# 3. 配音
python tools/tts_batch.py "15_综合篇" 1 24

# 4. 成片
python tools/build_video.py "15_综合篇" --audio-dir audio_tts --jobs 8 --out summary.mp4

# 5. 同步 Markdown 讲义
python tools/gen_summary_docs.py
```

中间产物落在 `video/_work/`（已被 `.gitignore` 忽略），根目录只保留成片。
"""


def main():
    script = json.load(open(
        os.path.join(LECTURE_DIR, "video", "讲解脚本.json"), encoding="utf-8"))
    assert len(script) == len(PAGE_TITLES), (len(script), len(PAGE_TITLES))

    md = build_script_md(script)
    p = os.path.join(LECTURE_DIR, "讲解稿.md")
    open(p, "w", encoding="utf-8", newline="\n").write(md)
    print("讲解稿.md  %d 字" % len(md))

    p = os.path.join(LECTURE_DIR, "README.md")
    open(p, "w", encoding="utf-8", newline="\n").write(README)
    print("README.md  %d 字" % len(README))


if __name__ == "__main__":
    main()
