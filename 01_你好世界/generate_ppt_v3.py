# -*- coding: utf-8 -*-
"""
第1阶段：表达式 —— V3 深度版 PPT生成脚本
重点：编译四阶段详解 + 知识图谱 + 选择题
风格：轻松愉快、卡通风、明亮配色
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 配色方案（轻松活泼风）
COLORS = {
    'primary': RGBColor(0xFF, 0x8C, 0x42),    # 暖橙色
    'secondary': RGBColor(0x4E, 0xCD, 0xC4),   # 薄荷绿
    'accent': RGBColor(0xFF, 0x6B, 0x6B),      # 珊瑚红
    'dark': RGBColor(0x2C, 0x3E, 0x50),        # 深灰蓝
    'light': RGBColor(0xF7, 0xF9, 0xFC),       # 浅灰蓝
    'yellow': RGBColor(0xFF, 0xD9, 0x3D),      # 明黄色
    'purple': RGBColor(0xA2, 0x9B, 0xFE),      # 薰衣草紫
    'pink': RGBColor(0xFF, 0x85, 0xA6),        # 粉红色
    'green': RGBColor(0x6B, 0xCB, 0x77),       # 草绿色
    'blue': RGBColor(0x74, 0xB9, 0xFF),        # 天蓝色
    'white': RGBColor(0xFF, 0xFF, 0xFF),
    'text': RGBColor(0x2C, 0x3E, 0x50),
    'text_light': RGBColor(0x7F, 0x8C, 0x8D),
}

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_bg(slide, color=COLORS['light']):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_rounded_rect(slide, left, top, width, height, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(2)
    else:
        shape.line.fill.background()
    return shape

def add_circle(slide, left, top, size, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text(slide, left, top, width, height, text, font_size=24, color=COLORS['text'], bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = '微软雅黑'
    return txBox

def add_title_bar(slide, title, subtitle=None):
    # 顶部装饰条
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLORS['primary']
    bar.line.fill.background()
    
    add_text(slide, Inches(0.8), Inches(0.4), Inches(12), Inches(0.7),
             title, font_size=34, color=COLORS['dark'], bold=True)
    
    if subtitle:
        add_text(slide, Inches(0.8), Inches(1.05), Inches(12), Inches(0.45),
                 subtitle, font_size=16, color=COLORS['text_light'])
    
    add_text(slide, Inches(0.8), Inches(7.05), Inches(12), Inches(0.3),
             "从程序员到架构师 · 第1讲：表达式（深度版）", font_size=11, color=COLORS['text_light'])

# ========== 第1页：封面 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, COLORS['light'])

# 装饰圆形
for x, y, size, color in [
    (Inches(11), Inches(0.3), Inches(2.2), COLORS['primary']),
    (Inches(0.3), Inches(5.3), Inches(1.8), COLORS['secondary']),
    (Inches(11.5), Inches(5.5), Inches(1.2), COLORS['yellow']),
    (Inches(1.5), Inches(0.8), Inches(0.9), COLORS['pink']),
    (Inches(10), Inches(6.3), Inches(0.7), COLORS['purple']),
]:
    circle = add_circle(slide, x, y, size, color)
    circle.fill.transparency = 0.25

add_text(slide, Inches(1), Inches(2.0), Inches(11), Inches(1.0),
         "第1讲：表达式", font_size=56, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(3.1), Inches(11), Inches(0.7),
         "—— C语言的灵魂（深度版）", font_size=30, color=COLORS['primary'], bold=True, align=PP_ALIGN.CENTER)

# 分隔线
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5), Inches(4.0), Inches(3.3), Inches(0.05))
line.fill.solid()
line.fill.fore_color.rgb = COLORS['secondary']
line.line.fill.background()

add_text(slide, Inches(1), Inches(4.3), Inches(11), Inches(0.5),
         "从程序员到架构师 · C语言插件框架演进之旅", font_size=20, color=COLORS['text_light'], align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(5.0), Inches(11), Inches(0.5),
         "一行 printf 背后的完整故事", font_size=18, color=COLORS['accent'], align=PP_ALIGN.CENTER)
add_text(slide, Inches(5), Inches(5.7), Inches(3.3), Inches(0.6),
         "01 / 12", font_size=24, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# ========== 第2页：知识图谱 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🗺️ 知识图谱 · 第1讲", "本讲在整个知识体系中的位置")

# 中心节点
center_x = Inches(6.1)
center_y = Inches(3.5)
add_rounded_rect(slide, center_x - Inches(1.2), center_y - Inches(0.5), Inches(2.4), Inches(1),
                 COLORS['primary'], COLORS['primary'])
add_text(slide, center_x - Inches(1.2), center_y - Inches(0.4), Inches(2.4), Inches(0.4),
         "📌 表达式", font_size=22, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, center_x - Inches(1.2), center_y + Inches(0.1), Inches(2.4), Inches(0.35),
         "（第1讲 核心）", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 周围节点
nodes = [
    ("C语言基础", COLORS['yellow'], Inches(2.5), Inches(1.8), "前置知识"),
    ("编译四阶段", COLORS['blue'], Inches(1.5), Inches(4.0), "预处理/编译/汇编/链接"),
    ("C标准库", COLORS['purple'], Inches(9.5), Inches(1.8), "libc / printf"),
    ("函数调用", COLORS['secondary'], Inches(9.8), Inches(4.0), "→ 第2讲"),
    ("可执行文件", COLORS['green'], Inches(5.5), Inches(5.8), "程序的诞生"),
]

for name, color, x, y, desc in nodes:
    add_rounded_rect(slide, x, y, Inches(2.2), Inches(0.8), color, color)
    add_text(slide, x, y + Inches(0.08), Inches(2.2), Inches(0.35),
             name, font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(0.45), Inches(2.2), Inches(0.3),
             desc, font_size=11, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 连接线（简单的直线表示）
for nx, ny in [(Inches(3.6), Inches(2.2)), (Inches(2.6), Inches(4.4)),
               (Inches(9.6), Inches(2.2)), (Inches(9.9), Inches(4.4)),
               (Inches(6.6), Inches(5.8))]:
    line = slide.shapes.add_connector(1, center_x, center_y, nx + Inches(1.1), ny + Inches(0.4))
    line.line.color.rgb = COLORS['text_light']
    line.line.width = Pt(1.5)

# 底部说明
add_text(slide, Inches(1), Inches(6.5), Inches(11), Inches(0.4),
         "💡 本讲核心：表达式是代码的最小单元，连接了编译原理、标准库、函数调用等多个知识领域",
         font_size=14, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ========== 第3页：拆解printf表达式 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔍 拆解 printf 表达式", "一行代码里的大学问")

# 代码展示
code_box = add_rounded_rect(slide, Inches(1.5), Inches(2.0), Inches(10.3), Inches(1.5),
                            RGBColor(0x2C, 0x3E, 0x50), RGBColor(0x2C, 0x3E, 0x50))
add_text(slide, Inches(2), Inches(2.5), Inches(9.3), Inches(0.6),
         'printf("Hello, Plugin Framework!\\n");', font_size=28, color=COLORS['green'], bold=True, align=PP_ALIGN.CENTER)

# 四个拆解部分
parts = [
    ("printf", "函数名", "print formatted\n格式化打印", COLORS['primary'], Inches(1.0)),
    ('"Hello..."', "字符串参数", "要打印的内容\n双引号=字符串", COLORS['secondary'], Inches(3.8)),
    ("\\n", "转义字符", "换行符\n像按回车键", COLORS['yellow'], Inches(6.6)),
    (";", "分号", "语句结束标志\n像句子的句号", COLORS['pink'], Inches(9.2)),
]

for code, name, desc, color, x in parts:
    add_rounded_rect(slide, x, Inches(4.0), Inches(2.8), Inches(2.5),
                     COLORS['white'], color)
    add_text(slide, x, Inches(4.15), Inches(2.8), Inches(0.5),
             code, font_size=18, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, Inches(4.75), Inches(2.8), Inches(0.4),
             name, font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.2), Inches(5.3), Inches(2.4), Inches(1.0),
             desc, font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ========== 第4页：关键问题 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "❓ 一个关键问题", "printf 的代码在哪里？")

# 左边：我们的代码
add_rounded_rect(slide, Inches(1), Inches(2.0), Inches(4.5), Inches(4.5),
                 COLORS['white'], COLORS['blue'])
add_text(slide, Inches(1), Inches(2.2), Inches(4.5), Inches(0.5),
         "📄 我们写的 hello.c", font_size=20, color=COLORS['blue'], bold=True, align=PP_ALIGN.CENTER)

our_code = [
    '#include <stdio.h>',
    '',
    'int main() {',
    '    printf("Hello!");',
    '    return 0;',
    '}',
]
for i, line in enumerate(our_code):
    add_text(slide, Inches(1.3), Inches(2.9 + i * 0.45), Inches(4), Inches(0.4),
             line, font_size=14, color=COLORS['text'])

add_text(slide, Inches(1.3), Inches(5.7), Inches(4), Inches(0.5),
         "🤔 printf 的实现在哪？", font_size=16, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# 中间：问号箭头
add_text(slide, Inches(5.7), Inches(3.5), Inches(2), Inches(1),
         "❓\n从哪来？", font_size=24, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# 右边：标准库
add_rounded_rect(slide, Inches(8), Inches(2.0), Inches(4.5), Inches(4.5),
                 COLORS['white'], COLORS['purple'])
add_text(slide, Inches(8), Inches(2.2), Inches(4.5), Inches(0.5),
         "📦 C 标准库（libc）", font_size=20, color=COLORS['purple'], bold=True, align=PP_ALIGN.CENTER)

lib_funcs = [
    "✅ printf / scanf",
    "✅ malloc / free",
    "✅ strcpy / strlen",
    "✅ fopen / fread",
    "✅ sin / cos / sqrt",
    "✅ ...还有几百个函数",
]
for i, func in enumerate(lib_funcs):
    add_text(slide, Inches(8.5), Inches(3.0 + i * 0.45), Inches(3.5), Inches(0.4),
             func, font_size=14, color=COLORS['text'])

add_text(slide, Inches(8), Inches(5.8), Inches(4.5), Inches(0.5),
         "工具箱里有几百个工具", font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ========== 第5页：编译四阶段总览 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🏭 编译四阶段总览", "从 hello.c 到 hello.exe 的流水线")

# 流水线
stages = [
    ("hello.c", "源代码", COLORS['blue'], Inches(0.5)),
    ("📋 预处理", "展开头文件", COLORS['yellow'], Inches(2.5)),
    ("⚙️ 编译", "翻译成汇编", COLORS['primary'], Inches(4.7)),
    ("🔢 汇编", "生成机器码", COLORS['secondary'], Inches(6.9)),
    ("🔗 链接", "拼入库代码", COLORS['purple'], Inches(9.1)),
    ("hello.exe", "可执行文件", COLORS['green'], Inches(11.3)),
]

for i, (name, desc, color, x) in enumerate(stages):
    # 箭头（除了第一个）
    if i > 0:
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x - Inches(0.6), Inches(3.5), Inches(0.5), Inches(0.4))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = COLORS['text_light']
        arrow.line.fill.background()
    
    # 阶段框
    add_rounded_rect(slide, x, Inches(2.8), Inches(1.9), Inches(1.8),
                     color, color)
    add_text(slide, x, Inches(3.0), Inches(1.9), Inches(0.5),
             name, font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, Inches(3.7), Inches(1.9), Inches(0.7),
             desc, font_size=12, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 底部记忆口诀
add_rounded_rect(slide, Inches(3.5), Inches(5.5), Inches(6.3), Inches(0.9),
                 COLORS['light'], COLORS['accent'])
add_text(slide, Inches(3.5), Inches(5.65), Inches(6.3), Inches(0.4),
         "💡 记忆口诀：预 → 编 → 汇 → 链", font_size=20, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(3.5), Inches(6.05), Inches(6.3), Inches(0.35),
         "（谐音：预判会练）", font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ========== 第6页：阶段4链接的秘密（重点） ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "⭐ 重点：链接的秘密", "printf 是怎么跑进我们的程序里的？")

# 链接过程图示
add_text(slide, Inches(1), Inches(1.8), Inches(11), Inches(0.5),
         "链接器做了什么？", font_size=24, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# 左边：hello.o
add_rounded_rect(slide, Inches(0.8), Inches(2.6), Inches(3), Inches(3.5),
                 COLORS['white'], COLORS['blue'])
add_text(slide, Inches(0.8), Inches(2.8), Inches(3), Inches(0.5),
         "📄 hello.o", font_size=18, color=COLORS['blue'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.1), Inches(3.5), Inches(2.4), Inches(2.2),
         "✅ 我们的代码\n   (main函数)\n\n❌ printf 未定义\n   (U printf)\n\n⚠️ 不能独立运行！",
         font_size=13, color=COLORS['text'])

# 中间：链接器 + 标准库
add_rounded_rect(slide, Inches(4.5), Inches(2.6), Inches(4.3), Inches(3.5),
                 COLORS['white'], COLORS['purple'])
add_text(slide, Inches(4.5), Inches(2.8), Inches(4.3), Inches(0.5),
         "🔗 链接器 + 📦 标准库", font_size=17, color=COLORS['purple'], bold=True, align=PP_ALIGN.CENTER)

link_steps = [
    "1️⃣ 符号解析：找未定义函数",
    "2️⃣ 库中查找：去libc找printf",
    "3️⃣ 代码合并：把printf拼进来",
    "4️⃣ 地址重定位：调整调用地址",
]
for i, step in enumerate(link_steps):
    add_text(slide, Inches(4.8), Inches(3.5 + i * 0.55), Inches(3.7), Inches(0.45),
             step, font_size=13, color=COLORS['text'])

# 右边：hello.exe
add_rounded_rect(slide, Inches(9.5), Inches(2.6), Inches(3), Inches(3.5),
                 COLORS['white'], COLORS['green'])
add_text(slide, Inches(9.5), Inches(2.8), Inches(3), Inches(0.5),
         "🚀 hello.exe", font_size=18, color=COLORS['green'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(9.8), Inches(3.5), Inches(2.4), Inches(2.2),
         "✅ 我们的代码\n   (main函数)\n\n✅ printf 的实现\n   (从库中拼进来)\n\n🎉 可以独立运行！",
         font_size=13, color=COLORS['text'])

# 箭头
for start_x, end_x in [(Inches(3.8), Inches(4.5)), (Inches(8.8), Inches(9.5))]:
    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, start_x, Inches(4.1), Inches(0.7), Inches(0.5))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = COLORS['primary']
    arrow.line.fill.background()

# 底部金句
add_rounded_rect(slide, Inches(2), Inches(6.4), Inches(9.3), Inches(0.7),
                 COLORS['primary'], COLORS['primary'])
add_text(slide, Inches(2), Inches(6.55), Inches(9.3), Inches(0.45),
         "🔑 链接的本质：把我们的代码和库的代码拼在一起，形成完整的可执行程序。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ========== 第7页：头文件 vs 库文件 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📋 头文件 vs 🍳 库文件", "很多初学者搞混的概念，一次讲清楚")

# 左边：头文件
add_rounded_rect(slide, Inches(0.8), Inches(2.0), Inches(5.5), Inches(4.8),
                 COLORS['white'], COLORS['secondary'])
add_text(slide, Inches(0.8), Inches(2.2), Inches(5.5), Inches(0.6),
         "📋 头文件 (.h)", font_size=24, color=COLORS['secondary'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, Inches(1.3), Inches(3.0), Inches(4.5), Inches(0.5),
         "= 菜单", font_size=20, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

h_points = [
    "• 里面是函数声明（接口）",
    "• 告诉编译器：有这个函数，长这样",
    "• 不包含具体实现代码",
    "• 编译阶段使用",
    "• 例子：stdio.h, stdlib.h, string.h",
]
for i, p in enumerate(h_points):
    add_text(slide, Inches(1.3), Inches(3.7 + i * 0.5), Inches(4.5), Inches(0.45),
             p, font_size=14, color=COLORS['text'])

# 右边：库文件
add_rounded_rect(slide, Inches(7), Inches(2.0), Inches(5.5), Inches(4.8),
                 COLORS['white'], COLORS['purple'])
add_text(slide, Inches(7), Inches(2.2), Inches(5.5), Inches(0.6),
         "🍳 库文件 (.a/.dll)", font_size=24, color=COLORS['purple'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, Inches(7.5), Inches(3.0), Inches(4.5), Inches(0.5),
         "= 厨房", font_size=20, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

lib_points = [
    "• 里面是函数实现（真正的代码）",
    "• 链接器把它拼进你的程序",
    "• 包含几百个函数的二进制代码",
    "• 链接阶段使用",
    "• 例子：libc.a, msvcrt.dll",
]
for i, p in enumerate(lib_points):
    add_text(slide, Inches(7.5), Inches(3.7 + i * 0.5), Inches(4.5), Inches(0.45),
             p, font_size=14, color=COLORS['text'])

# 中间VS
add_text(slide, Inches(6), Inches(4.0), Inches(1.3), Inches(0.8),
         "VS", font_size=32, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# ========== 第8页：课堂小测 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "✅ 课堂小测", "看看你掌握了多少？")

# 题目
add_rounded_rect(slide, Inches(1), Inches(1.8), Inches(11.3), Inches(1.2),
                 COLORS['white'], COLORS['primary'])
add_text(slide, Inches(1.3), Inches(2.0), Inches(10.7), Inches(0.5),
         "题目：目标文件（.o）为什么不能直接运行？", font_size=22, color=COLORS['dark'], bold=True)

# 选项
options = [
    ("A", "因为它是二进制的", COLORS['text_light']),
    ("B", "因为缺少库函数的实现", COLORS['green']),
    ("C", "因为它太大了", COLORS['text_light']),
    ("D", "因为操作系统不认识 .o 格式", COLORS['text_light']),
]

for i, (letter, text, color) in enumerate(options):
    x = Inches(1 + (i % 2) * 5.8)
    y = Inches(3.3 + (i // 2) * 1.5)
    
    opt_box = add_rounded_rect(slide, x, y, Inches(5.5), Inches(1.2),
                               COLORS['white'], color)
    add_text(slide, x + Inches(0.3), y + Inches(0.3), Inches(0.8), Inches(0.6),
             letter, font_size=28, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(1.2), y + Inches(0.4), Inches(4), Inches(0.5),
             text, font_size=18, color=COLORS['text'])

# 答案（底部）
add_rounded_rect(slide, Inches(2.5), Inches(6.3), Inches(8.3), Inches(0.8),
                 COLORS['green'], COLORS['green'])
add_text(slide, Inches(2.5), Inches(6.45), Inches(8.3), Inches(0.5),
         "✅ 正确答案：B —— 目标文件只有我们的代码，库函数还没链接进来！",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ========== 第9页：进化视角 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🌱 进化视角", "从表达式到插件框架")

# 演进路线
stages = [
    ("01", "表达式", COLORS['primary'], True),
    ("02", "函数", COLORS['secondary'], False),
    ("03", "模块", COLORS['yellow'], False),
    ("04", "静态库", COLORS['purple'], False),
    ("05", "动态库", COLORS['pink'], False),
    ("...", "...", COLORS['text_light'], False),
    ("10", "插件框架", COLORS['accent'], False),
]

for i, (num, name, color, active) in enumerate(stages):
    x = Inches(0.5 + i * 1.75)
    y = Inches(3.0)
    
    # 连接线
    if i < len(stages) - 1:
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                       x + Inches(1.1), y + Inches(0.45),
                                       Inches(0.65), Inches(0.1))
        line.fill.solid()
        line.fill.fore_color.rgb = COLORS['text_light']
        line.line.fill.background()
    
    # 圆圈
    circle = add_circle(slide, x, y, Inches(1), color)
    if not active:
        circle.fill.transparency = 0.4
    
    add_text(slide, x, y + Inches(0.2), Inches(1), Inches(0.4),
             num, font_size=20, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x - Inches(0.2), y + Inches(1.1), Inches(1.4), Inches(0.4),
             name, font_size=13, color=COLORS['dark'], bold=active, align=PP_ALIGN.CENTER)

# 种子概念
add_text(slide, Inches(1), Inches(4.8), Inches(11), Inches(0.5),
         "🌱 今天播下的种子，后面都会发芽：", font_size=20, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

seeds = [
    ("函数调用", "→ 第2讲"),
    ("头文件vs实现", "→ 第3讲"),
    ("标准库", "→ 第4讲"),
    ("链接思想", "→ 贯穿全系列"),
]
for i, (seed, next_) in enumerate(seeds):
    x = Inches(1 + i * 2.9)
    add_rounded_rect(slide, x, Inches(5.5), Inches(2.6), Inches(1),
                     COLORS['white'], COLORS['yellow'])
    add_text(slide, x, Inches(5.65), Inches(2.6), Inches(0.4),
             seed, font_size=15, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, Inches(6.1), Inches(2.6), Inches(0.35),
             next_, font_size=12, color=COLORS['accent'], align=PP_ALIGN.CENTER)

# ========== 第10页：小结 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📝 小结", "一行 printf 的完整生命周期")

add_text(slide, Inches(1), Inches(1.8), Inches(11), Inches(0.6),
         "🎯 一句话总结", font_size=28, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

summary_box = add_rounded_rect(slide, Inches(1.5), Inches(2.6), Inches(10.3), Inches(1.4),
                               COLORS['primary'], COLORS['primary'])
add_text(slide, Inches(1.5), Inches(2.85), Inches(10.3), Inches(1),
         "一行 printf 表达式，从代码到输出，经历了编译四阶段，\n通过链接把标准库的 printf 拼进来，最终在屏幕上打出 Hello。\n这就是复用的起点，也是框架的起点。",
         font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 五个知识点
points = [
    ("1️⃣", "表达式", "能算值的代码片段\nC语言几乎一切都是表达式"),
    ("2️⃣", "C标准库", "自带的工具箱\nprintf/malloc/strcpy都在这"),
    ("3️⃣", "头文件vs库", "头文件是接口（菜单）\n库文件是实现（厨房）"),
    ("4️⃣", "编译四阶段", "预→编→汇→链\n记忆口诀：预判会练"),
    ("5️⃣", "链接的本质", "把我们的代码和库的代码\n拼在一起"),
]

for i, (num, title, desc) in enumerate(points):
    x = Inches(0.5 + i * 2.55)
    y = Inches(4.4)
    
    add_rounded_rect(slide, x, y, Inches(2.35), Inches(2.3),
                     COLORS['white'], COLORS['secondary'])
    add_text(slide, x, y + Inches(0.15), Inches(2.35), Inches(0.5),
             num, font_size=28, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(0.7), Inches(2.35), Inches(0.4),
             title, font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.15), y + Inches(1.2), Inches(2.05), Inches(1),
             desc, font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 保存
output_path = r"e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\01_你好世界\docs\课件.pptx"
prs.save(output_path)
print(f"PPT V3生成完成：{output_path}")
