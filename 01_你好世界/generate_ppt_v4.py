# -*- coding: utf-8 -*-
"""
第1阶段：表达式 —— V4 设计版 PPT生成脚本
重点：卡通图形设计 + 图标符号 + 整体构图美感
风格：轻松愉快、卡通风、明亮配色、有设计感
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

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
    'code_bg': RGBColor(0x1E, 0x29, 0x3B),     # 代码背景深蓝
}

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ============================================================
# 基础工具函数
# ============================================================

def add_bg(slide, color=COLORS['light']):
    """添加背景"""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_shape(slide, shape_type, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    """通用形状创建"""
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
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
    # 调整圆角
    shape.adjustments[0] = radius
    return shape

def add_circle(slide, left, top, size, fill_color, transparency=0):
    """圆形"""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    if transparency > 0:
        shape.fill.transparency = transparency
    return shape

def add_text(slide, left, top, width, height, text, font_size=24, color=COLORS['text'],
             bold=False, align=PP_ALIGN.LEFT, font_name='微软雅黑'):
    """添加文本"""
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

def add_multiline_text(slide, left, top, width, height, lines, font_size=14, color=COLORS['text'],
                       bold=False, align=PP_ALIGN.LEFT, line_spacing=1.3):
    """添加多行文本"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.name = '微软雅黑'
    return txBox

def add_title_bar(slide, title, subtitle=None):
    """标题栏"""
    # 顶部装饰条
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLORS['primary']
    bar.line.fill.background()
    
    # 左侧装饰小圆点
    add_circle(slide, Inches(0.3), Inches(0.5), Inches(0.35), COLORS['primary'])
    add_circle(slide, Inches(0.55), Inches(0.55), Inches(0.25), COLORS['secondary'])
    
    add_text(slide, Inches(1.0), Inches(0.4), Inches(11), Inches(0.7),
             title, font_size=32, color=COLORS['dark'], bold=True)
    
    if subtitle:
        add_text(slide, Inches(1.0), Inches(1.05), Inches(11), Inches(0.45),
                 subtitle, font_size=15, color=COLORS['text_light'])
    
    add_text(slide, Inches(0.8), Inches(7.05), Inches(12), Inches(0.3),
             "第1讲 表达式", font_size=11, color=COLORS['text_light'])

# ============================================================
# 图形组件（卡通风格）
# ============================================================

def draw_toolbox(slide, left, top, size, color=COLORS['purple']):
    """画一个工具箱图标"""
    # 箱体
    body = add_rounded_rect(slide, left, top + size * 0.3, size, size * 0.65, color, color, 0.1)
    # 箱盖
    lid = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.05, top + size * 0.15, size * 0.9, size * 0.25, color, color)
    # 提手
    handle = add_shape(slide, MSO_SHAPE.ARC, left + size * 0.25, top, size * 0.5, size * 0.3, None, COLORS['white'], 3)
    # 锁扣
    lock = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.42, top + size * 0.35, size * 0.16, size * 0.1, COLORS['yellow'], COLORS['yellow'])
    return body

def draw_book(slide, left, top, size, color=COLORS['blue']):
    """画一本书"""
    # 书身
    body = add_rounded_rect(slide, left, top, size, size * 0.75, color, color, 0.05)
    # 书页
    page = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.08, top + size * 0.08, size * 0.84, size * 0.59, COLORS['white'], COLORS['white'])
    # 书脊线
    spine = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.48, top + size * 0.08, size * 0.04, size * 0.59, color, color)
    # 几行文字
    for i in range(3):
        line = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.15, top + size * (0.18 + i * 0.12), size * 0.28, size * 0.04, COLORS['text_light'], COLORS['text_light'])
        line2 = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.57, top + size * (0.18 + i * 0.12), size * 0.25, size * 0.04, COLORS['text_light'], COLORS['text_light'])
    return body

def draw_lightbulb(slide, left, top, size, color=COLORS['yellow']):
    """画一个灯泡（创意/想法）"""
    # 灯泡
    bulb = add_circle(slide, left, top, size * 0.8, color)
    # 灯头
    base1 = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.22, top + size * 0.7, size * 0.36, size * 0.12, RGBColor(0x95, 0xA5, 0xA6), RGBColor(0x95, 0xA5, 0xA6))
    base2 = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.28, top + size * 0.82, size * 0.24, size * 0.1, RGBColor(0x7F, 0x8C, 0x8D), RGBColor(0x7F, 0x8C, 0x8D))
    tip = add_shape(slide, MSO_SHAPE.OVAL, left + size * 0.35, top + size * 0.9, size * 0.1, size * 0.08, RGBColor(0x5D, 0x6D, 0x6E), RGBColor(0x5D, 0x6D, 0x6E))
    # 光芒线
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        import math
        rad = math.radians(angle)
        cx = left + size * 0.4
        cy = top + size * 0.4
        inner = size * 0.45
        outer = size * 0.6
        x1 = cx + inner * math.cos(rad)
        y1 = cy + inner * math.sin(rad)
        x2 = cx + outer * math.cos(rad)
        y2 = cy + outer * math.sin(rad)
        ray = slide.shapes.add_connector(1, x1, y1, x2, y2)
        ray.line.color.rgb = color
        ray.line.width = Pt(2)
    return bulb

def draw_gear(slide, left, top, size, color=COLORS['secondary']):
    """画一个齿轮图标"""
    # 中心圆
    center = add_circle(slide, left + size * 0.2, top + size * 0.2, size * 0.6, color)
    # 内圆
    inner = add_circle(slide, left + size * 0.35, top + size * 0.35, size * 0.3, COLORS['white'])
    # 齿（8个矩形）
    import math
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        cx = left + size * 0.5
        cy = top + size * 0.5
        tooth_w = size * 0.15
        tooth_h = size * 0.2
        offset = size * 0.35
        tx = cx - tooth_w / 2 + offset * math.cos(rad)
        ty = cy - tooth_h / 2 + offset * math.sin(rad)
        tooth = add_shape(slide, MSO_SHAPE.RECTANGLE, tx, ty, tooth_w, tooth_h, color, color)
        # 旋转
        tooth.rotation = angle
    return center

def draw_puzzle(slide, left, top, size, color=COLORS['green']):
    """画一个拼图块"""
    # 主体
    body = add_rounded_rect(slide, left, top + size * 0.1, size * 0.85, size * 0.8, color, color, 0.1)
    # 凸起（上面）
    bump_top = add_circle(slide, left + size * 0.3, top, size * 0.3, color)
    # 凹陷（右边） - 用白色圆模拟
    hole_right = add_circle(slide, left + size * 0.7, top + size * 0.35, size * 0.3, COLORS['white'])
    return body

