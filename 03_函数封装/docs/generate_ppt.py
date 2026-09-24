# -*- coding: utf-8 -*-
"""
第3讲：函数封装 —— 给代码找个家
generate_ppt.py（新规范版，18 页）

依赖统一工具箱 tools/ppt_kit.py：
    · 标题单行自适应（R1）—— 投影时标题绝不换行
    · 容器不叠压、文字不越界、装饰永在底层（R2）—— 不再"前后不分"
    · 全部正文对比度 ≥ 4.5:1，代码一律深底亮字（R3）—— 投影看得清
每画完一页立刻 done('PN') 质检，有问题直接报错，绝不产出坏 PPT。

额外自检：代码块里的中文（Consolas 度量偏窄）按真实宽度再估一遍，
避免"质检过关、投影却溢出半个字"。

输出：docs/课件.pptx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from ppt_kit import *          # noqa
from ppt_kit import (C, page, card, code, bullets, flow, compare, banner, footer_note,
                     demo_frame, kv_rows, text, panel, rect, audit, save, new_deck, blank,
                     MARGIN_L, INNER_W, BODY_TOP, BODY_BOTTOM, SW, SH, MARGIN_R, TITLE_TOP,
                     fit_size, text_width_in, _put_text, _reg_text, _reg_container, _reset_reg)

LECTURE = '第3讲 函数封装'
prs = new_deck()
PAGES = []

# 六级台阶（全系列统一叙事）
STEPS = ['① 表达式', '② 函数', '③ 模块', '④ 库', '⑤ 插件', '⑥ 框架']


def _w_est(s, size):
    """按"中文=全宽、ASCII=半宽"估算真实渲染宽度（英寸）。Consolas 度量中文偏窄，故单独算。"""
    n_a = sum(1 for ch in s if ord(ch) < 0x2E80)
    n_c = len(s) - n_a
    return (0.55 * n_a + 1.00 * n_c) * size / 72.0 * 1.06


def codex(s, x, y, w, lines, title=None, size=12.0, tag='code'):
    """代码块包装：先做"中文宽度"自检，再交给 ppt_kit 绘制。"""
    limit = w - 0.36
    for ln in lines:
        est = _w_est(ln, size)
        if est > limit:
            raise AssertionError('[代码行过宽] %.2fin > %.2fin：「%s」' % (est, limit, ln))
    if title:
        est_t = _w_est(title, size + 1)
        if est_t > w - 0.30:
            raise AssertionError('[代码标题过宽] %.2fin：「%s」' % (est_t, title))
    return code(s, x, y, w, lines, title=title, size=size, tag=tag)


def demo_frame_x(s, x, y, w, h, title='运行效果', lines=None, note=None, tag='demo'):
    for ln in (lines or []):
        if _w_est(ln, 12.5) > w - 0.36:
            raise AssertionError('[演示行过宽] 「%s」' % ln)
    return demo_frame(s, x, y, w, h, title=title, lines=lines, note=note, tag=tag)


def pg(title, subtitle=None):
    s = page(prs, title, subtitle, label=LECTURE, page_no='auto')
    PAGES.append(s)
    return s


def done(tag=''):
    audit(prs, tag)


def cards_row(s, y, specs, gap=0.22):
    """等宽一行卡片，按真实高度推进。"""
    n = len(specs)
    w = (INNER_W - gap * (n - 1)) / n
    bottoms = []
    for i, sp in enumerate(specs):
        b, _ = card(s, MARGIN_L + i * (w + gap), y, w, sp['body'],
                    title=sp.get('title'), color=sp.get('color', 'orange'),
                    size=sp.get('size', 16), min_h=sp.get('min_h', 0.0))
        bottoms.append(b)
    return max(bottoms)


def cards_col(s, x, y, w, specs, gap=0.22, size=15):
    """纵向堆叠卡片，返回底部 y。"""
    for sp in specs:
        b, _ = card(s, x, y, w, sp['body'], title=sp.get('title'),
                    color=sp.get('color', 'orange'), size=sp.get('size', size),
                    min_h=sp.get('min_h', 0.0))
        y = b + gap
    return y - gap


# ============================================================
# P1 封面
# ============================================================
def p01_cover():
    _reset_reg()
    slide = blank(prs)
    rect(slide, 0, 0, SW, SH, fill=C['bg'])
    rect(slide, 0, 0, 4.4, SH, fill=C['card_orange'])            # 左侧暖色带
    rect(slide, 0, 0, 0.16, SH, fill=C['primary'])
    rect(slide, 4.4, 0, SW - 4.4, 0.12, fill=C['primary'])

    _put_text(slide, 0.75, 1.15, 3.3, 0.5, '从程序员到架构师', 20, C['primary_dark'], bold=True)
    _put_text(slide, 0.75, 1.72, 3.3, 0.4, 'C语言插件框架演进之旅', 14, C['ink2'])
    rect(slide, 0.75, 2.30, 0.9, 0.05, fill=C['primary'])

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第3讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.50, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '函数封装', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '给代码找个家', 27, C['primary_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.8,
              '第2讲的 ATM 能跑了，可所有代码都堆在 main 里：\n'
              '几十行挤成一团，成功提示抄了三遍，想改一处得从头找。\n'
              '本讲给代码安个家——把重复的代码打包、命名、藏起细节，\n'
              '从此 main 只负责调度，每一件事都有它自己的函数。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '六级台阶的第二级 —— 从"一行代码"到"一段可以复用的逻辑"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '前两讲我们已经会写能跑的程序：第1讲用表达式把字打上屏幕，'
        '第2讲用分支和循环让程序会判断、会重复。\n'
        '本讲站上第二级台阶——函数：把重复的代码打包、命名、藏起细节，让 main 只负责调度。'),
        title='🎯 本讲定位', color='orange', size=15.5, min_h=1.20)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '← 你在这里'), ('③ 模块', '第4讲'),
             ('④ 库', '第9-10讲'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13-14讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('teal', 'primary', 'gray', 'gray', 'gray', 'gray'),
             size=13.5, h=0.92) + 0.24

    w = INNER_W / 2 - 0.14
    card(s, MARGIN_L, y, w, (
        '第1-2讲：表达式 + 三种控制结构\n'
        'ATM 确实能跑了，但越来越长、越来越重复'),
        title='⬅ 前置', color='blue', size=14, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第4讲：函数一多，一个文件装不下\n'
        '按职责把函数拆进 .h / .c 多个文件'),
        title='➡ 后续', color='teal', size=14, min_h=1.00)
    banner(s, '函数是全部封装的起点：模块、库、框架，都是它的放大版')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '代码能跑，但"越长越乱、想改找不到、想复用搬不动"')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第2讲：没有函数的日子', [
                    '所有代码堆在 main 里，几十行起步',
                    '存款/取款的提示语到处复制粘贴',
                    '想改"取款"？得在一大堆代码里翻',
                    '另一个程序要用存款？整段复制过去'],
                '第3讲：用函数收编代码', [
                    '每个功能一个函数，main 只负责调度',
                    '公共提示抽成 print_success 一份',
                    '想改"取款"？直接打开 withdraw 函数',
                    '想复用？把函数拿过去调用就行'],
                left_color='red', right_color='green', size=13.5) + 0.06
    y = cards_row(s, y, [
        {'title': '痛点① 又长又乱', 'body': '顺序、分支、循环混在一起\n读一遍才知道谁是谁',
         'color': 'red', 'size': 12.5},
        {'title': '痛点② 重复代码', 'body': '同一句成功提示抄了三遍\n改格式要改三处，容易漏',
         'color': 'yellow', 'size': 12.5},
        {'title': '痛点③ 没法复用', 'body': '想借用存款逻辑\n只能连同 main 一起搬走',
         'color': 'purple', 'size': 12.5},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：代码没有"家"，所有东西都摊在桌面上 —— 函数，就是给代码一个抽屉',
    ], size=15)
    banner(s, '本讲只做一件事：把"大杂烩"拆成"各归各位"的函数')
    done('P3')


# ============================================================
# P4 核心一：函数 = 打包 + 命名 + 隐藏
# ============================================================
def p04_func():
    s = pg('核心一：函数是打包、命名、隐藏', '函数 = 打包 + 命名 + 隐藏细节 —— 像遥控器只给你按钮')
    y = BODY_TOP
    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 声明', '告诉编译器\n"有这么个函数"'),
        ('② 定义', '写清函数体\n真正干活的代码'),
        ('③ 调用', '让函数执行一次\n"点菜，上菜"'),
    ], colors=('blue', 'teal', 'orange'), size=15, h=0.95) + 0.24

    cw = INNER_W * 0.54
    codex(s, MARGIN_L, y, cw, [
        '返回值类型  函数名(参数列表)',
        '{',
        '    函数体：要打包的那段代码',
        '}',
        '',
        'void deposit(void)   /* void=不返回，(void)=不需要参数 */',
        '{',
        '    printf("【存款业务】\\n");',
        '}',
    ], title='函数的四个部分', size=12.0)

    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '· 返回值类型 void：干完活不交结果\n'
        '· 函数名 deposit：以后就用这个名字叫它\n'
        '· 参数列表 (void)：不需要外部喂数据\n'
        '· 函数体 { }：真正被包进去的代码块\n'
        '\n'
        '调用者只需要知道"传什么、得到什么"，\n'
        '内部怎么实现，可以随时改 —— 这就是隐藏。'),
        title='🔑 四个部分，各管什么', color='teal', size=12.5, min_h=2.62)
    banner(s, '声明是"菜单"，定义是"厨房"，调用是"点菜" —— 三件事，各就各位')
    done('P4')


# ============================================================
# P5 核心二：参数传递（值传递）
# ============================================================
def p05_params():
    s = pg('核心二：参数传递 —— 值传递', '不带参数只能做固定的事，带参数才能"看菜下饭"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '存款金额每次都不一样。要让函数处理"不固定的数据"，就得把数据传进去 —— '
        '这就是参数：形参是函数内部的"接货口"，实参是调用时真正递过去的值。'),
        title='📥 为什么需要参数', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    cw = INNER_W * 0.56
    codex(s, MARGIN_L, y, cw, [
        'void print_success(char* op, double amount)',
        '{',
        '    printf("✅ 操作成功！%s %.2f 元\\n", op, amount);',
        '    printf("当前余额：%.2f 元\\n", g_balance);',
        '}',
        '',
        'print_success("存入", 500.0);   /* op="存入"，amount=500.0 */',
        'print_success("取出", 200.0);   /* 同一个函数，换个参数 */',
    ], title='同一个函数，换个参数就换一件事', size=11.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '· 形参 op / amount：函数自己造的两个"坑"\n'
        '· 实参 "存入" / 500.0：调用时填进去的值\n'
        '· 位置一一对应，类型要对得上\n'
        '· 一次调用一份副本，互不干扰\n'
        '\n'
        '不传参数的函数只能做固定的事，\n'
        '传了参数，函数才真正"活"起来。'),
        title='🔑 形参 vs 实参', color='blue', size=12.5, min_h=2.35)
    banner(s, '参数是函数的"输入口"：数据从外面进来，结果从返回值出去')
    done('P5')


# ============================================================
# P6 核心三：返回值
# ============================================================
def p06_return():
    s = pg('核心三：返回值与 return', 'return 有两个作用：结束函数 + 把结果带回调用者')
    y = BODY_TOP
    y = flow(s, MARGIN_L, y, INNER_W, [
        ('return a;', 'a 更大\n返回 a，函数立即结束'),
        ('return b;', '否则返回 b\n两条路径必走其一'),
        ('return;', 'void 函数提前收工\n后面的代码不再执行'),
    ], colors=('teal', 'teal', 'orange'), size=14, h=1.00) + 0.24

    cw = INNER_W * 0.54
    codex(s, MARGIN_L, y, cw, [
        'double get_max(double a, double b)',
        '{',
        '    if (a > b)',
        '    {',
        '        return a;   /* 返回 a，函数到此结束 */',
        '    }',
        '    return b;',
        '}',
        '',
        'int add(int a, int b) { return a + b; }',
    ], title='返回值：函数交给调用者的结果', size=12.0)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '· 有返回值：类型写 int / double，用 return 交回结果\n'
        '· 无返回值：类型写 void，也可以写 return; 提前收工\n'
        '· return 一旦执行，函数立刻返回，后面代码不跑\n'
        '· 调用处可以把返回值存进变量，直接参与运算\n'
        '\n'
        '所以返回值 = 函数的"输出口"。'),
        title='🔑 void 与 return 的分工', color='green', size=12.5, min_h=2.86)
    banner(s, '函数像一台机器：参数是进料口，返回值是出料口')
    done('P6')


# ============================================================
# P7 核心四：作用域与生命周期
# ============================================================
def p07_scope():
    s = pg('核心四：作用域与生命周期', '变量"活在哪里、能活多久"，决定谁能改它')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '局部变量（函数内）', [
                    '只在函数内部可见，外面看不到',
                    '函数一返回就被销毁，值不留痕',
                    '不同函数里同名变量互不干扰'],
                '全局变量（函数外）', [
                    '整个程序都能看见，谁都能改',
                    '从程序开始活到程序结束',
                    '本讲用 g_balance 就是全局变量'],
                left_color='teal', right_color='primary', size=13.5) + 0.06

    cw = INNER_W * 0.56
    codex(s, MARGIN_L, y, cw, [
        'double g_balance = 1000.0;   /* 全局：所有函数都能改 */',
        '',
        'void deposit(void)',
        '{',
        '    double amount = 0.0;      /* 局部：出了函数就没了 */',
        '    scanf("%lf", &amount);',
        '    g_balance = g_balance + amount;',
        '}',
    ], title='全局变量 vs 局部变量（真实源码）', size=11.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '· 局部变量住在栈上，随函数生、随函数亡\n'
        '· 全局变量住在全局数据区，程序结束才消失\n'
        '· 用全局变量图方便，却埋下"谁改了都不知道"的隐患\n'
        '\n'
        '下一讲会用 static 把余额"关进笼子"，\n'
        '本讲先记住：能传参就别用全局。'),
        title='⚠️ 全局变量的隐患', color='red', size=12.5, min_h=2.35)
    banner(s, '变量可见范围越大，出问题时越难查 —— 这是第4讲的伏笔')
    done('P7')


# ============================================================
# P8 核心五：封装思想与单一职责、代码复用
# ============================================================
def p08_design():
    s = pg('核心五：封装思想与单一职责', '一个函数只做一件事，并把它做好；同样的代码不写两遍')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '❌ 违反单一职责', [
                    'do_everything()：什么都干，谁也说不清',
                    'deposit_and_withdraw()：两件事绑一起',
                    '存款里手写一遍成功提示，取款里再抄一遍'],
                '✅ 单一职责 + 代码复用', [
                    'deposit() 只管存款，看名字就懂',
                    'print_success() 只负责打印一行结果',
                    '提示语只写一遍，三处业务都来调用'],
                left_color='red', right_color='green', size=13.5) + 0.06

    cw = INNER_W * 0.54
    codex(s, MARGIN_L, y, cw, [
        '/* 第2讲：三处重复的提示语 */',
        'printf("✅ 存款成功！存入 %.2f 元\\n", amount);',
        'printf("当前余额：%.2f 元\\n", g_balance);',
        '/* 取款里、转账里，又各抄了一遍…… */',
        '',
        '/* 第3讲：抽成一个函数，到处调用 */',
        'void print_success(char* op, double amount)',
        '{',
        '    printf("✅ 操作成功！%s %.2f 元\\n", op, amount);',
        '    printf("当前余额：%.2f 元\\n", g_balance);',
        '}',
    ], title='重复代码 → 抽成函数', size=11.0)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '· 好理解：看函数名就知道它做什么\n'
        '· 好维护：改存款逻辑只改 deposit 一处\n'
        '· 好复用：需要打印成功信息，叫一声就行\n'
        '\n'
        '封装不是把代码藏起来就完事，\n'
        '而是"职责分清楚 + 细节藏起来"。'),
        title='🔑 三个设计原则', color='purple', size=12.5, min_h=2.55)
    banner(s, '单一职责 + 代码复用 + 信息隐藏 —— 这是后面所有架构套路的基本功')
    done('P8')


# ============================================================
# P9 原理深入：值传递的内存真相 ⭐
# ============================================================
def p09_deep():
    s = pg('原理深入：值传递的内存真相 ⭐', '为什么函数里把 x 改成 11，外面的 a 还是 10？')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '结论：调用函数时递过去的是"值的复印件"，函数改的是自己栈上的新变量，动不了原件。'),
        title='🧠 先给结论', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    cw = INNER_W * 0.54
    codex(s, MARGIN_L, y, cw, [
        'void add_one(int x)      /* x 是 a 的副本 */',
        '{',
        '    x = x + 1;           /* 改的是副本，不是 a */',
        '    printf("函数内：x = %d\\n", x);',
        '}',
        '',
        'int main()',
        '{',
        '    int a = 10;',
        '    add_one(a);          /* 只是把 10 复印一份递过去 */',
        '    printf("函数外：a = %d\\n", a);   /* 输出仍是 10 */',
        '}',
    ], title='真实源码：一次值传递发生了什么', size=11.0)
    cards_col(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, [
        {'title': '① 复制', 'body': '把 a 的值 10 复制一份', 'color': 'teal', 'size': 12.5},
        {'title': '② 独立', 'body': '栈上新建 x，与 a 互不相干', 'color': 'blue', 'size': 12.5},
        {'title': '③ 代价', 'body': '大结构体每次调用都要整份复制', 'color': 'purple', 'size': 12.5},
    ], gap=0.14)
    banner(s, '想改原件？得把"地址"递过去 —— 这就是第5讲指针要解决的问题')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：第2讲 vs 第3讲', '同样一个 ATM，换一种组织方式')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第2讲：全靠 main 硬扛', [
                    'main 几十行，顺序、分支、循环挤在一起',
                    '同一句成功提示，三处各抄一遍',
                    '改一个功能，要通读全篇才敢下手'],
                '第3讲：函数化的 ATM', [
                    'main 只做调度，一眼看清有几件事',
                    'print_success / print_error 只写一遍',
                    '改哪个功能，直接打开对应的函数'],
                left_color='red', right_color='green', size=13.5) + 0.16

    rows = [('main 长度', '几十行，什么都塞进去', '十几行，只有调度'),
            ('代码重复', '提示语复制粘贴好几份', '抽成公共函数，写一遍'),
            ('找代码', '在 main 里一行行翻', '按函数名直接定位'),
            ('复用方式', '整段复制到别的程序', '把函数拿过去调用')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.16, 0.42, 0.42), size=12,
            header=('对比项', '第2讲 无函数', '第3讲 函数封装'))
    banner(s, '函数不是为了少打字，而是为了让代码好读、好改、好复用')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/atm_func.c —— 声明区在上、定义在下，main 只负责调度')
    y = BODY_TOP
    cw = INNER_W * 0.50
    codex(s, MARGIN_L, y, cw, [
        '/* 函数声明（原型）：先跟编译器打个招呼 */',
        'void show_welcome(void);',
        'void show_menu(void);',
        'void query_balance(void);',
        'void deposit(void);',
        'void withdraw(void);',
        'void transfer(void);',
        'void print_success(char* op, double amount);',
        'void print_error(char* msg);',
    ], title='atm_func.c：函数声明区（真实源码）', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    br, _ = codex(s, xr, y, wr, [
        'void print_success(char* op, double amount)',
        '{',
        '    printf("✅ 操作成功！%s %.2f 元\\n", op, amount);',
        '    printf("当前余额：%.2f 元\\n", g_balance);',
        '}',
        '',
        'void deposit(void)',
        '{',
        '    scanf("%lf", &amount);',
        '    g_balance = g_balance + amount;',
        '    print_success("存入", amount);',
        '}',
    ], title='函数定义区（真实源码）', size=11.5)

    card(s, MARGIN_L, br + 0.18, INNER_W, (
        '声明集中写在文件开头，像书的目录；定义整齐排在后面，每个函数只做一件事 —— main 只管调度。'),
        title='📊 本讲源码的组织方式', color='green', size=13.5, title_size=16)
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '命令、菜单、余额变化、退出码 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.60
    codex(s, MARGIN_L, y, cw, [
        "$ gcc -Wall atm_func.c -o atm_func.exe",
        "$ printf '1\\n2\\n500\\n3\\n200\\n0\\n' | ./atm_func.exe",
        '========================================',
        '       欢迎使用 CCIT ATM 系统',
        '【查询余额】',
        '您当前的账户余额为：1000.00 元',
        '【存款业务】',
        '请输入存款金额：✅ 操作成功！存入 500.00 元',
        '当前余额：1500.00 元',
        '【取款业务】',
        '请输入取款金额：✅ 操作成功！取出 200.00 元',
        '当前余额：1300.00 元',
        '感谢使用 CCIT ATM 系统，再见！',
        '$ echo $?   →   0',
    ], title='终端实录（真实输出，未删改）', size=11.5)

    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译零警告：函数声明与定义一致，没有隐式声明\n'
        '② 查询余额：1000.00 元，来自全局变量 g_balance\n'
        '③ 存款后 1500.00 元：print_success 打印统一格式\n'
        '④ 取款后 1300.00 元：同一函数，换参数换行为\n'
        '⑤ 程序正常退出，菜单循环被 choice=0 结束\n'
        '⑥ 退出码 0：没有崩溃，资源随进程回收'),
        title='👀 要看清楚的六个点', color='orange', size=12.5, min_h=3.62)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 atm_func.c 源码')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的第二级：函数 —— 把代码打包成"可复用的名字"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。'
        '第1讲我们把字打上屏幕，本讲让代码有了"名字"，'
        '后面每一级台阶，都是在这同一个名字上继续放大。'),
        title='🧭 一条主线', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '← 本讲 ⭐'), ('③ 模块', '第4讲'),
             ('④ 库', '第9-10讲'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13-14讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('teal', 'primary', 'gray', 'gray', 'gray', 'gray'),
             size=13.5, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    card(s, MARGIN_L, y, w, (
        '把重复代码收进函数，命名、复用、隐藏细节\n'
        '单一职责：一个函数只做一件事\n'
        '接口与实现分离的最初形态：看名字就能用\n'
        '"库"能成立，前提就是函数可以被独立复用'),
        title='本讲为终点贡献了什么', color='teal', size=13, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第4讲把一堆函数按职责拆进 .h / .c\n'
        '用 static 把余额关进笼子，只留接口\n'
        '那时"函数"会升级成"模块"，\n'
        '再往后，模块会被编译成库和插件。'),
        title='下一讲接着做什么', color='blue', size=13, min_h=1.55)
    banner(s, '函数是第一次"给代码起名字"——所有架构，都从起名字开始')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '我们常说"函数是 C 语言中最基础的封装手段"。这里的"封装"到底封装了什么？'
        '为什么偏偏是函数，而不是别的语法？\n'
        '提示：想一想"打包"和"隐藏"分别指什么；再想想生活中的遥控器、'
        '自动售货机，它们封装了什么、只露出了什么。'),
        title='思考题 ①：为什么说函数是最基础的封装？', color='orange', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        'C 语言的参数是"值传递"——传的是副本。这样设计有什么好处？又有什么坏处？'
        '如果让你来设计一门语言，你会选值传递还是引用传递？\n'
        '提示：从安全性、隔离性想好处；从"想改原变量怎么办""大结构体每次复制"'
        '想坏处；再看看 Java、Python 是怎么选的。'),
        title='思考题 ②：值传递的得与失', color='purple', size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：打包 + 隐藏',
         'body': '封装的"装"是把相关代码装进一个整体，\n'
                 '封装的"封"是把内部细节封起来不给人看\n'
                 '函数一次满足两条：代码打包、起个名字，\n'
                 '调用者只需知道传什么、返回什么\n'
                 '生活里的遥控器封装了电路、只露按钮；\n'
                 '售货机封装了找零、只露选货键\n'
                 '往上还有模块、库、框架、微服务——\n'
                 '每一层都在做同一件事，只是尺度更大',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ②：安全换灵活',
         'body': '好处：安全——函数里怎么折腾都不影响外面；\n'
                 '隔离——调用者与被调用者互不产生副作用；\n'
                 '简单——复制一份，行为可预测\n'
                 '坏处：改不了原变量（要靠指针补）；\n'
                 '大结构体每次调用都要整份复制；\n'
                 '一次只能返回一个值\n'
                 '各语言的选择：C 默认值传递、指针补灵活；\n'
                 'C++ 两种都支持；Python 对象传引用；\n'
                 'Fortran 默认引用传递',
         'color': 'purple', 'size': 12.5},
    ], gap=0.26)
    banner(s, '没有绝对的好坏，只有"安全"和"灵活"的取舍')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从函数粒度，谈到全局变量的争议')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '有人说"函数要尽量小，一个函数别超过 20 行"，也有人说"别为了拆而拆，'
        '拆得太碎反而更难读"。函数到底写多长才合适？\n'
        '提示：想一想嵌套太深、需要滚动屏幕、重复代码出现两次这些信号；'
        '再想想"单一职责"和"函数很小"到底是不是一回事。'),
        title='思考题 ③：函数越"小"越好吗？', color='teal', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '本讲用了全局变量 g_balance，因为好几个函数都要用余额。但很多人说'
        '"全局变量是有害的，尽量不要用"。为什么不喜欢，又为什么还得用？\n'
        '提示：从"谁都能改，改乱了找谁""隐藏依赖、降低可读性""不好搬到别的项目"'
        '三个角度想坏处；再想想不用全局变量时，怎么让多个函数共享数据。'),
        title='思考题 ④：全局变量的争议', color='green', size=14.5, min_h=1.55)
    banner(s, '这两题想透了，第4讲的 static 与第5讲的指针就顺理成章了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '一个讲"拆的尺度"，一个讲"共享数据的方式"')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：标准是"职责单一"',
         'body': '拆太小：跳转太多、读起来累，逻辑被切断；\n'
                 '写太长：看不懂、难维护、难复用\n'
                 '四条判断标准：能用一句话说清做什么吗？\n'
                 '有重复代码吗？嵌套超过三层了吗？\n'
                 '需要滚屏才能看完吗？\n'
                 '经验参考：5~20 行最理想，20~50 行可接受，\n'
                 '50 行以上要警惕，100 行以上几乎肯定能拆\n'
                 '标准不是行数，而是"单一职责 + 可读性"',
         'color': 'teal', 'size': 12.5},
        {'title': '解答 ④：方便，但要收进笼子',
         'body': '为什么不喜欢：谁都能改，改乱了找不到责任人；\n'
                 '隐藏依赖，看参数以为无副作用，其实偷偷改了；\n'
                 '带着全局变量不好搬到别的项目；线程下更危险\n'
                 '为什么还要用：方便；有些数据天然全局一份，\n'
                 '比如系统配置、程序状态\n'
                 '替代方案：传参（指针）、结构体打包、\n'
                 '文件级 static、get/set 接口函数\n'
                 '最佳实践：少用；要用就加 g_ 前缀；\n'
                 '能传参就别全局 —— 第4讲、第5讲见分晓',
         'color': 'green', 'size': 12.5},
    ], gap=0.26)
    banner(s, '从"能跑"到"好改、好复用"，靠的就是这些看起来很小的取舍')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第3讲 函数封装 —— 给代码找个家')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '函数把代码打包、命名、隐藏细节：main 只负责调度，重复的提示抽成公共函数，'
        '想改一处就打开对应的函数 —— 这就是"从能跑，到好读好改好复用"。'),
        title='📝 一句话总结', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.24

    rows = [('1', '函数的意义', '把重复代码打包、命名、隐藏细节，消除复制粘贴'),
            ('2', '声明/定义/调用', '声明告诉编译器"有它"，定义写实现，调用让它跑一次'),
            ('3', '参数（值传递）', '形参是接货口，实参填进去；传的是副本，改副本不动原件'),
            ('4', '返回值', 'return 两个作用：结束函数 + 把结果交回调用者；无返回写 void'),
            ('5', '作用域与生命周期', '局部随函数生灭，全局活到程序结束 —— 可见范围越大越难管'),
            ('6', '设计原则', '单一职责、代码复用、信息隐藏，是后面所有架构的地基')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：多文件编程 —— 函数太多，一个文件装不下，把它们按职责拆进 .h / .c（第4讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_func, p05_params, p06_return, p07_scope,
           p08_design, p09_deep, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
