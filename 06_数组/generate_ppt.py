# -*- coding: utf-8 -*-
"""
第6讲：数组 —— PPT生成脚本
风格：轻松愉快、卡通风、明亮配色、有设计感
12页幻灯片，16:9，底部标注"第6讲 数组"
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ============================================================
# 配色方案（轻松活泼风，与系列一致）
# ============================================================
COLORS = {
    'primary':   RGBColor(0xFF, 0x8C, 0x42),    # 暖橙色
    'secondary':  RGBColor(0x4E, 0xCD, 0xC4),    # 薄荷绿
    'accent':     RGBColor(0xFF, 0x6B, 0x6B),    # 珊瑚红
    'dark':       RGBColor(0x2C, 0x3E, 0x50),    # 深灰蓝
    'light':      RGBColor(0xF7, 0xF9, 0xFC),    # 浅灰蓝
    'yellow':     RGBColor(0xFF, 0xD9, 0x3D),    # 明黄色
    'purple':     RGBColor(0xA2, 0x9B, 0xFE),    # 薰衣草紫
    'pink':       RGBColor(0xFF, 0x85, 0xA6),    # 粉红色
    'green':      RGBColor(0x6B, 0xCB, 0x77),    # 草绿色
    'blue':       RGBColor(0x74, 0xB9, 0xFF),    # 天蓝色
    'white':      RGBColor(0xFF, 0xFF, 0xFF),
    'text':       RGBColor(0x2C, 0x3E, 0x50),
    'text_light': RGBColor(0x7F, 0x8C, 0x8D),
    'code_bg':    RGBColor(0x1E, 0x29, 0x3B),    # 代码背景深色
    'code_header':RGBColor(0x34, 0x49, 0x5E),    # 代码标题栏
}

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ============================================================
# 工具函数
# ============================================================

def add_bg(slide, color=COLORS['light']):
    """设置幻灯片背景"""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_shape(slide, shape_type, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    """通用形状创建"""
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    if fill_color is not None:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color is not None:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape

def add_rounded_rect(slide, left, top, width, height, fill_color, border_color=None, radius=0.08):
    """圆角矩形"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(2)
    else:
        shape.line.fill.background()
    shape.adjustments[0] = radius
    return shape