def draw_rocket(slide, left, top, size, color=COLORS['primary']):
    """画一个火箭"""
    # 箭身
    body = add_shape(slide, MSO_SHAPE.TRAPEZOID, left + size * 0.3, top + size * 0.3, size * 0.4, size * 0.5, color, color)
    body.rotation = 180
    # 头锥
    nose = add_shape(slide, MSO_SHAPE.ISOSCELES_TRIANGLE, left + size * 0.3, top, size * 0.4, size * 0.35, color, color)
    # 窗户
    window = add_circle(slide, left + size * 0.4, top + size * 0.35, size * 0.2, COLORS['white'])
    window_inner = add_circle(slide, left + size * 0.43, top + size * 0.38, size * 0.14, COLORS['blue'])
    # 尾翼左
    fin_l = add_shape(slide, MSO_SHAPE.RIGHT_TRIANGLE, left + size * 0.1, top + size * 0.6, size * 0.2, size * 0.25, RGBColor(0xE6, 0x7E, 0x22), RGBColor(0xE6, 0x7E, 0x22))
    # 尾翼右
    fin_r = add_shape(slide, MSO_SHAPE.RIGHT_TRIANGLE, left + size * 0.7, top + size * 0.6, size * 0.2, size * 0.25, RGBColor(0xE6, 0x7E, 0x22), RGBColor(0xE6, 0x7E, 0x22))
    fin_r.rotation = 90
    # 火焰
    flame1 = add_shape(slide, MSO_SHAPE.ISOSCELES_TRIANGLE, left + size * 0.32, top + size * 0.8, size * 0.36, size * 0.25, COLORS['yellow'], COLORS['yellow'])
    flame1.rotation = 180
    flame2 = add_shape(slide, MSO_SHAPE.ISOSCELES_TRIANGLE, left + size * 0.38, top + size * 0.85, size * 0.24, size * 0.18, COLORS['accent'], COLORS['accent'])
    flame2.rotation = 180
    return body

def draw_factory(slide, left, top, size, color=COLORS['secondary']):
    """画一个工厂/流水线图标"""
    # 主体建筑
    body = add_shape(slide, MSO_SHAPE.RECTANGLE, left, top + size * 0.35, size * 0.8, size * 0.65, color, color)
    # 屋顶（锯齿状，用多个三角形）
    for i in range(4):
        roof = add_shape(slide, MSO_SHAPE.ISOSCELES_TRIANGLE, left + i * size * 0.2, top + size * 0.15, size * 0.2, size * 0.25, color, color)
    # 烟囱
    chimney = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.65, top, size * 0.12, size * 0.4, RGBColor(0x3D, 0x99, 0x91), RGBColor(0x3D, 0x99, 0x91))
    # 烟
    smoke1 = add_circle(slide, left + size * 0.6, top - size * 0.05, size * 0.12, COLORS['text_light'], 0.5)
    smoke2 = add_circle(slide, left + size * 0.72, top - size * 0.1, size * 0.1, COLORS['text_light'], 0.4)
    # 门
    door = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.3, top + size * 0.6, size * 0.2, size * 0.4, RGBColor(0x3D, 0x99, 0x91), RGBColor(0x3D, 0x99, 0x91))
    # 窗户
    for i in range(2):
        win = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * (0.08 + i * 0.3), top + size * 0.45, size * 0.15, size * 0.12, COLORS['yellow'], COLORS['yellow'])
    return body

def draw_tree(slide, left, top, size, color=COLORS['green']):
    """画一棵生长的树（进化/成长）"""
    # 树冠（三层圆）
    leaf3 = add_circle(slide, left + size * 0.1, top, size * 0.8, color)
    leaf2 = add_circle(slide, left, top + size * 0.15, size * 0.5, color)
    leaf1 = add_circle(slide, left + size * 0.5, top + size * 0.1, size * 0.5, color)
    # 树干
    trunk = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.35, top + size * 0.6, size * 0.3, size * 0.4, RGBColor(0x8B, 0x45, 0x13), RGBColor(0x8B, 0x45, 0x13))
    return leaf3

def draw_question_mark(slide, left, top, size, color=COLORS['accent']):
    """画一个问号气泡"""
    # 气泡
    bubble = add_rounded_rect(slide, left, top, size, size * 0.85, color, color, 0.3)
    # 气泡尾巴
    tail = add_shape(slide, MSO_SHAPE.ISOSCELES_TRIANGLE, left + size * 0.3, top + size * 0.75, size * 0.25, size * 0.25, color, color)
    tail.rotation = 180
    # 问号文字
    add_text(slide, left, top + size * 0.05, size, size * 0.6, "?",
             font_size=int(size * 0.6), color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    return bubble

def draw_menu(slide, left, top, size, color=COLORS['secondary']):
    """画一个菜单（头文件比喻）"""
    # 菜单板
    board = add_rounded_rect(slide, left, top, size * 0.9, size * 1.1, color, color, 0.05)
    # 夹子
    clip = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.35, top - size * 0.05, size * 0.2, size * 0.12, RGBColor(0x3D, 0x99, 0x91), RGBColor(0x3D, 0x99, 0x91))
    # 菜单项（几行）
    for i in range(4):
        line = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.12, top + size * (0.15 + i * 0.22), size * 0.4, size * 0.05, COLORS['white'], COLORS['white'])
        price = add_shape(slide, MSO_SHAPE.RECTANGLE, left + size * 0.6, top + size * (0.15 + i * 0.22), size * 0.18, size * 0.05, COLORS['yellow'], COLORS['yellow'])
    return board

def draw_kitchen(slide, left, top, size, color=COLORS['purple']):
    """画一个厨房（库文件比喻）"""
    # 灶台
    stove = add_rounded_rect(slide, left, top + size * 0.4, size, size * 0.6, color, color, 0.08)
    # 灶台面
    top_ = add_shape(slide, MSO_SHAPE.RECTANGLE, left - size * 0.02, top + size * 0.35, size * 1.04, size * 0.1, RGBColor(0x7B, 0x68, 0xEE), RGBColor(0x7B, 0x68, 0xEE))
    # 两个灶眼
    eye1 = add_circle(slide, left + size * 0.1, top + size * 0.15, size * 0.3, COLORS['dark'])
    eye2 = add_circle(slide, left + size * 0.6, top + size * 0.15, size * 0.3, COLORS['dark'])
    # 火焰
    flame1 = add_circle(slide, left + size * 0.18, top + size * 0.22, size * 0.15, COLORS['yellow'])
    flame2 = add_circle(slide, left + size * 0.68, top + size * 0.22, size * 0.15, COLORS['yellow'])
    # 锅
    pot = add_shape(slide, MSO_SHAPE.ARC, left + size * 0.25, top + size * 0.45, size * 0.5, size * 0.3, None, RGBColor(0x5D, 0x4B, 0xCE), 4)
    # 蒸汽
    steam1 = add_circle(slide, left + size * 0.35, top, size * 0.1, COLORS['text_light'], 0.5)
    steam2 = add_circle(slide, left + size * 0.5, top - size * 0.05, size * 0.08, COLORS['text_light'], 0.4)
    return stove

