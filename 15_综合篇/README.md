# 综合篇：从表达式到框架

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
