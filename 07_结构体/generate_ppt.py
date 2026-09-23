# -*- coding: utf-8 -*-
"""
第7讲：结构体 —— PPT生成脚本
风格：轻松愉快、卡通风、明亮配色、有设计感
12页幻灯片，16:9，底部标注"第7讲 结构体"
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
    'primary':    RGBColor(0xFF, 0x8C, 0x42),    # 暖橙色
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
             "第7讲 结构体", font_size=11, color=COLORS['text_light'])

def draw_business_card(slide, left, top, width, height, name, phone, email, color):
    """画一张名片"""
    # 名片主体
    card = add_rounded_rect(slide, left, top, width, height, COLORS['white'], color, 0.05)
    # 顶部色条
    top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.15), color)
    # 姓名
    add_text(slide, left + Inches(0.2), top + Inches(0.25), width - Inches(0.4), Inches(0.5),
             name, font_size=22, color=COLORS['dark'], bold=True)
    # 电话
    add_text(slide, left + Inches(0.2), top + Inches(0.8), width - Inches(0.4), Inches(0.35),
             phone, font_size=13, color=COLORS['text_light'])
    # 邮箱
    add_text(slide, left + Inches(0.2), top + Inches(1.15), width - Inches(0.4), Inches(0.35),
             email, font_size=13, color=COLORS['text_light'])

def draw_struct_box(slide, left, top, width, height, struct_name, members, color):
    """画一个结构体框（带成员列表）"""
    # 容器
    card = add_rounded_rect(slide, left, top, width, height, COLORS['white'], color, 0.06)
    # 标题栏
    header = add_shape(slide, MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.45), color)
    add_text(slide, left + Inches(0.1), top + Inches(0.05), width - Inches(0.2), Inches(0.35),
             struct_name, font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    # 成员列表
    for i, (mtype, mname, mcolor) in enumerate(members):
        my = top + Inches(0.55 + i * 0.4)
        add_text(slide, left + Inches(0.15), my, Inches(1.2), Inches(0.32),
                 mtype, font_size=11, color=mcolor, font_name='Consolas')
        add_text(slide, left + Inches(1.35), my, width - Inches(1.5), Inches(0.32),
                 mname, font_size=11, color=COLORS['text'], font_name='Consolas')

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

# 左侧 - 名片图标（结构体比喻）
card_y = Inches(2.3)
# 画三张名片叠在一起
draw_business_card(slide, Inches(2.0), card_y + Inches(0.3), Inches(3.0), Inches(1.5),
                   "Account", "id: 1001", "balance: 1000.0", COLORS['primary'])
draw_business_card(slide, Inches(2.3), card_y + Inches(1.0), Inches(3.0), Inches(1.5),
                   "Account", "id: 1002", "balance: 2000.0", COLORS['secondary'])
draw_business_card(slide, Inches(2.6), card_y + Inches(1.7), Inches(3.0), Inches(1.5),
                   "Account", "id: 1003", "balance: 500.0", COLORS['purple'])

add_text(slide, Inches(1.8), Inches(4.7), Inches(3.2), Inches(0.4),
         "一盒名片 = 一个结构体数组", font_size=14, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 右侧文字
add_text(slide, Inches(5.8), Inches(2.3), Inches(6), Inches(1),
         "第7讲：结构体", font_size=52, color=COLORS['dark'], bold=True)
add_text(slide, Inches(5.8), Inches(3.3), Inches(6), Inches(0.6),
         "把相关数据打包到一起", font_size=26, color=COLORS['primary'], bold=True)

# 分隔线
divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), Inches(4.1), Inches(1.5), Inches(0.06))
divider.fill.solid()
divider.fill.fore_color.rgb = COLORS['secondary']
divider.line.fill.background()

add_text(slide, Inches(5.8), Inches(4.3), Inches(6), Inches(0.5),
         "《从程序员到架构师》· C语言插件框架演进之旅", font_size=16, color=COLORS['text_light'])
add_text(slide, Inches(5.8), Inches(4.8), Inches(6), Inches(0.5),
         "结构体定义 · 成员访问 · 指针传递 · typedef · 数据封装", font_size=18, color=COLORS['accent'], bold=True)

add_text(slide, Inches(6.0), Inches(5.4), Inches(2.3), Inches(0.5),
         "07 / 14", font_size=22, color=COLORS['accent'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, Inches(0.8), Inches(7.05), Inches(12), Inches(0.3),
         "第7讲 结构体", font_size=11, color=COLORS['text_light'])

# ============================================================
# 第2页：知识图谱
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "知识图谱 · 第7讲", "本讲在整个知识体系中的位置")

# 中心节点
center_x = Inches(5.8)
center_y = Inches(3.7)

add_circle(slide, center_x - Inches(1.5), center_y - Inches(1), Inches(3), COLORS['secondary'])
add_circle(slide, center_x - Inches(1.1), center_y - Inches(0.6), Inches(2.2), COLORS['secondary'])

center_card = add_rounded_rect(slide, center_x - Inches(1.3), center_y - Inches(0.55), Inches(2.6), Inches(1.1),
                               COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, center_x - Inches(1.3), center_y - Inches(0.45), Inches(2.6), Inches(0.45),
         "结构体", font_size=24, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, center_x - Inches(1.3), center_y + Inches(0.1), Inches(2.6), Inches(0.35),
         "（第7讲 核心）", font_size=13, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 周围节点
nodes = [
    ("指针", COLORS['purple'], Inches(1.0), Inches(1.3), "第5讲 · 前置", "指针"),
    ("数组", COLORS['yellow'], Inches(0.5), Inches(3.8), "第6讲 · 前置", "数组"),
    ("链表", COLORS['blue'], Inches(9.8), Inches(1.3), "第8讲 · 后续", "链表"),
    ("接口抽象", COLORS['green'], Inches(9.8), Inches(3.8), "第9讲 · 后续", "接口"),
    ("ATM账户封装", COLORS['accent'], Inches(5.3), Inches(6.0), "本讲实战案例", "ATM"),
]

for name, color, x, y, desc, icon in nodes:
    card = add_rounded_rect(slide, x, y, Inches(2.4), Inches(1.0),
                            COLORS['white'], color, 0.15)
    add_text(slide, x + Inches(0.1), y + Inches(0.15), Inches(0.6), Inches(0.7),
             icon, font_size=18, bold=True, align=PP_ALIGN.CENTER)
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
         "结构体是从'平行数组'到'数据封装'的关键一步——衔接指针/数组，预告链表/接口",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第3页：为什么需要结构体（名片比喻）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "为什么需要结构体？", "从'散落的纸条'到'一盒名片'")

# 左侧 - 平行数组的痛苦
left_x = Inches(0.6)
left_y = Inches(2.0)

pain_card = add_rounded_rect(slide, left_x, left_y, Inches(5.5), Inches(4.3),
                              COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, left_y, Inches(5.5), Inches(0.55), COLORS['accent'])
add_text(slide, left_x, left_y + Inches(0.08), Inches(5.5), Inches(0.4),
         "第6讲：平行数组太散了", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 三张散落的纸条
notes = [
    ("ids[5] = {1001, 1002, ...}", COLORS['accent']),
    ("names[5][20] = {\"张三\", ...}", COLORS['yellow']),
    ("balances[5] = {1000, ...}", COLORS['secondary']),
]
for i, (text, color) in enumerate(notes):
    ny = left_y + Inches(0.8 + i * 0.75)
    # 倾斜的纸条效果（用不同x偏移模拟散落）
    nx = left_x + Inches(0.3 + (i % 2) * 1.0)
    note = add_rounded_rect(slide, nx, ny, Inches(4.5), Inches(0.6), color, color, 0.1)
    add_text(slide, nx, ny + Inches(0.08), Inches(4.5), Inches(0.45),
             text, font_size=13, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

add_text(slide, left_x + Inches(0.3), left_y + Inches(3.3), Inches(5.0), Inches(0.3),
         "三个数组靠索引关联，改一处要同步改三处", font_size=12, color=COLORS['accent'], bold=True)
add_text(slide, left_x + Inches(0.3), left_y + Inches(3.7), Inches(5.0), Inches(0.3),
         "加字段？再加一个数组——越来越乱", font_size=12, color=COLORS['accent'])

# 右侧 - 结构体的清爽
right_x = Inches(6.8)
right_y = Inches(2.0)

struct_card = add_rounded_rect(slide, right_x, right_y, Inches(5.8), Inches(4.3),
                               COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, right_y, Inches(5.8), Inches(0.55), COLORS['secondary'])
add_text(slide, right_x, right_y + Inches(0.08), Inches(5.8), Inches(0.4),
         "第7讲：结构体打包到一起", font_size=17, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 结构体名片
struct_members = [
    ("int", "id", COLORS['green']),
    ("char[20]", "name", COLORS['primary']),
    ("double", "balance", COLORS['purple']),
]
draw_struct_box(slide, right_x + Inches(0.8), right_y + Inches(0.8), Inches(4.0), Inches(2.0),
               "struct Account", struct_members, COLORS['secondary'])

add_text(slide, right_x + Inches(0.3), right_y + Inches(3.1), Inches(5.2), Inches(0.35),
         "Account accounts[5] = {{1001,\"张三\",1000.0}, ...};",
         font_size=12, color=COLORS['secondary'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, right_x + Inches(0.3), right_y + Inches(3.6), Inches(5.2), Inches(0.35),
         "一个结构体数组 = 一盒名片，整齐不散落", font_size=13, color=COLORS['text'])

# 中间箭头
arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.0), Inches(3.8), Inches(0.8), Inches(0.5))
arrow.fill.solid()
arrow.fill.fore_color.rgb = COLORS['primary']
arrow.line.fill.background()

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.6),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.58), Inches(10.3), Inches(0.45),
         "结构体 = 数据封装：把相关数据绑在一起，从'散落纸条'到'完整名片'",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第4页：结构体定义与使用
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "结构体定义与使用", "struct 自定义类型，把相关数据绑在一起")

# 左侧 - 语法图示
left_x = Inches(0.6)

syntax_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.5), Inches(4.3),
                                COLORS['white'], COLORS['blue'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.5), Inches(0.5), COLORS['blue'])
add_text(slide, left_x, Inches(1.85), Inches(5.5), Inches(0.4),
         "结构体定义语法", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 语法标注
parts = [
    ("struct", "关键字", COLORS['green']),
    ("Account", "标签名", COLORS['primary']),
    ("{ ... }", "成员列表", COLORS['purple']),
]
for i, (code, label, color) in enumerate(parts):
    px = left_x + Inches(0.3 + i * 1.7)
    py = Inches(2.5)
    box = add_rounded_rect(slide, px, py, Inches(1.5), Inches(0.7), color, color, 0.2)
    add_text(slide, px, py + Inches(0.05), Inches(1.5), Inches(0.35),
             code, font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, px, py + Inches(0.4), Inches(1.5), Inches(0.3),
             label, font_size=10, color=COLORS['white'], align=PP_ALIGN.CENTER)

# 代码示例
code_lines = [
    ('struct Account {', COLORS['blue']),
    ('    int    id;        // 账户ID', COLORS['green']),
    ('    char   name[20];  // 账户姓名', COLORS['primary']),
    ('    double balance;   // 账户余额', COLORS['purple']),
    ('};', COLORS['blue']),
    ('', COLORS['text']),
    ('// 声明并初始化', COLORS['text_light']),
    ('Account acc = {1001, "张三", 1000.0};', COLORS['green']),
]
for i, (code, color) in enumerate(code_lines):
    add_text(slide, left_x + Inches(0.3), Inches(3.4 + i * 0.32), Inches(5.0), Inches(0.3),
             code, font_size=12, color=color, font_name='Consolas')

# 右侧 - 初始化方式
right_x = Inches(6.5)

init_methods = [
    ("完全初始化", "{1001, \"张三\", 1000.0}", COLORS['green'], "按成员顺序赋值"),
    ("部分初始化", "{1002}", COLORS['yellow'], "只给前几个，其余补0"),
    ("指定初始化", "{.id=1003, .balance=500}", COLORS['purple'], "按成员名赋值（C99）"),
    ("先声明后赋值", "acc.id=1004; strcpy(...)", COLORS['accent'], "逐个成员赋值"),
]

for i, (name, code, color, desc) in enumerate(init_methods):
    x = Inches(6.5 + (i % 2) * 3.3)
    y = Inches(1.8 + (i // 2) * 2.1)
    card = add_rounded_rect(slide, x, y, Inches(3.0), Inches(1.9),
                            COLORS['white'], color, 0.12)
    top_bar = add_shape(slide, MSO_SHAPE.RECTANGLE, x, y, Inches(3.0), Inches(0.08), color)

    add_text(slide, x, y + Inches(0.15), Inches(3.0), Inches(0.4),
             name, font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    add_text(slide, x + Inches(0.1), y + Inches(0.65), Inches(2.8), Inches(0.5),
             code, font_size=10, color=color, bold=True, align=PP_ALIGN.CENTER, font_name='Consolas')

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.8), y + Inches(1.2), Inches(1.4), Inches(0.03))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.1), y + Inches(1.3), Inches(2.8), Inches(0.4),
             desc, font_size=10, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部提示
tip = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.55),
                        COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(1.5), Inches(6.57), Inches(10.3), Inches(0.4),
         "结构体定义只是'图纸'，不占内存；声明变量时才分配内存",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第5页：成员访问（. 和 ->）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "成员访问：. 和 -> 的区别", "变量用点，指针用箭头")

# 上半部分 - 两种方式对比
left_x = Inches(0.6)

# 左侧 - 点号 .
dot_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.8), Inches(3.5),
                             COLORS['white'], COLORS['green'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.8), Inches(0.5), COLORS['green'])
add_text(slide, left_x, Inches(1.85), Inches(5.8), Inches(0.4),
         "点号 . —— 变量访问成员", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

dot_lines = [
    ('Account acc = {1001, "张三", 1000.0};', COLORS['text_light']),
    ('', COLORS['text']),
    ('acc.id        // 1001', COLORS['green']),
    ('acc.name      // "张三"', COLORS['green']),
    ('acc.balance   // 1000.0', COLORS['green']),
    ('', COLORS['text']),
    ('acc.balance += 500;  // 修改成员', COLORS['primary']),
]
for i, (code, color) in enumerate(dot_lines):
    add_text(slide, left_x + Inches(0.3), Inches(2.5 + i * 0.35), Inches(5.2), Inches(0.3),
             code, font_size=12, color=color, font_name='Consolas')

# 右侧 - 箭头 ->
right_x = Inches(6.9)
arrow_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(5.8), Inches(3.5),
                               COLORS['white'], COLORS['purple'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(5.8), Inches(0.5), COLORS['purple'])
add_text(slide, right_x, Inches(1.85), Inches(5.8), Inches(0.4),
         "箭头 -> —— 指针访问成员", font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

arrow_lines = [
    ('Account* p = &acc;  // p 是指针', COLORS['text_light']),
    ('', COLORS['text']),
    ('p->id        // 等价于 (*p).id', COLORS['purple']),
    ('p->name      // 等价于 (*p).name', COLORS['purple']),
    ('p->balance   // 等价于 (*p).balance', COLORS['purple']),
    ('', COLORS['text']),
    ('p->balance += 500;  // 通过指针修改', COLORS['primary']),
]
for i, (code, color) in enumerate(arrow_lines):
    add_text(slide, right_x + Inches(0.3), Inches(2.5 + i * 0.35), Inches(5.2), Inches(0.3),
             code, font_size=12, color=color, font_name='Consolas')

# 下半部分 - 记忆口诀和对比表
tip = add_rounded_rect(slide, Inches(1.0), Inches(5.6), Inches(11.3), Inches(0.8),
                       COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.0), Inches(5.65), Inches(11.3), Inches(0.35),
         "记忆口诀：变量用点（.），指针用箭头（->）",
         font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.0), Inches(6.0), Inches(11.3), Inches(0.35),
         "p->id 完全等价于 (*p).id，-> 是 (*p). 的语法糖（简写）",
         font_size=13, color=COLORS['text'], align=PP_ALIGN.CENTER)

# 错误示例
err_card = add_rounded_rect(slide, Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.6),
                             COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(1.0), Inches(6.55), Inches(11.3), Inches(0.5),
         "常见错误：acc->id（错！acc是变量不是指针）  p.id（错！p是指针不是结构体）  *p.id（错！. 优先级高于 *）",
         font_size=12, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第6页：结构体指针
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "结构体指针（衔接第5讲）", "一个指针遍历所有信息——对比第6讲的三个指针")

# 左侧 - 第6讲：三个指针
left_x = Inches(0.6)

old_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.5), Inches(4.3),
                             COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.5), Inches(0.5), COLORS['accent'])
add_text(slide, left_x, Inches(1.85), Inches(5.5), Inches(0.4),
         "第6讲：三个指针同步递增", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

old_lines = [
    ('int    *pid  = account_ids;', COLORS['accent']),
    ('char   (*pn)[20] = names;', COLORS['accent']),
    ('double *pbal = balances;', COLORS['accent']),
    ('', COLORS['text']),
    ('for (i = 0; i < 5; i++) {', COLORS['blue']),
    ('    printf("%d %s %.2f",', COLORS['green']),
    ('        *pid, *pn, *pbal);', COLORS['green']),
    ('    pid++;  pn++;  pbal++;', COLORS['primary']),
    ('    // 三个指针要同步递增！', COLORS['accent']),
    ('}', COLORS['blue']),
]
for i, (code, color) in enumerate(old_lines):
    add_text(slide, left_x + Inches(0.3), Inches(2.5 + i * 0.35), Inches(5.0), Inches(0.3),
             code, font_size=11, color=color, font_name='Consolas')

# 右侧 - 第7讲：一个指针
right_x = Inches(6.5)

new_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(6.2), Inches(4.3),
                             COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(6.2), Inches(0.5), COLORS['secondary'])
add_text(slide, right_x, Inches(1.85), Inches(6.2), Inches(0.4),
         "第7讲：一个结构体指针搞定", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

new_lines = [
    ('Account *p = accounts;', COLORS['secondary']),
    ('', COLORS['text']),
    ('for (i = 0; i < 5; i++) {', COLORS['blue']),
    ('    printf("%d %s %.2f",', COLORS['green']),
    ('        p->id, p->name, p->balance);', COLORS['green']),
    ('    p++;  // 一个指针递增即可！', COLORS['primary']),
    ('}', COLORS['blue']),
    ('', COLORS['text']),
    ('// p->id   等价于 (*p).id', COLORS['text_light']),
    ('// p++ 步长 = sizeof(Account)', COLORS['text_light']),
]
for i, (code, color) in enumerate(new_lines):
    add_text(slide, right_x + Inches(0.3), Inches(2.5 + i * 0.35), Inches(5.7), Inches(0.3),
             code, font_size=11, color=color, font_name='Consolas')

# 底部对比金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.6),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.58), Inches(10.3), Inches(0.45),
         "第6讲三个指针容易出错，第7讲一个指针信息完整——结构体的威力",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第7页：结构体作为函数参数
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "结构体作函数参数：值传递 vs 指针传递", "什么时候传值？什么时候传指针？")

# 左侧 - 值传递
left_x = Inches(0.6)

val_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.8), Inches(4.3),
                             COLORS['white'], COLORS['green'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.8), Inches(0.5), COLORS['green'])
add_text(slide, left_x, Inches(1.85), Inches(5.8), Inches(0.4),
         "值传递（复制整个结构体）", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

val_lines = [
    ('void print(Account acc) {', COLORS['green']),
    ('    printf("%d", acc.id);', COLORS['blue']),
    ('    acc.balance = 0;  // 改副本', COLORS['accent']),
    ('}', COLORS['green']),
    ('', COLORS['text']),
    ('// 调用：传整个结构体', COLORS['text_light']),
    ('print(accounts[0]);', COLORS['green']),
    ('// accounts[0] 不受影响', COLORS['text_light']),
]
for i, (code, color) in enumerate(val_lines):
    add_text(slide, left_x + Inches(0.3), Inches(2.5 + i * 0.35), Inches(5.2), Inches(0.3),
             code, font_size=12, color=color, font_name='Consolas')

# 值传递特点
val_points = [
    ("安全", "修改不影响原数据"),
    ("浪费", "复制所有成员，大结构体开销大"),
]
for i, (name, desc) in enumerate(val_points):
    py = Inches(5.2 + i * 0.4)
    icon_color = COLORS['green'] if name == "安全" else COLORS['accent']
    add_text(slide, left_x + Inches(0.3), py, Inches(1.0), Inches(0.3),
             name, font_size=12, color=icon_color, bold=True)
    add_text(slide, left_x + Inches(1.3), py, Inches(4.0), Inches(0.3),
             desc, font_size=11, color=COLORS['text_light'])

# 右侧 - 指针传递
right_x = Inches(6.9)

ptr_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(5.8), Inches(4.3),
                             COLORS['white'], COLORS['purple'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(5.8), Inches(0.5), COLORS['purple'])
add_text(slide, right_x, Inches(1.85), Inches(5.8), Inches(0.4),
         "指针传递（只传地址）", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

ptr_lines = [
    ('void deposit(Account* p, double amt) {', COLORS['purple']),
    ('    p->balance += amt;  // 改原数据', COLORS['green']),
    ('}', COLORS['purple']),
    ('', COLORS['text']),
    ('// 只读模式：const 保护', COLORS['text_light']),
    ('void print(const Account* p) {', COLORS['blue']),
    ('    // p->balance=0; // 编译报错!', COLORS['accent']),
    ('}', COLORS['blue']),
]
for i, (code, color) in enumerate(ptr_lines):
    add_text(slide, right_x + Inches(0.3), Inches(2.5 + i * 0.35), Inches(5.2), Inches(0.3),
             code, font_size=12, color=color, font_name='Consolas')

# 指针传递特点
ptr_points = [
    ("高效", "只传地址（4/8字节），不复制数据"),
    ("能改", "通过指针直接修改原数据"),
]
for i, (name, desc) in enumerate(ptr_points):
    py = Inches(5.2 + i * 0.4)
    icon_color = COLORS['green']
    add_text(slide, right_x + Inches(0.3), py, Inches(1.0), Inches(0.3),
             name, font_size=12, color=icon_color, bold=True)
    add_text(slide, right_x + Inches(1.3), py, Inches(4.0), Inches(0.3),
             desc, font_size=11, color=COLORS['text_light'])

# 底部选择原则
gold = add_rounded_rect(slide, Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.6),
                        COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.45),
         "选择原则：只读小结构体→值传递；大结构体或需修改→指针传递（加const保护只读）",
         font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第8页：typedef 类型重定义
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "typedef 类型重定义", "给类型起'短名字'，代码更简洁")

# 上半部分 - 对比有无 typedef
left_x = Inches(0.6)

# 没有 typedef
no_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.8), Inches(2.3),
                            COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.8), Inches(0.5), COLORS['accent'])
add_text(slide, left_x, Inches(1.85), Inches(5.8), Inches(0.4),
         "没有 typedef（繁琐）", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

no_lines = [
    ('struct Account acc1;           // 每次都要写 struct', COLORS['accent']),
    ('struct Account arr[5];         // 声明数组也要加', COLORS['accent']),
    ('void func(struct Account* p);  // 函数参数也要加', COLORS['accent']),
]
for i, (code, color) in enumerate(no_lines):
    add_text(slide, left_x + Inches(0.3), Inches(2.5 + i * 0.4), Inches(5.2), Inches(0.3),
             code, font_size=11, color=color, font_name='Consolas')

# 有 typedef
right_x = Inches(6.9)
yes_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(5.8), Inches(2.3),
                             COLORS['white'], COLORS['green'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(5.8), Inches(0.5), COLORS['green'])
add_text(slide, right_x, Inches(1.85), Inches(5.8), Inches(0.4),
         "有 typedef（简洁）", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

yes_lines = [
    ('typedef struct Account Account;  // 起短名', COLORS['green']),
    ('Account acc1;           // 不用加 struct 了！', COLORS['green']),
    ('Account arr[5];         // 声明数组也简洁', COLORS['green']),
    ('void func(Account* p);  // 函数参数也简洁', COLORS['green']),
]
for i, (code, color) in enumerate(yes_lines):
    add_text(slide, right_x + Inches(0.3), Inches(2.5 + i * 0.4), Inches(5.2), Inches(0.3),
             code, font_size=11, color=color, font_name='Consolas')

# 下半部分 - 用法示例
usage_card = add_rounded_rect(slide, Inches(0.6), Inches(4.4), Inches(12.1), Inches(2.0),
                               COLORS['white'], COLORS['blue'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(4.4), Inches(12.1), Inches(0.45), COLORS['blue'])
add_text(slide, Inches(0.6), Inches(4.45), Inches(12.1), Inches(0.35),
         "三种用法 + 重要提示", font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

usage_lines = [
    ('// 用法1：先 struct 再 typedef', COLORS['text_light']),
    ('typedef struct Account Account;              // 先定义结构体，再起别名', COLORS['blue']),
    ('// 用法2：定义同时 typedef（不能自引用，链表用法1）', COLORS['text_light']),
    ('typedef struct { int id; char name[20]; double balance; } Account;', COLORS['purple']),
    ('// 用法3：给基本类型起别名（提高可读性）', COLORS['text_light']),
    ('typedef double Money;   typedef int AccountId;     // Money/AccountId 就是 double/int', COLORS['green']),
]
for i, (code, color) in enumerate(usage_lines):
    add_text(slide, Inches(0.9), Inches(5.0 + i * 0.25), Inches(11.5), Inches(0.22),
             code, font_size=10, color=color, font_name='Consolas')

# 底部提示
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.5), Inches(10.3), Inches(0.55),
                        COLORS['secondary'], COLORS['secondary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.57), Inches(10.3), Inches(0.4),
         "typedef 不创建新类型，只是给已有类型起别名——人还是那个人，名字短了",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第9页：结构体数组
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "结构体数组", "一盒名片 = 一个结构体数组，替代平行数组")

# 上半部分 - 代码对比
left_x = Inches(0.6)

# 第6讲平行数组
old_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.5), Inches(2.5),
                             COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.5), Inches(0.45), COLORS['accent'])
add_text(slide, left_x, Inches(1.85), Inches(5.5), Inches(0.35),
         "第6讲：平行数组（3个数组）", font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

old_code = [
    ('int    ids[5]       = {1001, 1002, ...};', COLORS['accent']),
    ('char   names[5][20] = {"张三", "李四", ...};', COLORS['accent']),
    ('double bals[5]      = {1000, 2000, ...};', COLORS['accent']),
    ('// 改一个要同步改三个！', COLORS['text_light']),
]
for i, (code, color) in enumerate(old_code):
    add_text(slide, left_x + Inches(0.3), Inches(2.4 + i * 0.38), Inches(5.0), Inches(0.32),
             code, font_size=11, color=color, font_name='Consolas')

# 第7讲结构体数组
right_x = Inches(6.5)
new_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(6.2), Inches(2.5),
                             COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(6.2), Inches(0.45), COLORS['secondary'])
add_text(slide, right_x, Inches(1.85), Inches(6.2), Inches(0.35),
         "第7讲：结构体数组（1个数组）", font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

new_code = [
    ('Account accounts[5] = {', COLORS['secondary']),
    ('    {1001, "张三", 1000.0},  // 第0个账户完整信息', COLORS['green']),
    ('    {1002, "李四", 2000.0},  // 第1个', COLORS['green']),
    ('    // ...', COLORS['text_light']),
    ('};', COLORS['secondary']),
]
for i, (code, color) in enumerate(new_code):
    add_text(slide, right_x + Inches(0.3), Inches(2.4 + i * 0.38), Inches(5.7), Inches(0.32),
             code, font_size=11, color=color, font_name='Consolas')

# 下半部分 - 对比表
table_y = Inches(4.6)
diffs = [
    ("对比项", "平行数组", "结构体数组", COLORS['dark']),
    ("定义", "3个独立数组", "1个结构体数组", COLORS['primary']),
    ("加字段", "再加一个数组", "加一个成员", COLORS['green']),
    ("删除元素", "3个数组同步删", "删一个结构体", COLORS['purple']),
    ("函数参数", "3个数组+长度", "结构体指针+长度", COLORS['accent']),
]

for i, (item, arr_val, struct_val, color) in enumerate(diffs):
    y = table_y + Inches(i * 0.38)
    is_header = (i == 0)
    bg_color = COLORS['light'] if not is_header else color
    txt_color = COLORS['white'] if is_header else COLORS['text']

    cell1 = add_rounded_rect(slide, Inches(1.5), y, Inches(2.5), Inches(0.35), bg_color, color, 0.1)
    add_text(slide, Inches(1.5), y + Inches(0.03), Inches(2.5), Inches(0.29),
             item, font_size=12, color=txt_color, bold=is_header, align=PP_ALIGN.CENTER)
    cell2 = add_rounded_rect(slide, Inches(4.1), y, Inches(4.0), Inches(0.35), bg_color, color, 0.1)
    add_text(slide, Inches(4.1), y + Inches(0.03), Inches(4.0), Inches(0.29),
             arr_val, font_size=11, color=txt_color, bold=is_header, align=PP_ALIGN.CENTER)
    cell3 = add_rounded_rect(slide, Inches(8.2), y, Inches(3.8), Inches(0.35), bg_color, color, 0.1)
    add_text(slide, Inches(8.2), y + Inches(0.03), Inches(3.8), Inches(0.29),
             struct_val, font_size=11, color=txt_color, bold=is_header, align=PP_ALIGN.CENTER)

# 底部金句
gold = add_rounded_rect(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.45),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.5), Inches(6.75), Inches(10.3), Inches(0.35),
         "结构体数组 = 把平行数组的信息合并，一个数组管理所有账户",
         font_size=14, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第10页：ATM 结构体实战
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "ATM 结构体实战", "从平行数组到数据封装的完整演进")

# 左侧 - 账户结构体
left_x = Inches(0.6)

acct_card = add_rounded_rect(slide, left_x, Inches(1.8), Inches(5.0), Inches(4.5),
                              COLORS['white'], COLORS['secondary'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, left_x, Inches(1.8), Inches(5.0), Inches(0.5), COLORS['secondary'])
add_text(slide, left_x, Inches(1.85), Inches(5.0), Inches(0.4),
         "Account 结构体（名片）", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

acct_members = [
    ("int", "id = 1001", COLORS['green']),
    ("char[20]", "name = \"张三\"", COLORS['primary']),
    ("double", "balance = 1000.0", COLORS['purple']),
]
draw_struct_box(slide, left_x + Inches(0.3), Inches(2.5), Inches(4.4), Inches(1.8),
               "struct Account", acct_members, COLORS['secondary'])

# 结构体数组展示
add_text(slide, left_x + Inches(0.3), Inches(4.5), Inches(4.4), Inches(0.35),
         "Account accounts[5]：", font_size=13, color=COLORS['text'], bold=True)

acct_data = [
    ("张三", "1000", COLORS['primary']),
    ("李四", "2000", COLORS['secondary']),
    ("王五", "500", COLORS['yellow']),
    ("赵六", "3000", COLORS['purple']),
    ("钱七", "1500", COLORS['green']),
]
for i, (name, bal, color) in enumerate(acct_data):
    y = Inches(4.9 + i * 0.25)
    row = add_rounded_rect(slide, left_x + Inches(0.5), y, Inches(4.0), Inches(0.22), COLORS['light'], color, 0.1)
    add_text(slide, left_x + Inches(0.6), y, Inches(1.5), Inches(0.22),
             f"[{i}] {name}", font_size=10, color=COLORS['dark'], bold=True)
    add_text(slide, left_x + Inches(2.5), y, Inches(1.8), Inches(0.22),
             f"余额: {bal}", font_size=10, color=color, bold=True, align=PP_ALIGN.RIGHT)

# 右侧 - 核心操作对比
right_x = Inches(6.0)

ops_card = add_rounded_rect(slide, right_x, Inches(1.8), Inches(6.7), Inches(4.5),
                             COLORS['white'], COLORS['accent'], 0.08)
top_c = add_shape(slide, MSO_SHAPE.RECTANGLE, right_x, Inches(1.8), Inches(6.7), Inches(0.5), COLORS['accent'])
add_text(slide, right_x, Inches(1.85), Inches(6.7), Inches(0.4),
         "核心操作：第6讲 vs 第7讲", font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

ops = [
    ("查询余额", "bals[i]", "accounts[i].balance"),
    ("存款", "bals[i] += amt", "accounts[i].balance += amt"),
    ("遍历账户", "*pid++; *pbal++", "p->id; p++; (一个指针)"),
    ("记录交易", "trans_amt[slot]=amt;\ntrans_type[slot]=t;", "strcpy(t[slot].type,...);\nt[slot].amount=amt;"),
    ("对方账户", "（没有此功能）", "t[slot].target_account=id"),
]

for i, (op, old, new) in enumerate(ops):
    y = Inches(2.5 + i * 0.75)
    # 操作名
    add_text(slide, right_x + Inches(0.2), y, Inches(1.2), Inches(0.3),
             op, font_size=12, color=COLORS['dark'], bold=True)
    # 旧代码
    add_text(slide, right_x + Inches(1.4), y, Inches(2.5), Inches(0.65),
             old, font_size=9, color=COLORS['accent'], font_name='Consolas')
    # 箭头
    add_text(slide, right_x + Inches(3.8), y + Inches(0.02), Inches(0.3), Inches(0.3),
             "->", font_size=14, color=COLORS['text_light'], bold=True, align=PP_ALIGN.CENTER)
    # 新代码
    add_text(slide, right_x + Inches(4.1), y, Inches(2.5), Inches(0.65),
             new, font_size=9, color=COLORS['green'], font_name='Consolas')

# 底部金句
gold = add_rounded_rect(slide, Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.6),
                        COLORS['primary'], COLORS['primary'], 0.3)
add_text(slide, Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.45),
         "从'三个平行数组'到'一个结构体数组'——数据封装让代码更清晰、更安全、更易扩展",
         font_size=15, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# 第11页：思考题
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "思考题 · 往深了想", "没有标准答案，重要的是思考过程")

questions = [
    ("结构体大小\n= 成员之和?", "sizeof(struct)\n真的等于\n4+20+8=32吗？\n内存对齐是什么？", COLORS['primary'], Inches(0.6), Inches(2.0)),
    ("浅拷贝\n还是深拷贝?", "结构体赋值时\n指针成员只复制\n地址还是数据？\n会有什么问题？", COLORS['purple'], Inches(3.85), Inches(2.0)),
    (". 和 ->\n有什么区别?", "变量用点\n指针用箭头\n*p.id 为什么错？\n语法糖是什么？", COLORS['secondary'], Inches(7.1), Inches(2.0)),
    ("结构体\n= 类吗?", "结构体有什么\n类有什么？\n能用结构体模拟\n面向对象吗？", COLORS['accent'], Inches(10.35), Inches(2.0)),
]

for title, desc, color, x, y in questions:
    card = add_rounded_rect(slide, x, y, Inches(2.8), Inches(3.8), COLORS['white'], color, 0.1)

    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.8), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = color
    top_bar.line.fill.background()

    # 图标圆
    add_circle(slide, x + Inches(1.0), y + Inches(0.3), Inches(0.8), color)
    add_text(slide, x + Inches(1.0), y + Inches(0.35), Inches(0.8), Inches(0.7),
             "?", font_size=36, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

    add_text(slide, x + Inches(0.15), y + Inches(1.3), Inches(2.5), Inches(0.8),
             title, font_size=15, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.8), y + Inches(2.15), Inches(1.2), Inches(0.04))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.15), y + Inches(2.35), Inches(2.5), Inches(1.2),
             desc, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部鼓励
encourage = add_rounded_rect(slide, Inches(1.5), Inches(6.2), Inches(10.3), Inches(0.9),
                             COLORS['yellow'], COLORS['yellow'], 0.3)
add_text(slide, Inches(1.5), Inches(6.3), Inches(10.3), Inches(0.4),
         "结构体是从'平行数组'到'数据封装'的关键一步。",
         font_size=16, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.35),
         "带着这些问题学习下一讲——链表和接口抽象，你会理解得更深刻！",
         font_size=13, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# ============================================================
# 第12页：小结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "小结", "结构体——把相关数据打包到一起")

# 金句
gold_card = add_rounded_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.1),
                             COLORS['primary'], COLORS['primary'], 0.08)
add_text(slide, Inches(1.5), Inches(1.9), Inches(10.3), Inches(0.4),
         "一句话总结", font_size=15, color=COLORS['yellow'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(2.25), Inches(10.3), Inches(0.6),
         "结构体是把相关数据打包到一起的自定义类型——\n从'散落的平行数组'到'封装的名片'，为面向对象打下基础。",
         font_size=16, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

# 5个知识点
points = [
    ("1", "结构体定义", "struct 自定义类型\n把相关数据\n绑在一起", COLORS['blue']),
    ("2", "成员访问", "变量用点(.)\n指针用箭头(->)\n-> 等价于 (*p).", COLORS['green']),
    ("3", "结构体指针", "衔接第5讲\n一个指针遍历\n所有信息", COLORS['purple']),
    ("4", "值传递vs\n指针传递", "值传递安全\n指针传递高效\nconst保护只读", COLORS['yellow']),
    ("5", "typedef", "给类型起短名\n代码更简洁\n不创建新类型", COLORS['accent']),
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

    # 数字圆
    add_circle(slide, x + Inches(0.8), y + Inches(0.2), Inches(0.75), color)
    add_text(slide, x + Inches(0.8), y + Inches(0.25), Inches(0.75), Inches(0.65),
             num, font_size=28, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)

    add_text(slide, x, y + Inches(1.05), Inches(2.35), Inches(0.45),
             title, font_size=14, color=COLORS['dark'], bold=True, align=PP_ALIGN.CENTER)

    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.8), y + Inches(1.55), Inches(0.75), Inches(0.04))
    divider.fill.solid()
    divider.fill.fore_color.rgb = color
    divider.line.fill.background()

    add_text(slide, x + Inches(0.15), y + Inches(1.7), Inches(2.05), Inches(0.75),
             desc, font_size=11, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

# 底部预告
next_card = add_rounded_rect(slide, Inches(1.5), Inches(6.2), Inches(10.3), Inches(0.85),
                             COLORS['accent'], COLORS['accent'], 0.3)
add_text(slide, Inches(1.5), Inches(6.3), Inches(10.3), Inches(0.4),
         "下一讲：链表 —— 结构体 + 指针 = 动态数据结构，打破固定大小的局限！",
         font_size=18, color=COLORS['white'], bold=True, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.35),
         "再后续：接口抽象 —— 数据 + 行为绑在一起，面向对象编程的正式起步",
         font_size=13, color=COLORS['yellow'], align=PP_ALIGN.CENTER)

# 保存
output_path = r"e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\07_结构体\docs\课件.pptx"
prs.save(output_path)
print(f"PPT生成完成：{output_path}")
print(f"共 {len(prs.slides)} 页")