# ============================================================
# 第1页：封面
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, COLORS['light'])

# 背景装饰 - 大圆形
add_circle(slide, Inches(9.5), Inches(-1.5), Inches(5), COLORS['primary'], 0.15)
add_circle(slide, Inches(-2), Inches(4.5), Inches(4.5), COLORS['secondary'], 0.12)
add_circle(slide, Inches(11), Inches(5), Inches(2.5), COLORS['yellow'], 0.2)

# 小装饰圆
for x, y, s, c in [
    (Inches(2), Inches(1.2), Inches(0.5), COLORS['pink']),
    (Inches(10.5), Inches(2), Inches(0.4), COLORS['purple']),
    (Inches(1.5), Inches(6.2), Inches(0.35), COLORS['green']),
]:
    add_circle(slide, x, y, s, c, 0.3)

# 主标题区域 - 一个大卡片
card = add_rounded_rect(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5),
                        COLORS['white'], COLORS['white'], 0.05)
# 卡片阴影效果（用一个稍微偏移的形状模拟）
shadow = add_rounded_rect(slide, Inches(1.6), Inches(1.6), Inches(10.3), Inches(4.5),
                          RGBColor(0x00, 0x00, 0x00), RGBColor(0x00, 0x00, 0x00), 0.05)
shadow.fill.transparency = 0.92
# 把阴影放到后面
slide.shapes._spTree.remove(shadow._element)
slide.shapes._spTree.insert(2, shadow._element)

# 左侧图形 - 一个发光的代码符号
add_circle(slide, Inches(2.3), Inches(2.5), Inches(2.2), COLORS['primary'], 0.1)
add_circle(slide, Inches(2.6), Inches(2.8), Inches(1.6), COLORS['primary'])
add_text(slide, Inches(2.6), Inches(3.1), Inches(1.6), Inches(1),
         "{ }", font_size=56, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 右侧文字
add_text(slide, Inches(5.2), Inches(2.3), Inches(6), Inches(1),
         "第1讲：表达式", font_size=52, color=COLORS['dark'], bold=True)
add_text(slide, Inches(5.2), Inches(3.3), Inches(6), Inches(0.6),
         "从一行代码到软件架构", font_size=26, color=COLORS['primary'], bold=True)

# 分隔线
divider = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(5.2), Inches(4.1), Inches(1.5), Inches(0.06))
divider.fill.solid()
divider.fill.fore_color.rgb = COLORS['secondary']
divider.line.fill.background()

add_text(slide, Inches(5.2), Inches(4.3), Inches(6), Inches(0.5),
         "《从程序员到架构师》· C语言插件框架演进之旅", font_size=16, color=COLORS['text_light'])
add_text(slide, Inches(5.2), Inches(4.8), Inches(6), Inches(0.5),
         "一行 printf 背后的完整故事", font_size=18, color=COLORS['accent'], bold=True)

# 底部进度
add_text(slide, Inches(5.5), Inches(5.4), Inches(2.3), Inches(0.5),
         "01 / 12", font_size=22, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第2页：知识图谱
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🗺️ 知识图谱 · 第1讲", "本讲在整个知识体系中的位置")

# 中心节点 - 发光效果
center_x = Inches(5.8)
center_y = Inches(3.7)

# 发光圆
add_circle(slide, center_x - Inches(1.5), center_y - Inches(1), Inches(3), COLORS['primary'], 0.15)
add_circle(slide, center_x - Inches(1.1), center_y - Inches(0.6), Inches(2.2), COLORS['primary'], 0.25)

# 中心卡片
center_card = add_rounded_rect(slide, center_x - Inches(1.3), center_y - Inches(0.55), Inches(2.6), Inches(1.1),
                               COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, center_x - Inches(1.3), center_y - Inches(0.45), Inches(2.6), Inches(0.45),
         "📌 表达式", font_size=24, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, center_x - Inches(1.3), center_y + Inches(0.1), Inches(2.6), Inches(0.35),
         "（第1讲 核心）", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 周围节点（带图标）
nodes = [
    ("C语言基础", COLORS['yellow'], Inches(1.8), Inches(1.5), "前置知识", "📚"),
    ("编译四阶段", COLORS['blue'], Inches(0.8), Inches(4.2), "预处理/编译/汇编/链接", "🏭"),
    ("C标准库", COLORS['purple'], Inches(9.5), Inches(1.5), "libc / printf", "📦"),
    ("函数调用", COLORS['secondary'], Inches(9.8), Inches(4.2), "→ 第2讲", "🔧"),
    ("可执行文件", COLORS['green'], Inches(5.3), Inches(6.0), "程序的诞生", "🚀"),
]

for name, color, x, y, desc, icon in nodes:
    # 节点卡片
    card = add_rounded_rect(slide, x, y, Inches(2.4), Inches(1.0),
                            COLORS['white'], color, 0.15)
    # 图标
    add_text(slide, x + Inches(0.1), y + Inches(0.15), Inches(0.6), Inches(0.7),
             icon, font_size=28, align=PP_ALIGN.CENTER)
    # 文字
    add_text(slide, x + Inches(0.7), y + Inches(0.1), Inches(1.6), Inches(0.4),
             name, font_size=15, color=COLORS['dark'], bold=True)
    add_text(slide, x + Inches(0.7), y + Inches(0.5), Inches(1.6), Inches(0.4),
             desc, font_size=10, color=COLORS['text_light'])

# 连接线
connections = [
    (center_x - Inches(0.5), center_y, Inches(3.0), Inches(2.0)),
    (center_x - Inches(0.5), center_y + Inches(0.3), Inches(2.0), Inches(4.7)),
    (center_x + Inches(0.5), center_y, Inches(9.5), Inches(2.0)),
    (center_x + Inches(0.5), center_y + Inches(0.3), Inches(9.8), Inches(4.7)),
    (center_x, center_y + Inches(0.5), Inches(6.5), Inches(6.5)),
]

for sx, sy, ex, ey in connections:
    line = slide.shapes.add_connector(1, sx, sy, ex, ey)
    line.line.color.rgb = COLORS['text_light']
    line.line.width = Pt(1.5)
    line.line.dash_style = 1  # 虚线

# 底部金句
tip_card = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.6),
                            COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.5), Inches(6.58), Inches(10.3), Inches(0.45),
         "💡 表达式是代码的最小单元，连接了编译原理、标准库、函数调用等多个知识领域",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第3页：C语言的江湖地位
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "👑 C语言的江湖地位", "为什么我们从C语言开始讲起？")

