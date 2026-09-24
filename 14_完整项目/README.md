# 第14讲 · 完整项目与全系列总结

> **从程序员到架构师 · C语言插件框架演进之旅**
>
> 第14讲 / 共14讲 ｜ 视频时长：10 分 03 秒

---

## 📋 本讲概览

| 项目 | 内容 |
|:---:|---|
| **讲次** | 14 / 14 |
| **主题** | 完整项目 |
| **关键词** | 完整项目 · 框架 |
| **视频** | `video/讲解.mp4`（10 分 03 秒，含硬字幕） |
| **课件** | `docs/课件.pptx`（18 页） ｜ `docs/课件.md` |
| **代码** | `src/`（可直接编译运行） |

---

## 🎯 本讲目标

- 把十四讲的零件装成一台能跑的机器，并收回整条演进路线。

---

## 📁 目录结构

```
14_完整项目/
├── src/
│   ├── account.c
│   ├── account.h
│   ├── console_utf8.h
│   ├── dynamic_loader.c
│   ├── dynamic_loader.h
│   ├── framework.c
│   ├── framework.h
│   ├── main.c
│   ├── plugin.h
│   ├── plugins/
│       deposit_plugin.c
│       plugins.h
│       query_plugin.c
│       transfer_plugin.c
│       withdraw_plugin.c
│   ├── transaction.c
│   ├── transaction.h
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

1. **看视频**（10 分 03 秒）→ `video/讲解.mp4`
2. **读课件**（20 分钟）→ `docs/课件.md`
3. **跑代码**（15 分钟）→ `src/`，照着 `运行示例.txt` 复现一遍
4. **做思考题**（5 分钟）→ `思考题.md`（课件与视频内均含答案）

---

## 🔗 前后衔接

| 方向 | 讲次 | 内容 |
|:---:|:---|:---|
| ⬅️ 上一讲 | [插件框架](../13_插件框架/) | 框架定骨架、插件填血肉，控制反转让框架来调用你。 |
| ➡️ 下一讲 | —— | 全系列收官 |

---

*主线位置：表达式 → 函数 → 模块 → 库 → 插件 → 框架*
