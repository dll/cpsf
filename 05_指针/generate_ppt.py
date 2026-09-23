# -*- coding: utf-8 -*-
"""
第5讲：指针 —— PPT生成脚本
风格：轻松愉快、卡通风、明亮配色、有设计感
12页：封面、知识图谱、地址的概念、指针定义与使用、取地址和解引用、
      指针作为函数参数、指针与数组、内存模型简图、ATM指针版对比、
      函数指针预告、思考题、小结
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import math

# ============================================================
# 配色方案（轻松活泼风 —— 与系列保持一致）
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
    'code_bg': RGBColor(0x1E, 0x29, 0x3B),     # 深色代码背景
    'code_top': RGBColor(0x34, 0x49, 0x5E),    # 代码区标题栏
}

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ============================================================
# 工具函数
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
             bold=False, align=PP_ALIGN.LEFT):
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
    run.font.name = '微软雅黑'
    return txBox

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
             "第5讲 指针", font_size=11, color=COLORS['text_light'])

def add_code_block(slide, left, top, width, height, title, code_lines):
    """代码块（深色背景+标题栏）"""
    # 代码卡片
    add_rounded_rect(slide, left, top, width, height,
                     COLORS['code_bg'], COLORS['code_bg'], 0.08)
    # 标题栏
    code_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.4))
    code_top.fill.solid()
    code_top.fill.fore_color.rgb = COLORS['code_top']
    code_top.line.fill.background()
    # 窗口按钮
    for i, c in enumerate([COLORS['accent'], COLORS['yellow'], COLORS['green']]):
        add_circle(slide, left + Inches(0.2 + i * 0.35), top + Inches(0.08), Inches(0.2), c)
    # 标题文字
    add_text(slide, left + Inches(3.5), top + Inches(0.03), Inches(1.5), Inches(0.35),
             title, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)
    # 代码内容
    for i, (code, color) in enumerate(code_lines):
        add_text(slide, left + Inches(0.5), top + Inches(0.55 + i * 0.38), width - Inches(1), Inches(0.35),
                 code, font_size=13, color=color)

# ============================================================
# 卡通图形绘制函数
# ============================================================

def draw_hotel(slide, left, top, size, color=COLORS['yellow']):
    """画一个卡通酒店（地址比喻）"""
    # 酒店主体
    body = add_rounded_rect(slide, left, top + size * 0.15, size * 0.8, size * 0.85,
                            color, color, 0.05)
    # 屋顶
    roof = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,
                                   left - size * 0.05, top, size * 0.9, size * 0.25)
    roof.fill.solid()
    roof.fill.fore_color.rgb = COLORS['accent']
    roof.line.fill.background()

    # 窗户（格子）
    for row in range(3):
        for col in range(3):
            wx = left + size * (0.12 + col * 0.22)
            wy = top + size * (0.3 + row * 0.2)
            win = add_rounded_rect(slide, wx, wy, size * 0.15, size * 0.13,
                                   COLORS['blue'], COLORS['blue'], 0.2)
    # 门
    door = add_rounded_rect(slide, left + size * 0.32, top + size * 0.72, size * 0.16, size * 0.28,
                            COLORS['dark'], COLORS['dark'], 0.3)
    # 门牌号
    sign = add_rounded_rect(slide, left + size * 0.55, top + size * 0.05, size * 0.25, size * 0.12,
                            COLORS['white'], COLORS['dark'], 0.3)
    add_text(slide, left + size * 0.55, top + size * 0.06, size * 0.25, size * 0.1,
             "A123", font_size=10, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

def draw_key(slide, left, top, size, color=COLORS['yellow']):
    """画一把卡通钥匙（解引用比喻）"""
    # 钥匙头（圆环）
    head_outer = add_circle(slide, left, top, size * 0.4, color)
    head_inner = add_circle(slide, left + size * 0.12, top + size * 0.12, size * 0.16, COLORS['light'])
    # 钥匙杆
    shaft = add_shape(slide, MSO_SHAPE.RECTANGLE,
                      left + size * 0.35, top + size * 0.15, size * 0.45, size * 0.1,
                      color, color)
    # 钥匙齿
    tooth1 = add_shape(slide, MSO_SHAPE.RECTANGLE,
                       left + size * 0.65, top + size * 0.25, size * 0.06, size * 0.12,
                       color, color)
    tooth2 = add_shape(slide, MSO_SHAPE.RECTANGLE,
                       left + size * 0.75, top + size * 0.25, size * 0.06, size * 0.08,
                       color, color)

def draw_atm(slide, left, top, size, color=COLORS['blue']):
    """画一个ATM机图标"""
    body = add_rounded_rect(slide, left, top, size * 0.8, size, color, color, 0.08)
    screen = add_rounded_rect(slide, left + size * 0.1, top + size * 0.08, size * 0.6, size * 0.35,
                              COLORS['code_bg'], COLORS['code_bg'], 0.1)
    for i in range(3):
        add_shape(slide, MSO_SHAPE.RECTANGLE,
                  left + size * 0.15, top + size * (0.13 + i * 0.08), size * 0.4, size * 0.03,
                  COLORS['green'], COLORS['green'])
    keypad_y = top + size * 0.5
    for row in range(3):
        for col in range(3):
            add_circle(slide, left + size * (0.12 + col * 0.2), keypad_y + row * size * 0.12, size * 0.12,
                       COLORS['white'])
    add_shape(slide, MSO_SHAPE.RECTANGLE,
              left + size * 0.2, top + size * 0.88, size * 0.4, size * 0.05,
              COLORS['dark'], COLORS['dark'])

def draw_memory_map(slide, left, top, width, height):
    """画内存模型四个区域"""
    regions = [
        ("代码区 (Text)", "函数的机器指令\n只读，程序运行期间存在", COLORS['purple'], 0.2),
        ("全局区 (Data/BSS)", "全局变量、静态变量\n程序启动到结束", COLORS['accent'], 0.25),
        ("栈区 (Stack)", "局部变量、函数参数\n函数调用到返回", COLORS['secondary'], 0.3),
        ("堆区 (Heap)", "malloc 分配的内存\n手动分配回收", COLORS['yellow'], 0.25),
    ]
    y_offset = 0
    for name, desc, color, ratio in regions:
        h = int(height * ratio)
        bar = add_rounded_rect(slide, left, top + Inches(y_offset), width, Inches(h),
                               color, color, 0.1)
        add_text(slide, left + Inches(0.2), top + Inches(y_offset + 0.05), width - Inches(0.4), Inches(0.35),
                 name, font_size=14, color=COLORS['white'], bold=True)
        add_text(slide, left + Inches(0.2), top + Inches(y_offset + 0.35), width - Inches(0.4), Inches(h - 0.4),
                 desc, font_size=10, color=COLORS['white'])
        y_offset += h

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
shadow = add_rounded_rect(slide, Inches(1.6), Inches(1.6), Inches(10.3), Inches(4.5),
                          RGBColor(0x00, 0x00, 0x00), RGBColor(0x00, 0x00, 0x00), 0.05)
shadow.fill.transparency = 0.92
slide.shapes._spTree.remove(shadow._element)
slide.shapes._spTree.insert(2, shadow._element)

# 左侧 - 钥匙图标
draw_key(slide, Inches(2.5), Inches(2.5), Inches(2.5), COLORS['primary'])
add_text(slide, Inches(2.0), Inches(4.2), Inches(3.5), Inches(0.5),
         "& 取地址  * 解引用", font_size=16, color=COLORS['primary'], bold=True, align=PP_ALIGN.CENTER)

# 右侧文字
add_text(slide, Inches(5.2), Inches(2.3), Inches(6), Inches(1),
         "第5讲：指针", font_size=52, color=COLORS['dark'], bold=True)
add_text(slide, Inches(5.2), Inches(3.3), Inches(6), Inches(0.6),
         "打通任督二脉", font_size=26, color=COLORS['primary'], bold=True)

# 分隔线
divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.2), Inches(4.1), Inches(1.5), Inches(0.06))
divider.fill.solid()
divider.fill.fore_color.rgb = COLORS['secondary']
divider.line.fill.background()

add_text(slide, Inches(5.2), Inches(4.3), Inches(6), Inches(0.5),
         "《从程序员到架构师》· C语言插件框架演进之旅", font_size=16, color=COLORS['text_light'])
add_text(slide, Inches(5.2), Inches(4.8), Inches(6), Inches(0.5),
         "地址 · 解引用 · 指针传参 —— 消灭全局变量", font_size=18, color=COLORS['accent'], bold=True)

add_text(slide, Inches(5.5), Inches(5.4), Inches(2.3), Inches(0.5),
         "05 / 14", font_size=22, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第2页：知识图谱
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "知识图谱 · 第5讲", "本讲在整个知识体系中的位置")

center_x = Inches(5.8)
center_y = Inches(3.7)

# 中心节点
add_circle(slide, center_x - Inches(1.5), center_y - Inches(1), Inches(3), COLORS['secondary'])
add_circle(slide, center_x - Inches(1.1), center_y - Inches(0.6), Inches(2.2), COLORS['secondary'])

center_card = add_rounded_rect(slide, center_x - Inches(1.3), center_y - Inches(0.55), Inches(2.6), Inches(1.1),
                               COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, center_x - Inches(1.3), center_y - Inches(0.45), Inches(2.6), Inches(0.45),
         "指针", font_size=24, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, center_x - Inches(1.3), center_y + Inches(0.1), Inches(2.6), Inches(0.35),
         "（第5讲 核心）", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 周围节点
nodes = [
    ("函数封装", COLORS['primary'], Inches(1.0), Inches(1.3), "第3讲 · 前置", ""),
    ("多文件编程", COLORS['yellow'], Inches(0.5), Inches(3.8), "第4讲 · 前置", ""),
    ("数组与字符串", COLORS['purple'], Inches(9.8), Inches(1.3), "第6讲 · 后续", ""),
    ("结构体", COLORS['blue'], Inches(9.8), Inches(3.8), "第7讲 · 后续", ""),
    ("函数指针", COLORS['accent'], Inches(5.3), Inches(6.0), "第12讲 · 插件框架", ""),
]

for name, color, x, y, desc, icon in nodes:
    card = add_rounded_rect(slide, x, y, Inches(2.4), Inches(1.0),
                            COLORS['white'], color, 0.15)
    add_text(slide, x + Inches(0.1), y + Inches(0.15), Inches(2.2), Inches(0.4),
             name, font_size=15, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.1), y + Inches(0.55), Inches(2.2), Inches(0.35),
             desc, font_size=10, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 连接线
connections = [
    (center_x - Inches(0.5), center_y, Inches(2.5), Inches(1.8)),
    (center_x - Inches(0.5), center_y + Inches(0.2), Inches(2.0), Inches(4.3)),
    (center_x + Inches(0.5), center_y, Inches(10.0), Inches(1.8)),
    (center_x + Inches(0.5), center_y + Inches(0.2), Inches(10.0), Inches(4.3)),
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
         "指针 = 地址 + 类型 —— 让函数能修改调用者的变量，消灭全局变量",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第3页：地址的概念（酒店房间号比喻）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "什么是指针？", "内存就像一栋酒店——房间号就是地址")

# 左侧 - 卡通酒店
draw_hotel(slide, Inches(0.8), Inches(2.0), Inches(3.5), COLORS['yellow'])

add_text(slide, Inches(0.5), Inches(5.8), Inches(4), Inches(0.5),
         "每个房间有编号（地址）\n每个房间住着客人（数据）",
         font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧 - 内存图示
right_x = Inches(5.0)

mem_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(7.7), Inches(4.8),
                             COLORS['white'], COLORS['blue'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(7.7), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['blue']
top_c.line.fill.background()

add_text(slide, right_x, Inches(1.88), Inches(7.7), Inches(0.4),
         "内存酒店 · 房间分布图", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 内存格子
mem_cells = [
    ("0x7FFF0000", "1000.0", "balance", COLORS['green']),
    ("0x7FFF0008", "42",     "count",   COLORS['blue']),
    ("0x7FFF0010", "3.14",   "pi",      COLORS['purple']),
    ("0x7FFF0018", "'A'",    "ch",      COLORS['accent']),
    ("0x7FFF0020", "0x7FFF0000", "p_balance (指针!)", COLORS['yellow']),
]

for i, (addr, val, name, color) in enumerate(mem_cells):
    y = Inches(2.55 + i * 0.75)
    # 地址格
    addr_box = add_rounded_rect(slide, right_x + Inches(0.3), y, Inches(1.8), Inches(0.6),
                                 COLORS['code_bg'], COLORS['code_bg'], 0.15)
    add_text(slide, right_x + Inches(0.3), y + Inches(0.1), Inches(1.8), Inches(0.4),
             addr, font_size=11, color=COLORS['secondary'], align=PP_ALIGN.CENTER)
    # 值格
    val_box = add_rounded_rect(slide, right_x + Inches(2.3), y, Inches(1.5), Inches(0.6),
                               color, color, 0.15)
    add_text(slide, right_x + Inches(2.3), y + Inches(0.1), Inches(1.5), Inches(0.4),
             val, font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    # 变量名
    add_text(slide, right_x + Inches(4.0), y + Inches(0.1), Inches(3), Inches(0.4),
             name, font_size=13, color=COLORS['dark'], bold=True)

# 高亮最后一行（指针）
highlight = add_rounded_rect(slide, right_x + Inches(0.2), Inches(2.55 + 4 * 0.75) - Inches(0.05),
                             Inches(7.3), Inches(0.7),
                             RGBColor(0xFF, 0xFF, 0xE0), RGBColor(0xFF, 0xD9, 0x3D), 0.1)
# 把高亮移到指针行后面
slide.shapes._spTree.remove(highlight._element)
# 找到指针行文本的位置插入
add_text(slide, right_x + Inches(0.3), Inches(6.55), Inches(7), Inches(0.3),
         "p_balance 存的不是数据，是 balance 的地址！",
         font_size=12, color=COLORS['primary'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第4页：指针变量的定义和使用
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "指针变量的定义", "int* p = &a —— 一行代码三种含义")

# 代码拆解图
code_x = Inches(1.5)
code_y = Inches(2.0)

# 大代码块
code_card = add_rounded_rect(slide, code_x, code_y, Inches(10.3), Inches(1.2),
                              COLORS['code_bg'], COLORS['code_bg'], 0.08)
add_text(slide, code_x + Inches(0.5), code_y + Inches(0.2), Inches(9), Inches(0.8),
         "int*  p  =  &a;",
         font_size=36, color=COLORS['green'], bold=True, align=PP_ALIGN.CENTER)

# 拆解标注
parts = [
    ("int*", "指针类型\n指向 int 的指针", COLORS['blue'], Inches(1.8), Inches(0.5)),
    ("p", "指针变量名\np_ 前缀表示指针", COLORS['accent'], Inches(4.0), Inches(0.5)),
    ("=", "赋值\n把地址赋给指针", COLORS['text_light'], Inches(5.8), Inches(0.5)),
    ("&a", "取地址\n得到 a 的内存地址", COLORS['yellow'], Inches(7.5), Inches(0.5)),
]

for text, desc, color, x, _ in parts:
    # 箭头指向代码中的对应部分
    arrow = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, code_x + x, code_y + Inches(1.3), Inches(0.3), Inches(0.4))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()

    # 标注卡片
    card = add_rounded_rect(slide, code_x + x - Inches(0.5), code_y + Inches(1.8), Inches(2.0), Inches(1.2),
                            COLORS['white'], color, 0.15)
    add_text(slide, code_x + x - Inches(0.5), code_y + Inches(1.85), Inches(2.0), Inches(0.45),
             text, font_size=18, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, code_x + x - Inches(0.4), code_y + Inches(2.3), Inches(1.8), Inches(0.6),
             desc, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部对比：不同类型的指针
type_card = add_rounded_rect(slide, Inches(1.5), Inches(5.5), Inches(10.3), Inches(1.3),
                              COLORS['white'], COLORS['secondary'], 0.08)
add_text(slide, Inches(1.8), Inches(5.55), Inches(3), Inches(0.35),
         "不同类型的指针", font_size=15, color=COLORS['dark'], bold=True)

types = [
    ("int*", "4字节", COLORS['blue']),
    ("double*", "8字节", COLORS['purple']),
    ("char*", "1字节", COLORS['accent']),
]
for i, (t, size, color) in enumerate(types):
    x = Inches(2.0 + i * 3.3)
    type_box = add_rounded_rect(slide, x, Inches(5.95), Inches(2.8), Inches(0.7),
                                color, color, 0.15)
    add_text(slide, x, Inches(6.0), Inches(2.8), Inches(0.35),
             t, font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, Inches(6.3), Inches(2.8), Inches(0.3),
             "解引用读 " + size, font_size=10, color=COLORS['white'], align=PP_ALIGN.CENTER)

# ============================================================
# 第5页：取地址和解引用（钥匙比喻）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "两个核心操作：& 和 *", "取地址 = 问房间号，解引用 = 拿钥匙开门")

# 两个操作并排
operations = [
    {
        "symbol": "&",
        "name": "取地址",
        "desc": "从变量 → 得到地址",
        "analogy": "你住哪个房间？",
        "example": "int a = 42;\nint* p = &a;\n// p 得到 a 的地址",
        "color": COLORS['blue'],
        "icon_func": draw_key,
    },
    {
        "symbol": "*",
        "name": "解引用",
        "desc": "从地址 → 得到变量",
        "analogy": "按房间号去找人",
        "example": "int b = *p;\n// b = 42\n*p = 100;\n// a 变成 100",
        "color": COLORS['accent'],
        "icon_func": draw_key,
    },
]

for i, op in enumerate(operations):
    x = Inches(0.6 + i * 6.4)
    y = Inches(2.0)

    # 卡片
    card = add_rounded_rect(slide, x, y, Inches(5.8), Inches(4.5),
                            COLORS['white'], op['color'], 0.12)

    # 顶部色条
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(5.8), Inches(0.7))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = op['color']
    top_bar.line.fill.background()

    # 大符号
    add_text(slide, x + Inches(0.2), y + Inches(0.05), Inches(0.8), Inches(0.6),
             op['symbol'], font_size=36, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(1.0), y + Inches(0.1), Inches(4.5), Inches(0.5),
             op['name'], font_size=20, color=COLORS['white'], bold=True)

    # 比喻
    analogy_card = add_rounded_rect(slide, x + Inches(0.3), y + Inches(0.9), Inches(5.2), Inches(0.7),
                                     COLORS['light'], op['color'], 0.2)
    add_text(slide, x + Inches(0.3), y + Inches(0.95), Inches(5.2), Inches(0.6),
             op['analogy'], font_size=16, color=op['color'], bold=True, align=PP_ALIGN.CENTER)

    # 代码示例
    code_lines = op['example'].split('\n')
    for j, line in enumerate(code_lines):
        add_text(slide, x + Inches(0.5), y + Inches(1.8 + j * 0.4), Inches(5), Inches(0.35),
                 line, font_size=14, color=COLORS['dark'])

    # 说明
    add_text(slide, x + Inches(0.3), y + Inches(3.8), Inches(5.2), Inches(0.5),
             op['desc'], font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.6),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.78), Inches(10.3), Inches(0.45),
         "& 和 * 是互逆操作：*(&a) == a，&(*p) == p",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第6页：指针作为函数参数（对比值传递）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "指针作为函数参数", "解决值传递的局限 —— 让函数能修改调用者的变量")

# 左右对比
# 左侧：值传递（失败）
left_x = Inches(0.6)

left_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.8), Inches(5.0),
                              COLORS['white'], COLORS['accent'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.8), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['accent']
top_c.line.fill.background()

add_text(slide, left_x, Inches(1.88), Inches(5.8), Inches(0.4),
         "值传递 —— 改不了！", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

left_code = [
    ("void add_one(int x) {", COLORS['accent']),
    ("    x = x + 1;  // 改副本", COLORS['text']),
    ("}", COLORS['accent']),
    ("", COLORS['text']),
    ("int a = 10;", COLORS['blue']),
    ("add_one(a);", COLORS['blue']),
    ('printf("%d", a);', COLORS['text_light']),
    ("// 输出: 10  没变!", COLORS['accent']),
]
for i, (code, color) in enumerate(left_code):
    add_text(slide, left_x + Inches(0.5), Inches(2.55 + i * 0.4), Inches(5), Inches(0.35),
             code, font_size=13, color=color)

# 红叉
add_text(slide, left_x + Inches(4.5), Inches(5.8), Inches(1), Inches(0.8),
         "X", font_size=40, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

# 右侧：指针传递（成功）
right_x = Inches(6.9)

right_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(5.8), Inches(5.0),
                               COLORS['white'], COLORS['green'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(5.8), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['green']
top_c.line.fill.background()

add_text(slide, right_x, Inches(1.88), Inches(5.8), Inches(0.4),
         "指针传递 —— 改成功!", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

right_code = [
    ("void add_one(int* p) {", COLORS['green']),
    ("    *p = *p + 1;  // 改原件", COLORS['text']),
    ("}", COLORS['green']),
    ("", COLORS['text']),
    ("int a = 10;", COLORS['blue']),
    ("add_one(&a);  // 传地址", COLORS['blue']),
    ('printf("%d", a);', COLORS['text_light']),
    ("// 输出: 11  变了!", COLORS['green']),
]
for i, (code, color) in enumerate(right_code):
    add_text(slide, right_x + Inches(0.5), Inches(2.55 + i * 0.4), Inches(5), Inches(0.35),
             code, font_size=13, color=color)

# 绿勾
add_text(slide, right_x + Inches(4.5), Inches(5.8), Inches(1), Inches(0.8),
         "OK", font_size=32, color=COLORS['green'], bold=True, align=PP_ALIGN.CENTER)

# 底部比喻
tip = add_rounded_rect(slide, Inches(0.6), Inches(6.3), Inches(12.1), Inches(0.5),
                       COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(0.6), Inches(6.35), Inches(12.1), Inches(0.4),
         "值传递 = 给复印件    指针传递 = 给钥匙 —— 钥匙能打开保险箱改原件",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第7页：指针与数组
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "指针与数组", "数组名就是指针 —— arr[i] 等价于 *(arr+i)")

# 上半部分：数组内存图
arr_x = Inches(1.5)
arr_y = Inches(1.9)

add_text(slide, arr_x, arr_y, Inches(10), Inches(0.35),
         "int arr[5] = {10, 20, 30, 40, 50};", font_size=16, color=COLORS['dark'], bold=True)

# 画5个格子
arr_values = [10, 20, 30, 40, 50]
arr_colors = [COLORS['blue'], COLORS['green'], COLORS['yellow'], COLORS['purple'], COLORS['accent']]
for i, (val, color) in enumerate(zip(arr_values, arr_colors)):
    x = arr_x + Inches(i * 1.8)
    # 格子
    cell = add_rounded_rect(slide, x, arr_y + Inches(0.5), Inches(1.6), Inches(1.0),
                            color, color, 0.1)
    add_text(slide, x, arr_y + Inches(0.6), Inches(1.6), Inches(0.4),
             str(val), font_size=22, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    # 下标
    add_text(slide, x, arr_y + Inches(1.0), Inches(1.6), Inches(0.35),
             "arr[" + str(i) + "]", font_size=12, color=COLORS['text_light'], align=PP_ALIGN.CENTER)
    # 地址
    add_text(slide, x, arr_y + Inches(1.55), Inches(1.6), Inches(0.3),
             "addr+" + str(i * 4), font_size=10, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 等价关系
eq_card = add_rounded_rect(slide, Inches(1.5), Inches(4.3), Inches(10.3), Inches(0.8),
                            COLORS['yellow'], COLORS['yellow'], 0.2)
add_text(slide, Inches(1.5), Inches(4.35), Inches(10.3), Inches(0.7),
         "arr[i]  ==  *(arr + i)      下标写法  ==  指针写法",
         font_size=20, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# 下半部分：区别对比
diff_data = [
    ("特性", "数组名", "指针变量", ""),
    ("本质", "地址常量", "变量", ""),
    ("能否赋值", "不能", "能", ""),
    ("sizeof", "数组大小", "指针大小(8字节)", ""),
]

for i, (feat, arr_val, ptr_val, _) in enumerate(diff_data):
    y = Inches(5.3 + i * 0.4)
    color = COLORS['dark'] if i == 0 else COLORS['text']
    bold = True if i == 0 else False
    bg = COLORS['secondary'] if i == 0 else COLORS['white']

    if i == 0:
        row = add_rounded_rect(slide, Inches(2.0), y, Inches(9.3), Inches(0.35),
                               bg, bg, 0.3)

    add_text(slide, Inches(2.5), y, Inches(2.5), Inches(0.35),
             feat, font_size=12, color=color, bold=bold)
    add_text(slide, Inches(5.5), y, Inches(3), Inches(0.35),
             arr_val, font_size=12, color=color, bold=bold)
    add_text(slide, Inches(9.0), y, Inches(3), Inches(0.35),
             ptr_val, font_size=12, color=color, bold=bold)

# ============================================================
# 第8页：内存模型简图
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "内存模型简图", "程序运行时，内存分为四个区域")

# 左侧 - 内存区域图
draw_memory_map(slide, Inches(1.0), Inches(1.8), Inches(5.5), Inches(5.0))

# 右侧 - 说明
right_x = Inches(7.0)

regions_info = [
    ("代码区", "存放函数的机器指令\n只读，程序运行期间存在", COLORS['purple']),
    ("全局区", "全局变量、静态变量\n第3讲的 g_balance 在这里\n第5讲没有全局变量了!", COLORS['accent']),
    ("栈区", "局部变量、函数参数\n第5讲的 balance 在这里\n指针参数 p_balance 也在这", COLORS['secondary']),
    ("堆区", "malloc 分配的内存\n手动分配，手动回收\n不用指针没法操作堆", COLORS['yellow']),
]

for i, (name, desc, color) in enumerate(regions_info):
    y = Inches(1.9 + i * 1.25)
    card = add_rounded_rect(slide, right_x, y, Inches(5.5), Inches(1.1),
                            COLORS['white'], color, 0.1)
    # 色块
    add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, y, Inches(0.15), Inches(1.1), color, color)
    add_text(slide, right_x + Inches(0.3), y + Inches(0.05), Inches(2), Inches(0.35),
             name, font_size=15, color=color, bold=True)
    add_text(slide, right_x + Inches(0.3), y + Inches(0.4), Inches(5), Inches(0.65),
             desc, font_size=11, color=COLORS['text_light'])

# 底部金句
gold = add_rounded_rect(slide, Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.6),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.45),
         "第5讲消灭了全局区里的 g_balance —— 余额搬到了栈区的 main 函数里",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第9页：ATM指针版对比（全局变量 vs 指针）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "ATM 指针版对比", "全局变量 vs 指针 —— 从公共牧场到钥匙授权")

# 左右对比卡片
# 左侧：全局变量版
left_x = Inches(0.6)
left_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.8), Inches(4.8),
                              COLORS['white'], COLORS['accent'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.8), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['accent']
top_c.line.fill.background()
add_text(slide, left_x, Inches(1.88), Inches(5.8), Inches(0.4),
         "第3讲：全局变量版", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

left_code = [
    ("double g_balance = 1000.0;", COLORS['accent']),
    ("", COLORS['text']),
    ("void deposit(void) {", COLORS['accent']),
    ("    g_balance += amount;", COLORS['text']),
    ("    // 直接改全局变量", COLORS['text_light']),
    ("}", COLORS['accent']),
    ("", COLORS['text']),
    ("// 调用", COLORS['text_light']),
    ("deposit();  // 看不出依赖", COLORS['accent']),
]
for i, (code, color) in enumerate(left_code):
    add_text(slide, left_x + Inches(0.4), Inches(2.55 + i * 0.38), Inches(5), Inches(0.35),
             code, font_size=12, color=color)

# 问题标注
problems = [
    "X 谁都能改，改乱了找谁？",
    "X 隐藏依赖，参数列表看不出来",
    "X 搬到别的程序要带全局变量",
]
for i, p in enumerate(problems):
    add_text(slide, left_x + Inches(0.4), Inches(5.5 + i * 0.35), Inches(5), Inches(0.3),
             p, font_size=11, color=COLORS['accent'])

# 右侧：指针版
right_x = Inches(6.9)
right_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(5.8), Inches(4.8),
                               COLORS['white'], COLORS['green'], 0.08)
top_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(5.8), Inches(0.55))
top_c.fill.solid()
top_c.fill.fore_color.rgb = COLORS['green']
top_c.line.fill.background()
add_text(slide, right_x, Inches(1.88), Inches(5.8), Inches(0.4),
         "第5讲：指针版", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

right_code = [
    ("// 余额在 main 中（局部变量）", COLORS['text_light']),
    ("double balance = 1000.0;", COLORS['green']),
    ("", COLORS['text']),
    ("void deposit(double* p) {", COLORS['green']),
    ("    if (p == NULL) return;", COLORS['text']),
    ("    *p += amount;  // 通过指针改", COLORS['text']),
    ("}", COLORS['green']),
    ("", COLORS['text']),
    ("deposit(&balance);  // 显式传地址", COLORS['green']),
]
for i, (code, color) in enumerate(right_code):
    add_text(slide, right_x + Inches(0.4), Inches(2.55 + i * 0.38), Inches(5), Inches(0.35),
             code, font_size=12, color=color)

# 优势标注
advantages = [
    "OK 余额只在 main 中可见",
    "OK 函数参数明确声明依赖",
    "OK const 保护 + NULL 检查",
]
for i, a in enumerate(advantages):
    add_text(slide, right_x + Inches(0.4), Inches(5.5 + i * 0.35), Inches(5), Inches(0.3),
             a, font_size=11, color=COLORS['green'])

# 底部金句
gold = add_rounded_rect(slide, Inches(0.6), Inches(6.7), Inches(12.1), Inches(0.5),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(0.6), Inches(6.75), Inches(12.1), Inches(0.4),
         "全局变量 = 钥匙挂在走廊墙上    指针传参 = 钥匙在 main 手里，谁用谁借",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第10页：函数指针预告
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "函数指针（预告）", "今天学数据指针，后面学函数指针 —— 插件框架的钥匙")

# 演进路线图
roadmap_y = Inches(2.2)

# 四个阶段
stages = [
    ("数据指针", "指向变量的地址\nint* p = &a", COLORS['blue'], "今天"),
    ("函数指针", "指向函数的地址\nvoid (*f)(double*)", COLORS['purple'], "第12讲"),
    ("回调函数", "把函数当参数传\nregister(deposit)", COLORS['accent'], "第12讲"),
    ("插件框架", "动态注册功能\n新增功能不改主程序", COLORS['green'], "第13-14讲"),
]

for i, (name, desc, color, when) in enumerate(stages):
    x = Inches(0.5 + i * 3.2)
    y = roadmap_y

    # 卡片
    card = add_rounded_rect(slide, x, y, Inches(2.9), Inches(2.8),
                            COLORS['white'], color, 0.12)
    # 顶部色条
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.9), Inches(0.6))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    add_text(slide, x, y + Inches(0.1), Inches(2.9), Inches(0.4),
             name, font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.2), y + Inches(0.8), Inches(2.5), Inches(1.2),
             desc, font_size=12, color=COLORS['text'], align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.2), y + Inches(2.2), Inches(2.5), Inches(0.4),
             when, font_size=13, color=color, bold=True, align=PP_ALIGN.CENTER)

    # 箭头连接
    if i < 3:
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                        x + Inches(2.95), y + Inches(1.1), Inches(0.2), Inches(0.3))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = COLORS['text_light']
        arrow.line.fill.background()

# 底部代码示例
code_card = add_rounded_rect(slide, Inches(1.5), Inches(5.3), Inches(10.3), Inches(1.5),
                              COLORS['code_bg'], COLORS['code_bg'], 0.08)

add_text(slide, Inches(2.0), Inches(5.4), Inches(9.5), Inches(0.35),
         "// 函数指针数组：把函数当数据存 —— 不用 switch 了！", font_size=12, color=COLORS['text_light'])
add_text(slide, Inches(2.0), Inches(5.75), Inches(9.5), Inches(0.35),
         "void (*ops[])(double*) = {NULL, query_balance, deposit, withdraw, transfer};", font_size=13, color=COLORS['green'])
add_text(slide, Inches(2.0), Inches(6.1), Inches(9.5), Inches(0.35),
         "ops[choice](&balance);  // 一行替代整个 switch！", font_size=13, color=COLORS['yellow'])
add_text(slide, Inches(2.0), Inches(6.45), Inches(9.5), Inches(0.3),
         "// 这就是插件框架的雏形 —— 从程序员到架构师", font_size=11, color=COLORS['secondary'])

# ============================================================
# 第11页：思考题
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "思考题 · 往深了想", "没有标准答案，重要的是思考过程")

questions = [
    ("指针是灵魂", "为什么说指针是C语言的灵魂？\n没有指针会失去什么能力？",
     COLORS['primary'], Inches(0.8), Inches(2.0)),
    ("值传递vs指针", "值传递和指针传递的\n本质区别是什么？",
     COLORS['purple'], Inches(4.6), Inches(2.0)),
    ("数组名vs指针", "数组名和指针有什么\n联系和区别？",
     COLORS['secondary'], Inches(8.4), Inches(2.0)),
    ("NULL检查", "空指针(NULL)是什么？\n为什么要检查NULL？",
     COLORS['accent'], Inches(0.8), Inches(4.5)),
]

for i, (title, desc, color, x, y) in enumerate(questions):
    # 思考题1-3在第一行，思考题4在第二行（居中）
    if i < 3:
        card_width = Inches(3.7)
        card_height = Inches(2.8)
    else:
        card_width = Inches(7.0)
        card_height = Inches(2.0)
        x = Inches(3.2)

    card = add_rounded_rect(slide, x, y, card_width, card_height,
                            COLORS['white'], color, 0.1)

    # 顶部色条
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, card_width, Inches(0.6))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    add_text(slide, x + Inches(0.2), y + Inches(0.1), Inches(0.5), Inches(0.4),
             str(i+1), font_size=22, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x + Inches(0.8), y + Inches(0.15), card_width - Inches(1), Inches(0.45),
             title, font_size=16, color=COLORS['white'], bold=True)

    add_text(slide, x + Inches(0.3), y + Inches(0.8), card_width - Inches(0.6), Inches(1.5),
             desc, font_size=13, color=COLORS['text'], align=PP_ALIGN.CENTER)

    tip = add_rounded_rect(slide, x + Inches(0.3), y + card_height - Inches(0.55),
                           card_width - Inches(0.6), Inches(0.4),
                           COLORS['light'], color, 0.3)
    add_text(slide, x + Inches(0.3), y + card_height - Inches(0.5),
             card_width - Inches(0.6), Inches(0.3),
             "答案见课件文档", font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部鼓励
encourage = add_rounded_rect(slide, Inches(3.2), Inches(6.7), Inches(7.0), Inches(0.5),
                              COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(3.2), Inches(6.75), Inches(7.0), Inches(0.4),
         "带着问题学下一讲——数组与字符串，你会理解得更深！",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第12页：小结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "小结", "指针 = 地址 —— 消灭全局变量，让数据共享更安全")

# 金句
gold_card = add_rounded_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.1),
                             COLORS['primary'], COLORS['primary'], 0.08)
add_text(slide, Inches(1.5), Inches(1.9), Inches(10.3), Inches(0.4),
         "一句话总结", font_size=15, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(2.25), Inches(10.3), Inches(0.6),
         "指针就是地址 —— 通过地址，函数可以修改调用者的变量，\n消灭全局变量，让数据共享更安全、更可控。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 6个知识点
points = [
    ("1", "指针的本质", "存地址的变量\n内存的房间号", COLORS['blue']),
    ("2", "取地址 &", "从变量得到地址\n你住哪个房间？", COLORS['accent']),
    ("3", "解引用 *", "从地址得到变量\n按房间号找人", COLORS['yellow']),
    ("4", "指针传参", "函数能改外部变量\n消灭全局变量", COLORS['green']),
    ("5", "指针与数组", "数组名就是指针\narr[i] = *(arr+i)", COLORS['purple']),
    ("6", "函数指针", "指向函数的地址\n插件框架的钥匙", COLORS['pink']),
]

for i, (num, title, desc, color) in enumerate(points):
    x = Inches(0.5 + i * 2.15)
    y = Inches(3.4)

    card = add_rounded_rect(slide, x, y, Inches(2.0), Inches(2.5),
                            COLORS['white'], color, 0.12)

    # 顶部色条
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.0), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    # 序号圆
    add_circle(slide, x + Inches(0.7), y + Inches(0.2), Inches(0.6), color)
    add_text(slide, x + Inches(0.7), y + Inches(0.25), Inches(0.6), Inches(0.5),
             num, font_size=24, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

    add_text(slide, x, y + Inches(0.9), Inches(2.0), Inches(0.4),
             title, font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.6), y + Inches(1.35), Inches(0.8), Inches(0.04))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.1), y + Inches(1.5), Inches(1.8), Inches(0.9),
             desc, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部预告
next_card = add_rounded_rect(slide, Inches(3), Inches(6.2), Inches(7.3), Inches(0.8),
                             COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(3), Inches(6.3), Inches(7.3), Inches(0.6),
         "下一讲：数组与字符串 —— 把同类数据打包在一起！",
         font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 保存
# ============================================================
output_path = r"e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\05_指针\docs\课件.pptx"
prs.save(output_path)
print(f"PPT生成完成：{output_path}")
print(f"共 {len(prs.slides)} 页")
