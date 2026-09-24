# -*- coding: utf-8 -*-
"""
第9讲：静态库 —— 把代码打包成工具箱
generate_ppt.py（新规范版，18 页）

依赖统一工具箱 tools/ppt_kit.py：
    · 标题单行自适应（R1）——投影时标题绝不换行
    · 容器不叠压、文字不越界、装饰永在底层（R2）——不再"前后不分"
    · 全部正文对比度 ≥ 4.5:1，代码一律深底亮字（R3）——投影看得清
每画完一页立刻 done('PN') 质检，有问题直接报错，绝不产出坏 PPT。

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
    BODY_TOP, BODY_BOTTOM, SW, SH, MARGIN_R, TITLE_TOP, fit_size, text_width_in, \
    _put_text, _reg_text, _reg_container, _reset_reg

LECTURE = '第9讲 静态库'
prs = new_deck()
PAGES = []


def pg(title, subtitle=None):
    s = page(prs, title, subtitle, label=LECTURE, page_no='auto')
    PAGES.append(s)
    return s


def done(tag=''):
    audit(prs, tag)


def cards_row(s, y, specs, gap=0.22):
    """等宽一行卡片。specs: [{'title','body','color','size','min_h'}]，按真实高度推进。"""
    n = len(specs)
    w = (INNER_W - gap * (n - 1)) / n
    bottoms = []
    for i, sp in enumerate(specs):
        b, _ = card(s, MARGIN_L + i * (w + gap), y, w, sp['body'],
                    title=sp.get('title'), color=sp.get('color', 'orange'),
                    size=sp.get('size', 16), title_size=sp.get('title_size', 18),
                    min_h=sp.get('min_h', 0.0))
        bottoms.append(b)
    return max(bottoms)


def cards_col(s, x, y, w, specs, gap=0.22, size=15):
    """纵向堆叠卡片，返回底部 y。"""
    for sp in specs:
        b, _ = card(s, x, y, w, sp['body'], title=sp.get('title'),
                    color=sp.get('color', 'orange'), size=sp.get('size', size),
                    title_size=sp.get('title_size', 18),
                    min_h=sp.get('min_h', 0.0))
        y = b + gap
    return y - gap


def code_h(n_lines, size, title=None):
    """手工推算 code 块高度（用于在它下方继续排内容）。"""
    head = 0.40 if title else 0.0
    return head + 0.36 + size * 1.42 / 72.0 * n_lines


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

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第9讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.55, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '静态库', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '把代码打包成工具箱', 27, C['primary_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.6,
              '第4讲把 ATM 拆成多个文件，编译却要一次次重来：\n'
              '重复编译、不便分发、命令冗长、源码全暴露。\n'
              '本讲请出 ar 工具，把一堆 .o 打包成一个 .a，\n'
              '别人只拿头文件和库就能用——实现藏在里面。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '六级台阶的第四级 —— 库，第一次把"编译好的二进制"当零件复用')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '前八讲，我们一直在"往上搭"：表达式、函数、模块，一级比一级抽象，'
        '但代码始终以"源文件"的形式在项目之间流转。\n'
        '本讲站上第四级——库。从这一级起，复用的单位不再是源码，'
        '而是编译好的目标文件；别人拿到的只是接口，不是实现。'),
        title='🎯 本讲定位', color='orange', size=15.5, min_h=1.15)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '第3讲 ✅'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '← 你在这里'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('gray', 'gray', 'gray', 'primary', 'gray', 'gray'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第4讲：头文件分离了接口与实现\n'
        '第5~8讲：指针 / 数组 / 结构体 / 链表'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第10讲：动态库，让多个程序共享一份代码\n'
        '第11讲：运行时加载，插件雏形登场'),
        title='➡ 后续', color='teal', size=14.5, min_h=1.00)
    banner(s, '本讲把多个 .o 封成一个 .a：复用从"源码级"升级为"二进制级"')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '第4讲的多文件编程，撑不起"跨项目复用"')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第4讲：已经做到的', [
                    '头文件分离接口与实现，模块化初成',
                    '用 gcc 一次编译多个 .c 源文件',
                    '改动一个 .c，重编全部源文件'],
                '第9讲：要补上的', [
                    '把编译好的 .o 打包成一个 .a 归档',
                    '只用 main.c + .h + .a 就能构建',
                    '不给源码也能用：实现藏在库里'],
                left_color='blue', right_color='green', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '痛一：重复编译', 'body': 'account.c 没改过\n也要跟着重编一遍',
         'color': 'red', 'size': 13},
        {'title': '痛二：不便分发', 'body': '想给别人用账户模块\n得给一堆 .c 源文件',
         'color': 'purple', 'size': 13},
        {'title': '痛三：命令冗长', 'body': '文件越多\ngcc 后面跟的名字越长',
         'color': 'yellow', 'size': 13},
        {'title': '痛四：无法保密', 'body': '给源码 = 给全部实现\n知识产权保不住',
         'color': 'orange', 'size': 13},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：代码想跨项目复用，却只能以"源码"形式交付，重编、冗长、还泄密',
    ], size=15)
    banner(s, '本讲用 ar 打一个包，同时填掉这四个坑')
    done('P3')


# ============================================================
# P4 核心内容一：静态库是什么
# ============================================================
def p04_concept():
    s = pg('静态库是什么：把 .o 收进一个工具箱', '静态库 = 把多个目标文件(.o)打包成一个归档文件(.a)')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '编译到"汇编"这一步，每个 .c 都会变成一个 .o 目标文件——里面的机器码已经生成，'
        '只差最后一步"把地址接上"。\n'
        '静态库做的事非常朴素：把这堆 .o 原封不动地装进一个文件，'
        '再配一张"谁在哪个 .o 里"的索引表。'),
        title='📌 先想清楚：一个 .o 已经能用了，为什么还要打包', color='orange', size=15, min_h=1.05)
    y = y2 + 0.24

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 编译各模块', 'gcc -c 逐个\n.c → .o'),
        ('② ar 打包', 'ar rcs 合成\nlibaccount.a'),
        ('③ 编译主程序', 'gcc -c main.c\n→ main.o'),
        ('④ 链接', '-L. -laccount\n复制代码进 exe'),
    ], colors=('blue', 'teal', 'purple', 'orange'), size=15, h=1.05) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        'Linux / MinGW 下叫 libaccount.a\n'
        'MSVC 下叫 account.lib\n'
        '归档格式不同，思路完全一样'),
        title='🖥️ 与平台有关', color='blue', size=13.5, min_h=1.20)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '命名规则：lib + 名字 + .a\n'
        '链接时写 -laccount，gcc 自动补全为\n'
        'libaccount.a，少写多省事'),
        title='🔖 命名规则', color='teal', size=13.5, min_h=1.20)
    banner(s, '静态库不产生新代码，它只是把已经编好的 .o 装进一个盒子')
    done('P4')


# ============================================================
# P5 核心内容二：ar rcs 三个参数
# ============================================================
def p05_ar():
    s = pg('ar rcs：三个字母各有分工', 'r 插入替换 / c 静默创建 / s 建立符号索引，缺一个都别扭')
    y = BODY_TOP
    cw = INNER_W * 0.52
    rows = [('r · replace', '把 .o 插入归档；同名成员直接替换'),
            ('c · create', '归档不存在时静默创建，不弹警告'),
            ('s · symbol', '写入符号索引表，链接器可快速定位')]
    kv_rows(s, MARGIN_L, y, cw, rows, widths=(0.26, 0.74), size=12.5,
            header=('参数', '作用'))

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '$ ar rcs libaccount.a account.o transaction.o',
        '',
        '/* 不加 s：也能生成库，但库里没有索引表 */',
        '$ ar rcs libaccount.a account.o transaction.o',
        '  → libaccount.a（缺符号索引）',
        '$ gcc -o atm main.o -L. -laccount',
        '  → 链接器只能逐个 .o 线性查找，',
        '    慢；旧版链接器甚至报',
        '    "no symbol table" 直接失败',
    ], title='加 s / 不加 s 的区别', size=11)
    y = y + code_h(9, 11, 'x') + 0.24

    card(s, MARGIN_L, y, INNER_W, (
        's 省掉的是链接器的麻烦：有索引表，链接器一眼就知道 '
        'account_create 在 account.o 里；没有索引，只能把每个成员翻一遍。'
        'ranlib 命令等价于补建索引，ar rcs 的 s 就是顺手把它做了。'),
        title='💡 为什么偏偏是 s 这么重要', color='red', size=14, min_h=1.05)
    banner(s, 'r 管放进去，c 管静静建，s 管查得快 —— 三个字母少一个都不顺手')
    done('P5')


# ============================================================
# P6 核心内容三：归档里到底装了什么
# ============================================================
def p06_inside():
    s = pg('归档里到底装了什么：ar t 与 nm', '一张表看清 .a 的内部；两条命令随时验货')
    y = BODY_TOP
    cw = INNER_W * 0.50
    code(s, MARGIN_L, y, cw, [
        'libaccount.a  （归档文件）',
        '┌────────────────────────────────┐',
        '│ 归档头：成员名 + 偏移            │',
        '├────────────────────────────────┤',
        '│ account.o                      │',
        '│   account_create / _deposit    │',
        '│   account_withdraw / _find     │',
        '│   static accounts[]            │',
        '├────────────────────────────────┤',
        '│ transaction.o                  │',
        '│   transaction_deposit / _transfer',
        '├────────────────────────────────┤',
        '│ 符号索引表（ar s 生成）          │',
        '└────────────────────────────────┘',
    ], title='libaccount.a 内部结构', size=11)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    y2 = y
    code(s, xr, y2, wr, [
        '$ ar t libaccount.a      # 看有哪些成员',
        'account.o',
        'transaction.o',
        '',
        '$ nm libaccount.a        # 看导出了哪些符号',
        'account.o:',
        '0000...05c9 T account_count',
        '0000...1c20 b account_count_val',
        '0000...0000 T account_create',
        '0000...01e9 T account_deposit',
    ], title='两条验货命令（真实输出）', size=11)
    y2 = y2 + code_h(10, 11, 'x') + 0.22
    card(s, xr, y2, wr, (
        'T 表示导出的函数（Text 段），b 表示文件级 static 数据。'
        '名字带 static 的 accounts[] 不会出现在 T 里——外部拿不到它。'),
        title='🔍 怎么看符号表', color='purple', size=12.5, min_h=1.35)
    banner(s, '界面（T 符号）露在外面，实现（static 数据）锁在 .a 里面')
    done('P6')


# ============================================================
# P7 核心内容四：静态链接原理
# ============================================================
def p07_link():
    s = pg('静态链接：链接器怎么把代码接上', 'main.o 带着一串"未定义符号"找上库，库把对应的 .o 交出来')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'main.o 里对 account_create 只有"调用"、没有"定义"，于是留下一个未定义符号（U）。'
        '链接器的任务就是拿这个 U 去库里换回一份定义（T），改对地址，合成可执行文件。'),
        title='🧭 一句话说清链接在干什么', color='blue', size=14.5, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.62
    code(s, MARGIN_L, y, cw, [
        'main.o                    libaccount.a',
        '┌────────────┐            ┌─────────────────┐',
        '│ main()     │  查符号    │ account.o  T:   │',
        '│ U account_ │ ────────> │  account_create │',
        '│   create   │           │  account_deposit│',
        '│ U account_ │           │ transaction.o   │',
        '│   deposit  │           │  transaction_*  │',
        '└─────┬──────┘           └────────┬────────┘',
        '      │    复制定义所在的 .o 代码    │',
        '      └───────────┬──────────────┘',
        '                  ▼  atm_static.exe（自带库代码）',
    ], title='链接器工作示意（U = 未定义，T = 已定义）', size=10.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '① 收集未定义符号', 'body': '扫 main.o，记录所有 U',
         'color': 'blue', 'size': 12.5, 'title_size': 13.5, 'min_h': 0.85},
        {'title': '② 到库里查索引', 'body': '靠 ar s 建的索引定位 .o',
         'color': 'teal', 'size': 12.5, 'title_size': 13.5, 'min_h': 0.85},
        {'title': '③ 复制并重定位', 'body': '搬代码、改地址、写 exe',
         'color': 'orange', 'size': 12.5, 'title_size': 13.5, 'min_h': 0.85},
    ], gap=0.16)
    banner(s, '链接 = 把"引用"换成"定义"，把分散的 .o 拼成一个自洽的可执行文件')
    done('P7')


# ============================================================
# P8 核心内容五：优缺点
# ============================================================
def p08_pros_cons():
    s = pg('静态库的优点与代价', '执行快、部署简单、能保护实现；但体积大、内存重复、更新要重链')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '优点', [
                    '执行快：代码已在 exe 里，无加载开销',
                    '部署简单：一个 exe 走天下，不怕缺库',
                    '兼容好：不受目标机器库版本影响',
                    '能保密：只给 .a + .h，不给 .c 源码'],
                '代价', [
                    '体积大：每个程序都复制一份库代码',
                    '内存重复：多进程同时跑，各占一份',
                    '更新麻烦：库修 bug，全部程序重链',
                    '无法热更：程序跑着不能换库的代码'],
                left_color='green', right_color='red', size=13.5) + 0.14
    y = kv_rows(s, MARGIN_L, y, INNER_W, [
        ('适合', '小型项目、嵌入式、对启动与性能极敏感、交付单文件的场景'),
        ('不适合', '库会被频繁更新、多个程序想共享同一份库代码的大型系统'),
    ], widths=(0.14, 0.86), size=12.5, header=('判断', '什么时候该用静态库'))[0]
    banner(s, '一句话：静态库用"重复一份"换来"简单可靠"——那能不能不重复？')
    done('P8')


# ============================================================
# P9 原理深入：复制粒度与代码副本 ⭐
# ============================================================
def p09_deep():
    s = pg('原理深入：链接器到底搬走了多少？ ⭐', '提取的粒度是目标文件，不是单个函数 —— 这正是静态库的要害')
    y = BODY_TOP
    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        '/* account.o 里有 1 个函数被用到 */',
        'account_create()   ← main 调用',
        'account_find()     ← 没人调用',
        'account_withdraw() ← 没人调用',
        '... 共 7 个函数',
        '',
        '/* 链接结果：整个 account.o 被复制 */',
        'atm_static.exe 里同时躺着 7 个函数',
        '其中 6 个永远不会被执行（死代码）',
    ], title='粒度是 .o，不是函数', size=11.5)
    cards_col(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, [
        {'title': '① 没被用到的 .o 不进来',
         'body': '库里的 transaction.o 若无人调用，\n根本不会进入 exe', 'color': 'green', 'size': 12.5},
        {'title': '② 用到 1 个函数，整份 .o 进来',
         'body': '链接器不拆目标文件内部，\n同 .o 里的"死代码"一并搬走',
         'color': 'orange', 'size': 12.5},
        {'title': '③ 每个程序各复制一份',
         'body': '3 个程序链接同一个库，\n磁盘 3 份、内存 3 份',
         'color': 'red', 'size': 12.5},
    ], gap=0.14)
    banner(s, '"每个程序自带一份副本"—— 下一讲动态库要解决的，正是这个问题')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：静态库 vs 动态库', '链接时复制代码，还是运行时共享代码？')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '静态库 libaccount.a', [
                    '链接时把用到的代码复制进 exe',
                    '运行时不再需要库文件',
                    '换库 = 重新链接每个程序'],
                '动态库 libaccount.dll（下一讲）', [
                    '链接时只记下"我要用哪个函数"',
                    '运行时才把代码加载 / 共享到内存',
                    '换库 = 直接替换那一个文件'],
                left_color='blue', right_color='purple', size=14) + 0.14

    kv_rows(s, MARGIN_L, y, INNER_W, [
        ('代码副本', '每个 exe 一份', '磁盘一份，多进程共享'),
        ('更新库', '所有程序重新链接', '替换库文件即可，无需重编'),
        ('部署', '只需 exe，最省心', 'exe + 库文件，缺一不可'),
        ('启动开销', '零加载开销', '启动要解析、加载符号'),
    ], widths=(0.16, 0.42, 0.42), size=12,
        header=('维度', '静态库', '动态库'))
    banner(s, '一句话分界：静态 = 链接时复制代码；动态 = 运行时共享代码')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/account.c 打包装库，src/main.c 只用头文件调用')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        '/* account.c —— 会被打包进 libaccount.a */',
        'static Account accounts[MAX_ACCOUNTS];  /* 内部数据 */',
        'static int next_id = 1001;              /* 外部看不见 */',
        'int account_create(const char *name, double initial_balance)',
        '{',
        '    Account *acc = &accounts[account_count_val];',
        '    acc->id = next_id++;',
        '    strncpy(acc->name, name, MAX_NAME_LEN - 1);',
        '    printf("[开户] ID:%d  户名:%s\\n", acc->id, acc->name);',
        '    return acc->id;',
        '}',
    ], title='account.c 关键片段（实现藏在库里）', size=11)
    y2 = y + code_h(11, 11, 'x') + 0.22
    card(s, MARGIN_L, y2, cw, (
        'account.h 里只有函数声明，没有一行实现。给客户时，account.c 不必出门。'),
        title='📄 account.h：只暴露接口', color='teal', size=12.5,
        title_size=14, min_h=0.90)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '/* main.c —— 不需要账户/交易模块源码 */',
        '#include "account.h"',
        '#include "transaction.h"',
        'int main(void) {',
        '    int id1 = account_create("张三", 1000.0);',
        '    int id2 = account_create("李四", 2000.0);',
        '    transaction_deposit(id1, 500.0);',
        '    transaction_transfer(id1, id2, 300.0);',
        '    account_list_all();',
        '    return 0;',
        '}',
    ], title='main.c：只需 include 头文件', size=11)
    demo_frame(s, xr, y + code_h(11, 11, 'x') + 0.22, wr, 1.30,
               title='构建四步（真实执行）',
               lines=['$ gcc -c account.c transaction.c',
                      '$ ar rcs libaccount.a account.o transaction.o',
                      '$ gcc -c main.c',
                      '$ gcc -o atm_static main.o -L. -laccount'])
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '从 .c 到 .a 再到 exe，命令与输出全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.62
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall -c account.c -o account.o',
        '$ gcc -Wall -c transaction.c -o transaction.o',
        '$ ar rcs libaccount.a account.o transaction.o',
        '$ ar t libaccount.a',
        'account.o',
        'transaction.o',
        '$ gcc -c main.c -o main.o',
        '$ gcc -o atm_static main.o -L. -laccount',
        '$ ./atm_static.exe',
        '=== ATM静态库版初始化 ===',
        '[开户] ID:1001  户名:张三  余额:1000.00',
        '[开户] ID:1002  户名:李四  余额:2000.00',
        '[转账] 1001 -> 1003  金额:300.00',
        '--- ATM 主菜单：请选择: 0',
        '感谢使用ATM静态库版，再见！',
        '$ echo $?   →   0',
    ], title='终端实录（真实输出，节选）', size=11)

    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译产物：account.o、transaction.o 两个目标文件\n'
        '② 打包：ar t 列出的两个成员，就是库的全部内容\n'
        '③ 链接：-L. 指定当前目录，-laccount 指向 libaccount.a\n'
        '④ 运行：初始化开户与转账全部由库函数完成\n'
        '⑤ 主程序里没有一行账户 / 交易的实现\n'
        '⑥ 退出码 0：exe 自带库代码，删掉 .a 也照跑'
        ),
        title='👀 要看清楚的六个点', color='orange', size=12, min_h=4.30)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 account.c / main.c 源码')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的第四级：库 —— 复用单位从源码变成二进制')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。'
        '前三级解决"怎么把代码写清楚"，第四级解决"怎么把代码跨项目复用"。'
        '库这一级的关键转变是：交付物从 .c 源文件，变成编译好的 .a。'),
        title='🧭 一条主线', color='orange', size=15, min_h=1.05)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '第3讲 ✅'),
        ('③ 模块', '第4讲 ✅'),
        ('④ 库', '← 本讲 ⭐'),
        ('⑤ 插件', '第11-12讲'),
        ('⑥ 框架', '第13讲'),
    ], colors=('gray', 'gray', 'gray', 'primary', 'gray', 'gray'),
        size=14, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '复用单位升级为二进制 .o / .a\n'
        '接口与实现第一次真正分离\n'
        'ar rcs 打包 + -L. -laccount 链接'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '"每个程序都复制一份"是静态库的硬伤。\n'
        '下一讲用动态库把代码共享出去：\n'
        '磁盘一份、内存一份，多程序共用 ——\n'
        '这一步，就是插件的技术地基。'),
        title='下一讲要解决的正是这个', color='blue', size=13.5, min_h=1.55)
    banner(s, '库让代码被复用，却也被复制；越往下走，越要想办法"只留一份"')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '假设有 A、B、C 三个程序都链接了 libaccount.a，并且都调用了 account_create。'
        '磁盘上有几份这个函数的机器码副本？三个程序同时运行时，内存里又有几份？\n'
        '提示：链接器把代码"复制"进 exe，程序运行时自带代码、不再依赖 .a；'
        '再想想，如果这个库修了一个 bug，要重新做哪些事。'),
        title='思考题 ①：代码副本有几份？', color='orange', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        'ar rcs 里的 r、c、s 分别是什么意思？如果只写 cs、不写 r，会得到什么？\n'
        '如果只写 rc、漏掉 s，又会怎样？ar t 和 nm 分别能帮你看到什么？\n'
        '提示：c 只管"创建空归档"，r 才管"把成员放进去"；s 建的是链接器用的符号索引表。'),
        title='思考题 ②：ar 三个参数各管什么？', color='purple', size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：各三份，且更新要全链',
         'body': '磁盘上 3 份：每个 exe 都复制了一份\n'
                 'account_create 的机器码\n'
                 '内存里 3 份：三个进程各有独立\n'
                 '地址空间，代码不共享\n'
                 '库修了 bug：重编库 → 重新链接\n'
                 '全部 3 个程序（有 100 个就链 100 次）\n'
                 '这正是第10讲动态库要解决的问题：\n'
                 '让多个程序共享同一份只读代码',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ②：r 放成员，s 建索引',
         'body': 'r（replace）：把 .o 插入归档，\n'
                 '同名成员直接替换\n'
                 'c（create）：归档不存在就静默创建，\n'
                 '不弹"正在创建"的警告\n'
                 's（symbol）：写入符号索引表，\n'
                 '链接器据此快速定位符号在哪个 .o\n'
                 '只用 cs：得到的是空库（没放成员）\n'
                 '漏掉 s：库能用，但链接器只能线性\n'
                 '遍历，慢，旧版还会报 no symbol table\n'
                 'ar t 看成员，nm 看符号（T 为导出）',
         'color': 'purple', 'size': 12.5},
    ], gap=0.26)
    banner(s, '关键：c 只建壳，r 才装货，s 才开索引')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：链接器的粒度，与"静态"的含义')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '静态链接时，链接器会把整个 libaccount.a 原样塞进可执行文件吗？'
        '如果主程序只用到 account.o 里的一个函数，而 account.o 里一共 7 个函数，'
        '会有几个被复制进去？\n'
        '提示：先想清楚"提取的粒度"到底是单个函数，还是整个目标文件；'
        '再想想这种粒度的优缺点，以及能不能用 -ffunction-sections 之类的办法改进。'),
        title='思考题 ③：链接器的提取粒度', color='teal', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '"静态"这两个字，指的是哪个时机？程序运行的时候，还需不需要 libaccount.a 这个文件？\n'
        '提示：把它和"动态"对照着理解——一个在链接时就把代码固定下来，'
        '一个把加载推迟到程序启动；再想想删掉 .a 之后 exe 还能不能跑。'),
        title='思考题 ④：静态的"静"体现在哪', color='green', size=14.5, min_h=1.55)
    banner(s, '这两题想通了，第10讲动态库的动机就提前明白了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '把今天的"复制"接到下一讲的"共享"')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：粒度是 .o，不是函数',
         'body': '不会整库搬走：没用到的 .o 不进来\n'
                 '但粒度是目标文件，不是单个函数：\n'
                 '用到 account.o 里 1 个函数，\n'
                 '整个 account.o 的 7 个函数都被复制\n'
                 '其中 6 个成为"死代码"（不会被调用）\n'
                 '优点：链接器实现简单，不需拆 .o\n'
                 '缺点：体积里含无用代码\n'
                 '现代链接器可用 --gc-sections、\n'
                 '-ffunction-sections 做更细粒度的裁剪',
         'color': 'teal', 'size': 12.5},
        {'title': '解答 ④："静"在链接时机',
         'body': '"静态"指链接时机：在链接阶段就把\n'
                 '用到的机器码固定复制进 exe\n'
                 '运行时不需要 .a：程序自带全部库代码，\n'
                 '删掉 libaccount.a，exe 照常运行\n'
                 '动态库相反：链接时只记"要哪个函数"，\n'
                 '真正的代码在启动或运行时才加载\n'
                 '一句话对照：\n'
                 '静态 = 链接时复制代码\n'
                 '动态 = 运行时共享代码',
         'color': 'green', 'size': 12.5},
    ], gap=0.26)
    banner(s, '理解了"复制"的代价，就理解了下一讲为什么要"共享"')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第9讲 静态库 —— 把代码打包成工具箱')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '静态库用 ar 把多个 .o 打包成一个 .a；链接时，链接器把用到的代码'
        '复制进可执行文件——简单可靠、部署省心，但每个程序都自带一份副本。'),
        title='📝 一句话总结', color='orange', size=14.5, min_h=0.98)
    y = y2 + 0.24

    rows = [('1', '静态库概念', '把多个目标文件 .o 打包成一个归档文件 .a'),
            ('2', 'ar 工具', 'ar rcs libaccount.a account.o transaction.o（r/c/s 各有分工）'),
            ('3', '静态链接', '链接器按"未定义符号"去库里取定义，复制进 exe'),
            ('4', '提取粒度', '粒度是目标文件 .o，不是单个函数；用到一个就搬整个 .o'),
            ('5', '优缺点', '执行快 / 部署简单 / 能保密；体积大 / 内存重复 / 更新要重链'),
            ('6', '与第4讲关系', '多文件是"散装源码"，静态库是"打包成二进制零件"')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：动态库 —— 让多个程序共享同一份代码（第10讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_concept, p05_ar, p06_inside, p07_link,
           p08_pros_cons, p09_deep, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
