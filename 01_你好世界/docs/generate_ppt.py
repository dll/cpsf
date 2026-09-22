"""
第1阶段：你好世界 - PPT课件生成脚本
基于 python-pptx 生成图文并茂的教学课件
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

# ==========================================
# 配色方案（亮色版）
# ==========================================
COLORS = {
    'primary': RGBColor(0x2C, 0x5F, 0x8B),    # 主色：深蓝（概念）
    'secondary': RGBColor(0x2E, 0xCC, 0xFA),   # 辅助色：青（流程）
    'accent': RGBColor(0x9C, 0x27, 0xB0),      # 强调色：紫（案例）
    'highlight': RGBColor(0xFF, 0xA0, 0x00),   # 重点色：金（重点）
    'bg_light': RGBColor(0xF5, 0xF7, 0xFA),    # 浅色背景
    'bg_dark': RGBColor(0x1A, 0x23, 0x32),     # 深色背景
    'text_dark': RGBColor(0x33, 0x33, 0x33),   # 深色文字
    'text_light': RGBColor(0xFF, 0xFF, 0xFF),  # 浅色文字
    'text_gray': RGBColor(0x66, 0x66, 0x66),   # 灰色文字
    'success': RGBColor(0x4C, 0xAF, 0x50),     # 成功绿
}

# 字体设置
FONT_TITLE = '微软雅黑'
FONT_BODY = '微软雅黑'
FONT_CODE = 'Consolas'


def set_slide_bg(slide, color):
    """设置幻灯片背景色"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=18,
                font_name=FONT_BODY, color=COLORS['text_dark'],
                bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """添加文本框"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor

    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.name = font_name
    run.font.color.rgb = color
    run.font.bold = bold

    return txBox


def add_rounded_rect(slide, left, top, width, height, fill_color, line_color=None):
    """添加圆角矩形"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape


def add_card(slide, left, top, width, height, title, content,
             title_color=COLORS['primary']):
    """添加卡片式布局"""
    # 卡片背景
    card = add_rounded_rect(slide, left, top, width, height,
                            RGBColor(0xFF, 0xFF, 0xFF),
                            RGBColor(0xE0, 0xE0, 0xE0))
    card.shadow.inherit = False

    # 顶部色条
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, Emu(50800)  # ~4pt
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = title_color
    bar.line.fill.background()

    # 标题
    add_textbox(slide, left + Inches(0.3), top + Inches(0.2),
                width - Inches(0.6), Inches(0.5),
                title, font_size=16, bold=True, color=title_color)

    # 内容
    add_textbox(slide, left + Inches(0.3), top + Inches(0.7),
                width - Inches(0.6), height - Inches(0.9),
                content, font_size=14, color=COLORS['text_dark'])


def add_code_block(slide, left, top, width, height, code_text):
    """添加代码块"""
    # 背景
    bg = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x1E, 0x1E, 0x1E)
    bg.line.fill.background()

    # 代码文本
    txBox = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15),
                                     width - Inches(0.4), height - Inches(0.3))
    tf = txBox.text_frame
    tf.word_wrap = True

    lines = code_text.strip().split('\n')
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = line
        run.font.size = Pt(13)
        run.font.name = FONT_CODE
        run.font.color.rgb = RGBColor(0xD4, 0xD4, 0xD4)


def add_table(slide, left, top, width, height, data, header_color=COLORS['primary']):
    """添加表格"""
    rows = len(data)
    cols = len(data[0])

    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    for i in range(rows):
        for j in range(cols):
            cell = table.cell(i, j)
            cell.text = str(data[i][j])

            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = FONT_BODY
                    run.font.size = Pt(13)
                    if i == 0:
                        run.font.bold = True
                        run.font.color.rgb = COLORS['text_light']
                    else:
                        run.font.color.rgb = COLORS['text_dark']

            if i == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
            elif i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xF8, 0xF9, 0xFA)

    return table