def add_circle(slide, left, top, size, fill_color):
    """圆形"""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text(slide, left, top, width, height, text, font_size=24, color=COLORS['text'],
             bold=False, align=PP_ALIGN.LEFT, font_name='微软雅黑'):
    """文本框"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = font_name
    return txBox

def add_code_block(slide, left, top, width, height, title, code_lines):
    """代码块（深色背景 + 标题栏 + 代码行）"""
    # 代码容器
    card = add_rounded_rect(slide, left, top, width, height, COLORS['code_bg'], COLORS['code_bg'], 0.06)
    # 标题栏
    header = add_shape(slide, MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.4), COLORS['code_header'])
    # 小圆点
    for i, c in enumerate([COLORS['accent'], COLORS['yellow'], COLORS['green']]):
        add_circle(slide, left + Inches(0.15 + i * 0.3), top + Inches(0.08), Inches(0.18), c)
    add_text(slide, left + Inches(1.2), top + Inches(0.02), Inches(3), Inches(0.36),
             title, font_size=11, color=COLORS['text_light'])
    # 代码行
    for i, (code, color) in enumerate(code_lines):
        add_text(slide, left + Inches(0.4), top + Inches(0.5 + i * 0.32), width - Inches(0.6), Inches(0.3),
                 code, font_size=12, color=color, font_name='Consolas')

def add_title_bar(slide, title, subtitle=None):
    """标题栏（统一风格）"""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLORS['primary']
    bar.line.fill.background()

    add_circle(slide, Inches(0.3), Inches(0.5), Inches(0.35), COLORS['primary'])
    add_circle(slide, Inches(0.55), Inches(0.55), Inches(0.25), COLORS['secondary'])

    add_text(slide, Inches(1.0), Inches(0.4), Inches(11), Inches(0.7),
             title, font_size=32, color=COLORS['dark'], bold=True)

    if subtitle:
        add_text(slide, Inches(1.0), Inches(1.05), Inches(11), Inches(0.45),
                 subtitle, font_size=15, color=COLORS['text_light'])

    # 底部标注
    add_text(slide, Inches(0.8), Inches(7.05), Inches(12), Inches(0.3),
             "第6讲 数组", font_size=11, color=COLORS['text_light'])

def draw_locker(slide, left, top, unit_w, unit_h, count, fill_colors, labels=None):
    """画一排储物柜（连续格子比喻数组）"""
    for i in range(count):
        x = left + i * unit_w
        color = fill_colors[i % len(fill_colors)]
        # 柜体
        locker = add_rounded_rect(slide, x, top, unit_w, unit_h, COLORS['white'], color, 0.1)
        # 顶部色条
        top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, x, top, unit_w, Inches(0.12), color)
        # 编号
        add_text(slide, x, top + Inches(0.18), unit_w, Inches(0.35),
                 str(i), font_size=18, color=color, bold=True, align=PP_ALIGN.CENTER)
        # 内容（如果有标签）
        if labels and i < len(labels):
            add_text(slide, x + Inches(0.05), top + Inches(0.6), unit_w - Inches(0.1), unit_h - Inches(0.7),
                     labels[i], font_size=11, color=COLORS['text'], align=PP_ALIGN.CENTER)
        # 把手
        handle = add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + unit_w * 0.35, top + unit_h - Inches(0.18), unit_w * 0.3, Inches(0.08), COLORS['text_light'])

def draw_memory_cells(slide, left, top, cell_w, cell_h, count, values, addr_labels=None):
    """画连续内存格子（带地址标注）"""
    for i in range(count):
        x = left + i * cell_w
        # 格子边框
        cell = add_rounded_rect(slide, x, top, cell_w, cell_h, COLORS['white'], COLORS['text_light'], 0.05)
        # 值
        if i < len(values):
            add_text(slide, x, top + Inches(0.05), cell_w, cell_h - Inches(0.1),
                     values[i], font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
        # 索引
        add_text(slide, x, top + cell_h + Inches(0.05), cell_w, Inches(0.3),
                 f"[{i}]", font_size=10, color=COLORS['text_light'], align=PP_ALIGN.CENTER)
        # 地址
        if addr_labels and i < len(addr_labels):
            add_text(slide, x, top - Inches(0.3), cell_w, Inches(0.25),
                     addr_labels[i], font_size=8, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

def draw_atm(slide, left, top, size, color=COLORS['blue']):
    """画一个ATM机图标"""
    body = add_rounded_rect(slide, left, top, size * 0.8, size, color, color, 0.08)
    screen = add_rounded_rect(slide, left + size * 0.1, top + size * 0.08, size * 0.6, size * 0.35,
                               RGBColor(0x1E, 0x29, 0x3B), RGBColor(0x1E, 0x29, 0x3B), 0.1)
    for i in range(3):
        line = add_shape(slide, MSO_SHAPE.RECTANGLE,
                         left + size * 0.15, top + size * (0.13 + i * 0.08),
                         size * 0.4, size * 0.03, COLORS['green'], COLORS['green'])
    keypad_y = top + size * 0.5
    for row in range(3):
        for col in range(3):
            add_circle(slide, left + size * (0.12 + col * 0.2), keypad_y + row * size * 0.12, size * 0.12, COLORS['white'])
    slot = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.2, top + size * 0.88, size * 0.4, size * 0.05,
                     COLORS['dark'], COLORS['dark'])
    return body

# ============================================================
# 第1页：封面
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, COLORS['light'])

# 背景装饰圆
add_circle(slide, Inches(9.5), Inches(-1.5), Inches(5), COLORS['secondary'])
add_circle(slide, Inches(-2), Inches(4.5), Inches(4.5), COLORS['primary'])
add_circle(slide, Inches(11), Inches(5), Inches(2.5), COLORS['yellow'])

# 卡片
card = add_rounded_rect(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5),
                        COLORS['white'], COLORS['white'], 0.05)

# 左侧 - 储物柜图标（数组比喻）
locker_y = Inches(2.5)
locker_colors = [COLORS['primary'], COLORS['secondary'], COLORS['yellow'], COLORS['green'], COLORS['purple']]
draw_locker(slide, Inches(2.0), locker_y, Inches(0.55), Inches(1.6), 5, locker_colors,
            labels=["1000", "2000", "500", "3000", "1500"])
add_text(slide, Inches(1.8), Inches(4.3), Inches(3.2), Inches(0.4),
         "一排储物柜 = 一个数组", font_size=14, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧文字
add_text(slide, Inches(5.8), Inches(2.3), Inches(6), Inches(1),
         "第6讲：数组", font_size=52, color=COLORS['dark'], bold=True)
add_text(slide, Inches(5.8), Inches(3.3), Inches(6), Inches(0.6),
         "批量数据的容器", font_size=26, color=COLORS['primary'], bold=True)

# 分隔线
divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), Inches(4.1), Inches(1.5), Inches(0.06))
divider.fill.solid()
divider.fill.fore_color.rgb = COLORS['secondary']
divider.line.fill.background()

add_text(slide, Inches(5.8), Inches(4.3), Inches(6), Inches(0.5),
         "《从程序员到架构师》· C语言插件框架演进之旅", font_size=16, color=COLORS['text_light'])
add_text(slide, Inches(5.8), Inches(4.8), Inches(6), Inches(0.5),
         "一维数组 · 字符数组 · 数组与指针 · 二维数组", font_size=18, color=COLORS['accent'], bold=True)

add_text(slide, Inches(6.0), Inches(5.4), Inches(2.3), Inches(0.5),
         "06 / 14", font_size=22, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, Inches(0.8), Inches(7.05), Inches(12), Inches(0.3),
         "第6讲 数组", font_size=11, color=COLORS['text_light'])

# ============================================================
# 第2页：知识图谱
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🗺️ 知识图谱 · 第6讲", "本讲在整个知识体系中的位置")

# 中心节点
center_x = Inches(5.8)
center_y = Inches(3.7)

add_circle(slide, center_x - Inches(1.5), center_y - Inches(1), Inches(3), COLORS['secondary'])
add_circle(slide, center_x - Inches(1.1), center_y - Inches(0.6), Inches(2.2), COLORS['secondary'])

center_card = add_rounded_rect(slide, center_x - Inches(1.3), center_y - Inches(0.55), Inches(2.6), Inches(1.1),
                               COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, center_x - Inches(1.3), center_y - Inches(0.45), Inches(2.6), Inches(0.45),
         "📦 数组", font_size=24, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, center_x - Inches(1.3), center_y + Inches(0.1), Inches(2.6), Inches(0.35),
         "（第6讲 核心）", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 周围节点
nodes = [
    ("指针", COLORS['purple'], Inches(1.0), Inches(1.3), "第5讲 · 前置", "📍"),
    ("for循环", COLORS['yellow'], Inches(0.5), Inches(3.8), "第2讲 · 前置", "🔄"),
    ("结构体", COLORS['green'], Inches(9.8), Inches(1.3), "→ 第7讲", "🔧"),
    ("链表", COLORS['blue'], Inches(9.8), Inches(3.8), "→ 第8讲", "🔗"),
    ("ATM多账户", COLORS['accent'], Inches(5.3), Inches(6.0), "本讲实战案例", "🏧"),
]

for name, color, x, y, desc, icon in nodes:
    card = add_rounded_rect(slide, x, y, Inches(2.4), Inches(1.0),
                            COLORS['white'], color, 0.15)
    add_text(slide, x + Inches(0.1), y + Inches(0.15), Inches(0.6), Inches(0.7),
             icon, font_size=28, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.7), y + Inches(0.1), Inches(1.6), Inches(0.4),
             name, font_size=15, color=COLORS['dark'], bold=True)
    add_text(slide, x + Inches(0.7), y + Inches(0.5), Inches(1.6), Inches(0.4),
             desc, font_size=10, color=COLORS['text_light'])

# 连接线
connections = [
    (center_x - Inches(0.5), center_y, Inches(3.0), Inches(1.8)),
    (center_x - Inches(0.5), center_y + Inches(0.2), Inches(2.0), Inches(4.3)),
    (center_x + Inches(0.5), center_y, Inches(9.8), Inches(1.8)),
    (center_x + Inches(0.5), center_y + Inches(0.2), Inches(9.8), Inches(4.3)),
    (center_x, center_y + Inches(0.5), Inches(6.5), Inches(6.5)),
]
for sx, sy, ex, ey in connections:
    line = slide.shapes.add_connector(1, sx, sy, ex, ey)
    line.line.color.rgb = COLORS['text_light']
    line.line.width = Pt(1.5)
    line.line.dash_style = 1

# 底部金句
tip_card = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.6),
                            COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.5), Inches(6.58), Inches(10.3), Inches(0.45),
         "💡 数组是从'单变量'到'数据结构'的第一步——衔接指针，预告结构体和链表",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第3页：为什么需要数组（储物柜比喻）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🗄️ 为什么需要数组？", "从'一堆便利贴'到'一排储物柜'")

# 左侧 - 单变量的痛苦
left_x = Inches(0.6)
left_y = Inches(2.0)

pain_card = add_rounded_rect(slide, left_x, left_y, Inches(5.5), Inches(4.3),
                              COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, left_y, Inches(5.5), Inches(0.55), COLORS['accent'])
add_text(slide, left_x, left_y + Inches(0.08), Inches(5.5), Inches(0.4),
         "😵 单变量时代的痛苦", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 散落的便利贴
notes = [
    ("balance1 = 1000", COLORS['accent']),
    ("balance2 = 2000", COLORS['yellow']),
    ("balance3 = 500", COLORS['secondary']),
    ("balance4 = 3000", COLORS['purple']),
    ("balance5 = 1500", COLORS['pink']),
]
for i, (text, color) in enumerate(notes):
    ny = left_y + Inches(0.8 + i * 0.65)
    nx = left_x + Inches(0.3 + (i % 2) * 2.5)
    note = add_rounded_rect(slide, nx, ny, Inches(2.3), Inches(0.5), color, color, 0.15)
    add_text(slide, nx, ny + Inches(0.05), Inches(2.3), Inches(0.4),
             text, font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, left_x + Inches(0.3), left_y + Inches(4.0), Inches(5.0), Inches(0.3),
         "100个账户？定义100个变量...", font_size=13, color=COLORS['accent'], bold=True)

# 右侧 - 数组的清爽
right_x = Inches(6.8)
right_y = Inches(2.0)

array_card = add_rounded_rect(slide, right_x, right_y, Inches(5.8), Inches(4.3),
                               COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, right_y, Inches(5.8), Inches(0.55), COLORS['secondary'])
add_text(slide, right_x, right_y + Inches(0.08), Inches(5.8), Inches(0.4),
         "😌 数组时代的清爽", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 储物柜图示
locker_colors = [COLORS['accent'], COLORS['yellow'], COLORS['secondary'], COLORS['purple'], COLORS['green']]
draw_locker(slide, right_x + Inches(0.5), right_y + Inches(1.0), Inches(0.85), Inches(1.8), 5, locker_colors,
            labels=["1000", "2000", "500", "3000", "1500"])

add_text(slide, right_x + Inches(0.3), right_y + Inches(3.1), Inches(5.2), Inches(0.35),
         "balances[5] = {1000, 2000, 500, 3000, 1500};",
         font_size=13, color=COLORS['secondary'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, right_x + Inches(0.3), right_y + Inches(3.6), Inches(5.2), Inches(0.35),
         "一个名字 + 编号 = 管理一整组数据", font_size=13, color=COLORS['text'])

# 中间箭头
arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.0), Inches(3.8), Inches(0.8), Inches(0.5))
arrow.fill.solid()
arrow.fill.fore_color.rgb = COLORS['primary']
arrow.line.fill.background()

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.6),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.58), Inches(10.3), Inches(0.45),
         "🏆 金句：数组就是用'一个名字 + 一个编号'管理一组同类型数据——从便利贴到储物柜！",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第4页：一维数组定义与初始化
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📋 一维数组：定义与初始化", "类型 数组名[元素个数] = {值列表};")

# 上半部分 - 语法图示
syntax_card = add_rounded_rect(slide, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.8),
                                COLORS['white'], COLORS['blue'], 0.08)
add_text(slide, Inches(1.0), Inches(1.9), Inches(11), Inches(0.4),
         "语法：类型  数组名[元素个数] = {值1, 值2, ...};",
         font_size=18, color=COLORS['dark'], bold=True)

# 四个部分用不同颜色标注
parts = [
    ("double", "类型", COLORS['green']),
    ("balances", "数组名", COLORS['primary']),
    ("[5]", "元素个数", COLORS['accent']),
    ("{1000, 2000, ...}", "初始值列表", COLORS['purple']),
]
for i, (code, label, color) in enumerate(parts):
    px = Inches(1.2 + i * 2.9)
    py = Inches(2.4)
    box = add_rounded_rect(slide, px, py, Inches(2.5), Inches(0.7), color, color, 0.2)
    add_text(slide, px, py + Inches(0.05), Inches(2.5), Inches(0.35),
             code, font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, px, py + Inches(0.4), Inches(2.5), Inches(0.3),
             label, font_size=11, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 下半部分 - 初始化方式
init_methods = [
    ("完全初始化", "double arr[5] = {1, 2, 3, 4, 5};", COLORS['green'], "5个值对应5个元素"),
    ("部分初始化", "int arr[5] = {1, 2, 3};", COLORS['yellow'], "只给3个，其余自动补0"),
    ("省略大小", "int arr[] = {10, 20, 30};", COLORS['secondary'], "编译器自动数 = 3"),
    ("全部清零", "int arr[5] = {0};", COLORS['purple'], "全部初始化为0"),
]

for i, (name, code, color, desc) in enumerate(init_methods):
    x = Inches(0.6 + i * 3.15)
    y = Inches(4.0)
    card = add_rounded_rect(slide, x, y, Inches(2.9), Inches(2.3),
                            COLORS['white'], color, 0.12)
    top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, x, y, Inches(2.9), Inches(0.08), color)

    add_text(slide, x, y + Inches(0.2), Inches(2.9), Inches(0.4),
             name, font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    add_text(slide, x + Inches(0.15), y + Inches(0.75), Inches(2.6), Inches(0.6),
             code, font_size=11, color=color, bold=True, align=PP_ALIGN.CENTER)

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.8), y + Inches(1.45), Inches(1.3), Inches(0.03))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.15), y + Inches(1.6), Inches(2.6), Inches(0.5),
             desc, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部提示
tip = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.55),
                        COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(1.5), Inches(6.57), Inches(10.3), Inches(0.4),
         "⚠️ 索引从 0 开始！arr[5] 有5个元素，索引是 0~4，没有 arr[5]",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第5页：数组遍历（for + 数组 = 天作之合）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔄 数组遍历：for + 数组 = 天作之合", "第2讲的 for 循环终于找到了主场")

# 左侧 - 内存格子图示
left_x = Inches(0.6)
left_y = Inches(2.2)

add_text(slide, left_x, left_y, Inches(5), Inches(0.4),
         "double balances[5] 内存布局：", font_size=14, color=COLORS['text'], bold=True)

# 画5个内存格子
cell_vals = ["1000.0", "2000.0", "500.0", "3000.0", "1500.0"]
addrs = ["0x1000", "0x1008", "0x1010", "0x1018", "0x1020"]
draw_memory_cells(slide, left_x + Inches(0.3), left_y + Inches(0.8), Inches(0.9), Inches(0.8), 5, cell_vals, addrs)

# 箭头标注 i 的移动
for i in range(5):
    x = left_x + Inches(0.3) + i * Inches(0.9)
    arrow_down = add_shape(slide, MSO_SHAPE.DOWN_ARROW, x + Inches(0.25), left_y + Inches(1.7), Inches(0.4), Inches(0.3), COLORS['primary'])

add_text(slide, left_x, left_y + Inches(2.2), Inches(5), Inches(0.4),
         "i = 0 → 1 → 2 → 3 → 4，逐个访问", font_size=13, color=COLORS['primary'], bold=True, align=PP_ALIGN.CENTER)

# 右侧 - 代码
right_x = Inches(6.2)
code_lines = [
    ('// 第2讲：for 循环打印5次', COLORS['text_light']),
    ('for (i = 0; i < 5; i++) {', COLORS['blue']),
    ('    printf("欢迎光临！\\n");', COLORS['green']),
    ('}', COLORS['blue']),
    ('', COLORS['text']),
    ('// 第6讲：for 循环遍历数组', COLORS['yellow']),
    ('for (i = 0; i < 5; i++) {', COLORS['primary']),
    ('    printf("%.2f\\n", balances[i]);', COLORS['green']),
    ('}', COLORS['primary']),
    ('', COLORS['text']),
    ('// 模式完全一样！i 从0到4', COLORS['secondary']),
]
add_code_block(slide, right_x, Inches(2.0), Inches(6.5), Inches(3.8), "for_loop_array.c", code_lines)

# 底部对比
compare = add_rounded_rect(slide, Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.8),
                           COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.35),
         "💡 for 循环的三件套 i=0（初始化）、i<5（条件）、i++（更新）",
         font_size=13, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.0), Inches(6.6), Inches(11.3), Inches(0.35),
         "天然匹配数组的 0~N-1 索引范围——这就是'天作之合'",
         font_size=13, color=COLORS['dark'], align=PP_ALIGN.CENTER)

# ============================================================
# 第6页：字符数组与字符串
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔤 字符数组与字符串", "C语言没有 string 类型，字符串 = 字符数组 + '\\0'")

# 上半部分 - 字符串的内存布局
add_text(slide, Inches(0.8), Inches(1.8), Inches(5), Inches(0.4),
         "char name[] = \"张三\"; 的内存布局：", font_size=14, color=COLORS['text'], bold=True)

# 画字符格子
str_cells = ["'张'", "'三'", "'\\0'", "?", "?"]
str_colors = [COLORS['green'], COLORS['green'], COLORS['accent'], COLORS['text_light'], COLORS['text_light']]
for i, (val, color) in enumerate(zip(str_cells, str_colors)):
    x = Inches(0.8 + i * 1.2)
    y = Inches(2.4)
    cell = add_rounded_rect(slide, x, y, Inches(1.1), Inches(0.9), COLORS['white'], color, 0.1)
    add_text(slide, x, y + Inches(0.05), Inches(1.1), Inches(0.4),
             val, font_size=16, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(0.5), Inches(1.1), Inches(0.3),
             f"[{i}]", font_size=10, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 箭头指向 '\0'
arrow = add_shape(slide, MSO_SHAPE.DOWN_ARROW, Inches(3.0), Inches(3.4), Inches(0.4), Inches(0.3), fill_color=COLORS['accent'])
add_text(slide, Inches(2.2), Inches(3.8), Inches(2.5), Inches(0.3),
         "↑ 字符串结束标志", font_size=12, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# 右侧 - 对比有无 '\0'
right_x = Inches(6.5)
compare_card = add_rounded_rect(slide, right_x, Inches(2.0), Inches(6.2), Inches(2.5),
                                COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(2.0), Inches(6.2), Inches(0.45), COLORS['secondary'])
add_text(slide, right_x, Inches(2.05), Inches(6.2), Inches(0.35),
         "📝 有无 '\\0' 的区别", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

lines = [
    ("char a[] = \"Wang\";   ✅ 自动加 '\\0'", COLORS['green']),
    ("char b[4] = {'W','a','n','g'};  ❌ 没有 '\\0'", COLORS['accent']),
    ("char c[5] = {'W','a','n','g','\\0'};  ✅ 手动加", COLORS['green']),
    ("", COLORS['text']),
    ("printf(\"%s\", b);  → 输出 Wang 后继续读...", COLORS['accent']),
    ("                      可能输出乱码！", COLORS['accent']),
]
for i, (code, color) in enumerate(lines):
    add_text(slide, right_x + Inches(0.3), Inches(2.6 + i * 0.3), Inches(5.7), Inches(0.28),
             code, font_size=11, color=color, font_name='Consolas')

# 下半部分 - ATM 中的字符数组
atm_card = add_rounded_rect(slide, Inches(0.8), Inches(4.8), Inches(11.7), Inches(1.8),
                             COLORS['white'], COLORS['purple'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.8), Inches(11.7), Inches(0.45), COLORS['purple'])
add_text(slide, Inches(0.8), Inches(4.85), Inches(11.7), Inches(0.35),
         "🏦 ATM 中的二维字符数组（字符串数组）", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

code_lines2 = [
    ('char account_names[5][20] = {"张三", "李四", "王五", "赵六", "钱七"};', COLORS['purple']),
    ('// 5个账户名，每个最多20字符（含\\0），本质是"数组的数组"', COLORS['text_light']),
    ('printf("%s", account_names[2]);  // 输出：王五', COLORS['green']),
]
for i, (code, color) in enumerate(code_lines2):
    add_text(slide, Inches(1.1), Inches(5.4 + i * 0.35), Inches(11), Inches(0.3),
             code, font_size=12, color=color, font_name='Consolas')

# ============================================================
# 第7页：数组作为函数参数（退化为指针）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📥 数组作为函数参数", "数组传参时退化为指针——只传地址，不复制数据")

# 上方 - 三种等价写法
equiv_card = add_rounded_rect(slide, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.8),
                              COLORS['white'], COLORS['blue'], 0.08)
add_text(slide, Inches(1.0), Inches(1.9), Inches(11), Inches(0.4),
         "以下三种写法完全等价——编译器眼里都是 int 指针", font_size=16, color=COLORS['dark'], bold=True)

variants = [
    ("void func(int arr[10], int n)", COLORS['green'], "看着像传数组"),
    ("void func(int arr[], int n)", COLORS['yellow'], "省略大小"),
    ("void func(int *arr, int n)", COLORS['primary'], "实际就是指针"),
]
for i, (code, color, desc) in enumerate(variants):
    x = Inches(1.0 + i * 3.9)
    y = Inches(2.4)
    box = add_rounded_rect(slide, x, y, Inches(3.6), Inches(0.9), color, color, 0.15)
    add_text(slide, x + Inches(0.1), y + Inches(0.05), Inches(3.4), Inches(0.4),
             code, font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.1), y + Inches(0.5), Inches(3.4), Inches(0.3),
             desc, font_size=11, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 中间 - 为什么退化
left_x = Inches(0.8)
mid_y = Inches(4.0)

why_card = add_rounded_rect(slide, left_x, mid_y, Inches(5.5), Inches(2.6),
                            COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, mid_y, Inches(5.5), Inches(0.5), COLORS['secondary'])
add_text(slide, left_x, mid_y + Inches(0.05), Inches(5.5), Inches(0.4),
         "🤔 为什么退化？", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

reasons = [
    "复制 1000 个元素的数组？太浪费内存和时间",
    "只传首地址（4或8字节），高效！",
    "代价：函数不知道数组有多长",
    "所以需要额外传一个长度参数 n",
]
for i, reason in enumerate(reasons):
    add_text(slide, left_x + Inches(0.3), mid_y + Inches(0.65 + i * 0.42), Inches(5.0), Inches(0.35),
             f"• {reason}", font_size=12, color=COLORS['text'])

# 右侧 - sizeof 陷阱
right_x = Inches(6.8)
trap_card = add_rounded_rect(slide, right_x, mid_y, Inches(5.7), Inches(2.6),
                             COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, mid_y, Inches(5.7), Inches(0.5), COLORS['accent'])
add_text(slide, right_x, mid_y + Inches(0.05), Inches(5.7), Inches(0.4),
         "⚠️ sizeof 的陷阱", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

trap_lines = [
    ('sizeof(arr)  → 40（外部）', COLORS['green']),
    ('sizeof(arr)  → 4 或 8（函数内）', COLORS['accent']),
    ('// 退化成指针后 sizeof 返回指针大小', COLORS['text_light']),
    ('// 千万别在函数里用 sizeof 算长度！', COLORS['accent']),
]
for i, (code, color) in enumerate(trap_lines):
    add_text(slide, right_x + Inches(0.3), mid_y + Inches(0.65 + i * 0.4), Inches(5.2), Inches(0.32),
             code, font_size=12, color=color, font_name='Consolas')

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.8), Inches(10.3), Inches(0.55),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.87), Inches(10.3), Inches(0.4),
         "💡 数组传参 = 传地址 + 传长度，缺一不可！",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第8页：数组与指针的关系
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔗 数组与指针的关系", "数组名 = 首元素地址，arr[i] 等价于 *(arr+i)")

# 上半部分 - 图解关系
diag_card = add_rounded_rect(slide, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.8),
                             COLORS['white'], COLORS['purple'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.5), COLORS['purple'])
add_text(slide, Inches(0.8), Inches(1.85), Inches(11.7), Inches(0.4),
         "🔍 arr[i] 就是 *(arr + i)，编译器内部就是这么实现的", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 画内存格子和指针
cell_vals = ["10", "20", "30", "40", "50"]
addrs = ["0x1000", "0x1004", "0x1008", "0x100C", "0x1010"]
draw_memory_cells(slide, Inches(1.5), Inches(2.6), Inches(1.8), Inches(0.7), 5, cell_vals, addrs)

# 指针标注
add_text(slide, Inches(1.5), Inches(3.8), Inches(2.5), Inches(0.35),
         "arr = &arr[0] → 0x1000", font_size=12, color=COLORS['primary'], bold=True)
add_text(slide, Inches(5.0), Inches(3.8), Inches(3), Inches(0.35),
         "arr+2 → 0x1008 → *(arr+2)=30", font_size=12, color=COLORS['green'], bold=True)
add_text(slide, Inches(9.0), Inches(3.8), Inches(3), Inches(0.35),
         "arr+4 → 0x1010 → *(arr+4)=50", font_size=12, color=COLORS['accent'], bold=True)

# 下半部分 - 两种区别
left_x = Inches(0.8)
diff_y = Inches(4.9)

# 区别表
diffs = [
    ("区别", "数组名", "指针变量", COLORS['dark']),
    ("本质", "地址常量", "地址变量", COLORS['primary']),
    ("sizeof", "整个数组大小", "指针大小(4/8)", COLORS['secondary']),
    ("++自增", "❌ 不行", "✅ 可以", COLORS['accent']),
    ("=赋值", "❌ 不行", "✅ 可以", COLORS['purple']),
]

for i, (item, arr_val, ptr_val, color) in enumerate(diffs):
    y = diff_y + Inches(i * 0.35)
    is_header = (i == 0)
    bg_color = COLORS['light'] if not is_header else color
    txt_color = COLORS['white'] if is_header else COLORS['text']

    # 项目名
    cell1 = add_rounded_rect(slide, Inches(1.0), y, Inches(2.5), Inches(0.32), bg_color, color, 0.1)
    add_text(slide, Inches(1.0), y + Inches(0.03), Inches(2.5), Inches(0.26),
             item, font_size=12, color=txt_color, bold=is_header, align=PP_ALIGN.CENTER)
    # 数组名
    cell2 = add_rounded_rect(slide, Inches(3.6), y, Inches(4.5), Inches(0.32), bg_color, color, 0.1)
    add_text(slide, Inches(3.6), y + Inches(0.03), Inches(4.5), Inches(0.26),
             arr_val, font_size=12, color=txt_color, bold=is_header, align=PP_ALIGN.CENTER)
    # 指针
    cell3 = add_rounded_rect(slide, Inches(8.2), y, Inches(4.5), Inches(0.32), bg_color, color, 0.1)
    add_text(slide, Inches(8.2), y + Inches(0.03), Inches(4.5), Inches(0.26),
             ptr_val, font_size=12, color=txt_color, bold=is_header, align=PP_ALIGN.CENTER)

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.8), Inches(10.3), Inches(0.55),
                        COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.87), Inches(10.3), Inches(0.4),
         "💡 数组名是'钉死的地址标签'，指针是'可以移动的地址标签'——访问元素时等价，身份不同",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第9页：二维数组
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📊 二维数组简介", "数组的数组——有行有列的表格")

# 左侧 - 表格比喻
left_x = Inches(0.6)

table_card = add_rounded_rect(slide, left_x, Inches(2.0), Inches(5.5), Inches(4.3),
                              COLORS['white'], COLORS['green'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(2.0), Inches(5.5), Inches(0.5), COLORS['green'])
add_text(slide, left_x, Inches(2.05), Inches(5.5), Inches(0.4),
         "📊 二维数组 = 表格", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 画 3x4 矩阵
matrix_vals = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]
for r in range(3):
    for c in range(4):
        x = left_x + Inches(0.5 + c * 1.1)
        y = Inches(2.8 + r * 0.85)
        color = COLORS['blue'] if r == 0 else (COLORS['secondary'] if r == 1 else COLORS['purple'])
        cell = add_rounded_rect(slide, x, y, Inches(1.0), Inches(0.75), COLORS['white'], color, 0.1)
        add_text(slide, x, y + Inches(0.1), Inches(1.0), Inches(0.55),
                 str(matrix_vals[r][c]), font_size=16, color=color, bold=True, align=PP_ALIGN.CENTER)

add_text(slide, left_x + Inches(0.3), Inches(5.4), Inches(5.0), Inches(0.35),
         "matrix[1][2] → 第1行第2列 = 7", font_size=13, color=COLORS['green'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, left_x + Inches(0.3), Inches(5.8), Inches(5.0), Inches(0.35),
         "行索引在前，列索引在后", font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - 代码
right_x = Inches(6.5)
code_lines = [
    ('// 定义 3行4列 二维数组', COLORS['text_light']),
    ('int matrix[3][4] = {', COLORS['blue']),
    ('    {1, 2, 3, 4},', COLORS['green']),
    ('    {5, 6, 7, 8},', COLORS['green']),
    ('    {9, 10, 11, 12}', COLORS['green']),
    ('};', COLORS['blue']),
    ('', COLORS['text']),
    ('// 二维字符数组 = 字符串数组', COLORS['text_light']),
    ('char names[5][20] = {', COLORS['purple']),
    ('    "张三", "李四", "王五",', COLORS['green']),
    ('    "赵六", "钱七"', COLORS['green']),
    ('};', COLORS['purple']),
]
add_code_block(slide, right_x, Inches(2.0), Inches(6.2), Inches(4.5), "2d_array.c", code_lines)

# 底部提示
tip = add_rounded_rect(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.55),
                        COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.5), Inches(6.77), Inches(10.3), Inches(0.4),
         "💡 二维数组在内存中仍是连续排列的（行优先存储）——本质还是一维的",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第10页：ATM 交易记录数组实战
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🏦 ATM 交易记录数组实战", "用数组管理多账户 + 记录最近10笔交易")

# 左侧 - ATM 图标 + 多账户
left_x = Inches(0.6)

atm_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(4.5), Inches(4.5),
                             COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(4.5), Inches(0.5), COLORS['secondary'])
add_text(slide, left_x, Inches(1.85), Inches(4.5), Inches(0.4),
         "🏧 多账户管理", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 5个账户的迷你储物柜
mini_colors = [COLORS['primary'], COLORS['secondary'], COLORS['yellow'], COLORS['purple'], COLORS['green']]
mini_names = ["张三", "李四", "王五", "赵六", "钱七"]
mini_bals = ["1000", "2000", "500", "3000", "1500"]

for i in range(5):
    y = Inches(2.5 + i * 0.65)
    color = mini_colors[i]
    # 账户行
    row = add_rounded_rect(slide, left_x + Inches(0.2), y, Inches(4.1), Inches(0.55), COLORS['white'], color, 0.15)
    # ID 圆
    add_circle(slide, left_x + Inches(0.3), y + Inches(0.08), Inches(0.35), color)
    add_text(slide, left_x + Inches(0.3), y + Inches(0.1), Inches(0.35), Inches(0.3),
             str(i), font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    # 名称和余额
    add_text(slide, left_x + Inches(0.8), y + Inches(0.05), Inches(1.5), Inches(0.45),
             mini_names[i], font_size=13, color=COLORS['dark'], bold=True)
    add_text(slide, left_x + Inches(2.3), y + Inches(0.05), Inches(1.8), Inches(0.45),
             f"余额: {mini_bals[i]}", font_size=12, color=color, bold=True, align=PP_ALIGN.RIGHT)

# 右侧 - 交易记录数组
right_x = Inches(5.5)
trans_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(7.2), Inches(4.5),
                               COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(7.2), Inches(0.5), COLORS['accent'])
add_text(slide, right_x, Inches(1.85), Inches(7.2), Inches(0.4),
         "📝 交易记录数组（循环缓冲区）", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 循环缓冲区图示
add_text(slide, right_x + Inches(0.2), Inches(2.5), Inches(6.8), Inches(0.35),
         "trans_amounts[10] —— 最近10笔交易：", font_size=13, color=COLORS['text'], bold=True)

# 10个格子
trans_vals = ["500", "200", "100", "?", "?", "?", "?", "?", "?", "?"]
for i in range(10):
    x = right_x + Inches(0.2 + i * 0.68)
    y = Inches(3.0)
    color = COLORS['green'] if i < 3 else COLORS['light']
    border = COLORS['accent'] if i < 3 else COLORS['text_light']
    cell = add_rounded_rect(slide, x, y, Inches(0.62), Inches(0.7), color, border, 0.1)
    add_text(slide, x, y + Inches(0.05), Inches(0.62), Inches(0.35),
             trans_vals[i], font_size=11, color=COLORS['dark'] if i < 3 else COLORS['text_light'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(0.45), Inches(0.62), Inches(0.2),
             f"[{i}]", font_size=8, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 循环说明
add_text(slide, right_x + Inches(0.2), Inches(4.0), Inches(6.8), Inches(0.35),
         "第11笔 → 覆盖 [0]（取模 %10 实现循环）", font_size=12, color=COLORS['accent'], bold=True)

# 代码片段
code_lines = [
    ('void add_transaction(double amt, int type) {', COLORS['accent']),
    ('    int slot = trans_count % 10;  // 循环', COLORS['green']),
    ('    trans_amounts[slot] = amt;', COLORS['blue']),
    ('    trans_types[slot] = type;', COLORS['blue']),
    ('    trans_count++;', COLORS['purple']),
    ('}', COLORS['accent']),
]
for i, (code, color) in enumerate(code_lines):
    add_text(slide, right_x + Inches(0.3), Inches(4.5 + i * 0.3), Inches(6.5), Inches(0.26),
             code, font_size=11, color=color, font_name='Consolas')

# 底部对比
gold = add_rounded_rect(slide, Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.6),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.45),
         "🏆 从'只能管1个账户+忘了交易'到'管理5个账户+记住10笔交易'——数组的威力！",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第11页：思考题
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🤔 思考题 · 往深了想", "没有标准答案，重要的是思考过程")

questions = [
    ("数组名 vs 指针", "它们大部分时候可以互换\n但有两个关键区别你知道吗？", COLORS['primary'], Inches(0.6), Inches(2.0), "🔍"),
    ("为什么不做\n越界检查", "arr[100]（只有5个元素）\n编译不报错，是bug还是特性？", COLORS['purple'], Inches(3.85), Inches(2.0), "⚠️"),
    ("为什么要加\n'\\0'", "字符数组末尾的'\\0'\n到底是什么？不加会怎样？", COLORS['secondary'], Inches(7.1), Inches(2.0), "🔤"),
    ("固定大小\n怎么解决", "数组大小定死了\n想动态扩容怎么办？", COLORS['accent'], Inches(10.35), Inches(2.0), "📏"),
]

for title, desc, color, x, y, icon in questions:
    card = add_rounded_rect(slide, x, y, Inches(2.8), Inches(3.8), COLORS['white'], color, 0.1)

    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.8), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    add_text(slide, x, y + Inches(0.25), Inches(2.8), Inches(1.0),
             icon, font_size=40, align=PP_ALIGN.CENTER)

    add_text(slide, x + Inches(0.15), y + Inches(1.4), Inches(2.5), Inches(0.8),
             title, font_size=15, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.8), y + Inches(2.2), Inches(1.2), Inches(0.04))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.15), y + Inches(2.4), Inches(2.5), Inches(1.1),
             desc, font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部鼓励
encourage = add_rounded_rect(slide, Inches(1.5), Inches(6.2), Inches(10.3), Inches(0.9),
                             COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.5), Inches(6.3), Inches(10.3), Inches(0.4),
         "🌟 数组是从'单变量'到'数据结构'的第一步。",
         font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.35),
         "带着这些问题学习下一讲——结构体和链表，你会理解得更深刻！",
         font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ============================================================
# 第12页：小结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📝 小结", "数组——批量数据的容器")

# 金句
gold_card = add_rounded_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.1),
                             COLORS['primary'], COLORS['primary'], 0.08)
add_text(slide, Inches(1.5), Inches(1.9), Inches(10.3), Inches(0.4),
         "🎯 一句话总结", font_size=15, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(2.25), Inches(10.3), Inches(0.6),
         "数组是用'一个名字 + 一个索引'管理一组同类型数据的容器——\n连续内存、随机访问、固定大小。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 5个知识点
points = [
    ("1️⃣", "一维数组", "同类型数据\n连续集合\n索引从0开始", COLORS['blue']),
    ("2️⃣", "数组遍历", "for循环+数组\n天作之合\ni从0到N-1", COLORS['green']),
    ("3️⃣", "字符数组", "没有string\n字符数组+'\\0'\n就是字符串", COLORS['purple']),
    ("4️⃣", "退化为指针", "传参只传地址\n丢失长度信息\n需要额外传n", COLORS['yellow']),
    ("5️⃣", "数组与指针", "数组名=首地址\narr[i]=*(arr+i)\n但身份不同", COLORS['accent']),
]

for i, (num, title, desc, color) in enumerate(points):
    x = Inches(0.5 + i * 2.55)
    y = Inches(3.4)

    card = add_rounded_rect(slide, x, y, Inches(2.35), Inches(2.5),
                            COLORS['white'], color, 0.12)

    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.35), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    add_text(slide, x, y + Inches(0.2), Inches(2.35), Inches(0.6),
             num, font_size=32, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(0.9), Inches(2.35), Inches(0.45),
             title, font_size=17, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.8), y + Inches(1.45), Inches(0.75), Inches(0.04))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.15), y + Inches(1.6), Inches(2.05), Inches(0.8),
             desc, font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部预告
next_card = add_rounded_rect(slide, Inches(1.5), Inches(6.2), Inches(10.3), Inches(0.85),
                             COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(1.5), Inches(6.3), Inches(10.3), Inches(0.4),
         "👉 下一讲：结构体 —— 把平行数组合并，数据打包到一起！",
         font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.35),
         "再下一讲：链表 —— 打破固定大小的局限，动态扩容！",
         font_size=13, color=COLORS['yellow'], align=PP_ALIGN.CENTER)

# 保存
output_path = r"e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\06_数组\docs\课件.pptx"
prs.save(output_path)
print(f"PPT生成完成：{output_path}")
print(f"共 {len(prs.slides)} 页")
