# -*- coding: utf-8 -*-
"""
第4讲：多文件编程 —— PPT生成脚本
风格：轻松愉快、卡通风、明亮配色、有设计感
每页都有卡通图形设计，用形状和图标增加视觉效果
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ============================================================
# 配色方案（轻松活泼风）
# ============================================================
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
    'code_bg': RGBColor(0x1E, 0x29, 0x3B),     # 代码背景色
    'code_header': RGBColor(0x34, 0x49, 0x5E), # 代码标题栏色
}

# 底部统一标注文字
FOOTER_TEXT = "第4讲 多文件编程"

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
    """创建圆角矩形"""
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
    """创建圆形"""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text(slide, left, top, width, height, text, font_size=24, color=COLORS['text'],
             bold=False, align=PP_ALIGN.LEFT, font_name='微软雅黑'):
    """添加文本框"""
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

def add_footer(slide):
    """底部统一标注"""
    add_text(slide, Inches(0.8), Inches(7.05), Inches(12), Inches(0.3),
             FOOTER_TEXT, font_size=11, color=COLORS['text_light'])

def add_title_bar(slide, title, subtitle=None):
    """添加标题栏（含装饰和底部标注）"""
    # 顶部色条
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLORS['primary']
    bar.line.fill.background()

    # 标题装饰圆
    add_circle(slide, Inches(0.3), Inches(0.5), Inches(0.35), COLORS['primary'])
    add_circle(slide, Inches(0.55), Inches(0.55), Inches(0.25), COLORS['secondary'])

    # 标题文字
    add_text(slide, Inches(1.0), Inches(0.4), Inches(11), Inches(0.7),
             title, font_size=32, color=COLORS['dark'], bold=True)

    if subtitle:
        add_text(slide, Inches(1.0), Inches(1.05), Inches(11), Inches(0.45),
                 subtitle, font_size=15, color=COLORS['text_light'])

    add_footer(slide)

def draw_file_icon(slide, left, top, size, color, label, ext=".c"):
    """画一个文件图标（带折角）"""
    # 文件主体（圆角矩形）
    body = add_rounded_rect(slide, left, top, size * 0.75, size, color, color, 0.08)
    # 折角
    fold = add_shape(slide, MSO_SHAPE.RIGHT_TRIANGLE, left + size * 0.55, top, size * 0.2, size * 0.2,
                     COLORS['white'], COLORS['white'])
    fold.rotation = 90
    # 文件名标签
    add_text(slide, left, top + size * 0.3, size * 0.75, size * 0.3,
             label, font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, left, top + size * 0.6, size * 0.75, size * 0.25,
             ext, font_size=12, color=COLORS['white'], align=PP_ALIGN.CENTER)
    return body

def draw_atm_machine(slide, left, top, size, color=COLORS['secondary']):
    """画一个ATM机图标"""
    # 机身
    body = add_rounded_rect(slide, left, top, size * 0.8, size, color, color, 0.08)
    # 屏幕
    screen = add_rounded_rect(slide, left + size * 0.1, top + size * 0.08, size * 0.6, size * 0.35,
                              COLORS['code_bg'], COLORS['code_bg'], 0.1)
    # 屏幕内容线
    for i in range(3):
        line = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.15, top + size * (0.13 + i * 0.08),
                         size * 0.4, size * 0.03, COLORS['green'], COLORS['green'])
    # 键盘区
    keypad_y = top + size * 0.5
    for row in range(3):
        for col in range(3):
            key = add_circle(slide, left + size * (0.12 + col * 0.2),
                            keypad_y + row * size * 0.12, size * 0.12, COLORS['white'])
    # 出卡口
    slot = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.2, top + size * 0.88,
                     size * 0.4, size * 0.05, COLORS['dark'], COLORS['dark'])
    return body

def draw_folder_icon(slide, left, top, width, height, color, label):
    """画一个文件夹图标"""
    # 文件夹标签
    tab = add_shape(slide, MSO_SHAPE.RECTANGLE, left, top, width * 0.4, height * 0.25, color, color)
    # 文件夹主体
    body = add_rounded_rect(slide, left, top + height * 0.15, width, height * 0.85, color, color, 0.08)
    # 文字
    add_text(slide, left, top + height * 0.25, width, height * 0.5,
             label, font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
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

# 主卡片
card = add_rounded_rect(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5),
                        COLORS['white'], COLORS['white'], 0.05)

# 左侧 - 多文件图标（三个文件堆叠）
file_colors = [COLORS['secondary'], COLORS['primary'], COLORS['accent']]
file_labels = ["menu", "account", "utils"]
for i, (fc, fl) in enumerate(zip(file_colors, file_labels)):
    offset_x = i * Inches(0.4)
    offset_y = i * Inches(0.3)
    draw_file_icon(slide, Inches(2.2) + offset_x, Inches(2.5) + offset_y, Inches(1.5), fc, fl)

# 右侧文字
add_text(slide, Inches(5.2), Inches(2.3), Inches(6), Inches(1),
         "第4讲：多文件编程", font_size=52, color=COLORS['dark'], bold=True)
add_text(slide, Inches(5.2), Inches(3.3), Inches(6), Inches(0.6),
         "给代码分个家——从单文件到多模块", font_size=26, color=COLORS['primary'], bold=True)

# 分隔线
divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.2), Inches(4.1), Inches(1.5), Inches(0.06))
divider.fill.solid()
divider.fill.fore_color.rgb = COLORS['secondary']
divider.line.fill.background()

add_text(slide, Inches(5.2), Inches(4.3), Inches(6), Inches(0.5),
         "《从程序员到架构师》· C语言插件框架演进之旅", font_size=16, color=COLORS['text_light'])
add_text(slide, Inches(5.2), Inches(4.8), Inches(6), Inches(0.5),
         "头文件 · 源文件 · static · 接口与实现分离", font_size=18, color=COLORS['accent'], bold=True)

add_text(slide, Inches(5.5), Inches(5.4), Inches(2.3), Inches(0.5),
         "04 / 14", font_size=22, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

add_footer(slide)

# ============================================================
# 第2页：知识图谱
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🗺️ 知识图谱 · 第4讲", "本讲在整个知识体系中的位置")

# 中心节点
center_x = Inches(5.8)
center_y = Inches(3.7)

# 中心节点背景光晕
add_circle(slide, center_x - Inches(1.5), center_y - Inches(1), Inches(3), COLORS['secondary'])
add_circle(slide, center_x - Inches(1.1), center_y - Inches(0.6), Inches(2.2), COLORS['white'])

center_card = add_rounded_rect(slide, center_x - Inches(1.3), center_y - Inches(0.55), Inches(2.6), Inches(1.1),
                               COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, center_x - Inches(1.3), center_y - Inches(0.45), Inches(2.6), Inches(0.45),
         "📂 多文件编程", font_size=24, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, center_x - Inches(1.3), center_y + Inches(0.1), Inches(2.6), Inches(0.35),
         "（第4讲 核心）", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 周围节点
nodes = [
    ("函数封装", COLORS['purple'], Inches(1.8), Inches(1.3), "第3讲 · 前置", "🔧", "📌"),
    ("全局变量问题", COLORS['accent'], Inches(0.5), Inches(3.8), "第3讲痛点", "⚠️", ""),
    ("指针", COLORS['blue'], Inches(9.8), Inches(1.3), "→ 第5讲", "👆", ""),
    ("结构体", COLORS['green'], Inches(9.8), Inches(3.8), "→ 第7讲", "📦", ""),
    ("静态库/动态库", COLORS['yellow'], Inches(5.3), Inches(6.0), "→ 第9-10讲", "📚", ""),
]

for name, color, x, y, desc, icon, badge in nodes:
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
         "💡 多文件编程是模块化架构的第一步——从函数封装到模块封装",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第3页：单文件痛点
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🤔 第3讲的痛点", "函数封装很好，但单文件不够用了")

# 四个问题卡片
problems = [
    ("📏", "文件太长", "250+行代码全在一个文件\n函数越来越多\n文件越来越长", COLORS['accent']),
    ("🔓", "全局变量危险", "g_balance 谁都能改\n改乱了找不到凶手\n公共牧场悲剧", COLORS['yellow']),
    ("📦", "不好复用", "想拿走菜单模块？\n得从一大坨代码里抠\n复制粘贴容易错", COLORS['purple']),
    ("👥", "没法协作", "两人同时改一个文件\n合并代码是噩梦\n互相踩踏", COLORS['blue']),
]

for i, (icon, title, desc, color) in enumerate(problems):
    x = Inches(0.6 + i * 3.15)
    y = Inches(2.0)

    card = add_rounded_rect(slide, x, y, Inches(2.9), Inches(3.5),
                            COLORS['white'], color, 0.12)

    # 顶部色条
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.9), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    # 图标
    add_text(slide, x, y + Inches(0.3), Inches(2.9), Inches(1.0),
             icon, font_size=48, align=PP_ALIGN.CENTER)

    # 标题
    add_text(slide, x, y + Inches(1.4), Inches(2.9), Inches(0.5),
             title, font_size=18, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    # 描述
    add_text(slide, x + Inches(0.2), y + Inches(2.0), Inches(2.5), Inches(1.2),
             desc, font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部悬念
suspense = add_rounded_rect(slide, Inches(2), Inches(5.9), Inches(9.3), Inches(1.2),
                            COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(2), Inches(6.0), Inches(9.3), Inches(0.5),
         "💡 函数封装解决了代码重复，但单文件的问题怎么破？",
         font_size=20, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(2), Inches(6.5), Inches(9.3), Inches(0.5),
         "👉 按职责拆分到不同文件——给代码分个家！",
         font_size=16, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第4页：多文件思路
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📂 多文件思路", "按职责拆分——每个模块各管各的")

# 左侧：单文件（乱）
left_x = Inches(0.5)
# 大文件卡片
big_file = add_rounded_rect(slide, left_x, Inches(2.0), Inches(3.5), Inches(4.0),
                             COLORS['accent'], COLORS['accent'], 0.05)
add_text(slide, left_x, Inches(2.1), Inches(3.5), Inches(0.5),
         "📄 atm_func.c（250+行）", font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 混在一起的函数
func_names = ["show_welcome", "show_menu", "query_balance", "deposit", "withdraw", "transfer", "print_success", "print_error"]
for i, fn in enumerate(func_names):
    y = Inches(2.7 + i * 0.38)
    add_text(slide, left_x + Inches(0.3), y, Inches(3.0), Inches(0.3),
             "  " + fn + "()", font_size=11, color=COLORS['white'])

add_text(slide, left_x, Inches(5.8), Inches(3.5), Inches(0.3),
         "全部混在一起", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER, bold=True)

# 中间箭头
arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.2), Inches(3.8), Inches(1.0), Inches(0.6))
arrow.fill.solid()
arrow.fill.fore_color.rgb = COLORS['primary']
arrow.line.fill.background()
add_text(slide, Inches(4.2), Inches(4.5), Inches(1.0), Inches(0.4),
         "拆分", font_size=14, color=COLORS['primary'], bold=True, align=PP_ALIGN.CENTER)

# 右侧：多文件（整齐）
right_x = Inches(5.5)
modules = [
    ("main.c", COLORS['primary'], "程序入口\n调度各模块"),
    ("menu.c", COLORS['secondary'], "显示菜单\n读取选择"),
    ("account.c", COLORS['accent'], "余额管理\n存款取款转账"),
    ("utils.c", COLORS['purple'], "成功提示\n错误提示"),
]

for i, (name, color, desc) in enumerate(modules):
    y = Inches(2.0 + i * 1.15)
    # 文件卡片
    card = add_rounded_rect(slide, right_x, y, Inches(3.0), Inches(1.0),
                            COLORS['white'], color, 0.12)
    # 色条
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, y, Inches(0.08), Inches(1.0))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()
    # 文件名
    add_text(slide, right_x + Inches(0.2), y + Inches(0.1), Inches(1.5), Inches(0.4),
             name, font_size=16, color=COLORS['dark'], bold=True)
    # 描述
    add_text(slide, right_x + Inches(0.2), y + Inches(0.5), Inches(2.5), Inches(0.45),
             desc, font_size=11, color=COLORS['text_light'])

add_text(slide, right_x, Inches(6.3), Inches(3.0), Inches(0.3),
         "各管各的，互不干扰", font_size=13, color=COLORS['primary'], bold=True, align=PP_ALIGN.CENTER)

# 底部对比
compare_card = add_rounded_rect(slide, Inches(5.5), Inches(6.7), Inches(7.0), Inches(0.4),
                                  COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(5.5), Inches(6.72), Inches(7.0), Inches(0.35),
         "✅ 按职责拆分：改菜单只动 menu.c，改业务只动 account.c",
         font_size=12, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第5页：头文件原理
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📋 头文件原理", "头文件是菜单，源文件是厨房")

# 左侧：菜单比喻
left_x = Inches(0.6)

# 菜单卡片
menu_card = add_rounded_rect(slide, left_x, Inches(2.0), Inches(3.5), Inches(4.5),
                              COLORS['white'], COLORS['secondary'], 0.08)
# 标题栏
menu_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(2.0), Inches(3.5), Inches(0.6))
menu_top.fill.solid()
menu_top.fill.fore_color.rgb = COLORS['secondary']
menu_top.line.fill.background()

add_text(slide, left_x, Inches(2.08), Inches(3.5), Inches(0.45),
         "📋 menu.h（菜单）", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 菜单内容
menu_items = [
    "void show_welcome(void);",
    "void show_menu(void);",
    "int  read_choice(void);",
    "",
    "// 声明 = 告诉你有什么菜",
    "// 但不告诉你怎么做！",
]
for i, item in enumerate(menu_items):
    add_text(slide, left_x + Inches(0.3), Inches(2.8 + i * 0.35), Inches(3.0), Inches(0.3),
             item, font_size=12, color=COLORS['text'] if not item.startswith("//") else COLORS['text_light'])

# 箭头指向厨房
arrow_down = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, left_x + Inches(1.4), Inches(5.4), Inches(0.7), Inches(0.5))
arrow_down.fill.solid()
arrow_down.fill.fore_color.rgb = COLORS['secondary']
arrow_down.line.fill.background()

add_text(slide, left_x, Inches(5.9), Inches(3.5), Inches(0.4),
         "顾客看菜单点菜", font_size=13, color=COLORS['secondary'], bold=True, align=PP_ALIGN.CENTER)

# 右侧：厨房比喻
right_x = Inches(5.0)

# 厨房卡片
kitchen_card = add_rounded_rect(slide, right_x, Inches(2.0), Inches(7.3), Inches(4.5),
                                 COLORS['code_bg'], COLORS['code_bg'], 0.08)
# 标题栏
kit_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(2.0), Inches(7.3), Inches(0.55))
kit_top.fill.solid()
kit_top.fill.fore_color.rgb = COLORS['code_header']
kit_top.line.fill.background()

# 窗口按钮
for i, c in enumerate([COLORS['accent'], COLORS['yellow'], COLORS['green']]):
    add_circle(slide, right_x + Inches(0.2 + i * 0.35), Inches(2.08), Inches(0.2), c)

add_text(slide, right_x + Inches(3.0), Inches(2.03), Inches(2.0), Inches(0.35),
         "menu.c（厨房）", font_size=14, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 代码内容
code_lines = [
    ('#include "menu.h"', COLORS['text_light']),
    ('', COLORS['white']),
    ('void show_welcome(void) {', COLORS['blue']),
    ('    printf("欢迎使用ATM系统\\n");', COLORS['green']),
    ('}', COLORS['blue']),
    ('', COLORS['white']),
    ('void show_menu(void) {', COLORS['blue']),
    ('    printf("1.查询 2.存款...\\n");', COLORS['green']),
    ('}', COLORS['blue']),
    ('', COLORS['white']),
    ('// 定义 = 菜是怎么做的', COLORS['yellow']),
    ('// 外部不需要看到这些代码', COLORS['text_light']),
]

for i, (code, color) in enumerate(code_lines):
    add_text(slide, right_x + Inches(0.4), Inches(2.7 + i * 0.28), Inches(6.5), Inches(0.28),
             code, font_size=12, color=color)

# 底部金句
gold = add_rounded_rect(slide, Inches(0.6), Inches(6.7), Inches(12.1), Inches(0.4),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(0.6), Inches(6.72), Inches(12.1), Inches(0.35),
         "💡 头文件(.h) = 接口（声明），源文件(.c) = 实现（定义）——顾客看菜单，不用进厨房",
         font_size=13, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第6页：头文件保护
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🛡️ 头文件保护", "#ifndef / #define / #endif 三件套")

# 左侧：问题场景
left_x = Inches(0.6)

prob_card = add_rounded_rect(slide, left_x, Inches(2.0), Inches(5.2), Inches(4.0),
                              COLORS['white'], COLORS['accent'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(2.0), Inches(5.2), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['accent']
top_c.line.fill.background()
add_text(slide, left_x, Inches(2.08), Inches(5.2), Inches(0.4),
         "❌ 不加保护的后果", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 问题代码
prob_lines = [
    ("#include 的本质 = 复制粘贴", COLORS['accent']),
    ("", COLORS['text']),
    ("main.c 包含了 menu.h", COLORS['text']),
    ("menu.h 包含了 utils.h", COLORS['text']),
    ("→ utils.h 内容出现两遍！", COLORS['accent']),
    ("", COLORS['text']),
    ("函数声明重复 → 不报错（但浪费）", COLORS['yellow']),
    ("类型定义重复 → 编译错误！", COLORS['accent']),
]
for i, (code, color) in enumerate(prob_lines):
    add_text(slide, left_x + Inches(0.3), Inches(2.7 + i * 0.38), Inches(4.6), Inches(0.35),
             code, font_size=12, color=color)

# 右侧：解决方案
right_x = Inches(6.2)

sol_card = add_rounded_rect(slide, right_x, Inches(2.0), Inches(6.5), Inches(4.0),
                            COLORS['code_bg'], COLORS['code_bg'], 0.08)
sol_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(2.0), Inches(6.5), Inches(0.55))
sol_top.fill.solid()
sol_top.fill.fore_color.rgb = COLORS['green']
sol_top.line.fill.background()
add_text(slide, right_x, Inches(2.08), Inches(6.5), Inches(0.4),
         "✅ 加上保护三件套", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 保护代码
protect_lines = [
    ("/* menu.h */", COLORS['text_light']),
    ("#ifndef MENU_H       ← 如果没定义过", COLORS['green']),
    ("#define MENU_H       ← 就定义它", COLORS['green']),
    ("", COLORS['white']),
    ("void show_menu(void);", COLORS['yellow']),
    ("int  read_choice(void);", COLORS['yellow']),
    ("", COLORS['white']),
    ("#endif  /* MENU_H */  ← 保护结束", COLORS['green']),
    ("", COLORS['white']),
    ("// 第一次包含：处理内容 + 定义宏", COLORS['secondary']),
    ("// 后续包含：宏已定义 → 跳过！", COLORS['secondary']),
]
for i, (code, color) in enumerate(protect_lines):
    add_text(slide, right_x + Inches(0.4), Inches(2.7 + i * 0.32), Inches(5.8), Inches(0.3),
             code, font_size=12, color=color)

# 底部比喻
metaphor = add_rounded_rect(slide, Inches(0.6), Inches(6.3), Inches(12.1), Inches(0.6),
                             COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, Inches(0.6), Inches(6.35), Inches(12.1), Inches(0.5),
         "🔒 头文件保护 = 一次性门：第一次打开后自动锁上，后面再推就推不动了",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第7页：static 两种用法
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔑 static 的两种用法", "一个关键词，两种含义")

# 左侧：函数级 static
left_x = Inches(0.6)

# 卡片
func_card = add_rounded_rect(slide, left_x, Inches(2.0), Inches(5.8), Inches(4.5),
                              COLORS['white'], COLORS['purple'], 0.08)
func_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(2.0), Inches(5.8), Inches(0.65))
func_top.fill.solid()
func_top.fill.fore_color.rgb = COLORS['purple']
func_top.line.fill.background()

add_text(slide, left_x + Inches(0.2), Inches(2.08), Inches(0.6), Inches(0.5),
         "1️⃣", font_size=24, align=PP_ALIGN.CENTER)
add_text(slide, left_x + Inches(0.8), Inches(2.1), Inches(4.5), Inches(0.45),
         "函数级 static（函数内部）", font_size=17, color=COLORS['white'], bold=True)

# 代码
func_code = [
    ("void counter() {", COLORS['purple']),
    ("  static int count = 0;", COLORS['yellow']),
    ("  count++;", COLORS['green']),
    ("  printf(\"%d\\n\", count);", COLORS['green']),
    ("}", COLORS['purple']),
    ("", COLORS['text']),
    ("counter();  → 1", COLORS['secondary']),
    ("counter();  → 2", COLORS['secondary']),
    ("counter();  → 3", COLORS['secondary']),
]
for i, (code, color) in enumerate(func_code):
    add_text(slide, left_x + Inches(0.3), Inches(2.9 + i * 0.3), Inches(5.2), Inches(0.3),
             code, font_size=12, color=color)

# 特点
func_features = add_rounded_rect(slide, left_x + Inches(0.3), Inches(5.7), Inches(5.2), Inches(0.65),
                                  COLORS['light'], COLORS['purple'], 0.2)
add_text(slide, left_x + Inches(0.3), Inches(5.73), Inches(5.2), Inches(0.55),
         "💡 生命周期=程序结束 | 作用域=仅本函数 | 价值=保持状态",
         font_size=11, color=COLORS['purple'], bold=True, align=PP_ALIGN.CENTER)

# 右侧：文件级 static
right_x = Inches(6.8)

file_card = add_rounded_rect(slide, right_x, Inches(2.0), Inches(5.9), Inches(4.5),
                              COLORS['white'], COLORS['accent'], 0.08)
file_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(2.0), Inches(5.9), Inches(0.65))
file_top.fill.solid()
file_top.fill.fore_color.rgb = COLORS['accent']
file_top.line.fill.background()

add_text(slide, right_x + Inches(0.2), Inches(2.08), Inches(0.6), Inches(0.5),
         "2️⃣", font_size=24, align=PP_ALIGN.CENTER)
add_text(slide, right_x + Inches(0.8), Inches(2.1), Inches(4.5), Inches(0.45),
         "文件级 static（函数外部）", font_size=17, color=COLORS['white'], bold=True)

# 代码
file_code = [
    ("/* account.c */", COLORS['text_light']),
    ("static double s_balance = 1000.0;", COLORS['yellow']),
    ("static int validate_amount(double amt);", COLORS['yellow']),
    ("", COLORS['text']),
    ("// s_balance 仅 account.c 可见", COLORS['accent']),
    ("// main.c / menu.c 看不到它！", COLORS['accent']),
    ("// 想查余额？→ account_get_balance()", COLORS['green']),
    ("// 想改余额？→ account_deposit()", COLORS['green']),
]
for i, (code, color) in enumerate(file_code):
    add_text(slide, right_x + Inches(0.3), Inches(2.9 + i * 0.3), Inches(5.3), Inches(0.3),
             code, font_size=12, color=color)

# 特点
file_features = add_rounded_rect(slide, right_x + Inches(0.3), Inches(5.7), Inches(5.3), Inches(0.65),
                                   COLORS['light'], COLORS['accent'], 0.2)
add_text(slide, right_x + Inches(0.3), Inches(5.73), Inches(5.3), Inches(0.55),
         "💡 生命周期=程序结束 | 作用域=仅本文件 | 价值=信息隐藏",
         font_size=11, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# 底部对比表
compare = add_rounded_rect(slide, Inches(0.6), Inches(6.5), Inches(12.1), Inches(0.5),
                            COLORS['dark'], COLORS['dark'], 0.3)
add_text(slide, Inches(0.6), Inches(6.52), Inches(12.1), Inches(0.45),
         "第3讲 g_balance（全局可见，谁都能改）  →  第4讲 s_balance（仅本文件可见，安全！）",
         font_size=13, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第8页：多文件编译过程
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "⚙️ 多文件编译过程", "编译器逐文件编译，链接器跨文件接线")

# 编译流程图
# 四个源文件
source_files = [
    ("main.c", COLORS['primary']),
    ("menu.c", COLORS['secondary']),
    ("account.c", COLORS['accent']),
    ("utils.c", COLORS['purple']),
]

# 目标文件
obj_files = [
    ("main.o", COLORS['primary']),
    ("menu.o", COLORS['secondary']),
    ("account.o", COLORS['accent']),
    ("utils.o", COLORS['purple']),
]

# 第一排：源文件
for i, (name, color) in enumerate(source_files):
    x = Inches(0.5 + i * 1.4)
    # 文件卡片
    card = add_rounded_rect(slide, x, Inches(2.0), Inches(1.2), Inches(0.7),
                            color, color, 0.15)
    add_text(slide, x, Inches(2.15), Inches(1.2), Inches(0.4),
             name, font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

    # 向下箭头
    arrow = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x + Inches(0.35), Inches(2.8), Inches(0.5), Inches(0.35))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()

# 第二排：编译器标签
compiler_card = add_rounded_rect(slide, Inches(0.5), Inches(3.25), Inches(11.3), Inches(0.5),
                                  COLORS['yellow'], COLORS['yellow'], 0.2)
add_text(slide, Inches(0.5), Inches(3.3), Inches(11.3), Inches(0.4),
         "🔧 编译器：逐文件编译（预处理→编译→汇编）",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# 第三排：目标文件
for i, (name, color) in enumerate(obj_files):
    x = Inches(0.5 + i * 1.4)
    card = add_rounded_rect(slide, x, Inches(3.9), Inches(1.2), Inches(0.7),
                            COLORS['white'], color, 0.15)
    add_text(slide, x, Inches(4.05), Inches(1.2), Inches(0.4),
             name, font_size=12, color=color, bold=True, align=PP_ALIGN.CENTER)

# 汇合箭头
for i in range(4):
    x = Inches(0.5 + i * 1.4 + 0.6)
    arrow = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x, Inches(4.7), Inches(0.35), Inches(0.3))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = COLORS['text_light']
    arrow.line.fill.background()

# 第四排：链接器
linker_card = add_rounded_rect(slide, Inches(2.5), Inches(5.1), Inches(7.3), Inches(0.55),
                                COLORS['secondary'], COLORS['secondary'], 0.2)
add_text(slide, Inches(2.5), Inches(5.15), Inches(7.3), Inches(0.45),
         "🔗 链接器：解决外部引用，把 .o 拼成 .exe",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 最终箭头
final_arrow = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(5.8), Inches(5.75), Inches(0.7), Inches(0.35))
final_arrow.fill.solid()
final_arrow.fill.fore_color.rgb = COLORS['primary']
final_arrow.line.fill.background()

# 第五排：可执行文件
exe_card = add_rounded_rect(slide, Inches(4.0), Inches(6.2), Inches(4.3), Inches(0.6),
                             COLORS['green'], COLORS['green'], 0.15)
add_text(slide, Inches(4.0), Inches(6.27), Inches(4.3), Inches(0.45),
         "✅ atm_multi.exe", font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 底部说明
add_text(slide, Inches(0.5), Inches(6.85), Inches(12.3), Inches(0.3),
         "gcc main.c menu.c account.c utils.c -o atm_multi.exe  ←  一行命令搞定四阶段",
         font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ============================================================
# 第9页：接口与实现分离
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔀 接口与实现分离", "对外只暴露'能做什么'，内部'怎么做'藏起来")

# 左侧：account.h（接口）
left_x = Inches(0.6)

iface_card = add_rounded_rect(slide, left_x, Inches(2.0), Inches(5.2), Inches(4.5),
                               COLORS['white'], COLORS['secondary'], 0.08)
iface_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(2.0), Inches(5.2), Inches(0.55))
iface_top.fill.solid()
iface_top.fill.fore_color.rgb = COLORS['secondary']
iface_top.line.fill.background()
add_text(slide, left_x, Inches(2.08), Inches(5.2), Inches(0.4),
         "📋 account.h（接口 = 菜单）", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

iface_lines = [
    ("#ifndef ACCOUNT_H", COLORS['green']),
    ("#define ACCOUNT_H", COLORS['green']),
    ("", COLORS['text']),
    ("void account_query(void);", COLORS['blue']),
    ("void account_deposit(void);", COLORS['blue']),
    ("void account_withdraw(void);", COLORS['blue']),
    ("void account_transfer(void);", COLORS['blue']),
    ("double account_get_balance(void);", COLORS['blue']),
    ("", COLORS['text']),
    ("// 只告诉你：能做什么", COLORS['text_light']),
    ("// 不告诉你：怎么做", COLORS['text_light']),
    ("#endif", COLORS['green']),
]
for i, (code, color) in enumerate(iface_lines):
    add_text(slide, left_x + Inches(0.3), Inches(2.7 + i * 0.3), Inches(4.6), Inches(0.3),
             code, font_size=12, color=color)

# 右侧：account.c（实现）
right_x = Inches(6.2)

impl_card = add_rounded_rect(slide, right_x, Inches(2.0), Inches(6.5), Inches(4.5),
                             COLORS['code_bg'], COLORS['code_bg'], 0.08)
impl_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(2.0), Inches(6.5), Inches(0.55))
impl_top.fill.solid()
impl_top.fill.fore_color.rgb = COLORS['code_header']
impl_top.line.fill.background()

for i, c in enumerate([COLORS['accent'], COLORS['yellow'], COLORS['green']]):
    add_circle(slide, right_x + Inches(0.2 + i * 0.35), Inches(2.08), Inches(0.2), c)
add_text(slide, right_x + Inches(2.5), Inches(2.03), Inches(2.5), Inches(0.35),
         "account.c（实现 = 厨房）", font_size=14, color=COLORS['white'], align=PP_ALIGN.CENTER)

impl_lines = [
    ("#include \"account.h\"", COLORS['text_light']),
    ("#include \"utils.h\"", COLORS['text_light']),
    ("", COLORS['white']),
    ("static double s_balance = 1000.0;", COLORS['yellow']),
    ("static int validate_amount(double amt)", COLORS['accent']),
    ("{ /* 内部验证逻辑... */ }", COLORS['text_light']),
    ("", COLORS['white']),
    ("void account_deposit(void) {", COLORS['blue']),
    ("  // 具体实现代码...", COLORS['text_light']),
    ("  s_balance += amount;", COLORS['green']),
    ("  print_success(\"存入\", amount, s_balance);", COLORS['green']),
    ("}", COLORS['blue']),
]
for i, (code, color) in enumerate(impl_lines):
    add_text(slide, right_x + Inches(0.4), Inches(2.7 + i * 0.3), Inches(5.8), Inches(0.3),
             code, font_size=12, color=color)

# 底部好处
benefits = add_rounded_rect(slide, Inches(0.6), Inches(6.4), Inches(12.1), Inches(0.6),
                             COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(0.6), Inches(6.45), Inches(12.1), Inches(0.5),
         "💡 好处：实现可替换 | 降低耦合 | 团队协作 | 信息隐藏 | 编译隔离",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第10页：ATM 多文件结构
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🏗️ ATM 多文件结构", "第3讲单文件 → 第4讲多文件")

# 左侧：项目结构树
left_x = Inches(0.6)

tree_card = add_rounded_rect(slide, left_x, Inches(2.0), Inches(5.2), Inches(4.5),
                              COLORS['code_bg'], COLORS['code_bg'], 0.08)
tree_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(2.0), Inches(5.2), Inches(0.5))
tree_top.fill.solid()
tree_top.fill.fore_color.rgb = COLORS['code_header']
tree_top.line.fill.background()
add_text(slide, left_x + Inches(0.3), Inches(2.05), Inches(4.5), Inches(0.35),
         "📁 src/ 项目结构", font_size=14, color=COLORS['white'], bold=True)

tree_lines = [
    ("src/", COLORS['yellow']),
    ("├── main.c        ← 主程序", COLORS['green']),
    ("├── menu.h        ← 菜单接口", COLORS['secondary']),
    ("├── menu.c        ← 菜单实现", COLORS['secondary']),
    ("├── account.h     ← 账户接口", COLORS['accent']),
    ("├── account.c     ← 账户实现", COLORS['accent']),
    ("├── utils.h       ← 工具接口", COLORS['purple']),
    ("├── utils.c       ← 工具实现", COLORS['purple']),
    ("└── build.bat     ← 编译脚本", COLORS['primary']),
    ("", COLORS['white']),
    ("3个模块 × (.h + .c) + main = 8个文件", COLORS['yellow']),
]
for i, (code, color) in enumerate(tree_lines):
    add_text(slide, left_x + Inches(0.3), Inches(2.65 + i * 0.33), Inches(4.6), Inches(0.3),
             code, font_size=12, color=color)

# 右侧：模块依赖关系图
right_x = Inches(6.3)

dep_card = add_rounded_rect(slide, right_x, Inches(2.0), Inches(6.4), Inches(4.5),
                             COLORS['white'], COLORS['secondary'], 0.08)
dep_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(2.0), Inches(6.4), Inches(0.5))
dep_top.fill.solid()
dep_top.fill.fore_color.rgb = COLORS['secondary']
dep_top.line.fill.background()
add_text(slide, right_x + Inches(0.3), Inches(2.05), Inches(5.5), Inches(0.35),
         "🔗 模块依赖关系", font_size=14, color=COLORS['white'], bold=True)

# main.c 在顶部
main_box = add_rounded_rect(slide, right_x + Inches(2.2), Inches(2.7), Inches(2.0), Inches(0.55),
                             COLORS['primary'], COLORS['primary'], 0.2)
add_text(slide, right_x + Inches(2.2), Inches(2.78), Inches(2.0), Inches(0.4),
         "main.c", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 三个模块
mod_data = [
    ("menu", COLORS['secondary'], right_x + Inches(0.3), Inches(3.8), "show_menu\nread_choice"),
    ("account", COLORS['accent'], right_x + Inches(2.2), Inches(3.8), "deposit\nwithdraw\ntransfer"),
    ("utils", COLORS['purple'], right_x + Inches(4.1), Inches(3.8), "print_success\nprint_error"),
]
for name, color, mx, my, funcs in mod_data:
    box = add_rounded_rect(slide, mx, my, Inches(2.0), Inches(1.3),
                           COLORS['white'], color, 0.15)
    # 色条
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, mx, my, Inches(2.0), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    add_text(slide, mx, my + Inches(0.15), Inches(2.0), Inches(0.35),
             name, font_size=14, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, mx, my + Inches(0.55), Inches(2.0), Inches(0.7),
             funcs, font_size=10, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 连接线 main → 三个模块
for _, _, mx, my, _ in mod_data:
    line = slide.shapes.add_connector(1, right_x + Inches(3.2), Inches(3.25),
                                       mx + Inches(1.0), my)
    line.line.color.rgb = COLORS['text_light']
    line.line.width = Pt(1.5)
    line.line.dash_style = 1

# account → utils 的依赖
line_au = slide.shapes.add_connector(1, right_x + Inches(4.2), Inches(4.45),
                                      right_x + Inches(4.1), Inches(4.45))
line_au.line.color.rgb = COLORS['accent']
line_au.line.width = Pt(2)
# 用文字标注
add_text(slide, right_x + Inches(3.5), Inches(4.5), Inches(0.8), Inches(0.3),
         "依赖", font_size=9, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# 底部关键变化
change_card = add_rounded_rect(slide, right_x + Inches(0.3), Inches(5.4), Inches(5.8), Inches(0.95),
                                COLORS['light'], COLORS['secondary'], 0.15)
add_text(slide, right_x + Inches(0.4), Inches(5.48), Inches(5.6), Inches(0.35),
         "🔑 关键变化：", font_size=13, color=COLORS['secondary'], bold=True)
add_text(slide, right_x + Inches(0.4), Inches(5.8), Inches(5.6), Inches(0.5),
         "g_balance(全局) → s_balance(文件级static)\n外部只能通过接口函数操作余额",
         font_size=11, color=COLORS['text'])

# ============================================================
# 第11页：思考题
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🤔 思考题 · 往深了想", "没有标准答案，重要的是思考过程")

questions = [
    ("头文件保护", "为什么需要 #ifndef 三件套？\n不加会怎样？", COLORS['primary'], "🛡️"),
    ("static两种用法", "函数内 static 和文件级 static\n有什么区别？", COLORS['purple'], "🔑"),
    ("编译 vs 链接", "编译器和链接器各做了什么？\nundefined reference 是什么错？", COLORS['secondary'], "⚙️"),
    ("接口与实现分离", "为什么要分离？\n好处是什么？", COLORS['accent'], "🔀"),
]

positions = [
    (Inches(0.8), Inches(2.0)),
    (Inches(4.6), Inches(2.0)),
    (Inches(0.8), Inches(4.3)),
    (Inches(4.6), Inches(4.3)),
]

for (title, desc, color, icon), (x, y) in zip(questions, positions):
    card = add_rounded_rect(slide, x, y, Inches(3.7), Inches(2.2),
                            COLORS['white'], color, 0.1)

    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(3.7), Inches(0.65))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    add_text(slide, x + Inches(0.15), y + Inches(0.1), Inches(0.6), Inches(0.5),
             icon, font_size=24, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.8), y + Inches(0.15), Inches(2.7), Inches(0.45),
             title, font_size=16, color=COLORS['white'], bold=True)

    add_text(slide, x + Inches(0.3), y + Inches(0.85), Inches(3.1), Inches(1.0),
             desc, font_size=12, color=COLORS['text'], align=PP_ALIGN.CENTER)

# 右侧大问号
qmark_card = add_rounded_rect(slide, Inches(8.4), Inches(2.0), Inches(4.0), Inches(4.5),
                               COLORS['yellow'], COLORS['yellow'], 0.1)
add_text(slide, Inches(8.4), Inches(2.5), Inches(4.0), Inches(2),
         "❓", font_size=80, align=PP_ALIGN.CENTER)
add_text(slide, Inches(8.4), Inches(4.5), Inches(4.0), Inches(0.5),
         "带着问题学习", font_size=20, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(8.4), Inches(5.1), Inches(4.0), Inches(1.0),
         "答案见课件文档和思考题.md\n思考过程比答案更重要",
         font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部鼓励
encourage = add_rounded_rect(slide, Inches(1.5), Inches(6.8), Inches(10.3), Inches(0.4),
                             COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.82), Inches(10.3), Inches(0.35),
         "🌟 从函数封装到模块封装——每一步演进都让代码更好一点",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第12页：小结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📝 小结", "多文件编程——从单文件到多模块")

# 金句
gold_card = add_rounded_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.1),
                             COLORS['primary'], COLORS['primary'], 0.08)
add_text(slide, Inches(1.5), Inches(1.9), Inches(10.3), Inches(0.4),
         "🎯 一句话总结", font_size=15, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(2.25), Inches(10.3), Inches(0.6),
         "多文件编程 = 按职责拆分 + 头文件做接口 + static 做信息隐藏\n让代码更安全、更好维护、更容易复用。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 6个知识点
points = [
    ("1️⃣", "多文件动机", "文件太长\n全局变量危险\n不好复用", COLORS['accent']),
    ("2️⃣", ".h 与 .c", "头文件=菜单(声明)\n源文件=厨房(定义)", COLORS['secondary']),
    ("3️⃣", "头文件保护", "#ifndef\n#define\n#endif", COLORS['purple']),
    ("4️⃣", "static两种", "函数级=保持状态\n文件级=信息隐藏", COLORS['blue']),
    ("5️⃣", "编译过程", "编译器逐文件编译\n链接器跨文件接线", COLORS['yellow']),
    ("6️⃣", "接口与实现分离", "对外暴露接口\n内部藏实现", COLORS['green']),
]

for i, (num, title, desc, color) in enumerate(points):
    x = Inches(0.4 + i * 2.12)
    y = Inches(3.4)

    card = add_rounded_rect(slide, x, y, Inches(2.0), Inches(2.5),
                            COLORS['white'], color, 0.12)

    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.0), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    add_text(slide, x, y + Inches(0.2), Inches(2.0), Inches(0.6),
             num, font_size=30, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(0.9), Inches(2.0), Inches(0.45),
             title, font_size=15, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.6), y + Inches(1.4), Inches(0.8), Inches(0.04))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.1), y + Inches(1.55), Inches(1.8), Inches(0.8),
             desc, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部预告
next_card = add_rounded_rect(slide, Inches(2.5), Inches(6.2), Inches(8.3), Inches(0.8),
                             COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(2.5), Inches(6.3), Inches(8.3), Inches(0.6),
         "👉 下一讲：指针 —— 给函数一双能摸到原件的手！",
         font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 保存
# ============================================================
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "课件.pptx")
prs.save(output_path)
print(f"PPT生成完成：{output_path}")
print(f"共 {len(prs.slides)} 页")
