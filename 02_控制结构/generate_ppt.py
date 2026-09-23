# -*- coding: utf-8 -*-
"""
第2阶段：控制结构 —— PPT生成脚本
风格：轻松愉快、卡通风、明亮配色、有设计感
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import math

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

# ============================================================
# 工具函数
# ============================================================

def add_bg(slide, color=COLORS['light']):
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

def add_circle(slide, left, top, size, fill_color, transparency=0):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    if transparency > 0:
        shape.fill.transparency = transparency
    return shape

def add_text(slide, left, top, width, height, text, font_size=24, color=COLORS['text'],
             bold=False, align=PP_ALIGN.LEFT):
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
    run.font.name = '微软雅黑'
    return txBox

def add_title_bar(slide, title, subtitle=None):
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
    
    add_text(slide, Inches(0.8), Inches(7.05), Inches(12), Inches(0.3),
             "第2讲 控制结构", font_size=11, color=COLORS['text_light'])

def draw_signpost(slide, left, top, size, color=COLORS['blue']):
    """画一个路标（分支比喻）"""
    # 杆子
    pole = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + size * 0.42, top + size * 0.4, size * 0.16, size * 0.6)
    pole.fill.solid()
    pole.fill.fore_color.rgb = RGBColor(0x8B, 0x45, 0x13)
    pole.line.fill.background()
    # 左路牌
    sign_l = slide.shapes.add_shape(MSO_SHAPE.PENTAGON, left, top + size * 0.15, size * 0.5, size * 0.3)
    sign_l.fill.solid()
    sign_l.fill.fore_color.rgb = color
    sign_l.line.fill.background()
    # 右路牌
    sign_r = slide.shapes.add_shape(MSO_SHAPE.PENTAGON, left + size * 0.5, top, size * 0.5, size * 0.3)
    sign_r.fill.solid()
    sign_r.fill.fore_color.rgb = COLORS['yellow']
    sign_r.line.fill.background()
    # 底座
    base = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + size * 0.3, top + size * 0.95, size * 0.4, size * 0.08)
    base.fill.solid()
    base.fill.fore_color.rgb = RGBColor(0x65, 0x43, 0x21)
    base.line.fill.background()

def draw_loop(slide, left, top, size, color=COLORS['purple']):
    """画一个循环箭头"""
    # 大圆环（用两个半圆模拟）
    ring = slide.shapes.add_shape(MSO_SHAPE.DONUT, left, top, size, size)
    ring.fill.solid()
    ring.fill.fore_color.rgb = color
    ring.line.fill.background()
    # 内圆（镂空）
    inner = add_circle(slide, left + size * 0.2, top + size * 0.2, size * 0.6, COLORS['light'])
    # 中心文字
    add_text(slide, left, top + size * 0.3, size, size * 0.4,
             "🔄", font_size=36, align=PP_ALIGN.CENTER)
    # 箭头（右下）
    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left + size * 0.75, top + size * 0.65, size * 0.25, size * 0.2)
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    arrow.rotation = 135

def draw_road(slide, left, top, width, height, color=RGBColor(0x7F, 0x8C, 0x8D)):
    """画一条直路（顺序比喻）"""
    # 路面
    road = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    road.fill.solid()
    road.fill.fore_color.rgb = color
    road.line.fill.background()
    # 虚线
    for i in range(6):
        dash = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + width * (0.1 + i * 0.15), top + height * 0.45, width * 0.08, height * 0.1)
        dash.fill.solid()
        dash.fill.fore_color.rgb = COLORS['yellow']
        dash.line.fill.background()

def draw_atm(slide, left, top, size, color=COLORS['blue']):
    """画一个ATM机图标"""
    # 机身
    body = add_rounded_rect(slide, left, top, size * 0.8, size, color, color, 0.08)
    # 屏幕
    screen = add_rounded_rect(slide, left + size * 0.1, top + size * 0.08, size * 0.6, size * 0.35, RGBColor(0x1E, 0x29, 0x3B), RGBColor(0x1E, 0x29, 0x3B), 0.1)
    # 屏幕内容（几行文字）
    for i in range(3):
        line = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.15, top + size * (0.13 + i * 0.08), size * 0.4, size * 0.03, COLORS['green'], COLORS['green'])
    # 键盘区
    keypad_y = top + size * 0.5
    for row in range(3):
        for col in range(3):
            key = add_circle(slide, left + size * (0.12 + col * 0.2), keypad_y + row * size * 0.12, size * 0.12, COLORS['white'])
    # 出卡口
    slot = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.2, top + size * 0.88, size * 0.4, size * 0.05, RGBColor(0x2C, 0x3E, 0x50), RGBColor(0x2C, 0x3E, 0x50))
    return body

# ============================================================
# 第1页：封面
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, COLORS['light'])

# 背景装饰
add_circle(slide, Inches(9.5), Inches(-1.5), Inches(5), COLORS['secondary'], 0.15)
add_circle(slide, Inches(-2), Inches(4.5), Inches(4.5), COLORS['primary'], 0.12)
add_circle(slide, Inches(11), Inches(5), Inches(2.5), COLORS['yellow'], 0.2)

# 卡片
card = add_rounded_rect(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5),
                        COLORS['white'], COLORS['white'], 0.05)
shadow = add_rounded_rect(slide, Inches(1.6), Inches(1.6), Inches(10.3), Inches(4.5),
                          RGBColor(0x00, 0x00, 0x00), RGBColor(0x00, 0x00, 0x00), 0.05)
shadow.fill.transparency = 0.92
slide.shapes._spTree.remove(shadow._element)
slide.shapes._spTree.insert(2, shadow._element)

# 左侧 - ATM图标
draw_atm(slide, Inches(2.2), Inches(2.2), Inches(2.5), COLORS['secondary'])

# 右侧文字
add_text(slide, Inches(5.2), Inches(2.3), Inches(6), Inches(1),
         "第2讲：控制结构", font_size=52, color=COLORS['dark'], bold=True)
add_text(slide, Inches(5.2), Inches(3.3), Inches(6), Inches(0.6),
         "ATM菜单背后的秘密", font_size=26, color=COLORS['primary'], bold=True)

# 分隔线
divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.2), Inches(4.1), Inches(1.5), Inches(0.06))
divider.fill.solid()
divider.fill.fore_color.rgb = COLORS['secondary']
divider.line.fill.background()

add_text(slide, Inches(5.2), Inches(4.3), Inches(6), Inches(0.5),
         "《从程序员到架构师》· C语言插件框架演进之旅", font_size=16, color=COLORS['text_light'])
add_text(slide, Inches(5.2), Inches(4.8), Inches(6), Inches(0.5),
         "顺序 · 分支 · 循环 —— 三种结构构建交互程序", font_size=18, color=COLORS['accent'], bold=True)

add_text(slide, Inches(5.5), Inches(5.4), Inches(2.3), Inches(0.5),
         "02 / 12", font_size=22, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第2页：知识图谱
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🗺️ 知识图谱 · 第2讲", "本讲在整个知识体系中的位置")

# 中心节点
center_x = Inches(5.8)
center_y = Inches(3.7)

add_circle(slide, center_x - Inches(1.5), center_y - Inches(1), Inches(3), COLORS['secondary'], 0.15)
add_circle(slide, center_x - Inches(1.1), center_y - Inches(0.6), Inches(2.2), COLORS['secondary'], 0.25)

center_card = add_rounded_rect(slide, center_x - Inches(1.3), center_y - Inches(0.55), Inches(2.6), Inches(1.1),
                               COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, center_x - Inches(1.3), center_y - Inches(0.45), Inches(2.6), Inches(0.45),
         "🔀 控制结构", font_size=24, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, center_x - Inches(1.3), center_y + Inches(0.1), Inches(2.6), Inches(0.35),
         "（第2讲 核心）", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 周围节点
nodes = [
    ("表达式", COLORS['primary'], Inches(1.8), Inches(1.3), "第1讲 · 基础", "📌"),
    ("变量与数据", COLORS['yellow'], Inches(0.5), Inches(3.8), "数据的容器", "📦"),
    ("函数封装", COLORS['purple'], Inches(9.8), Inches(1.3), "→ 第3讲", "🔧"),
    ("多文件编程", COLORS['blue'], Inches(9.8), Inches(3.8), "→ 第4讲", "📂"),
    ("ATM菜单", COLORS['green'], Inches(5.3), Inches(6.0), "本讲实战案例", "🏧"),
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
         "💡 控制结构是程序的骨架——顺序、分支、循环，三种结构组合出所有复杂逻辑",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第3页：什么是控制结构？
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🚗 什么是控制结构？", "想象你在开车...")

# 三个卡通比喻并排
analogies = [
    ("直行", "顺序结构", "一直往前开\n代码从上到下一行一行执行", COLORS['blue'], "⬆️"),
    ("岔路口", "分支结构", "选左边还是右边\n根据条件走不同的代码路径", COLORS['yellow'], "🔀"),
    ("绕圈", "循环结构", "围着广场转三圈\n重复执行同一段代码", COLORS['purple'], "🔄"),
]

for i, (scene, name, desc, color, icon) in enumerate(analogies):
    x = Inches(0.6 + i * 4.2)
    y = Inches(2.0)
    
    # 卡片
    card = add_rounded_rect(slide, x, y, Inches(3.8), Inches(4.0),
                            COLORS['white'], color, 0.12)
    
    # 顶部色条
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(3.8), Inches(0.7))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()
    
    # 场景名称
    add_text(slide, x, y + Inches(0.1), Inches(3.8), Inches(0.5),
             scene, font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    
    # 大图标
    add_text(slide, x, y + Inches(1.0), Inches(3.8), Inches(1.2),
             icon, font_size=56, align=PP_ALIGN.CENTER)
    
    # 结构名称
    add_text(slide, x, y + Inches(2.3), Inches(3.8), Inches(0.5),
             name, font_size=20, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    
    # 描述
    add_text(slide, x + Inches(0.3), y + Inches(2.9), Inches(3.2), Inches(0.9),
             desc, font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.4), Inches(10.3), Inches(0.7),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.5),
         "🏆 金句：无论多么复杂的程序，拆到底都是这三种结构的组合！",
         font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第4页：顺序结构
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "⬆️ 顺序结构", "最简单也最基本——从上到下，一行一行走")

# 左侧 - 道路图示
left_x = Inches(0.8)
left_y = Inches(2.0)

# 道路
draw_road(slide, left_x, left_y + Inches(0.5), Inches(2.5), Inches(3.5))

# 三辆车表示执行顺序
car_icons = ["🚗", "🚙", "🚕"]
for i, car in enumerate(car_icons):
    add_text(slide, left_x + Inches(0.8), left_y + Inches(i * 1.1), Inches(1), Inches(0.8),
             car, font_size=36, align=PP_ALIGN.CENTER)

add_text(slide, left_x, left_y + Inches(4.2), Inches(2.5), Inches(0.5),
         "一步一步向前走", font_size=14, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - 代码示例
right_x = Inches(4.0)

code_card = add_rounded_rect(slide, right_x, left_y, Inches(8.5), Inches(4.2),
                              RGBColor(0x1E, 0x29, 0x3B), RGBColor(0x1E, 0x29, 0x3B), 0.08)
# 标题栏
code_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, left_y, Inches(8.5), Inches(0.4))
code_top.fill.solid()
code_top.fill.fore_color.rgb = RGBColor(0x34, 0x49, 0x5E)
code_top.line.fill.background()

# 按钮
for i, c in enumerate([COLORS['accent'], COLORS['yellow'], COLORS['green']]):
    add_circle(slide, right_x + Inches(0.2 + i * 0.35), left_y + Inches(0.08), Inches(0.2), c)

add_text(slide, right_x + Inches(3.5), left_y + Inches(0.03), Inches(1.5), Inches(0.35),
         "atm_menu.c", font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 代码内容（带行号和执行顺序标注）
code_lines = [
    ("①", 'printf("==== 欢迎使用 ATM ====\\n");', COLORS['green']),
    ("②", 'printf("  1. 查询余额\\n");', COLORS['green']),
    ("③", 'printf("  2. 存款\\n");', COLORS['green']),
    ("④", 'printf("  3. 取款\\n");', COLORS['green']),
    ("⑤", 'printf("  0. 退出\\n");', COLORS['green']),
    ("⑥", 'printf("======================\\n");', COLORS['green']),
]

for i, (num, code, color) in enumerate(code_lines):
    y = left_y + Inches(0.6 + i * 0.55)
    # 序号圆
    num_circle = add_circle(slide, right_x + Inches(0.3), y + Inches(0.05), Inches(0.35), COLORS['yellow'])
    add_text(slide, right_x + Inches(0.3), y + Inches(0.08), Inches(0.35), Inches(0.3),
             num, font_size=12, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    # 代码
    add_text(slide, right_x + Inches(0.9), y, Inches(7), Inches(0.45),
             code, font_size=14, color=color)

# 底部说明
add_text(slide, right_x, left_y + Inches(3.8), Inches(8.5), Inches(0.35),
         "⬆️  从上到下，依次执行，不会跳，不会回头",
         font_size=12, color=COLORS['secondary'], align=PP_ALIGN.CENTER)

# ============================================================
# 第5页：分支结构 - if-else
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔀 分支结构：if-else", "岔路口——往左走还是往右走？")

# 左侧 - 路标图示
draw_signpost(slide, Inches(1.0), Inches(2.2), Inches(2.5), COLORS['blue'])

add_text(slide, Inches(0.5), Inches(5.0), Inches(3.5), Inches(0.5),
         "条件判断 = 路牌指示", font_size=14, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - 代码+流程图
right_x = Inches(4.5)

# if-else 代码
code_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(8.2), Inches(4.8),
                              COLORS['white'], COLORS['accent'], 0.08)
# 顶部色条
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(8.2), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['accent']
top_c.line.fill.background()

add_text(slide, right_x, Inches(1.88), Inches(8.2), Inches(0.4),
         "📝 取款的 if-else 判断", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 代码
code_lines = [
    ('if (amount <= 0) {', COLORS['accent']),
    ('    printf("金额必须大于0！");', COLORS['text']),
    ('}', COLORS['accent']),
    ('else if (amount > balance) {', COLORS['primary']),
    ('    printf("余额不足！");', COLORS['text']),
    ('}', COLORS['primary']),
    ('else {', COLORS['green']),
    ('    balance = balance - amount;', COLORS['text']),
    ('    printf("取款成功！");', COLORS['green']),
    ('}', COLORS['green']),
]

for i, (code, color) in enumerate(code_lines):
    add_text(slide, right_x + Inches(0.5), Inches(2.5 + i * 0.38), Inches(7), Inches(0.35),
             code, font_size=13, color=color)

# 三个分支的标注
branches = [
    ("❌ 金额无效", COLORS['accent'], Inches(0.3)),
    ("❌ 余额不足", COLORS['primary'], Inches(2.0)),
    ("✅ 正常取款", COLORS['green'], Inches(3.8)),
]

for label, color, y_offset in branches:
    y = Inches(2.5) + y_offset
    dot = add_circle(slide, right_x + Inches(7.3), y + Inches(0.05), Inches(0.25), color)
    add_text(slide, right_x + Inches(7.6), y, Inches(1.5), Inches(0.35),
             label, font_size=11, color=color, bold=True)

# ============================================================
# 第6页：分支结构 - switch
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🎯 分支结构：switch", "多选一的场景，用 switch 更清晰")

# 左侧 - 自动售货机比喻（多选一）
vending_x = Inches(0.8)
vending_y = Inches(2.0)

# 售货机机身
machine = add_rounded_rect(slide, vending_x, vending_y, Inches(3.5), Inches(4.5),
                           COLORS['purple'], COLORS['purple'], 0.05)
# 展示窗
window = add_rounded_rect(slide, vending_x + Inches(0.3), vending_y + Inches(0.3), Inches(2.9), Inches(2.5),
                          RGBColor(0x1E, 0x29, 0x3B), RGBColor(0x1E, 0x29, 0x3B), 0.08)
# 商品格子
items = ["🍔", "🍟", "🥤", "🍕", "🍩", "🍪"]
for i, item in enumerate(items):
    col = i % 3
    row = i // 3
    item_box = add_rounded_rect(slide, vending_x + Inches(0.4 + col * 0.95), vending_y + Inches(0.4 + row * 1.1),
                                Inches(0.85), Inches(1.0),
                                COLORS['white'], COLORS['text_light'], 0.1)
    add_text(slide, vending_x + Inches(0.4 + col * 0.95), vending_y + Inches(0.55 + row * 1.1),
             Inches(0.85), Inches(0.7),
             item, font_size=24, align=PP_ALIGN.CENTER)

# 按键区
for i in range(6):
    btn = add_circle(slide, vending_x + Inches(0.4 + i * 0.5), vending_y + Inches(3.1), Inches(0.35), COLORS['yellow'])
    add_text(slide, vending_x + Inches(0.4 + i * 0.5), vending_y + Inches(3.15), Inches(0.35), Inches(0.3),
             str(i+1), font_size=12, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# 取货口
out_slot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, vending_x + Inches(0.8), vending_y + Inches(3.8), Inches(1.9), Inches(0.4))
out_slot.fill.solid()
out_slot.fill.fore_color.rgb = RGBColor(0x2C, 0x3E, 0x50)
out_slot.line.fill.background()

add_text(slide, vending_x, vending_y + Inches(4.4), Inches(3.5), Inches(0.4),
         "选几号，出几号货", font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - switch 代码
right_x = Inches(5.0)

code_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(7.7), Inches(4.8),
                              COLORS['white'], COLORS['purple'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(7.7), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['purple']
top_c.line.fill.background()

add_text(slide, right_x, Inches(1.88), Inches(7.7), Inches(0.4),
         "📝 ATM 菜单的 switch 结构", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 代码
code_lines = [
    ('switch (choice) {', COLORS['purple']),
    ('  case 1: 查询余额; break;', COLORS['blue']),
    ('  case 2: 存款; break;', COLORS['green']),
    ('  case 3: 取款; break;', COLORS['yellow']),
    ('  case 4: 转账; break;', COLORS['pink']),
    ('  case 0: 退出; break;', COLORS['accent']),
    ('  default: 输入错误;', COLORS['text_light']),
    ('}', COLORS['purple']),
]

for i, (code, color) in enumerate(code_lines):
    add_text(slide, right_x + Inches(0.5), Inches(2.55 + i * 0.48), Inches(6.7), Inches(0.4),
             code, font_size=14, color=color)

# ⚠️ break 提醒
warn_card = add_rounded_rect(slide, right_x + Inches(0.5), Inches(6.0), Inches(6.7), Inches(0.5),
                              COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, right_x + Inches(0.5), Inches(6.05), Inches(6.7), Inches(0.4),
         "⚠️ 每个 case 后面要加 break！否则会发生 case 穿透",
         font_size=12, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第7页：循环结构 - while
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔄 循环结构：while", "重复做同一件事——不知道做多少次的时候用它")

# 左侧 - 循环图示
draw_loop(slide, Inches(1.0), Inches(2.0), Inches(3), COLORS['purple'])

add_text(slide, Inches(0.5), Inches(5.2), Inches(4), Inches(0.5),
         "条件为真，就再来一圈", font_size=14, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - ATM主循环
right_x = Inches(5.0)

code_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(7.7), Inches(4.8),
                              COLORS['white'], COLORS['purple'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(7.7), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['purple']
top_c.line.fill.background()

add_text(slide, right_x, Inches(1.88), Inches(7.7), Inches(0.4),
         "📝 ATM 菜单的 while 主循环", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 代码
code_lines = [
    ('int running = 1;', COLORS['blue']),
    ('', COLORS['text']),
    ('while (running) {        // 只要为真，就一直循环', COLORS['purple']),
    ('', COLORS['text']),
    ('    显示菜单...', COLORS['text_light']),
    ('    读取用户输入...', COLORS['text_light']),
    ('    switch (choice) {', COLORS['secondary']),
    ('        ...', COLORS['text_light']),
    ('        case 0:', COLORS['accent']),
    ('            running = 0;  // 设为0，循环就结束了', COLORS['accent']),
    ('    }', COLORS['secondary']),
    ('}', COLORS['purple']),
]

for i, (code, color) in enumerate(code_lines):
    add_text(slide, right_x + Inches(0.5), Inches(2.5 + i * 0.35), Inches(6.7), Inches(0.32),
             code, font_size=12, color=color)

# 底部说明
tip = add_rounded_rect(slide, right_x + Inches(0.5), Inches(6.0), Inches(6.7), Inches(0.5),
                       COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, right_x + Inches(0.5), Inches(6.05), Inches(6.7), Inches(0.4),
         "💡 这是菜单程序的经典写法——用标志变量控制循环",
         font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第8页：循环结构 - for
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔢 循环结构：for", "知道循环多少次的时候用它——计数器驱动")

# 左侧 - 计数器图示
counter_x = Inches(1.0)
counter_y = Inches(2.2)

# 计数器框
counter_card = add_rounded_rect(slide, counter_x, counter_y, Inches(3.2), Inches(3.8),
                                 COLORS['white'], COLORS['yellow'], 0.1)
# 顶部色条
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, counter_x, counter_y, Inches(3.2), Inches(0.6))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['yellow']
top_c.line.fill.background()

add_text(slide, counter_x, counter_y + Inches(0.1), Inches(3.2), Inches(0.4),
         "计数器 i = 0, 1, 2...", font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# 数字阶梯
numbers = ["0", "1", "2", "3", "...", "N"]
for i, n in enumerate(numbers):
    step_x = counter_x + Inches(0.3 + i * 0.45)
    step_y = counter_y + Inches(3.0 - i * 0.35)
    step = add_rounded_rect(slide, step_x, step_y, Inches(0.4), Inches(0.4),
                            COLORS['primary'], COLORS['primary'], 0.3)
    add_text(slide, step_x, step_y + Inches(0.05), Inches(0.4), Inches(0.3),
             n, font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, counter_x, counter_y + Inches(3.3), Inches(3.2), Inches(0.4),
         "从0数到N，数完就结束", font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - for循环三段式
right_x = Inches(5.0)

# 三段式图示
parts_card = add_rounded_rect(slide, right_x, Inches(1.9), Inches(7.7), Inches(2.0),
                              COLORS['white'], COLORS['blue'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.9), Inches(7.7), Inches(0.5))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['blue']
top_c.line.fill.background()

add_text(slide, right_x, Inches(1.95), Inches(7.7), Inches(0.4),
         "🔧 for 循环 = 三件套", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

for_parts = [
    ("初始化", "int i = 0", "从哪开始", COLORS['green']),
    ("条件", "i < 10", "到哪结束", COLORS['yellow']),
    ("更新", "i++", "每次加多少", COLORS['accent']),
]

for i, (name, code, desc, color) in enumerate(for_parts):
    px = right_x + Inches(0.3 + i * 2.45)
    py = Inches(2.6)
    
    part_card = add_rounded_rect(slide, px, py, Inches(2.2), Inches(1.1),
                                  color, color, 0.2)
    add_text(slide, px, py + Inches(0.05), Inches(2.2), Inches(0.35),
             name, font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, px, py + Inches(0.4), Inches(2.2), Inches(0.35),
             code, font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)
    add_text(slide, px, py + Inches(0.75), Inches(2.2), Inches(0.3),
             desc, font_size=10, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 代码示例
code_card = add_rounded_rect(slide, right_x, Inches(4.2), Inches(7.7), Inches(2.4),
                              RGBColor(0x1E, 0x29, 0x3B), RGBColor(0x1E, 0x29, 0x3B), 0.08)

code_lines = [
    ('// 打印 5 次欢迎语', COLORS['text_light']),
    ('for (int i = 1; i <= 5; i++) {', COLORS['blue']),
    ('    printf("第 %d 次：欢迎光临！\\n", i);', COLORS['green']),
    ('}', COLORS['blue']),
    ('', COLORS['text']),
    ('// 输出：', COLORS['text_light']),
    ('// 第 1 次：欢迎光临！', COLORS['secondary']),
    ('// 第 2 次：欢迎光临！', COLORS['secondary']),
    ('// ...', COLORS['text_light']),
]

for i, (code, color) in enumerate(code_lines):
    add_text(slide, right_x + Inches(0.5), Inches(4.3 + i * 0.24), Inches(6.7), Inches(0.24),
             code, font_size=11, color=color)

# ============================================================
# 第9页：三种结构的嵌套组合
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🎁 组合的力量", "大结构套小结构，层层嵌套 = 复杂程序")

# 左侧 - 嵌套结构图（像俄罗斯套娃）
left_x = Inches(0.8)
left_y = Inches(2.0)

# 用不同大小的圆表示嵌套
layers = [
    ("while 循环", "最外层", COLORS['purple'], Inches(2.5), Inches(0.8)),
    ("switch 分支", "中间层", COLORS['yellow'], Inches(1.8), Inches(1.5)),
    ("if 判断", "内层", COLORS['accent'], Inches(1.1), Inches(2.2)),
    ("顺序执行", "最内层", COLORS['green'], Inches(0.5), Inches(2.8)),
]

for name, desc, color, size, y_offset in layers:
    x = left_x + (Inches(3.5) - size) / 2
    circle = add_circle(slide, x, left_y + y_offset, size, color)
    add_text(slide, x, left_y + y_offset + size * 0.35, size, Inches(0.4),
             name, font_size=11, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, left_x, left_y + Inches(4.2), Inches(3.5), Inches(0.4),
         "像俄罗斯套娃一样层层嵌套", font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - ATM程序结构图
right_x = Inches(5.0)

struct_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(7.7), Inches(5.0),
                               COLORS['white'], COLORS['secondary'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(7.7), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['secondary']
top_c.line.fill.background()

add_text(slide, right_x, Inches(1.88), Inches(7.7), Inches(0.4),
         "🏗️ ATM 程序结构", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 结构树
struct_lines = [
    ("main 函数", COLORS['dark'], 0, True),
    ("├─ 顺序：变量定义", COLORS['text'], 1, False),
    ("├─ 顺序：打印欢迎界面", COLORS['text'], 1, False),
    ("└─ 🔄 while 循环", COLORS['purple'], 1, True),
    ("    ├─ 顺序：显示菜单", COLORS['text'], 2, False),
    ("    ├─ 顺序：读取输入", COLORS['text'], 2, False),
    ("    └─ 🔀 switch 分支", COLORS['yellow'], 2, True),
    ("        ├─ case 1 查询", COLORS['text'], 3, False),
    ("        ├─ case 2 存款 + if", COLORS['accent'], 3, False),
    ("        ├─ case 3 取款 + if-else", COLORS['accent'], 3, False),
    ("        ├─ case 4 转账 + if-else", COLORS['accent'], 3, False),
    ("        └─ case 0 退出", COLORS['green'], 3, False),
]

for i, (text, color, indent, bold) in enumerate(struct_lines):
    add_text(slide, right_x + Inches(0.5), Inches(2.55 + i * 0.33), Inches(6.7), Inches(0.3),
             text, font_size=12, color=color, bold=bold)

# 底部金句
gold = add_rounded_rect(slide, Inches(1), Inches(6.5), Inches(11.3), Inches(0.7),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1), Inches(6.58), Inches(11.3), Inches(0.5),
         "🎯 顺序让代码跑起来，分支让代码有选择，循环让代码有力量。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第10页：代码的坏味道
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🤔 代码的坏味道", "ATM能跑，但代码写得好吗？—— 为下一讲埋伏笔")

# 四个问题卡片
problems = [
    ("📏", "main 太长了", "所有代码都堆在main里\n加功能 = 代码越来越长", COLORS['accent']),
    ("📋", "代码重复", "存款/取款/转账逻辑很像\n都是复制粘贴改一点点", COLORS['yellow']),
    ("🔍", "阅读困难", "想改取款逻辑？\n得在代码海里慢慢找", COLORS['purple']),
    ("📦", "没法复用", "另一个程序也要用存款？\n只能复制粘贴", COLORS['blue']),
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
         "💡 怎么办？代码越来越乱，怎么收拾？",
         font_size=20, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(2), Inches(6.5), Inches(9.3), Inches(0.5),
         "👉 下一讲：函数封装 —— 给代码找个家！",
         font_size=16, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第11页：思考题
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🤔 思考题 · 往深了想", "没有标准答案，重要的是思考过程")

questions = [
    ("case 穿透", "switch中忘记写break会怎样？\n这是bug还是特性？",
     COLORS['primary'], Inches(0.8), Inches(2.0), "⚠️"),
    ("while vs for", "while和for可以互相改写吗？\n什么时候用哪个？",
     COLORS['purple'], Inches(4.6), Inches(2.0), "🔄"),
    ("减少重复", "不用函数，怎么减少代码重复？\n你能想到什么办法？",
     COLORS['secondary'], Inches(8.4), Inches(2.0), "💭"),
]

for title, desc, color, x, y, icon in questions:
    card = add_rounded_rect(slide, x, y, Inches(3.7), Inches(3.5),
                            COLORS['white'], color, 0.1)
    
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(3.7), Inches(0.7))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()
    
    add_text(slide, x + Inches(0.2), y + Inches(0.1), Inches(0.6), Inches(0.5),
             icon, font_size=24, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.9), y + Inches(0.15), Inches(2.6), Inches(0.45),
             title, font_size=16, color=COLORS['white'], bold=True)
    
    add_text(slide, x + Inches(0.3), y + Inches(1.1), Inches(3.1), Inches(1.2),
             desc, font_size=13, color=COLORS['text'], align=PP_ALIGN.CENTER)
    
    tip = add_rounded_rect(slide, x + Inches(0.3), y + Inches(2.6), Inches(3.1), Inches(0.6),
                           COLORS['light'], color, 0.3)
    add_text(slide, x + Inches(0.3), y + Inches(2.7), Inches(3.1), Inches(0.4),
             "💡 答案见课件文档", font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部鼓励
encourage = add_rounded_rect(slide, Inches(1.5), Inches(5.9), Inches(10.3), Inches(1),
                             COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.5), Inches(6.0), Inches(10.3), Inches(0.4),
         "🌟 学编程，最重要的不是记住答案，而是学会提出好问题。",
         font_size=17, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(6.45), Inches(10.3), Inches(0.4),
         "带着问题学习下一讲——函数封装，你会理解得更深刻！",
         font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ============================================================
# 第12页：小结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📝 小结", "三种控制结构构建交互程序")

# 金句
gold_card = add_rounded_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.1),
                             COLORS['primary'], COLORS['primary'], 0.08)
add_text(slide, Inches(1.5), Inches(1.9), Inches(10.3), Inches(0.4),
         "🎯 一句话总结", font_size=15, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(2.25), Inches(10.3), Inches(0.6),
         "顺序让代码跑起来，分支让代码有选择，循环让代码有力量。\n三种结构组合起来，就能构建任何复杂的程序。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 5个知识点
points = [
    ("1️⃣", "顺序结构", "从上到下\n一行一行执行", COLORS['blue']),
    ("2️⃣", "if-else", "灵活的条件判断\n适合范围判断", COLORS['accent']),
    ("3️⃣", "switch", "简洁的多选一\n记得加 break", COLORS['yellow']),
    ("4️⃣", "while循环", "不知道次数\n用条件控制", COLORS['purple']),
    ("5️⃣", "for循环", "知道次数\n计数器驱动", COLORS['green']),
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
next_card = add_rounded_rect(slide, Inches(3), Inches(6.2), Inches(7.3), Inches(0.8),
                             COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(3), Inches(6.3), Inches(7.3), Inches(0.6),
         "👉 下一讲：函数封装 —— 给代码找个家！",
         font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 保存
output_path = r"e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\02_控制结构\docs\课件.pptx"
prs.save(output_path)
print(f"PPT生成完成：{output_path}")
print(f"共 {len(prs.slides)} 页")
