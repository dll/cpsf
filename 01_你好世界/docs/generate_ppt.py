# -*- coding: utf-8 -*-
"""
第1讲：表达式 —— 从一行 printf 到插件框架的第一块砖
generate_ppt.py（新版，18 页）

依赖统一工具箱 tools/ppt_kit.py：
    · 标题单行自适应（R1）——投影时标题绝不换行
    · 容器不叠压、文字不越界、装饰永在底层（R2）——不再"前后不分"
    · 全部正文对比度 ≥ 4.5:1，代码一律深底亮字（R3）——投影看得清
生成后自动质检（audit），有问题直接报错，不产出坏 PPT。

输出：docs/课件.pptx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from ppt_kit import *          # noqa
from ppt_kit import C, page, card, code, bullets, flow, compare, banner, footer_note, \
    demo_frame, kv_rows, text, panel, rect, audit, save, new_deck, blank, MARGIN_L, INNER_W, \
    BODY_TOP, BODY_BOTTOM, SW, MARGIN_R, TITLE_TOP, fit_size, text_width_in, \
    _put_text, _reg_text, _reg_container, _reset_reg

LECTURE = '第1讲 表达式'
prs = new_deck()
PAGES = []


def pg(title, subtitle=None):
    s = page(prs, title, subtitle, label=LECTURE, page_no='auto')
    PAGES.append(s)
    return s


def done(tag=''):
    audit(prs, tag)


def cards_row(s, y, specs, gap=0.22):
    """等宽一行卡片。specs: [{'title':,'body':,'color':,'size':,'min_h':}]，按真实高度推进。"""
    n = len(specs)
    w = (INNER_W - gap * (n - 1)) / n
    bottoms = []
    for i, sp in enumerate(specs):
        b, _ = card(s, MARGIN_L + i * (w + gap), y, w, sp['body'],
                    title=sp.get('title'), color=sp.get('color', 'orange'),
                    size=sp.get('size', 16), min_h=sp.get('min_h', 0.0))
        bottoms.append(b)
    return max(bottoms)


# ============================================================
# P1 封面
# ============================================================
def p01_cover():
    _reset_reg()
    slide = blank(prs)
    rect(slide, 0, 0, SW, SH, fill=C['bg'])
    rect(slide, 0, 0, 4.4, SH, fill=C['card_orange'])          # 左侧暖色带
    rect(slide, 0, 0, 0.16, SH, fill=C['primary'])
    rect(slide, 4.4, 0, SW - 4.4, 0.12, fill=C['primary'])

    _put_text(slide, 0.75, 1.15, 3.3, 0.5, '从程序员到架构师', 20, C['primary_dark'], bold=True)
    _put_text(slide, 0.75, 1.72, 3.3, 0.4, 'C语言插件框架演进之旅', 14, C['ink2'])
    rect(slide, 0.75, 2.30, 0.9, 0.05, fill=C['primary'])

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第1讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.60, 3.4, 0.9,
              '从一行 printf\n到软件体系的插件框架', 15, C['primary_dark'], bold=True)

    t = '表达式'
    _put_text(slide, 5.35, 2.05, 7.4, 1.5, t, 72, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.35, 7.4, 0.6, 'C 语言的灵魂 · 一切的起点', 26, C['primary_dark'])
    rect(slide, 5.35, 4.10, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.35, 7.2, 1.4,
              '一行 printf，五个要素，四个编译阶段，\n'
              '最后变成整个系列 14 讲的起点。\n'
              '看懂它，你就看懂了"代码如何变成软件"。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)


# ============================================================
# P2 知识图谱 · 本讲位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '表达式是整棵知识树最底层的那块砖')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '本讲（第1讲）：表达式  ——  它不是孤立的知识点，而是后面 13 讲全部内容的"地基"。\n'
        '函数调用的形式是表达式，库函数的调用是表达式，插件的注册与执行也是表达式。'),
        title='🎯 本讲定位', color='orange', size=16, min_h=1.05)
    y = y2 + 0.22

    items = [('表达式', '第1讲 · 你在这里'), ('函数', '第3讲'), ('模块', '第4讲'),
             ('库', '第9-10讲'), ('插件', '第11-12讲'), ('框架', '第13-14讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
         colors=('primary', 'blue', 'teal', 'purple', 'pink', 'green'), size=15, h=0.86) + 0.22

    y3, _ = card(s, MARGIN_L, y, INNER_W / 2 - 0.14, (
        '前置：C 语言基础语句\n本讲之后才有函数、模块可言'),
        title='⬅ 前置', color='blue', size=15, min_h=1.0)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, INNER_W / 2 - 0.14, (
        '后续：控制结构（第2讲）\n让程序会判断、会循环'),
        title='➡ 后续', color='teal', size=15, min_h=1.0)
    footer_note(s, '后面 13 讲的所有能力，都是用"表达式"一块块垒起来的')
    done('P2')


# ============================================================
# P3 什么是表达式
# ============================================================
def p03_expr():
    s = pg('什么是表达式？', '能计算出一个值的代码片段，就是表达式')
    y = BODY_TOP
    y = cards_row(s, y, [
        {'title': '算术表达式', 'body': '3 + 5\n算出 8', 'color': 'orange', 'size': 16},
        {'title': '赋值表达式', 'body': 'x = 10\n算出 10（赋完的值）', 'color': 'blue', 'size': 16},
        {'title': '函数调用表达式', 'body': 'printf("Hello")\n算出打印的字符数', 'color': 'teal', 'size': 14},
    ]) + 0.26

    code(s, MARGIN_L, y, INNER_W, [
        'int main(void) {',
        '    int a = 3 + 5;              // 算术表达式：算出 8',
        '    int b = (a = a * 2);        // 赋值表达式：算出 16，b 也是 16',
        '    printf("Hello, ATM!\\n");    // 函数调用表达式：算出 13（打印了 13 个字符）',
        '    return 0;                    // 表达式语句',
        '}',
    ], title='同一行代码里，三种表达式同时在算值', size=13.5)
    y += 6 * 13.5 * 1.42 / 72 + 0.94

    bul = bullets(s, MARGIN_L, y, INNER_W, [
        '关键：表达式有"值"，语句是"做一件事"——C 语言里很多语句本身就是表达式',
        '正因为有值，才能层层嵌套：printf 的返回值可以再喂给别的表达式',
    ], size=15)
    footer_note(s, 'C 语言是"表达式驱动"的语言：几乎一切操作都能算出值')
    done('P3')


# ============================================================
# P4 拆解 printf
# ============================================================
def p04_printf():
    s = pg('拆解一行代码：printf 的五个要素', '看似简单的一行，五个零件缺一不可')
    y = BODY_TOP
    code(s, MARGIN_L, y, INNER_W, [
        'printf("Hello, Plugin Framework!\\n");',
        '  |        |                      |  |',
        '  |        |                      |  ④ 转义字符 \\n：一个字符写成两个，表示换行',
        '  |        |                      ③ 字符串常量：要打印的内容，存在只读数据段',
        '  |        ② 括号：告诉编译器"这是一次函数调用"，不是普通变量',
        '  ① 函数名 printf：告诉编译器"要去调谁"',
    ], title='逐字符拆解', size=13)
    y += 0.40 + 0.36 + 6 * 13 * 1.42 / 72 + 0.26

    cards_row(s, y, [
        {'title': '① 函数名', 'body': 'printf\n链接器找代码的暗号', 'color': 'orange', 'size': 13},
        {'title': '② 括号', 'body': '( )\n表示一次函数调用', 'color': 'blue', 'size': 13},
        {'title': '③ 字符串', 'body': '常量\n存在只读数据段', 'color': 'teal', 'size': 13},
        {'title': '④ 转义', 'body': '\\n\n一个字符写成两个', 'color': 'purple', 'size': 13},
        {'title': '⑤ 分号', 'body': ';\n把表达式变成语句', 'color': 'green', 'size': 13},
    ], gap=0.16)
    footer_note(s, '一行代码 = 五个要素 = 编译器的五道检查')
    done('P4')


# ============================================================
# P5 printf 来自标准库 + 头文件/库文件
# ============================================================
def p05_lib():
    s = pg('printf 从哪里来？—— C 标准库', '头文件是菜单，库文件才是厨房')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '标准库 = 一个巨大的工具箱（libc）。stdio.h 只是这个工具箱的"目录清单"：\n'
        '它写下 printf、scanf 的名字和用法；真正的机器码藏在库文件里。\n'
        '你用 #include <stdio.h> 把清单拿进来，编译器才知道 printf 长什么样。'),
        title='🧰 工具箱比喻', color='orange', size=16, min_h=1.35)
    y = y2 + 0.26

    y = compare(s, MARGIN_L, y, INNER_W,
               '头文件 stdio.h（菜单）', ['只有声明：printf 的名字、参数、返回值', '参与"编译"阶段', '不产生任何机器码'],
               '库文件 libc（厨房）', ['真正的实现：函数机器码放在这里', '参与"链接"阶段', '最终被复制/引用进你的程序'],
               left_color='blue', right_color='teal', size=14) + 0.02
    for i, (t, sub) in enumerate([('声明 vs 实现', '接口与实现分离'), ('编译期 vs 链接期', '两个阶段各管一段'),
                                  ('这就是抽象', '后面所有架构的源头')]):
        w3 = (INNER_W - 0.44) / 3
        card(s, MARGIN_L + i * (w3 + 0.22), y, w3, sub, title=t, color=('blue', 'teal', 'purple')[i],
             size=15, min_h=0.85)
    banner(s, '接口与实现分离 —— 这句话贯穿后面 13 讲')
    done('P5')


# ============================================================
# P6 编译四阶段总览
# ============================================================
def p06_compile():
    s = pg('一行代码怎么跑起来：编译四阶段', '预处理 → 编译 → 汇编 → 链接')
    y = BODY_TOP
    y = flow(s, MARGIN_L, y, INNER_W,
         [('① 预处理', '展开 #include\n处理 #define'), ('② 编译', 'C 代码 → 汇编'),
          ('③ 汇编', '汇编 → 机器码\n(.o 目标文件)'), ('④ 链接', '拼接库函数\n生成可执行文件')],
         colors=('blue', 'teal', 'purple', 'primary'), size=15, h=1.05) + 0.26

    code(s, MARGIN_L, y, INNER_W, [
        '$ gcc -E hello.c -o hello.i     # ① 预处理：stdio.h 的内容被"复制粘贴"进来',
        '$ gcc -S hello.i -o hello.s     # ② 编译：得到汇编代码',
        '$ gcc -c hello.s -o hello.o     # ③ 汇编：得到目标文件（机器码，还不能跑）',
        '$ gcc hello.o -o hello.exe      # ④ 链接：把 printf 的机器码拼进来，终于能跑',
    ], title='四步命令，看得见的编译过程', size=13.5)
    y += 4 * 13.5 * 1.42 / 72 + 0.94

    bul = bullets(s, MARGIN_L, y, INNER_W, [
        '前三个阶段只认识"你写的代码"，第四阶段才开始管"库里的代码"',
        '每个阶段都产出一个中间文件——出错时，看是哪个阶段报的错，就知道该查哪一步',
    ], size=15)
    footer_note(s, '编译只管"你的代码"，链接才负责"把库接上"')
    done('P6')


# ============================================================
# P7 链接 ⭐
# ============================================================
def p07_link():
    s = pg('链接是整条链上最关键的一步 ⭐', '你写了 printf，可 printf 的实现在哪？')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'main.o 里只有一句"我要调用 printf"，并没有 printf 的机器码。\n'
        '链接器拿着这个"欠条"，去标准库里找到 printf 的实现，把两边拼成一个可执行文件。\n'
        '这就是"链接"——把分散的零件组装成一台能转的机器。'),
        title='📮 链接器 = 帮你把信寄出去的人', color='orange', size=16, min_h=1.35)
    y = y2 + 0.24

    w = (INNER_W - 1.8) / 3
    b1, _ = card(s, MARGIN_L, y, w, 'main.o\n\nmain()\n调用 printf → 欠条', title='① 你的目标文件',
                 color='blue', size=14.5)
    rect(s, MARGIN_L + w + 0.20, y + 0.55, 0.50, 0.34, fill=C['ink3'], shape=MSO_SHAPE.RIGHT_ARROW)
    b2, _ = card(s, MARGIN_L + w + 0.9, y, w, 'libc.a / libc.so\n\nprintf() 的真实机器码', title='② 标准库',
                 color='purple', size=14.5)
    rect(s, MARGIN_L + (w + 0.9) + w + 0.20, y + 0.55, 0.50, 0.34, fill=C['ink3'], shape=MSO_SHAPE.RIGHT_ARROW)
    b3, _ = card(s, MARGIN_L + (w + 0.9) * 2, y, w, 'hello.exe\n\nmain + printf\n一个能跑的程序',
                 title='③ 可执行文件', color='green', size=14.5)
    y = max(b1, b2, b3) + 0.24

    bullets(s, MARGIN_L, y, INNER_W, [
        '链接错误长什么样：undefined reference to `printf` —— 说明"欠条"没还上（库没接上）',
        '第9讲静态库、第10讲动态库，本质上都在讲"链接这一步的两种做法"',
    ], size=15)
    footer_note(s, '静态链接：把库代码复制进来 ｜ 动态链接：只留一张"引用单"')
    done('P7')


# ============================================================
# P8 从表达式到插件框架（本讲重点页）
# ============================================================
def p08_evolution():
    s = pg('重点：从表达式，到软件体系的插件框架', '本系列只有一条主线 —— 抽象层次的提升')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '一行 printf，怎么一步步长成能插拔组件的软件体系？答案就是这六级台阶。'),
        title='🧭 一条主线', color='orange', size=15)
    y = y2 + 0.22

    y = cards_row(s, y, [
        {'title': '① 表达式（第1讲）', 'body': '算出一个值\n最小执行单元 ← 你在这里', 'color': 'orange', 'size': 14},
        {'title': '② 函数（第3讲）', 'body': '把一段逻辑封成名字\n可以反复调用、复用', 'color': 'blue', 'size': 14},
        {'title': '③ 模块（第4讲）', 'body': '接口与实现分家\n多人分工、各写各的', 'color': 'teal', 'size': 14},
    ]) + 0.22
    cards_row(s, y, [
        {'title': '④ 库（第9-10讲）', 'body': '编译成二进制\n跨项目复用，不用给源码', 'color': 'purple', 'size': 14},
        {'title': '⑤ 插件（第11-12讲）', 'body': '运行时按需加载\n可插可拔，不用重编程序', 'color': 'pink', 'size': 14},
        {'title': '⑥ 框架（第13-14讲）', 'body': '框架反过来调用你的代码\n这就是控制反转（IoC）', 'color': 'green', 'size': 14},
    ])
    banner(s, '我们今天站的这一级最低，但它是唯一的地基')
    done('P8')


# ============================================================
# P9 前面的路：库与链接层预告
# ============================================================
def p09_next():
    s = pg('顺着这条主线，后面会走到哪儿', '库 → 链接 → 插件 → 框架')
    y = BODY_TOP
    y = flow(s, MARGIN_L, y, INNER_W,
         [('第9讲', '静态库\n代码复制'), ('第10讲', '动态库\n代码共享'),
          ('第11讲', '运行时加载\n按需加载'), ('第12讲', '接口抽象\n统一插头'),
          ('第13讲', '插件框架\n生命周期'), ('第14讲', '完整项目\n收官总结')],
         colors=('blue', 'teal', 'purple', 'pink', 'green', 'primary'), size=14, h=1.15) + 0.26

    y = cards_row(s, y, [
        {'title': '🔗 链接的两种做法（第9-10讲）',
         'body': '静态库：体积大、内存重复 —— 每个程序自带一份\n动态库：多个程序共享同一份代码，可单独更新',
         'color': 'teal', 'size': 15},
        {'title': '🧩 从库到插件（第11-13讲）',
         'body': '运行时加载：跑起来才知道加载谁 → 插件诞生\n插件框架：生命周期 / 配置化菜单 / 开闭原则',
         'color': 'purple', 'size': 15},
    ], gap=0.28) + 0.20

    bullets(s, MARGIN_L, y, INNER_W, [
        '今天讲的"头文件/库文件分离"，就是第9讲"静态库"的思想来源',
        '今天讲的"链接"，就是第10讲"动态库"要动手做的那件事',
    ], size=15)
    banner(s, '第1讲埋下的三颗种子：表达式 · 接口分离 · 链接')
    done('P9')


# ============================================================
# P10 ATM 实战
# ============================================================
def p10_demo_code():
    s = pg('动手：写第一个 ATM 程序', 'src/hello.c —— 从这一行开始，一直到插件框架')
    y = BODY_TOP
    code(s, MARGIN_L, y, INNER_W, [
        '#include <stdio.h>          /* 引入标准库的"菜单"，printf 的声明在这里 */',
        '',
        'int main(void)              /* main 是程序的入口，操作系统从这里进来 */',
        '{',
        '    printf("Hello, Plugin Framework!\\n");   /* 今天的主角 */',
        '    return 0;               /* 返回 0 表示程序正常结束 */',
        '}',
    ], title='hello.c：仓库里这份带 200 行注释，核心只有这几行', size=13)
    y += 0.40 + 0.36 + 7 * 13 * 1.42 / 72 + 0.26

    cards_row(s, y, [
        {'title': '① 写', 'body': '源文件 hello.c\n人看得懂的文字', 'color': 'blue', 'size': 14},
        {'title': '② 编', 'body': 'gcc -Wall hello.c\n-o hello.exe', 'color': 'teal', 'size': 14},
        {'title': '③ 跑', 'body': '屏幕出现\nHello, Plugin Framework!', 'color': 'green', 'size': 14},
    ])
    banner(s, '写 → 编 → 跑：这个循环会陪你走完 14 讲')
    done('P10')


def p11_run():
    s = pg('运行演示：看得见的效果', '编译命令、运行输出、退出码 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall hello.c -o hello.exe',
        '$ ./hello.exe',
        'Hello, Plugin Framework!',
        '$ echo $?',
        '0',
    ], title='终端实录（真实输出）', size=13)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译期：查语法、找符号，报错就停在这步\n'
        '② 链接期：把 printf 从库里接上\n'
        '③ 运行期：程序在内存里跑，向屏幕输出\n'
        '④ 退出码：0 = 正常，非 0 = 出错'),
        title='👀 要看清楚的四个点', color='orange', size=14.5, min_h=2.30)
    y += 2.55
    bullets(s, MARGIN_L, y, INNER_W, [
        '片尾会放一段真实的编译 + 运行演示动画：命令怎么敲、屏幕怎么亮、退出码怎么读',
    ], size=15)
    banner(s, '看得见的运行结果，是最好的老师')
    done('P11')


def p12_quiz():
    s = pg('课堂小测（当作热身）', '三题检验刚才的理解')
    y = BODY_TOP
    rows = [('Q1', 'C 语言的编译过程分为哪几个阶段？', '预处理 → 编译 → 汇编 → 链接'),
            ('Q2', 'printf 的实现在头文件里吗？', '不在。头文件只有声明，实现在库文件里'),
            ('Q3', '链接器到底做了什么？', '把你调用的库函数机器码（或引用单）接进你的程序')]
    y2, _ = kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.10, 0.45, 0.45), size=14.5,
                    header=('题号', '问题', '答案'))
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '这三题答对了，说明你已经能把"写一行代码"和"生成一个程序"两件事分开看了——\n'
        '这正是从"写代码的人"走向"懂架构的人"的第一步。'),
        title='💡 为什么要先答这三题', color='blue', size=15, min_h=1.05)
    footer_note(s, '能把过程讲清楚，才算真的懂了')
    done('P12')


# ============================================================
# P13 深入思考
# ============================================================
def p13_think():
    s = pg('深入思考：两个"为什么"', '答案没有唯一解，但能看出你的思维层次')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '为什么 C 是编译型语言，而不是像 Python 那样边解释边运行？\n'
        '→ 编译型把"翻译"提前到发布前，运行时没有翻译开销，所以快；\n'
        '→ 代价是改一行要重新编译、跨平台要重新编译。这是"性能 vs 便利"的取舍。'),
        title='问题一：为什么要有"编译"这一步？', color='orange', size=15.5, min_h=1.55)
    y = y2 + 0.24
    card(s, MARGIN_L, y, INNER_W, (
        '头文件与源文件为什么要分开？\n'
        '→ 分开之后，用的人只需看头文件（知道怎么调），不必关心实现（怎么做的）；\n'
        '→ 这就是"接口与实现分离"，第4讲多文件、第9讲静态库、第12讲插件接口，全是它的后代。'),
        title='问题二：为什么要把"声明"和"实现"拆开？', color='teal', size=15.5, min_h=1.55)
    footer_note(s, '今天想明白的两件事，会一直用到第14讲')
    done('P13')


# ============================================================
# P14-P17 思考题与解答
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '先分清两个层次：表达式是"写出来的东西"，程序是"跑起来的东西"。\n'
        '那么：一行 printf 里的每个零件，分别在哪个阶段起作用？\n'
        '如果我把分号去掉、把引号删掉，编译器会在哪一步、报什么错？'),
        title='思考题 ①：从一行代码到一次输出，中间隔了几层？', color='orange', size=15.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '表达式有值，语句只是"做一件事"——那为什么 C 语言要把绝大多数操作都设计成表达式？\n'
        '提示：想一想 printf 的返回值，如果它不返回值，你能不能写出\n'
        'if (printf("...") > 0) 这种写法？语言设计者为什么要留这个"值"给你？'),
        title='思考题 ②：为什么 C 语言强调"一切皆表达式"？', color='blue', size=15.5, min_h=1.55)
    footer_note(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


def p15_a12():
    s = pg('思考题 ①② 参考解答', '题目抄在这里，方便对照')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：四层，越早出错代价越小',
         'body': '题目：从一行代码到一次输出，中间隔了几层？\n'
                 '① 编译期：检查 printf 有没有声明\n'
                 '② 链接期：去库里把实现接上\n'
                 '③ 装载期：操作系统读进内存\n'
                 '④ 运行期：在内存中执行并输出\n'
                 '去分号→语法错；删引号→未定义标识符',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ②：因为"值"让代码可以拼装',
         'body': '题目：为什么 C 语言强调"一切皆表达式"？\n'
                 '有值 → 可以嵌套：f(g(x))\n'
                 '有值 → 可以判断：if (printf(..)>0)\n'
                 '有值 → 可以统计：返回打印字符数\n'
                 '把最小零件做成"可拼装"的，语言才有组合力',
         'color': 'blue', 'size': 12.5},
    ], gap=0.26)
    banner(s, '表达式的"值"，就是代码的"可拼装接口"')
    done('P15')


def p16_q34():
    s = pg('思考题 ③④', '两题进阶：把今天的知识接到"库"和"架构"上')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '静态链接和动态链接，在"你写的程序"里留下的东西完全不同：\n'
        '一个把库代码搬进你的 exe，一个只在 exe 里留一张"引用单"。\n'
        '那么：如果同一个库有 10 个程序要用，两种做法在磁盘上和内存里各占多少份？\n'
        '库修了一个 bug，两种做法分别要做什么？'),
        title='思考题 ③：静态链接 vs 动态链接，差别到底在哪？', color='purple', size=15.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '本讲说"接口与实现分离"是后面所有架构的源头。\n'
        '请试着推演：如果一行代码里"函数名"就是最小的"接口"，\n'
        '那么到了插件框架（第13讲），"接口"会变成什么样子？\n'
        '提示：从"函数名"到"函数指针"，再到"结构体里装一组函数指针"。'),
        title='思考题 ④：从"函数名"到"插件接口"，中间要跨几步？', color='green', size=15.5, min_h=1.55)
    footer_note(s, '这两题想通了，第9讲和第13讲就提前入门了')
    done('P16')


def p17_a34():
    s = pg('思考题 ③④ 参考解答', '题目抄在这里，方便对照')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：一份 vs 十份',
         'body': '题目：静态链接与动态链接，磁盘和内存各占几份？\n'
                 '静态：磁盘 10 份副本，内存 10 份\n'
                 '动态：磁盘只有 1 份 .dll，进程共享\n'
                 '库修 bug：静态要重链 10 次\n'
                 '动态只换 1 个库文件即可',
         'color': 'purple', 'size': 12.5},
        {'title': '解答 ④：三步进化',
         'body': '题目：从"函数名"到"插件接口"要跨几步？\n'
                 '第1步（第5讲）：函数名 → 函数指针\n'
                 '第2步（第12讲）：函数指针装进结构体 → 插座\n'
                 '第3步（第13讲）：框架拿着插座表调用你\n'
                 '本质：约定从"叫什么名"变成"长什么样"',
         'color': 'green', 'size': 12.5},
    ], gap=0.26)
    banner(s, '从函数名到插件接口：概念的进化，比语法更重要')
    done('P17')


def p18_summary():
    s = pg('小结与预告', '第1讲 表达式 —— 一切的起点')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '一行 printf 背后，是表达式、标准库、四个编译阶段和一次链接的精密协作 —— 它是这座软件体系的第一块砖。'),
        title='📝 一句话总结', color='orange', size=15)
    y = y2 + 0.24

    rows = [('1', '表达式', '能算出一个值的代码片段，C 语言的最小执行单元'),
            ('2', 'printf 五要素', '函数名 · 括号 · 字符串 · 转义字符 · 分号'),
            ('3', '标准库', '头文件给声明（菜单），库文件给实现（厨房）'),
            ('4', '编译四阶段', '预处理 → 编译 → 汇编 → 链接'),
            ('5', '链接 ⭐', '把"欠条"还上：找到库函数实现，拼成可执行文件'),
            ('6', '本讲的位置', '六级台阶第一级：表达式 → 函数 → 模块 → 库 → 插件 → 框架')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=13,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：控制结构 —— 让程序会判断、会循环（第2讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_expr, p04_printf, p05_lib, p06_compile, p07_link,
           p08_evolution, p09_next, p10_demo_code, p11_run, p12_quiz, p13_think,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 + 正文 17 页）' % len(prs.slides._sldIdLst))