def add_arrow(slide, left, top, width, height, color=COLORS['secondary']):
    """添加向下箭头"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def create_ppt():
    """生成PPT"""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ==========================================
    # 第1页：封面
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白
    set_slide_bg(slide, COLORS['bg_dark'])

    # 装饰线条
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1), Inches(2.8), Inches(0.1), Inches(2)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = COLORS['highlight']
    line.line.fill.background()

    # 主标题
    add_textbox(slide, Inches(1.5), Inches(2.5), Inches(10), Inches(1.2),
                '第1讲：你好世界', font_size=48, bold=True,
                color=COLORS['text_light'])

    # 副标题
    add_textbox(slide, Inches(1.5), Inches(3.7), Inches(10), Inches(0.8),
                '一切从一行代码开始', font_size=24,
                color=COLORS['secondary'])

    # 系列名称
    add_textbox(slide, Inches(1.5), Inches(5), Inches(10), Inches(0.6),
                '从程序员到软件框架 —— C语言插件框架演进之旅', font_size=16,
                color=COLORS['text_gray'])

    # 阶段标识
    add_textbox(slide, Inches(10.5), Inches(6.2), Inches(2), Inches(0.5),
                '01 / 10', font_size=20, bold=True,
                color=COLORS['highlight'], align=PP_ALIGN.RIGHT)

    # ==========================================
    # 第2页：导入 - 为什么从 Hello World 开始
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    # 标题栏
    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['primary'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '🤔 导入：为什么从 Hello World 开始？', font_size=24, bold=True,
                color=COLORS['text_light'])

    # 左：传统
    add_card(slide, Inches(0.8), Inches(1.6), Inches(5.5), Inches(2.5),
             '📚 一个经典的传统',
             '几乎每一本编程教材、每一门语言课程，\n第一个程序都是打印 "Hello, World!"。\n\n这个传统起源于 1978 年 K&R 的《C程序设计语言》。\n它是程序员与一门新语言"打招呼"的仪式。',
             title_color=COLORS['primary'])

    # 右：我们的不一样
    add_card(slide, Inches(7), Inches(1.6), Inches(5.5), Inches(2.5),
             '🚀 但我们的 Hello World 不一样',
             '普通的 Hello World 只是入门，\n我们的 Hello World 是起点。\n\n从这一行代码出发，经历 10 次进化，\n最终抵达「插件框架」的彼岸。',
             title_color=COLORS['accent'])

    # 底部问题
    add_rounded_rect(slide, Inches(1.5), Inches(4.8), Inches(10.3), Inches(1.5),
                     COLORS['highlight'])
    add_textbox(slide, Inches(2), Inches(5), Inches(9), Inches(1),
                '💡 思考：这一行代码 printf("Hello, Plugin Framework!") 里，\n    已经藏着软件框架的种子。你能看出来吗？',
                font_size=20, bold=True, color=COLORS['text_dark'])

    # ==========================================
    # 第3页：知识地图
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['primary'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '🗺️ 本讲知识地图', font_size=24, bold=True,
                color=COLORS['text_light'])

    # 知识点卡片
    cards = [
        ('1. C程序结构', '头文件、main函数、\n返回值', COLORS['primary']),
        ('2. 编译四步', '预处理→编译→\n汇编→链接', COLORS['secondary']),
        ('3. 函数调用', 'printf背后的\n接口思想', COLORS['accent']),
        ('4. 进化视角', '框架的种子\n在哪里', COLORS['highlight']),
    ]

    for i, (title, desc, color) in enumerate(cards):
        left = Inches(0.8 + i * 3.1)
        add_card(slide, left, Inches(1.8), Inches(2.8), Inches(2.2),
                 title, desc, title_color=color)
        # 编号
        add_textbox(slide, left + Inches(1), Inches(4.2), Inches(0.8), Inches(0.5),
                    str(i + 1), font_size=28, bold=True,
                    color=color, align=PP_ALIGN.CENTER)

    # 底部：三个三分之一
    add_rounded_rect(slide, Inches(1), Inches(5.5), Inches(11.3), Inches(1.2),
                     RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0xE0, 0xE0, 0xE0))
    add_textbox(slide, Inches(1.3), Inches(5.7), Inches(10.7), Inches(0.4),
                '📖 本讲教学范式：三个三分之一', font_size=16, bold=True,
                color=COLORS['primary'])
    add_textbox(slide, Inches(1.3), Inches(6.1), Inches(10.7), Inches(0.5),
                '前1/3 传统讲授 → 中1/3 AI辅助 → 后1/3 做中学',
                font_size=14, color=COLORS['text_gray'])

    # ==========================================
    # 第4页：C程序基本结构 - 代码全貌
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['primary'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '📝 一、C程序的基本结构', font_size=24, bold=True,
                color=COLORS['text_light'])

    # 左侧代码
    code = '''#include <stdio.h>

int main(void)
{
    printf("Hello, Plugin Framework!\\n");
    return 0;
}'''
    add_code_block(slide, Inches(0.8), Inches(1.6), Inches(6), Inches(4.5), code)

    # 右侧注释
    annotations = [
        ('① 头文件引入', '#include <stdio.h>\n引入标准输入输出库', COLORS['primary']),
        ('② 主函数入口', 'int main(void)\n所有C程序从这里开始', COLORS['secondary']),
        ('③ 函数调用', 'printf("...")\n调用标准库打印字符串', COLORS['accent']),
        ('④ 返回值', 'return 0;\n返回0表示正常结束', COLORS['highlight']),
    ]

    for i, (title, desc, color) in enumerate(annotations):
        top = Inches(1.6 + i * 1.15)
        add_card(slide, Inches(7.2), top, Inches(5.3), Inches(1),
                 title, desc, title_color=color)

    # ==========================================
    # 第5页：编译运行流程
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['secondary'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '⚙️ 编译运行的四个阶段', font_size=24, bold=True,
                color=COLORS['text_light'])

    # 流程图
    stages = [
        ('hello.c', '源代码'),
        ('预处理', '展开宏和头文件'),
        ('编译', '翻译成汇编代码'),
        ('汇编', '生成目标文件'),
        ('hello.exe', '可执行文件'),
    ]

    for i, (title, desc) in enumerate(stages):
        left = Inches(0.5 + i * 2.5)
        color = COLORS['primary'] if i in [0, 4] else COLORS['secondary']

        add_rounded_rect(slide, left, Inches(2.2), Inches(2.2), Inches(1.5),
                         color)
        add_textbox(slide, left, Inches(2.4), Inches(2.2), Inches(0.6),
                    title, font_size=16, bold=True,
                    color=COLORS['text_light'], align=PP_ALIGN.CENTER)
        add_textbox(slide, left + Inches(0.1), Inches(3), Inches(2), Inches(0.6),
                    desc, font_size=12,
                    color=COLORS['text_light'], align=PP_ALIGN.CENTER)

        if i < 4:
            # 箭头
            arrow_left = Inches(0.5 + i * 2.5 + 2.2)
            add_arrow(slide, arrow_left, Inches(2.7), Inches(0.3), Inches(0.5),
                      color=COLORS['highlight'])

    # 关键洞察
    add_rounded_rect(slide, Inches(1), Inches(4.5), Inches(11.3), Inches(2),
                     RGBColor(0xFF, 0xF8, 0xE1), RGBColor(0xFF, 0xA0, 0x00))
    add_textbox(slide, Inches(1.3), Inches(4.7), Inches(10.7), Inches(0.5),
                '🎯 关键洞察', font_size=18, bold=True, color=COLORS['highlight'])
    add_textbox(slide, Inches(1.3), Inches(5.2), Inches(10.7), Inches(1.2),
                '你写的代码里并没有 printf 的实现，但程序却能运行它。\n'
                '这是因为「链接器」把标准库里的 printf 函数和你的代码"拼"在了一起。\n\n'
                '这就是最朴素的"复用"思想——用别人写好的代码，做自己的事情。',
                font_size=14, color=COLORS['text_dark'])

    # ==========================================
    # 第6页：AI辅助 - 编译过程比喻
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['accent'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '🤖 二、AI化辅助：用比喻理解编译', font_size=24, bold=True,
                color=COLORS['text_light'])

    # Prompt 示例
    add_card(slide, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.8),
             '💬 Prompt 示例',
             '"我是一名大三学生，正在学习C语言。请用通俗的语言解释：\n'
             '当我执行 gcc hello.c -o hello.exe 时，预处理、编译、汇编、链接这四个阶段分别做了什么？\n'
             '请用「工厂流水线」的比喻来解释。"',
             title_color=COLORS['accent'])

    # AI输出（分栏）
    ai_outputs = [
        ('预处理 = 洗菜备料', '把 #include 的头文件"抄"进来，\n把宏定义替换掉。', '🥬'),
        ('编译 = 烹饪', '把C代码翻译成汇编语言。\n厨师按照食谱做菜。', '🍳'),
        ('汇编 = 装盘', '把汇编代码翻译成机器码（0和1），\n生成目标文件。', '🍽️'),
        ('链接 = 送上餐桌', '把你的代码和 printf 等库函数"拼"在一起，\n生成完整的可执行文件。', '🍱'),
    ]

    for i, (title, desc, emoji) in enumerate(ai_outputs):
        left = Inches(0.8 + i * 3.05)
        add_card(slide, left, Inches(3.8), Inches(2.85), Inches(2.5),
                 f'{emoji} {title}', desc, title_color=COLORS['secondary'])

    # 底部：核验提示
    add_rounded_rect(slide, Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.6),
                     RGBColor(0xE8, 0xF5, 0xE9), RGBColor(0x4C, 0xAF, 0x50))
    add_textbox(slide, Inches(1.1), Inches(6.65), Inches(11), Inches(0.5),
                '✅ 核验练习：用 gcc -E hello.c -o hello.i 查看预处理结果，验证 AI 说的对不对',
                font_size=13, bold=True, color=COLORS['success'])

    # ==========================================
    # 第7页：做中学 - 动手实验
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['highlight'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '🛠️ 三、做中学：动手实验', font_size=24, bold=True,
                color=COLORS['text_light'])

    experiments = [
        ('实验1：修改输出', '把字符串改成你的名字，\n重新编译运行。',
         '观察：修改源码→编译→运行\n这个过程你做了几次？', COLORS['primary']),
        ('实验2：制造错误', '删掉 #include <stdio.h>，\n编译看报什么错。',
         '思考：为什么没有 include\n就不能用 printf？', COLORS['secondary']),
        ('实验3：多个printf', '写三行 printf，\n打印三行不同的文字。',
         '观察：执行顺序和代码\n书写顺序一致吗？', COLORS['accent']),
    ]

    for i, (title, task, think, color) in enumerate(experiments):
        left = Inches(0.8 + i * 4.1)
        add_card(slide, left, Inches(1.6), Inches(3.8), Inches(4.5),
                 title, '', title_color=color)

        # 任务
        add_textbox(slide, left + Inches(0.3), Inches(2.4), Inches(3.2), Inches(0.4),
                    '📋 任务：', font_size=14, bold=True, color=color)
        add_textbox(slide, left + Inches(0.3), Inches(2.8), Inches(3.2), Inches(1.2),
                    task, font_size=13, color=COLORS['text_dark'])

        # 分割线
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left + Inches(0.3), Inches(4), Inches(3.2), Emu(12700)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
        line.line.fill.background()

        # 思考
        add_textbox(slide, left + Inches(0.3), Inches(4.2), Inches(3.2), Inches(0.4),
                    '💭 思考：', font_size=14, bold=True, color=color)
        add_textbox(slide, left + Inches(0.3), Inches(4.6), Inches(3.2), Inches(1.2),
                    think, font_size=13, color=COLORS['text_dark'])

    # ==========================================
    # 第8页：进化视角
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['accent'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '🌱 进化视角：本阶段的"种子"', font_size=24, bold=True,
                color=COLORS['text_light'])

    # 种子表格
    data = [
        ['现在的种子', '对应未来的概念', '出现阶段'],
        ['调用别人写好的函数（printf）', '接口 —— 定义"怎么用"，隐藏"怎么实现"', '第7阶段'],
        ['编译器把代码转成可执行文件', '编译与链接 —— 从源码到运行的桥梁', '第4-6阶段'],
        ['标准库提供通用功能', '库 —— 复用的基本单位', '第4-5阶段'],
        ['main函数是固定的入口点', '框架的控制反转 —— 你写的代码被框架调用', '第9阶段'],
    ]
    add_table(slide, Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.5), data,
              header_color=COLORS['accent'])

    # 本阶段痛点
    add_rounded_rect(slide, Inches(0.8), Inches(5.5), Inches(5.5), Inches(1.3),
                     RGBColor(0xFF, 0xEB, 0xEE), RGBColor(0xEF, 0x53, 0x50))
    add_textbox(slide, Inches(1.1), Inches(5.6), Inches(5), Inches(0.4),
                '😫 本阶段的痛点', font_size=16, bold=True,
                color=RGBColor(0xEF, 0x53, 0x50))
    add_textbox(slide, Inches(1.1), Inches(6), Inches(5), Inches(0.7),
                '所有代码都写在一个文件里\n代码多了之后，维护起来会很痛苦',
                font_size=13, color=COLORS['text_dark'])

    # 下一阶段预告
    add_rounded_rect(slide, Inches(7), Inches(5.5), Inches(5.5), Inches(1.3),
                     RGBColor(0xE8, 0xF5, 0xE9), RGBColor(0x4C, 0xAF, 0x50))
    add_textbox(slide, Inches(7.3), Inches(5.6), Inches(5), Inches(0.4),
                '➡️ 下一阶段', font_size=16, bold=True,
                color=COLORS['success'])
    add_textbox(slide, Inches(7.3), Inches(6), Inches(5), Inches(0.7),
                '02_函数封装\n把代码拆分成函数，迈向模块化的第一步',
                font_size=13, color=COLORS['text_dark'])

    # ==========================================
    # 第9页：小结
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['primary'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '📝 本讲小结', font_size=24, bold=True,
                color=COLORS['text_light'])

    summary_data = [
        ['知识点', '要点'],
        ['C程序结构', '头文件 + main函数 + 函数调用 + 返回值'],
        ['编译四步', '预处理 → 编译 → 汇编 → 链接'],
        ['函数调用', '调用者不需要知道实现细节，只需要知道接口'],
        ['进化思想', '每一个技术都是为了解决前一阶段的痛点'],
    ]
    add_table(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(3.5),
              summary_data, header_color=COLORS['primary'])

    # 课后任务
    add_rounded_rect(slide, Inches(1.5), Inches(5.7), Inches(10.3), Inches(1.3),
                     RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0xE0, 0xE0, 0xE0))
    add_textbox(slide, Inches(1.8), Inches(5.8), Inches(9.7), Inches(0.4),
                '📚 课后任务', font_size=16, bold=True, color=COLORS['primary'])
    add_textbox(slide, Inches(1.8), Inches(6.2), Inches(9.7), Inches(0.7),
                '① 必做：完成3个实验，记录过程和观察结果\n'
                '② 选做：用 AI 查 printf 的内部实现，写200字总结\n'
                '③ 预习：100行代码都写在 main 里，会有什么问题？',
                font_size=13, color=COLORS['text_dark'])

    # ==========================================
    # 第10页：思考题预告
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_light'])

    add_rounded_rect(slide, Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.8),
                     COLORS['highlight'])
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(12), Inches(0.6),
                '🤔 思辨思考题（预览）', font_size=24, bold=True,
                color=COLORS['text_light'])

    questions = [
        ('Q1', '编译和运行有什么区别？\n为什么不能直接运行 .c 文件？'),
        ('Q3', 'printf 是一种"接口"吗？\n这和面向对象的封装有什么联系？'),
        ('Q5', '从一行 printf 到插件框架，\n你觉得中间需要解决哪些问题？'),
    ]

    for i, (qnum, qtext) in enumerate(questions):
        left = Inches(0.8 + i * 4.1)
        add_card(slide, left, Inches(1.8), Inches(3.8), Inches(3),
                 qnum, qtext, title_color=COLORS['highlight'])

    # 底部提示
    add_rounded_rect(slide, Inches(2), Inches(5.3), Inches(9.3), Inches(1.2),
                     COLORS['bg_dark'])
    add_textbox(slide, Inches(2.3), Inches(5.5), Inches(8.7), Inches(0.8),
                '完整思考题（共6道）详见「思考题.md」\n'
                '没有标准答案，重在思考过程 💡',
                font_size=16, color=COLORS['text_light'], align=PP_ALIGN.CENTER)

    # ==========================================
    # 第11页：谢谢
    # ==========================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, COLORS['bg_dark'])

    add_textbox(slide, Inches(2), Inches(2.5), Inches(9.3), Inches(1.2),
                '谢谢！', font_size=54, bold=True,
                color=COLORS['text_light'], align=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(2), Inches(3.8), Inches(9.3), Inches(0.8),
                '下一讲：函数封装 —— 迈向模块化的第一步',
                font_size=22, color=COLORS['secondary'], align=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(2), Inches(5.5), Inches(9.3), Inches(0.6),
                '从程序员到软件框架 · 第01讲',
                font_size=14, color=COLORS['text_gray'], align=PP_ALIGN.CENTER)

    # 保存
    output_path = r'e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\01_你好世界\docs\课件.pptx'
    prs.save(output_path)
    print(f'PPT 已生成：{output_path}')
    print(f'共 {len(prs.slides)} 页')


if __name__ == '__main__':
    create_ppt()