# 左侧 - C语言大侠形象
hero_x = Inches(1)
hero_y = Inches(2.2)

# 披风
cape = add_shape(slide, MSO_SHAPE.PIE, hero_x - Inches(0.3), hero_y + Inches(0.5), Inches(3), Inches(3.5),
                 COLORS['primary'], COLORS['primary'])
# 身体
body = add_rounded_rect(slide, hero_x + Inches(0.3), hero_y + Inches(0.8), Inches(1.8), Inches(2.5),
                        COLORS['blue'], COLORS['blue'], 0.2)
# 头
head = add_circle(slide, hero_x + Inches(0.5), hero_y, Inches(1.4), COLORS['yellow'])
# 眼睛
eye_l = add_circle(slide, hero_x + Inches(0.75), hero_y + Inches(0.45), Inches(0.18), COLORS['dark'])
eye_r = add_circle(slide, hero_x + Inches(1.25), hero_y + Inches(0.45), Inches(0.18), COLORS['dark'])
# 眼镜
glass_l = add_shape(slide, MSO_SHAPE.OVAL, hero_x + Inches(0.68), hero_y + Inches(0.38), Inches(0.32), Inches(0.28),
                    None, COLORS['dark'], 2)
glass_r = add_shape(slide, MSO_SHAPE.OVAL, hero_x + Inches(1.18), hero_y + Inches(0.38), Inches(0.32), Inches(0.28),
                    None, COLORS['dark'], 2)
glass_bridge = add_shape(slide, MSO_SHAPE.RECTANGLE, hero_x + Inches(0.98), hero_y + Inches(0.5), Inches(0.22), Inches(0.03),
                         COLORS['dark'], COLORS['dark'])
# 嘴巴（微笑）
mouth = add_shape(slide, MSO_SHAPE.ARC, hero_x + Inches(0.8), hero_y + Inches(0.75), Inches(0.6), Inches(0.3),
                  None, COLORS['dark'], 2)
