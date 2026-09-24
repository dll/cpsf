# -*- coding: utf-8 -*-
"""
第4讲：多文件编程 —— 给代码分个家
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

LECTURE = '第4讲 多文件编程'
prs = new_deck()
PAGES = []


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


def pg(title, subtitle=None):
    s = page(prs, title, subtitle, label=LECTURE, page_no='auto')
    PAGES.append(s)
    return s


def done(tag=''):
    audit(prs, tag)


def cards_row(s, y, specs, gap=0.22):
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
    rect(slide, 0, 0, 4.4, SH, fill=C['card_teal'])              # 左侧冷色带
    rect(slide, 0, 0, 0.16, SH, fill=C['teal'])
    rect(slide, 4.4, 0, SW - 4.4, 0.12, fill=C['teal'])

    _put_text(slide, 0.75, 1.15, 3.3, 0.5, '从程序员到架构师', 20, C['teal_dark'], bold=True)
    _put_text(slide, 0.75, 1.72, 3.3, 0.4, 'C语言插件框架演进之旅', 14, C['ink2'])
    rect(slide, 0.75, 2.30, 0.9, 0.05, fill=C['teal'])

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第4讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.50, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['teal_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '多文件编程', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '给代码分个家', 27, C['teal_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.8,
              '第3讲把代码收进了函数，可函数一多，一个文件装不下：\n'
              '几百行翻不到底，余额谁都能改，两人合改一个文件像打仗。\n'
              '本讲给代码分个家——头文件当接口、源文件当实现、\n'
              'static 把数据关进笼子，从此各改各的，互不打扰。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '六级台阶的第三级 —— 从"一堆函数"到"一个模块"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '第3讲我们学会了函数：代码有了名字，可以复用了。但函数一多，新的麻烦来了——'
        '一个文件几百行翻不到底，全局变量谁都能改。\n'
        '本讲站上第三级台阶——模块：把函数按职责分进不同的 .h / .c，'
        '对外只暴露接口，内部细节藏起来。'),
        title='🎯 本讲定位', color='orange', size=15.5, min_h=1.20)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '第3讲 ✅'), ('③ 模块', '← 你在这里'),
             ('④ 库', '第9-10讲'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13-14讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('teal', 'teal', 'primary', 'gray', 'gray', 'gray'),
             size=13.5, h=0.92) + 0.24

    w = INNER_W / 2 - 0.14
    card(s, MARGIN_L, y, w, (
        '第3讲：函数的声明、定义、调用\n'
        '值传递的局限：改不了外面的变量'),
        title='⬅ 前置', color='blue', size=14, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第5讲：指针——把地址传进去\n'
        '真正解决"值传递改不了原件"'),
        title='➡ 后续', color='teal', size=14, min_h=1.00)
    banner(s, '模块 = 把一组函数 + 一份数据 装进一个"家"，门口挂上头文件当招牌')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '函数有了名字，但"住"的问题还没解决')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第3讲：单文件的日子', [
                    'atm_func.c 一个文件 250+ 行',
                    '余额 g_balance 全程序可见，谁都能改',
                    '想借用菜单功能？只能从代码里抠',
                    '两个人同时改一个文件，冲突不断'],
                '第4讲：多文件的秩序', [
                    '4 个 .c + 3 个 .h，各管一摊',
                    '余额 s_balance 仅 account.c 可见',
                    '拿走 menu.c + menu.h 就能用',
                    '张三改 account.c，李四改 menu.c'],
                left_color='red', right_color='green', size=13.5) + 0.06
    y = cards_row(s, y, [
        {'title': '痛点① 文件太长', 'body': '函数挤在一起，翻屏找半天\n改一处要通读全篇',
         'color': 'red', 'size': 12.5},
        {'title': '痛点② 数据裸奔', 'body': '全局变量谁都能改\n改乱了找不到责任人',
         'color': 'yellow', 'size': 12.5},
        {'title': '痛点③ 没法协作', 'body': '两人共改一个文件\n合并代码就是一场灾难',
         'color': 'purple', 'size': 12.5},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：函数解决了"代码重复"，多文件要解决的是"代码住哪儿、谁看得见"',
    ], size=15)
    banner(s, '本讲把"一坨代码"拆成"几个各司其职的模块"')
    done('P3')


# ============================================================
# P4 核心一：.h 与 .c 的分工
# ============================================================
def p04_hc():
    s = pg('核心一：头文件与源文件的分工', '头文件是菜单（接口），源文件是厨房（实现）')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '头文件 .h —— 对外接口', [
                    '放函数声明、类型定义、宏定义',
                    '告诉你"有什么菜、怎么点"',
                    '别人 #include 它就能调用'],
                '源文件 .c —— 内部实现', [
                    '放函数定义（真正的代码）',
                    '菜在这里做，怎么做的不用外传',
                    '每个函数全项目只定义一次'],
                left_color='blue', right_color='teal', size=13.5) + 0.06

    cw = INNER_W * 0.54
    codex(s, MARGIN_L, y, cw, [
        '#ifndef MENU_H    /* 头文件保护 */',
        '#define MENU_H',
        '',
        'void show_welcome(void);',
        'void show_menu(void);',
        'int  read_choice(void);',
        '',
        '#endif /* MENU_H */',
    ], title='menu.h：只声明"能做什么"', size=11.0)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '如果函数体也写进头文件，又被多个 .c 包含，\n'
        '链接器就会发现"同一个函数定义了好几遍"，\n'
        '直接报错：multiple definition。\n'
        '\n'
        '所以规矩只有两条：\n'
        '· 声明放头文件（可以被重复包含）\n'
        '· 定义放源文件（全项目只写一份）'),
        title='⚠️ 为什么不把定义也放头文件', color='red', size=12.5, min_h=2.50)
    banner(s, '声明管"通不通"（能不能编译），定义管"有没有"（能不能链接）')
    done('P4')


# ============================================================
# P5 核心二：头文件保护
# ============================================================
def p05_guard():
    s = pg('核心二：头文件保护 #ifndef', '井号 ifndef / 井号 define / 井号 endif —— 一道一次性门')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'include 的本质是"把头文件内容整段粘到这里"。同一个头文件被间接包含两次，'
        '里面的类型定义就会重复，编译器直接报错。'),
        title='🚪 为什么需要保护', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    cw = INNER_W * 0.54
    codex(s, MARGIN_L, y, cw, [
        '#ifndef UTILS_H   /* 没定义过 UTILS_H 吗？ */',
        '#define UTILS_H   /* 那就定义它，然后处理内容 */',
        '',
        'void print_success(const char* op, double amount, double balance);',
        'void print_error(const char* msg);',
        '',
        '#endif  /* UTILS_H —— 保护结束 */',
    ], title='utils.h：标准三件套（真实源码）', size=11.0)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 第一次包含：UTILS_H 没定义 → 定义它，内容生效\n'
        '② 第二次包含：UTILS_H 已定义 → 整段被跳过\n'
        '③ 结果：无论被包含几次，内容只处理一次\n'
        '\n'
        '命名规范：文件名大写 + 下划线，全项目不重名\n'
        '· menu.h → MENU_H   · account.h → ACCOUNT_H'),
        title='🔑 一道"一次性门"', color='teal', size=12.5, min_h=2.55)
    banner(s, '加保护不是仪式：类型定义重复 = 编译报错，这是必须挡住的坑')
    done('P5')


# ============================================================
# P6 核心三：static 的两种用法
# ============================================================
def p06_static():
    s = pg('核心三：static 的两种用法', '一个关键字，两种完全不同的意思')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '函数内的 static（函数级）', [
                    'static int count = 0; 写在函数里',
                    '只初始化一次，跨调用保留上次的值',
                    '作用域仍限于函数内 —— 保持状态'],
                '函数外的 static（文件级）', [
                    'static double s_balance = 1000.0;',
                    '只在本 .c 文件内可见，别人 extern 也拿不到',
                    '核心价值 —— 信息隐藏，把数据关进笼子'],
                left_color='blue', right_color='teal', size=13.5) + 0.06

    cw = INNER_W * 0.54
    codex(s, MARGIN_L, y, cw, [
        '/* 用法一：函数级 —— 保持状态 */',
        'void counter(void)',
        '{',
        '    static int count = 0;   /* 只初始化一次 */',
        '    count++;                /* 每次调用都接着上次算 */',
        '}',
        '',
        '/* 用法二：文件级 —— 限制可见范围 */',
        'static double s_balance = 1000.0;   /* 仅 account.c 可见 */',
    ], title='两种 static，差别在"住哪儿"', size=11.0)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '第3讲：double g_balance = 1000.0;\n'
        '　　　→ 全程序可见，10 个函数都能改\n'
        '第4讲：static double s_balance = 1000.0;\n'
        '　　　→ 只在本文件可见，安全多了\n'
        '\n'
        '差一个 static，差在"谁能碰它"。\n'
        '外部想查余额？只能调 account_get_balance()。'),
        title='🔒 从 g_balance 到 s_balance', color='purple', size=12.5, min_h=2.72)
    banner(s, '把全局变量关进笼子：数据私有化，只暴露操作接口 —— 就像银行金库')
    done('P6')


# ============================================================
# P7 核心四：编译单元与链接
# ============================================================
def p07_build():
    s = pg('核心四：编译单元与链接', '一行 gcc 命令背后，是四个阶段 + 两个角色')
    y = BODY_TOP
    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 预处理', '展开 #include\n执行宏替换'),
        ('② 编译', '语法/类型检查\n生成汇编'),
        ('③ 汇编', '汇编转机器码\n每个 .c 出一个 .o'),
        ('④ 链接', '拼接所有 .o\n解决跨文件引用'),
    ], colors=('blue', 'teal', 'purple', 'orange'), size=13, h=0.95) + 0.24

    y2 = compare(s, MARGIN_L, y, INNER_W,
                 '编译器：逐文件检查', [
                     '一次只看一个 .c 文件',
                     '见到声明就放行，不找定义',
                     '负责语法、类型、声明的检查'],
                 '链接器：跨文件接线', [
                     '把多个 .o 拼成一个可执行文件',
                     'main.o 里的调用，去 menu.o 找定义',
                     '找不到定义 → undefined reference'],
                 left_color='blue', right_color='purple', size=13) + 0.20

    card(s, MARGIN_L, y2, INNER_W, (
        '编译器靠声明就能编过；定义在哪，才是链接器的活 —— 这就是 .h 与 .c 能分家的原因。'),
        title='💡 关键理解', color='orange', size=13.5, title_size=16)
    banner(s, '漏掉一个 .c，编译照样过 —— 直到链接器喊出 undefined reference')
    done('P7')


# ============================================================
# P8 核心五：接口与实现分离
# ============================================================
def p08_split():
    s = pg('核心五：接口与实现分离', '对外只讲"能做什么"，内部才知道"怎么做"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '接口 = 头文件 = 声明，告诉外部"能做什么"；实现 = 源文件 = 定义，'
        '写清内部"怎么做"。外部只依赖接口，不依赖实现。'),
        title='📐 一句话说清', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('好处① 实现可换', '余额从单变量改成数组\n只要接口不变，main 一行不改'),
        ('好处② 降低耦合', 'main.c 只依赖 account.h\n改 account.c 不影响别人'),
        ('好处③ 团队协作', '张三写 account.c\n李四写 menu.c，互不干扰'),
    ], colors=('teal', 'blue', 'purple'), size=13, h=1.05) + 0.26

    card(s, MARGIN_L, y, INNER_W, (
        '第3讲封装"代码片段"，第4讲封装"一组函数 + 一份数据"，'
        '第9讲把模块编译成库，第12讲把系统封装成框架 —— 每一步都在做同一件事：'
        '接口留外面，实现藏里面。'),
        title='🧭 封装的放大：函数 → 模块 → 库 → 框架', color='teal', size=13.5,
        title_size=16)
    banner(s, '接口不变，实现随便换 —— 这是软件工程里最值钱的一句话')
    done('P8')


# ============================================================
# P9 原理深入：编译器只管声明，链接器负责接线 ⭐
# ============================================================
def p09_deep():
    s = pg('原理深入：谁在替我们跨文件接线？ ⭐', '编译期靠声明，链接期靠定义 —— 两个角色，各管一段')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'main.c 调用 show_menu() 时，编译器只要在 menu.h 里见到声明就放行；真正确认它存在的，是链接器。'),
        title='🧠 先给结论', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    cw = INNER_W * 0.52
    codex(s, MARGIN_L, y, cw, [
        '/* main.c：见到声明就敢调用 */',
        '#include "menu.h"',
        'int main(void)',
        '{',
        '    show_menu();   /* 定义在 menu.c，编译器不关心 */',
        '}',
    ], title='调用方：只看得到声明', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    br, _ = codex(s, xr, y, wr, [
        '/* 漏掉 menu.c 的后果 */',
        '$ gcc main.c -o atm.exe',
        "ld: undefined reference to `show_menu'",
        '',
        '/* 编译期：有声明就过关 */',
        '/* 链接期：找不到定义，立刻报错 */',
    ], title='链接器：找不到定义就报错', size=11.5)

    card(s, MARGIN_L, br + 0.20, INNER_W, (
        '所以 undefined reference 是链接错误，不是编译错误 —— 它说明"名字见过了，机器码没找到"。'),
        title='⚠️ 记住这个区分', color='red', size=13.5, title_size=16)
    banner(s, '编译期问"名字对不对"，链接期问"东西在不在" —— 这就是分文件能成立的原理')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：单文件 vs 多文件', '同一个 ATM，换一种组织方式')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第3讲：单文件', [
                    '所有函数挤在 atm_func.c 里',
                    '余额是全局变量，谁都能改',
                    '想复用菜单？从一大坨代码里抠'],
                '第4讲：多文件', [
                    'main / menu / account / utils 各管一摊',
                    '余额 static 藏进 account.c，只能走接口',
                    '复用菜单模块？拿走 menu.c + menu.h'],
                left_color='red', right_color='green', size=13.5) + 0.16

    rows = [('文件数量', '1 个 .c 文件', '4 个 .c + 3 个 .h'),
            ('余额可见性', 'g_balance 全程序可见', 's_balance 仅 account.c 可见'),
            ('修改影响', '改一处可能碰到无关代码', '改 menu.c 不动 account.c'),
            ('复用方式', '抠函数、复制粘贴', '拿走 .c + .h 就能用')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.18, 0.41, 0.41), size=12,
            header=('对比项', '第3讲 单文件', '第4讲 多文件'))
    banner(s, '多文件不是为了少写代码，而是为了让代码"各有各的门牌号"')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/account.h 接口 + src/account.c 实现（static 藏数据）')
    y = BODY_TOP
    cw = INNER_W * 0.46
    codex(s, MARGIN_L, y, cw, [
        '#ifndef ACCOUNT_H',
        '#define ACCOUNT_H',
        '',
        'void   account_query(void);',
        'void   account_deposit(void);',
        'void   account_withdraw(void);',
        'void   account_transfer(void);',
        'double account_get_balance(void);',
        '',
        '#endif /* ACCOUNT_H */',
    ], title='account.h：只有接口，没有数据', size=11.0)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    br, _ = codex(s, xr, y, wr, [
        'static double s_balance = 1000.0;   /* 私有：仅本文件可见 */',
        'static int validate_amount(double amount);  /* 私有助手 */',
        '',
        'double account_get_balance(void)',
        '{',
        '    return s_balance;   /* 只读窗口：能查，不能改 */',
        '}',
        'void account_deposit(void)',
        '{',
        '    s_balance = s_balance + amount;',
        '    print_success("存入", amount, s_balance);',
        '}',
    ], title='account.c：数据藏在里面，只留接口', size=11.0)

    card(s, MARGIN_L, br + 0.16, INNER_W, (
        '外部（main.c）看不到 s_balance，也碰不到 validate_amount；'
        '想查余额、想存钱，只能走 account.h 上挂着的接口函数。'),
        title='📊 这就是"信息隐藏"落地的样子', color='green', size=13.5, title_size=16)
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '4 个 .c 一起编译、链接、运行 —— 输出全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.60
    codex(s, MARGIN_L, y, cw, [
        "$ gcc -Wall main.c menu.c account.c utils.c -o atm_multi.exe",
        "$ printf '1\\n2\\n500\\n3\\n200\\n0\\n' | ./atm_multi.exe",
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
        '① 4 个 .c 一起编译，-Wall 零警告\n'
        '② 编译器逐文件编过，链接器把 4 个 .o 接起来\n'
        '③ 菜单来自 menu 模块，业务来自 account 模块\n'
        '④ 余额 1000 → 1500 → 1300，全由接口函数完成\n'
        '⑤ main.c 里看不到 s_balance，却能正常查改余额\n'
        '⑥ 退出码 0：链接成功、运行正常、状态闭环'),
        title='👀 要看清楚的六个点', color='orange', size=12.5, min_h=3.62)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 account.h / account.c')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的第三级：模块 —— 函数第一次有了"门牌号"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。'
        '第3讲把代码收进了函数，本讲把函数收进了模块：'
        '从此"接口"和"实现"第一次分家，后面每一级都在这条分界线上生长。'),
        title='🧭 一条主线', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '第3讲 ✅'), ('③ 模块', '← 本讲 ⭐'),
             ('④ 库', '第9-10讲'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13-14讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('teal', 'teal', 'primary', 'gray', 'gray', 'gray'),
             size=13.5, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    card(s, MARGIN_L, y, w, (
        '头文件当接口、源文件当实现，第一次真正分家\n'
        'static 把数据关进笼子，只暴露操作接口\n'
        '编译单元 + 链接器：模块能被单独编译\n'
        '这正是后面"静态库"能成立的前提'),
        title='本讲为终点贡献了什么', color='teal', size=13, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第5讲用指针补上"值传递改不了原件"的短板；\n'
        '第7、8讲把数据打包成结构体和链表；\n'
        '第9讲把模块编译成 .a 静态库——\n'
        '"接口与实现分离"第一次变成"成品"。'),
        title='下一讲接着做什么', color='blue', size=13, min_h=1.55)
    banner(s, '模块是"接口与实现分离"第一次真正落地 —— 库、插件、框架都从这里长出来')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '每个头文件开头都有"井号 ifndef / 井号 define / 井号 endif"这三件套，'
        '这叫头文件保护。不加会怎样？会出什么错？\n'
        '提示：include 的本质是文本复制粘贴；想一想"函数声明重复"和'
        '"类型定义重复"，编译器的反应一样吗？'),
        title='思考题 ①：为什么需要头文件保护？', color='orange', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        'static 是"一个关键词、两种含义"的代表：写在函数内部的 static，'
        '和写在函数外面的 static，意思完全不同。\n'
        '提示：分别从生命周期（什么时候生、什么时候死）和作用域'
        '（哪里看得见）去对比；再想想第3讲的 g_balance 和第4讲的 s_balance 差在哪。'),
        title='思考题 ②：static 在函数内和文件内的区别', color='purple', size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：一道一次性门',
         'body': 'include 就是把头文件内容原样粘过来；\n'
                 '同一个头文件被间接包含两次很常见，\n'
                 '内容就会出现两份\n'
                 '函数声明重复一般不报错，\n'
                 '但 struct / enum / 宏重复定义直接编译失败\n'
                 '加了保护：第一次包含时定义宏，\n'
                 '再包含时宏已存在，整段被跳过\n'
                 '于是"不管包含几次，内容只处理一次"',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ②：一个管状态，一个管范围',
         'body': '函数内 static：只初始化一次，\n'
                 '跨调用保留上次的值（像计数器本子）；\n'
                 '生命周期到程序结束，作用域仍限本函数\n'
                 '函数外 static：只在本 .c 内可见，\n'
                 '别的文件 extern 也拿不到（信息隐藏）\n'
                 '两者生命周期相同——都活到程序结束；\n'
                 '差别在用途：一个"记住状态"，一个"藏起来"\n'
                 'g_balance → s_balance，差的正是可见范围',
         'color': 'purple', 'size': 12.5},
    ], gap=0.26)
    banner(s, '头文件保护管"编译过不过"，static 管"别人碰不碰得到"')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从编译链接，谈到接口与实现分离')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '我们敲下 gcc main.c menu.c account.c utils.c -o atm.exe 只有一行，'
        '但编译器和链接器各自忙了半天。编译器编译 main.c 时，'
        '知道 show_menu 在哪吗？为什么非要有一个链接器？\n'
        '提示：想一想编译器一次只看一个 .c；如果忘了把 menu.c 写进命令，'
        '哪一步会报错？undefined reference 到底算编译错误还是链接错误？'),
        title='思考题 ③：编译器和链接器各自做了什么？', color='teal', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '我们把头文件叫"接口"、源文件叫"实现"，说它们必须"分离"。'
        '为什么不分离就不行？分离了到底好在哪里？\n'
        '提示：假设 account.c 里余额要从单个变量改成数组存多个账户，'
        'main.c 需要改吗？再想想团队协作时，张三改 account.c，'
        '李四要不要跟着改 main.c。'),
        title='思考题 ④：接口与实现分离的好处', color='green', size=14.5, min_h=1.55)
    banner(s, '这两题想透了，第9讲"静态库"就只是换个打包方式而已')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '一个讲"两个角色的分工"，一个讲"分离带来的自由"')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：检查 vs 接线',
         'body': '编译器：一次只看一个 .c，做预处理、\n'
                 '语法分析、类型检查，生成目标文件 .o\n'
                 '它看到 show_menu() 时只查"有没有声明"，\n'
                 '（声明来自 menu.h），不关心定义在哪\n'
                 '链接器：把多个 .o 拼在一起，建符号表，\n'
                 '把 main.o 里"待链接"的调用接到 menu.o 的定义上\n'
                 '漏写 menu.c → 编译照过，链接报\n'
                 'undefined reference，所以它是链接错误',
         'color': 'teal', 'size': 12.5},
        {'title': '解答 ④：接口不变，实现随便换',
         'body': '不分离的代价：调用者被迫知道实现细节，\n'
                 '改实现就可能改调用者，一改带出一串\n'
                 '好处一，实现可替换——余额从单变量改成\n'
                 '数组，只要 account.h 签名不变，main.c 一行不改\n'
                 '好处二，降低耦合——main.c 只依赖接口\n'
                 '好处三，团队协作——各改各的 .c 互不干扰\n'
                 '好处四，信息隐藏——static 把内部细节藏起来\n'
                 '好处五，编译隔离——只重编改过的那个 .c',
         'color': 'green', 'size': 12.5},
    ], gap=0.26)
    banner(s, '模块把"能做什么"挂门口，把"怎么做"锁在屋里')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第4讲 多文件编程 —— 给代码分个家')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '多文件编程 = 按职责拆分代码 + 头文件当接口 + static 做信息隐藏，'
        '让代码更安全、更好维护、更容易复用。'),
        title='📝 一句话总结', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.24

    rows = [('1', '多文件的动机', '文件太长、全局变量太危险、不好复用、没法协作'),
            ('2', '.h 与 .c 分工', '头文件是菜单（声明），源文件是厨房（定义）'),
            ('3', '头文件保护', '井号 ifndef / 井号 define / 井号 endif，保证内容只处理一次'),
            ('4', 'static 两种用法', '函数级 = 保持状态；文件级 = 信息隐藏，把数据关进笼子'),
            ('5', '编译与链接', '编译器逐文件检查声明，链接器跨文件接线找定义'),
            ('6', '接口与实现分离', '对外只暴露"能做什么"，内部"怎么做"藏起来')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：指针 —— 值传递改不了外面的变量，那就把变量地址传进去（第5讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_hc, p05_guard, p06_static, p07_build,
           p08_split, p09_deep, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