# C字标
add_text(slide, hero_x + Inches(0.5), hero_y + Inches(1.5), Inches(1.4), Inches(0.8),
         "C", font_size=48, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, hero_x, hero_y + Inches(3.3), Inches(2.4), Inches(0.5),
         "C语言大侠", font_size=18, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, hero_x, hero_y + Inches(3.7), Inches(2.4), Inches(0.4),
         "1972年 · 贝尔实验室", font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - 小弟们（各种应用）
disciples = [
    ("UNIX / Linux", COLORS['green'], Inches(4.5), Inches(1.8), "🐧"),
    ("Windows内核", COLORS['blue'], Inches(7.5), Inches(1.8), "🪟"),
    ("MySQL数据库", COLORS['purple'], Inches(10.5), Inches(1.8), "🗄️"),
    ("Python解释器", COLORS['yellow'], Inches(4.5), Inches(3.8), "🐍"),
    ("嵌入式设备", COLORS['secondary'], Inches(7.5), Inches(3.8), "📱"),
    ("游戏引擎", COLORS['pink'], Inches(10.5), Inches(3.8), "🎮"),
]

for name, color, x, y, icon in disciples:
    card = add_rounded_rect(slide, x, y, Inches(2.6), Inches(1.4),
                            COLORS['white'], color, 0.2)
    # 图标大
    add_text(slide, x, y + Inches(0.1), Inches(2.6), Inches(0.6),
             icon, font_size=28, align=PP_ALIGN.CENTER)
    # 名称
    add_text(slide, x, y + Inches(0.75), Inches(2.6), Inches(0.4),
             name, font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    # 小"C"标志
    add_text(slide, x + Inches(2.0), y + Inches(0.05), Inches(0.5), Inches(0.3),
             "C", font_size=11, color=color, bold=True, align=PP_ALIGN.CENTER)

# 底部金句
gold_card = add_rounded_rect(slide, Inches(1.5), Inches(5.8), Inches(10.3), Inches(1),
                             COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(5.9), Inches(10.3), Inches(0.4),
         "🏆 金句", font_size=14, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(6.25), Inches(10.3), Inches(0.5),
         "C语言是现代软件世界的地基——你现在用的几乎所有软件，往下挖，底层都有C的影子。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第4页：拆解printf表达式
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🔍 拆解 printf 表达式", "一行代码里的大学问")

# 代码展示框（像终端窗口）
code_frame = add_rounded_rect(slide, Inches(1.2), Inches(1.8), Inches(10.9), Inches(1.6),
                              COLORS['code_bg'], COLORS['code_bg'], 0.08)
# 窗口标题栏
title_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(10.9), Inches(0.35))
title_bar.fill.solid()
title_bar.fill.fore_color.rgb = RGBColor(0x34, 0x49, 0x5E)
title_bar.line.fill.background()
# 三个按钮
btn_colors = [COLORS['accent'], COLORS['yellow'], COLORS['green']]
for i, c in enumerate(btn_colors):
    btn = add_circle(slide, Inches(1.4 + i * 0.4), Inches(1.88), Inches(0.18), c)
# 窗口标题
add_text(slide, Inches(5.5), Inches(1.83), Inches(2.3), Inches(0.3),
         "hello.c", font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 代码内容
add_text(slide, Inches(2), Inches(2.3), Inches(9.3), Inches(0.8),
         'printf("Hello, Plugin Framework!\\n");', font_size=28, color=COLORS['green'], bold=True, align=PP_ALIGN.CENTER)

# 四个拆解卡片（带图标和彩色）
parts = [
    ("printf", "函数名", "print formatted\n格式化打印", COLORS['primary'], Inches(0.8), "🔤"),
    ('"Hello..."', "字符串参数", "要打印的内容\n双引号=字符串", COLORS['secondary'], Inches(3.8), "📝"),
    ("\\n", "转义字符", "换行符\n像按回车键", COLORS['yellow'], Inches(6.8), "↩️"),
    (";", "分号", "语句结束标志\n像句子的句号", COLORS['pink'], Inches(9.8), "🎯"),
]

for code, name, desc, color, x, icon in parts:
    # 卡片
    card = add_rounded_rect(slide, x, Inches(3.9), Inches(2.6), Inches(2.7),
                            COLORS['white'], color, 0.12)
    # 顶部色条
    top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, x, Inches(3.9), Inches(2.6), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()
    
    # 图标
    add_text(slide, x, Inches(4.1), Inches(2.6), Inches(0.6),
             icon, font_size=32, align=PP_ALIGN.CENTER)
    # 代码
    add_text(slide, x, Inches(4.7), Inches(2.6), Inches(0.5),
             code, font_size=18, color=color, bold=True, align=PP_ALIGN.CENTER)
    # 名称
    add_text(slide, x, Inches(5.25), Inches(2.6), Inches(0.4),
             name, font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    # 描述
    add_text(slide, x + Inches(0.2), Inches(5.7), Inches(2.2), Inches(0.8),
             desc, font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ============================================================
# 第5页：C标准库 = 工具箱
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📦 C 标准库", "站在巨人的肩膀上——代码复用的起点")

# 左侧 - 大工具箱
draw_toolbox(slide, Inches(1), Inches(2.5), Inches(3), COLORS['purple'])

add_text(slide, Inches(0.8), Inches(5.7), Inches(3.4), Inches(0.5),
         "C 标准库 (libc)", font_size=22, color=COLORS['purple'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(0.8), Inches(6.2), Inches(3.4), Inches(0.4),
         "几百个工具，开箱即用", font_size=14, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - 工具网格
tools = [
    ("printf/scanf", "输入输出", COLORS['primary'], "📤"),
    ("malloc/free", "内存管理", COLORS['secondary'], "🧠"),
    ("strcpy/strlen", "字符串处理", COLORS['blue'], "🔤"),
    ("fopen/fread", "文件操作", COLORS['green'], "📂"),
    ("sin/cos/sqrt", "数学计算", COLORS['yellow'], "🔢"),
    ("time/clock", "时间日期", COLORS['pink'], "⏰"),
]

for i, (name, desc, color, icon) in enumerate(tools):
    col = i % 3
    row = i // 3
    x = Inches(4.8 + col * 2.8)
    y = Inches(2.2 + row * 2.0)
    
    # 工具卡片
    card = add_rounded_rect(slide, x, y, Inches(2.5), Inches(1.7),
                            COLORS['white'], color, 0.15)
    
    # 图标圆圈
    icon_bg = add_circle(slide, x + Inches(0.15), y + Inches(0.25), Inches(0.7), color)
    add_text(slide, x + Inches(0.15), y + Inches(0.3), Inches(0.7), Inches(0.6),
             icon, font_size=22, align=PP_ALIGN.CENTER)
    
    # 名称
    add_text(slide, x + Inches(0.95), y + Inches(0.3), Inches(1.45), Inches(0.4),
             name, font_size=13, color=COLORS['dark'], bold=True)
    # 描述
    add_text(slide, x + Inches(0.95), y + Inches(0.75), Inches(1.45), Inches(0.4),
             desc, font_size=11, color=COLORS['text_light'])

# 底部思想
idea_card = add_rounded_rect(slide, Inches(1), Inches(6.4), Inches(11.3), Inches(0.7),
                             COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, Inches(1), Inches(6.5), Inches(11.3), Inches(0.5),
         "💡 核心思想：不用重复造轮子——用别人写好的、经过验证的代码，做自己的事情。这就是复用。",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第6页：编译四阶段总览（工厂流水线）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🏭 编译四阶段总览", "从 hello.c 到 hello.exe 的神奇流水线")

# 流水线轨道
track = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(4.0), Inches(12.3), Inches(0.15))
track.fill.solid()
track.fill.fore_color.rgb = COLORS['text_light']
track.fill.transparency = 0.5
track.line.fill.background()

# 6个阶段
stages = [
    ("hello.c", "源代码", COLORS['blue'], Inches(0.3), "📄"),
    ("📋 预处理", "展开头文件\n替换宏", COLORS['yellow'], Inches(2.3), "📋"),
    ("⚙️ 编译", "翻译成\n汇编代码", COLORS['primary'], Inches(4.6), "⚙️"),
    ("🔢 汇编", "生成\n机器码(.o)", COLORS['secondary'], Inches(6.9), "🔢"),
    ("🔗 链接", "拼入库\n函数代码", COLORS['purple'], Inches(9.2), "🔗"),
    ("hello.exe", "可执行\n文件", COLORS['green'], Inches(11.5), "🚀"),
]

for i, (name, desc, color, x, icon) in enumerate(stages):
    # 箭头（除了第一个）
    if i > 0:
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x - Inches(0.7), Inches(3.7), Inches(0.6), Inches(0.5))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = COLORS['text_light']
        arrow.line.fill.background()
    
    # 阶段卡片
    card = add_rounded_rect(slide, x, Inches(2.5), Inches(1.8), Inches(2.8),
                            COLORS['white'], color, 0.12)
    
    # 顶部图标背景
    icon_bg = add_rounded_rect(slide, x, Inches(2.5), Inches(1.8), Inches(1.0),
                               color, color, 0.12)
    add_text(slide, x, Inches(2.6), Inches(1.8), Inches(0.8),
             icon, font_size=36, align=PP_ALIGN.CENTER)
    
    # 名称
    add_text(slide, x, Inches(3.6), Inches(1.8), Inches(0.5),
             name, font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    
    # 描述
    add_text(slide, x + Inches(0.1), Inches(4.2), Inches(1.6), Inches(0.9),
             desc, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部记忆口诀
mnemonic = add_rounded_rect(slide, Inches(3.5), Inches(5.7), Inches(6.3), Inches(1.0),
                            COLORS['light'], COLORS['accent'], 0.3)
add_text(slide, Inches(3.5), Inches(5.8), Inches(6.3), Inches(0.45),
         "💡 记忆口诀：预 → 编 → 汇 → 链", font_size=22, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(3.5), Inches(6.3), Inches(6.3), Inches(0.35),
         "（谐音：预判会练 —— 提前预判，就会练习）", font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ============================================================
# 第7页：链接的秘密（重点页）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "⭐ 重点：链接的秘密", "printf 是怎么跑进我们的程序里的？")

# 大标题
add_text(slide, Inches(1), Inches(1.7), Inches(11), Inches(0.5),
         "链接器做了什么？四步走", font_size=22, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# 左边：hello.o（不完整的拼图）
left_x = Inches(0.8)
left_y = Inches(2.5)

left_card = add_rounded_rect(slide, left_x, left_y, Inches(3), Inches(3.8),
                             COLORS['white'], COLORS['blue'], 0.1)
# 顶部色条
add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, left_y, Inches(3), Inches(0.5)).fill.solid()
top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, left_y, Inches(3), Inches(0.5))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = COLORS['blue']
top_bar.line.fill.background()

add_text(slide, left_x, left_y + Inches(0.05), Inches(3), Inches(0.4),
         "📄 hello.o 目标文件", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 拼图图示（缺一块）
puzzle_area_y = left_y + Inches(0.8)
# 已有的拼图（main）
main_piece = add_rounded_rect(slide, left_x + Inches(0.5), puzzle_area_y, Inches(2), Inches(1.2),
                              COLORS['blue'], COLORS['blue'], 0.1)
add_text(slide, left_x + Inches(0.5), puzzle_area_y + Inches(0.35), Inches(2), Inches(0.5),
         "我们的代码\n(main函数)", font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 空缺位置（虚线框）
missing = add_rounded_rect(slide, left_x + Inches(0.5), puzzle_area_y + Inches(1.5), Inches(2), Inches(1.2),
                           COLORS['light'], COLORS['accent'], 0.1)
# 虚线效果用透明度模拟
missing.fill.transparency = 0.7

add_text(slide, left_x + Inches(0.5), puzzle_area_y + Inches(1.85), Inches(2), Inches(0.5),
         "❓ printf 在哪？\n（未定义符号）", font_size=11, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, left_x + Inches(0.2), left_y + Inches(3.3), Inches(2.6), Inches(0.4),
         "⚠️ 不能独立运行！", font_size=13, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# 中间：链接器+步骤
mid_x = Inches(4.3)
mid_card = add_rounded_rect(slide, mid_x, left_y, Inches(4.5), Inches(3.8),
                            COLORS['white'], COLORS['purple'], 0.1)
# 顶部色条
top_bar2 = add_shape(slide, MSO_SHAPE.RECTANGLE, mid_x, left_y, Inches(4.5), Inches(0.5))
top_bar2.fill.solid()
top_bar2.fill.fore_color.rgb = COLORS['purple']
top_bar2.line.fill.background()

add_text(slide, mid_x, left_y + Inches(0.05), Inches(4.5), Inches(0.4),
         "🔗 链接器 + 📦 标准库", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

link_steps = [
    ("1️⃣", "符号解析", "找出所有未定义的函数引用"),
    ("2️⃣", "库中查找", "去libc里找printf的实现"),
    ("3️⃣", "代码合并", "把printf的代码拼进来"),
    ("4️⃣", "地址重定位", "调整所有调用的地址"),
]

for i, (num, title, desc) in enumerate(link_steps):
    y = left_y + Inches(0.7 + i * 0.75)
    # 序号圆
    num_circle = add_circle(slide, mid_x + Inches(0.3), y, Inches(0.5), COLORS['purple'])
    add_text(slide, mid_x + Inches(0.3), y + Inches(0.05), Inches(0.5), Inches(0.4),
             num, font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    # 标题
    add_text(slide, mid_x + Inches(0.95), y + Inches(0.02), Inches(3.2), Inches(0.3),
             title, font_size=13, color=COLORS['dark'], bold=True)
    # 描述
    add_text(slide, mid_x + Inches(0.95), y + Inches(0.32), Inches(3.2), Inches(0.3),
             desc, font_size=11, color=COLORS['text_light'])

# 右边：hello.exe（完整拼图）
right_x = Inches(9.5)
right_card = add_rounded_rect(slide, right_x, left_y, Inches(3), Inches(3.8),
                              COLORS['white'], COLORS['green'], 0.1)
# 顶部色条
top_bar3 = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, left_y, Inches(3), Inches(0.5))
top_bar3.fill.solid()
top_bar3.fill.fore_color.rgb = COLORS['green']
top_bar3.line.fill.background()

add_text(slide, right_x, left_y + Inches(0.05), Inches(3), Inches(0.4),
         "🚀 hello.exe 可执行文件", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 完整拼图
puzzle_r_y = left_y + Inches(0.8)
main_piece_r = add_rounded_rect(slide, right_x + Inches(0.5), puzzle_r_y, Inches(2), Inches(1.2),
                                COLORS['green'], COLORS['green'], 0.1)
add_text(slide, right_x + Inches(0.5), puzzle_r_y + Inches(0.35), Inches(2), Inches(0.5),
         "我们的代码\n(main函数)", font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

printf_piece = add_rounded_rect(slide, right_x + Inches(0.5), puzzle_r_y + Inches(1.5), Inches(2), Inches(1.2),
                                COLORS['secondary'], COLORS['secondary'], 0.1)
add_text(slide, right_x + Inches(0.5), puzzle_r_y + Inches(1.85), Inches(2), Inches(0.5),
         "✅ printf 实现\n（从库中拼入）", font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, right_x + Inches(0.2), left_y + Inches(3.3), Inches(2.6), Inches(0.4),
         "🎉 可以独立运行！", font_size=13, color=COLORS['green'], bold=True, align=PP_ALIGN.CENTER)

# 箭头
for start_x, end_x in [(Inches(3.8), Inches(4.3)), (Inches(8.8), Inches(9.5))]:
    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, start_x, Inches(4.2), Inches(0.5), Inches(0.5))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = COLORS['primary']
    arrow.line.fill.background()

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.7),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.6), Inches(10.3), Inches(0.5),
         "🔑 链接的本质：把我们的代码和库的代码拼在一起，形成完整的可执行程序。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第8页：头文件 vs 库文件（菜单 vs 厨房）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📋 头文件 vs 🍳 库文件", "一个比喻搞懂接口与实现的分离")

# 左边：头文件 = 菜单
left_x = Inches(0.8)
left_y = Inches(2.0)

left_card = add_rounded_rect(slide, left_x, left_y, Inches(5.5), Inches(4.8),
                             COLORS['white'], COLORS['secondary'], 0.08)
# 顶部色条
top_l = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, left_y, Inches(5.5), Inches(0.6))
top_l.fill.solid()
top_l.fill.fore_color.rgb = COLORS['secondary']
top_l.line.fill.background()

add_text(slide, left_x, left_y + Inches(0.1), Inches(5.5), Inches(0.4),
         "📋 头文件 (.h)", font_size=22, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 菜单图形
draw_menu(slide, left_x + Inches(2), left_y + Inches(0.9), Inches(1.5), COLORS['secondary'])

# "= 菜单"
add_text(slide, left_x, left_y + Inches(2.7), Inches(5.5), Inches(0.5),
         "= 菜 单", font_size=22, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

h_points = [
    "• 里面是函数声明（接口描述）",
    "• 告诉编译器：有这个函数，长什么样",
    "• 不包含具体实现代码（不能吃）",
    "• 编译阶段使用",
    "• 例：stdio.h, stdlib.h, string.h",
]
for i, p in enumerate(h_points):
    add_text(slide, left_x + Inches(0.5), left_y + Inches(3.4 + i * 0.45), Inches(4.5), Inches(0.4),
             p, font_size=13, color=COLORS['text'])

# 右边：库文件 = 厨房
right_x = Inches(7)
right_card = add_rounded_rect(slide, right_x, left_y, Inches(5.5), Inches(4.8),
                              COLORS['white'], COLORS['purple'], 0.08)
top_r = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, left_y, Inches(5.5), Inches(0.6))
top_r.fill.solid()
top_r.fill.fore_color.rgb = COLORS['purple']
top_r.line.fill.background()

add_text(slide, right_x, left_y + Inches(0.1), Inches(5.5), Inches(0.4),
         "🍳 库文件 (.a / .dll)", font_size=22, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 厨房图形
draw_kitchen(slide, right_x + Inches(2), left_y + Inches(0.9), Inches(1.5), COLORS['purple'])

add_text(slide, right_x, left_y + Inches(2.7), Inches(5.5), Inches(0.5),
         "= 厨 房", font_size=22, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

lib_points = [
    "• 里面是函数实现（真正的代码）",
    "• 链接器把它拼进你的程序",
    "• 包含几百个函数的二进制代码",
    "• 链接阶段使用",
    "• 例：libc.a, msvcrt.dll",
]
for i, p in enumerate(lib_points):
    add_text(slide, right_x + Inches(0.5), left_y + Inches(3.4 + i * 0.45), Inches(4.5), Inches(0.4),
             p, font_size=13, color=COLORS['text'])

# 中间 VS
vs_circle = add_circle(slide, Inches(6.1), Inches(3.9), Inches(1), COLORS['accent'])
add_text(slide, Inches(6.1), Inches(4.1), Inches(1), Inches(0.6),
         "VS", font_size=28, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 底部总结
bottom_card = add_rounded_rect(slide, Inches(1), Inches(6.5), Inches(11.3), Inches(0.7),
                               COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1), Inches(6.58), Inches(11.3), Inches(0.5),
         "🎯 一句话：编译器看头文件（查菜单），链接器找库文件（找厨房）。接口与实现分离！",
         font_size=15, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第9页：从语言到架构（生长树）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🌱 从表达式到框架", "软件架构是怎样一步一步生长出来的？")

# 生长树图示（从下往上）
layers = [
    ("表达式", COLORS['primary'], Inches(6.0), 0, "最底层的砖"),
    ("函数封装", COLORS['secondary'], Inches(5.3), 1, "用砖砌墙"),
    ("模块编程", COLORS['yellow'], Inches(4.6), 2, "用墙搭房间"),
    ("静态库", COLORS['purple'], Inches(3.9), 3, "预制构件"),
    ("动态库", COLORS['pink'], Inches(3.2), 4, "可替换构件"),
    ("插件框架", COLORS['accent'], Inches(2.3), 5, "大楼设计图"),
]

# 树干（中间的连接线）
trunk = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(6.4), Inches(2.2), Inches(0.15), Inches(4.5))
trunk.fill.solid()
trunk.fill.fore_color.rgb = RGBColor(0x8B, 0x45, 0x13)
trunk.line.fill.background()

# 各层节点（左右交替）
for i, (name, color, x, level, desc) in enumerate(layers):
    y = Inches(6.2 - level * 0.8)
    
    # 枝叶（用圆/椭圆模拟）
    leaf_w = Inches(2.2 + level * 0.3)
    leaf_h = Inches(0.9 + level * 0.05)
    leaf = add_rounded_rect(slide, x, y, leaf_w, leaf_h, color, color, 0.4)
    
    # 层级数字
    num_circle = add_circle(slide, x - Inches(0.3), y + Inches(0.1), Inches(0.7), COLORS['white'])
    add_text(slide, x - Inches(0.3), y + Inches(0.15), Inches(0.7), Inches(0.4),
             f"0{level+1}" if level < 9 else str(level+1), font_size=16, color=color, bold=True, align=PP_ALIGN.CENTER)
    
    # 名称
    add_text(slide, x + Inches(0.5), y + Inches(0.05), Inches(1.5), Inches(0.4),
             name, font_size=16, color=COLORS['white'], bold=True)
    # 描述
    add_text(slide, x + Inches(0.5), y + Inches(0.45), Inches(1.5), Inches(0.35),
             desc, font_size=10, color=COLORS['white'])

# 右侧总结
right_card = add_rounded_rect(slide, Inches(9), Inches(2.2), Inches(3.8), Inches(4.5),
                              COLORS['white'], COLORS['green'], 0.08)
top_r = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(9), Inches(2.2), Inches(3.8), Inches(0.6))
top_r.fill.solid()
top_r.fill.fore_color.rgb = COLORS['green']
top_r.line.fill.background()

add_text(slide, Inches(9), Inches(2.3), Inches(3.8), Inches(0.4),
         "🌳 生长规律", font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

grow_points = [
    "每一层解决一个问题",
    "每一层引入一个新概念",
    "每一层建立在下一层之上",
    "",
    "💡 复用思想 → 从标准库开始",
    "💡 接口思想 → 从头文件开始",
    "💡 分层思想 → 从编译开始",
]
for i, p in enumerate(grow_points):
    add_text(slide, Inches(9.3), Inches(3.0 + i * 0.5), Inches(3.2), Inches(0.4),
             p, font_size=13, color=COLORS['text'])

# 底部金句
gold = add_rounded_rect(slide, Inches(1), Inches(6.5), Inches(7.5), Inches(0.7),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1), Inches(6.58), Inches(7.5), Inches(0.5),
         "🎯 理解了底层原理，再看框架，万变不离其宗。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第10页：课堂小测
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "✅ 课堂小测", "看看你掌握了多少？")

# 题目卡片
q_card = add_rounded_rect(slide, Inches(1), Inches(1.8), Inches(11.3), Inches(1.3),
                          COLORS['white'], COLORS['primary'], 0.1)
# 左侧问号图标
q_icon = add_circle(slide, Inches(1.3), Inches(2.05), Inches(0.8), COLORS['primary'])
add_text(slide, Inches(1.3), Inches(2.15), Inches(0.8), Inches(0.6),
         "?", font_size=36, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, Inches(2.3), Inches(2.1), Inches(9.7), Inches(0.5),
         "题目：目标文件（.o）为什么不能直接运行？", font_size=22, color=COLORS['dark'], bold=True)
add_text(slide, Inches(2.3), Inches(2.65), Inches(9.7), Inches(0.4),
         "请选择正确答案，思考一下再看解析～", font_size=13, color=COLORS['text_light'])

# 选项
options = [
    ("A", "因为它是二进制的", COLORS['text_light'], False),
    ("B", "因为缺少库函数的实现", COLORS['green'], True),
    ("C", "因为它太大了", COLORS['text_light'], False),
    ("D", "因为操作系统不认识 .o 格式", COLORS['text_light'], False),
]

for i, (letter, text, color, is_correct) in enumerate(options):
    x = Inches(1 + (i % 2) * 5.8)
    y = Inches(3.5 + (i // 2) * 1.4)
    
    opt_card = add_rounded_rect(slide, x, y, Inches(5.5), Inches(1.1),
                                COLORS['white'], color, 0.15)
    # 选项字母圆
    letter_circle = add_circle(slide, x + Inches(0.3), y + Inches(0.2), Inches(0.7), color)
    add_text(slide, x + Inches(0.3), y + Inches(0.28), Inches(0.7), Inches(0.5),
             letter, font_size=22, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    # 选项文字
    add_text(slide, x + Inches(1.2), y + Inches(0.3), Inches(4), Inches(0.5),
             text, font_size=17, color=COLORS['text'])

# 答案解析
ans_card = add_rounded_rect(slide, Inches(2), Inches(6.3), Inches(9.3), Inches(0.9),
                            COLORS['green'], COLORS['green'], 0.2)
add_text(slide, Inches(2), Inches(6.4), Inches(9.3), Inches(0.4),
         "✅ 正确答案：B", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(2), Inches(6.8), Inches(9.3), Inches(0.4),
         "解析：目标文件只有我们写的代码，printf 等库函数还没链接进来，所以不能独立运行！",
         font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# ============================================================
# 第11页：思考题引申
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "🤔 思考题 · 往深了想", "没有标准答案，重要的是思考过程")

questions = [
    ("编译型 vs 解释型", "C是编译型，Python是解释型，\n各有什么优缺点？和插件有什么关系？",
     COLORS['primary'], Inches(0.8), Inches(2.0), "⚡"),
    ("静态链接的代价", "100个程序都用printf，\n内存里就有100份？怎么解决？",
     COLORS['purple'], Inches(4.6), Inches(2.0), "💾"),
    ("灵活与安全的平衡", "C的表达式设计很灵活但易错，\n编程语言设计中这是矛盾吗？",
     COLORS['secondary'], Inches(8.4), Inches(2.0), "⚖️"),
]

for title, desc, color, x, y, icon in questions:
    # 卡片
    card = add_rounded_rect(slide, x, y, Inches(3.7), Inches(3.5),
                            COLORS['white'], color, 0.1)
    
    # 顶部色条
    top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, x, y, Inches(3.7), Inches(0.7))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()
    
    # 图标
    add_text(slide, x + Inches(0.2), y + Inches(0.1), Inches(0.6), Inches(0.5),
             icon, font_size=24, align=PP_ALIGN.CENTER)
    # 标题
    add_text(slide, x + Inches(0.9), y + Inches(0.15), Inches(2.6), Inches(0.45),
             title, font_size=16, color=COLORS['white'], bold=True)
    
    # 问题描述
    add_text(slide, x + Inches(0.3), y + Inches(1.1), Inches(3.1), Inches(1.2),
             desc, font_size=13, color=COLORS['text'], align=PP_ALIGN.CENTER)
    
    # 底部提示
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
         "这些问题会在后面的课程中逐一展开——带着问题学习，效率最高！",
         font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ============================================================
# 第12页：小结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "📝 小结", "一行 printf 的完整生命周期")

# 金句卡片
gold_card = add_rounded_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.3),
                             COLORS['primary'], COLORS['primary'], 0.08)
add_text(slide, Inches(1.5), Inches(1.95), Inches(10.3), Inches(0.4),
         "🎯 一句话总结", font_size=16, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(2.35), Inches(10.3), Inches(0.7),
         "一行 printf 表达式，从代码到输出，经历了编译四阶段，\n通过链接把标准库的 printf 拼进来，最终打出 Hello。这就是复用的起点。",
         font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 5个知识点卡片
points = [
    ("1️⃣", "表达式", "能算值的代码片段\nC几乎一切都是表达式", COLORS['primary']),
    ("2️⃣", "C标准库", "自带的工具箱\nprintf/malloc都在这", COLORS['purple']),
    ("3️⃣", "头文件vs库", "头文件是接口（菜单）\n库文件是实现（厨房）", COLORS['secondary']),
    ("4️⃣", "编译四阶段", "预→编→汇→链\n口诀：预判会练", COLORS['blue']),
    ("5️⃣", "链接的本质", "把我们的代码和库的代码\n拼在一起", COLORS['green']),
]

for i, (num, title, desc, color) in enumerate(points):
    x = Inches(0.5 + i * 2.55)
    y = Inches(3.6)
    
    card = add_rounded_rect(slide, x, y, Inches(2.35), Inches(2.5),
                            COLORS['white'], color, 0.12)
    
    # 顶部色条
    top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, x, y, Inches(2.35), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()
    
    # 序号
    add_text(slide, x, y + Inches(0.2), Inches(2.35), Inches(0.6),
             num, font_size=32, align=PP_ALIGN.CENTER)
    # 标题
    add_text(slide, x, y + Inches(0.9), Inches(2.35), Inches(0.45),
             title, font_size=17, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    # 分隔线
    divider = add_shape(slide, MSO_SHAPE.RECTANGLE, x + Inches(0.8), y + Inches(1.45), Inches(0.75), Inches(0.04))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()
    # 描述
    add_text(slide, x + Inches(0.15), y + Inches(1.6), Inches(2.05), Inches(0.8),
             desc, font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部预告
next_card = add_rounded_rect(slide, Inches(3), Inches(6.4), Inches(7.3), Inches(0.7),
                             COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(3), Inches(6.5), Inches(7.3), Inches(0.5),
         "👉 下一讲：函数封装 —— 给代码找个家",
         font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 保存
output_path = r"e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\01_你好世界\docs\课件.pptx"
prs.save(output_path)
print(f"PPT V4（设计版）生成完成：{output_path}")
print(f"共 {len(prs.slides)} 页")
