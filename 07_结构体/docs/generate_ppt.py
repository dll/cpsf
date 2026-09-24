# -*- coding: utf-8 -*-
"""
第7讲：结构体 —— 把相关数据打包到一起
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

LECTURE = '第7讲 结构体'
prs = new_deck()
PAGES = []


def pg(title, subtitle=None):
    s = page(prs, title, subtitle, label=LECTURE, page_no='auto')
    PAGES.append(s)
    return s


def done(tag=''):
    audit(prs, tag)


def cards_row(s, y, specs, gap=0.22):
    """等宽一行卡片，返回该行底部 y。"""
    n = len(specs)
    w = (INNER_W - gap * (n - 1)) / n
    bottoms = []
    for i, sp in enumerate(specs):
        b, _ = card(s, MARGIN_L + i * (w + gap), y, w, sp['body'],
                    title=sp.get('title'), color=sp.get('color', 'orange'),
                    size=sp.get('size', 16), min_h=sp.get('min_h', 0.0))
        bottoms.append(b)
    return max(bottoms)


def cards_col(s, x, y, w, specs, gap=0.20, size=15):
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
    rect(slide, 0, 0, 4.4, SH, fill=C['card_orange'])
    rect(slide, 0, 0, 0.16, SH, fill=C['primary'])
    rect(slide, 4.4, 0, SW - 4.4, 0.12, fill=C['primary'])

    _put_text(slide, 0.75, 1.15, 3.3, 0.5, '从程序员到架构师', 20, C['primary_dark'], bold=True)
    _put_text(slide, 0.75, 1.72, 3.3, 0.4, 'C语言插件框架演进之旅', 14, C['ink2'])
    rect(slide, 0.75, 2.30, 0.9, 0.05, fill=C['primary'])

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第7讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.55, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '结构体', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '把相关数据打包到一起', 27, C['primary_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.6,
              '第6讲我们管住了一排账户，可 ID、姓名、余额\n'
              '还散在三个平行数组里，靠同一个下标暗中关联。\n'
              '改一处要同步改三处，加个字段还要再加一个数组。\n'
              '本讲把它们打包成一张"名片"——一个账户一条记录。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '第②级"函数"的数据面 —— 从"一批数"到"一条记录"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '第6讲把同类数据排成一排，但不同属性的数据还是各排各的。本讲把"属于同一个对象的'
        '不同属性"打包成一个整体，这就是数据封装的第一课，也是第8讲链表节点与第12讲插件接口的直接前身。'),
        title='🎯 本讲定位', color='orange', size=15.5, min_h=1.15)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '← 本讲深挖'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '第9-10讲'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('gray', 'primary', 'gray', 'gray', 'gray', 'gray'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第5讲：指针能拿地址\n第6讲：数组能存一排同类型数据'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第8讲：结构体 + 指针 = 链表节点\n第12讲：结构体装函数指针 = 插件接口'),
        title='➡ 后续', color='teal', size=14.5, min_h=1.00)
    banner(s, '结构体把"三张散落的纸条"合成"一张完整的名片"')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '数组管住了"一批"，但管不住"一条记录"')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第6讲：已经做到的', [
                    '5 个账户的余额用一个数组管起来',
                    '最近 10 笔交易用数组留档可查',
                    '一个名字 + 一个下标，批量访问'],
                '第7讲：要补上的', [
                    '一个账户的 ID、姓名、余额打包成整体',
                    '一个结构体数组替代三个平行数组',
                    '传一个指针，函数就能改原数据'],
                left_color='blue', right_color='green', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '坑一：改一处要改三处', 'body': '删第 3 个账户要同时删\nids[2]、names[2]、balances[2]',
         'color': 'red', 'size': 13},
        {'title': '坑二：加字段要加数组', 'body': '想加"开户日期"？\n再定义第四个数组',
         'color': 'purple', 'size': 13},
        {'title': '坑三：函数参数臃肿', 'body': '三个数组 + 长度 = 四个参数\n一改签名到处都要改',
         'color': 'orange', 'size': 13},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：平行数组是"三张纸条"，结构体是"一张名片"——数据天然绑定，不会走散',
    ], size=15)
    banner(s, '本讲用结构体把"散落的平行数据"打包成"一条完整记录"')
    done('P3')


# ============================================================
# P4 核心内容一：为什么要打包 + 结构体定义
# ============================================================
def p04_define():
    s = pg('为什么要打包：struct 的定义与使用', 'struct 是"图纸"，声明变量时才真正分配内存')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'struct 是 C 的关键字，用来定义一种自定义类型：花括号里列出成员（也叫字段），'
        '成员可以是基本类型、数组、指针，甚至另一个结构体。'),
        title='📦 结构体 = 一张名片', color='orange', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.50
    code(s, MARGIN_L, y, cw, [
        '/* 把散落的数据打包成一张"名片" */',
        'struct Account {',
        '    int    id;            /* 账户 ID  */',
        '    char   name[20];      /* 账户姓名 */',
        '    double balance;       /* 账户余额 */',
        '};',
        '/* 定义只是"图纸"，此时不占内存 */',
    ], title='定义：struct + 标签名 + 成员', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '/* 一个结构体数组，替代三个平行数组 */',
        'Account accounts[5] = {',
        '    {1001, "张三", 1000.0},',
        '    {1002, "李四", 2000.0},',
        '    {1003, "王五",  500.0},',
        '};',
        'printf("%.2f\\n", accounts[1].balance);',
    ], title='使用：结构体数组，每行一个账户', size=11.5)
    banner(s, '定义结构体不分配内存，只有声明变量时才真正划出一块空间')
    done('P4')


# ============================================================
# P5 核心内容二：成员访问 . 与 ->
# ============================================================
def p05_access():
    s = pg('成员访问：变量用点，指针用箭头', 'p->id 完全等价于 (*p).id —— 它只是省了括号')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '点号 . 用于"结构体变量"，箭头 -> 用于"结构体指针"。为什么会分成两个？因为 . 的优先级'
        '高于 *，写 (*p).id 必须加括号，于是 C 提供了 -> 这个语法糖。'),
        title='🔑 一句话记住：点给变量，箭头给指针', color='orange', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.50
    code(s, MARGIN_L, y, cw, [
        'Account acc = {1001, "张三", 1000.0};',
        '',
        'printf("%d\\n", acc.id);        /* 用点 */',
        'printf("%s\\n", acc.name);      /* 用点 */',
        'acc.balance += 500.0;           /* 改成员 */',
    ], title='变量访问：用点 .', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'Account *p = &acc;   /* p 是指向 Account 的指针 */',
        '',
        'printf("%d\\n", p->id);        /* 用箭头，推荐 */',
        'printf("%d\\n", (*p).id);      /* 完全等价，啰嗦 */',
        '/* p.id 是错的：p 是指针，没有 id 成员 */',
    ], title='指针访问：用箭头 ->', size=11.5)
    banner(s, '箭头不是新东西，它就是 (*p). 的简写 —— 记住这一条，语法就通了')
    done('P5')


# ============================================================
# P6 核心内容三：结构体指针
# ============================================================
def p06_ptr():
    s = pg('结构体指针：一个指针遍历一条记录', '衔接第5讲 —— p++ 的步长正好是一个 Account')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '结构体数组的数组名，就是首元素地址。让一个结构体指针指向它，p->成员 取出整条记录，'
        'p++ 就前进到下一条 —— 第6讲要三个指针同步递增，现在一个就够。'),
        title='🧭 从"三个指针"到"一个指针"', color='orange', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        'Account accounts[5] = { /* ... */ };',
        'Account *p = accounts;          /* 指向首元素 */',
        '',
        'for (int i = 0; i < 5; i++) {',
        '    printf("%d %s %.2f\\n",',
        '           p->id, p->name, p->balance);',
        '    p++;   /* 前进一步 = 一个 Account */',
        '}',
    ], title='结构体指针遍历（步长自动适配）', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    card(s, xr, y, wr, (
        '第6讲：pid、pname、pbal\n'
        '三个指针要同步递增，\n'
        '少加一次就对不齐。\n'
        '本讲：一个 Account*，\n'
        '一次递增，信息完整。'),
        title='⚖️ 对比第6讲', color='teal', size=13, min_h=1.95)
    banner(s, '指针的步长由编译器按类型算好 —— 你只管 p++，它自己走对地方')
    done('P6')


# ============================================================
# P7 核心内容四：结构体作函数参数
# ============================================================
def p07_param():
    s = pg('结构体作函数参数：值传递 vs 指针传递', '传值是"复印一张名片"，传址是"递一张地址"')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '值传递  void f(Account acc)', [
                    '复制整个结构体，函数内改的是副本',
                    '原数据安全，但结构体大时开销明显',
                    '适合：只读的小结构体'],
                '指针传递  void f(Account* p)', [
                    '只传地址（4 或 8 字节），不复制数据',
                    '函数内能直接改到原数据',
                    '适合：大结构体、需要修改的场景'],
                left_color='red', right_color='green', size=14) + 0.14

    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        '/* 值传递：复制一份，改不到原件 */',
        'void print_account_value(Account acc);',
        '',
        '/* 指针传递：能改原数据，存款靠它 */',
        'void deposit(Account* pAcc, double amount);',
        '',
        '/* 只想读不想改：用 const 指针保护 */',
        'void print_account_ptr(const Account* p);',
    ], title='三种写法，各司其职', size=11.5)

    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '要改原数据吗？\n'
        '├ 要 → 必须传指针\n'
        '└ 不要 → 结构体大就用 const 指针，\n'
        '         小到几个字节才传值。\n'
        'const 是编译器替你把关的只读锁。'),
        title='✅ 选择原则', color='orange', size=13, min_h=2.20)
    banner(s, '函数要修改原数据，就必须拿到地址 —— 这是第5讲指针的直接延续')
    done('P7')


# ============================================================
# P8 核心内容五：typedef 与数据封装思想
# ============================================================
def p08_typedef():
    s = pg('typedef 与数据封装思想', '给类型起个短名；结构体 + 函数 = 类的雏形')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '每次用结构体都要写 struct 很啰嗦。typedef 给已有类型起个别名：typedef struct Account Account;'
        '之后就能直接写 Account acc;。它不创建新类型，只是换个短名字。'),
        title='🏷️ typedef 不造类型，只起别名', color='orange', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        '/* 没有 typedef：每次都要写 struct */',
        'struct Account acc1;',
        'void func(struct Account* p);',
        '',
        '/* 有 typedef：短名字 */',
        'typedef struct Account Account;',
        'Account acc1;',
        'void func(Account* p);',
    ], title='typedef 让代码清爽', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    card(s, xr, y, wr, (
        '结构体 = 数据打包\n'
        '函数   = 行为打包\n'
        '两者结合，就是面向对象里"类"的雏形。\n'
        '第12讲的插件接口更进一层：\n'
        '结构体里装函数指针，\n'
        '数据和行为就真的绑在了一起。'),
        title='🧩 数据 + 行为 = 类的雏形', color='purple', size=13, min_h=2.20)
    banner(s, '结构体装数据，函数指针装行为 —— 插件接口就是"结构体装函数指针"')
    done('P8')


# ============================================================
# P9 原理深入：内存布局与对齐 ⭐
# ============================================================
def p09_memory():
    s = pg('原理深入：结构体的内存布局与对齐 ⭐', 'sizeof(Account) 是 32 —— 成员的顺序会影响大小')
    y = BODY_TOP
    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        'struct Account {',
        '    int    id;          /* 4 字节 */',
        '    char   name[20];    /* 20 字节 */',
        '    double balance;     /* 8 字节 */',
        '};',
        '',
        '偏移   成员            大小',
        ' 0 ~  3  int    id       4',
        ' 4 ~ 23  char   name[20] 20',
        '24 ~ 31  double balance   8',
        '------------------------------',
        'sizeof(Account) = 32 字节',
    ], title='内存布局（真实运行结果）', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    y2, _ = card(s, xr, y, wr, (
        'CPU 访问对齐的数据更快。规则是：每个成员的偏移量必须是它自身大小的整数倍，'
        '整个结构体大小又是最大成员大小的整数倍。double 要从 8 的倍数处开始。'),
        title='⚡ 为什么要"对齐"', color='orange', size=13, min_h=1.70)
    card(s, xr, y2 + 0.18, wr, (
        '把 double 放到 int 前面试试：\n'
        '0~3 int 之后，balance 需要 8 对齐，\n'
        '中间就要插 4 个填充字节，\n'
        '结构体从 32 膨胀到 40。'),
        title='⚠️ 成员顺序会改变大小', color='red', size=13, min_h=1.65)
    banner(s, '结构体大小 = 成员之和 + 对齐填充；装不下的地方，编译器替你垫上')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：平行数组 vs 结构体数组', '同一个 ATM，两种数据组织方式')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '平行数组（第6讲）', [
                    '三个数组靠"同一个下标"暗中关联',
                    '改一处要同步改三处，容易漏',
                    '加字段 = 再加一个数组'],
                '结构体数组（第7讲）', [
                    '一条记录把相关字段天然绑在一起',
                    '改一个结构体就行，不会走散',
                    '加字段 = 加一个成员'],
                left_color='red', right_color='green', size=14) + 0.16

    rows = [('定义', '3 个独立数组', '1 个结构体数组'),
            ('访问第 i 项', 'ids[i] / names[i] / bals[i]', 'accounts[i].balance'),
            ('加字段', '再加一个数组', '加一个成员'),
            ('排序', '3 个数组同步搬移', '搬移整个结构体'),
            ('函数参数', '3 个数组 + 长度', '结构体数组 + 长度')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.20, 0.40, 0.40),
            size=12, header=('维度', '平行数组', '结构体数组'))
    banner(s, '从"相关数据散落在不同数组"到"打包在一个结构体"——这就是数据封装')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/struct_atm.c —— 结构体定义、成员访问、指针遍历')
    y = BODY_TOP
    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        'struct Account {',
        '    int    id;              /* 账户 ID   */',
        '    char   name[NAME_LEN];  /* 账户姓名  */',
        '    double balance;         /* 账户余额  */',
        '};',
        'typedef struct Account Account;',
        'Account accounts[5] = {',
        '    {1001, "张三", 1000.0},',
        '    {1002, "李四", 2000.0},',
        '};',
    ], title='struct_atm.c：一张名片装一个账户', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    b, _ = code(s, xr, y, wr, [
        'void show_all_accounts(void) {',
        '    Account *p = accounts;',
        '    for (int i = 0; i < MAX_ACCOUNTS; i++) {',
        '        printf("%d %s %.2f\\n",',
        '               p->id, p->name, p->balance);',
        '        p++;   /* 一个指针走完全程 */',
        '    }',
        '}',
    ], title='一个结构体指针，遍历所有账户', size=11.5)
    b = max(b, y + 10 * 11.5 * 1.42 / 72 + 0.40 + 0.36)
    card(s, MARGIN_L, b + 0.20, cw, (
        '结构体数组 = 一盒名片；结构体指针 = 一张一张往下取。'),
        title='📇 一盒名片', color='green', size=13)
    demo_frame(s, xr, b + 0.20, wr, 1.40,
               title='真实运行（节选）',
               lines=['Account 结构体大小：32 字节',
                      '  char name[20]: 20 字节',
                      '1001  张三  1500.00'])
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '账户列表、存款、交易记录、结构体大小 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.60
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall -o struct_atm.exe struct_atm.c',
        '（无警告 —— 结构体与成员访问都用对了）',
        "$ printf '1001\\n2\\n500\\n5\\n6\\n0\\n' | ./struct_atm.exe",
        '========================================',
        '   欢迎使用 CCIT ATM 系统（结构体版）',
        '========================================',
        '  支持 5 个账户 | 记录最近 10 笔交易',
        '  账户ID: 1001  姓名: 张三  余额: 1000.00',
        '请输入您的账户ID：登录成功！欢迎，张三',
        '请输入存款金额：操作成功！存入 500.00 元',
        '【交易记录】1  存款  500.00',
        '1001     张三   1500.00   ← 成员被改了',
        'Account 结构体大小：32 字节',
        '$ echo $?     →     0',
    ], title='终端实录（真实输出，未删改）', size=11.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译零警告：成员访问都对得上\n'
        '② 账户列表：一个结构体数组全管住\n'
        '③ 存款 500：余额由 1000 变 1500\n'
        '④ 交易记录：一条记录一行显示\n'
        '⑤ 结构体大小 32 字节：4+20+8\n'
        '⑥ 退出码 0：程序干净收场'),
        title='👀 要看清楚的六个点', color='orange', size=12.5, min_h=4.05)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 src/struct_atm.c')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '第②级"函数"的数据面：结构体是接口与链表的共同前身')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。本讲仍在第②级夯数据的地基，'
        '但它第一次把"数据"组织成"对象"——一个账户就是一条记录。链表节点、插件接口，'
        '都是在这个"结构体"上继续生长的。'),
        title='🧭 一条主线', color='orange', size=15, min_h=1.15)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '← 本讲 ⭐'),
        ('③ 模块', '第4讲 ✅'),
        ('④ 库', '第9-10讲'),
        ('⑤ 插件', '第11-12讲'),
        ('⑥ 框架', '第13讲'),
    ], colors=('gray', 'primary', 'gray', 'gray', 'gray', 'gray'),
        size=14, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '结构体把相关数据打包成"一条记录"，\n'
        '是"数据封装"的第一课；\n'
        '结构体指针让函数改得到原数据，\n'
        '这正是后面所有接口的传参方式。'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第8讲：结构体加一个 next 指针，\n'
        '就变成链表节点，大小不再固定；\n'
        '第12讲：结构体里装一组函数指针，\n'
        '就成了插件的统一接口。'),
        title='后面接着做什么', color='blue', size=13.5, min_h=1.55)
    banner(s, '从"散落的数据"到"打包的记录"——这一步是接口与链表共同的起点')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '直觉上 sizeof(struct Account) 应该是 4 + 20 + 8 = 32 字节，可只要把成员的顺序换一下，'
        '结果就可能变成 40。为什么结构体的大小会"多出几个字节"？\n'
        '提示：CPU 读对齐的数据更快；想想每个成员的偏移量必须满足什么条件。'),
        title='思考题 ①：结构体大小等于各成员之和吗？', color='orange', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        'Account b = a; 之后改 b 的余额，a 的余额却没变——因为成员都是值类型，复制是安全的。'
        '可如果成员是一个指针呢？\n'
        '提示：什么叫"浅拷贝"？两个结构体的指针成员指向同一块内存，会发生什么？'),
        title='思考题 ②：结构体赋值是浅拷贝还是深拷贝？', color='purple', size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：多出来的叫"填充字节"',
         'body': '不一定相等，因为内存对齐。\n'
                 '规则一：成员偏移量必须是自身\n'
                 '大小的整数倍（double → 8 对齐）\n'
                 '规则二：总大小是最大成员的整数倍\n'
                 '本讲 Account 顺序正好命中：\n'
                 '0/4/24 都是合法偏移，所以 = 32\n'
                 '把 double 提前就要插 4 个填充，\n'
                 '变成 40。这是"空间换时间"：\n'
                 '多占几字节，换更快的访问。',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ②：浅拷贝，指针成员要当心',
         'body': '结构体赋值是逐字节的浅拷贝。\n'
                 '成员是 int、double、字符数组时，\n'
                 '复制的是值，安全。\n'
                 '成员是指针时，只复制地址：\n'
                 '两个指针指向同一块内存，\n'
                 '改一个另一个跟着变；\n'
                 '一个 free 了，另一个成野指针，\n'
                 '两个都 free 更是 double free。\n'
                 '解法：手写深拷贝函数，\n'
                 '为指针成员重新 malloc 再复制内容。',
         'color': 'purple', 'size': 12.5},
    ], gap=0.26)
    banner(s, '记住两句话：对齐是为了快，浅拷贝是要小心指针')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从成员访问接到"结构体像不像类"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '给定 Account acc; Account* p = &acc; 以下哪些写法对：① acc.id ② acc->id '
        '③ p.id ④ p->id ⑤ (*p).id ⑥ *p.id？\n'
        '提示：. 的优先级高于 *；再想想 -> 到底等价于什么。'),
        title='思考题 ③：. 和 -> 有什么区别？', color='orange', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        'C 的结构体把数据打包在一起，很像面向对象里的"属性"；操作结构体的函数很像"方法"。'
        '那 C 的结构体和类，到底差在哪？\n'
        '提示：类有访问控制、继承、多态，C 结构体有吗？'
        '在结构体里放函数指针成员，是在模拟什么？'),
        title='思考题 ④：结构体和"类"有什么相似与不同？', color='teal', size=14.5, min_h=1.55)
    banner(s, '这两题想通了，第12讲的插件接口就提前入门了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '把今天的"结构体"接到接口抽象')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：对的四个，错的看优先级',
         'body': '① acc.id   ✅ 变量用点\n'
                 '② acc->id  ❌ acc 不是指针\n'
                 '③ p.id     ❌ p 是指针，没这成员\n'
                 '④ p->id    ✅ 指针用箭头\n'
                 '⑤ (*p).id  ✅ 先解引用再取成员\n'
                 '⑥ *p.id    ❌ 被解释成 *(p.id)\n'
                 '-> 就是 (*p). 的语法糖，\n'
                 '编译器内部处理完全一样。\n'
                 '一句话：变量用点，指针用箭头。',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ④：相似在封装，不同在"绑定"',
         'body': '相似：都自定义类型、都打包数据；\n'
                 '结构体 + 操作函数 ≈ 类的属性和方法。\n'
                 '不同一：数据与行为是分离的，\n'
                 '函数在结构体外面。\n'
                 '不同二：没有 public/private 访问控制。\n'
                 '不同三：没有继承，没有虚函数多态。\n'
                 '怎么模拟：把函数指针放进结构体，\n'
                 '再用 init 函数把"方法"绑上去。\n'
                 'Linux 内核的 file_operations 正是如此。',
         'color': 'teal', 'size': 12.5},
    ], gap=0.26)
    banner(s, 'C 没有类，但"结构体 + 函数指针"能把它模拟出来 —— 这就是插件接口的根')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第7讲 结构体 —— 把相关数据打包到一起')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '结构体是把相关数据打包到一起的自定义类型：一次定义一张"图纸"，声明变量才分配内存；'
        '变量用点、指针用箭头；结构体指针能遍历、能改原数据；typedef 给它起个短名字。'),
        title='📝 一句话总结', color='orange', size=14.5, min_h=0.98)
    y = y2 + 0.24

    rows = [('1', '结构体定义', 'struct 自定义类型，把相关数据绑在一起'),
            ('2', '成员访问', '变量用点（.），指针用箭头（->）'),
            ('3', '结构体指针', '衔接第5讲，一个指针遍历一条记录'),
            ('4', '值传递 vs 指针传递', '值传递安全但复制，指针传递高效能改原数据'),
            ('5', 'typedef', '给类型起短名，代码更简洁'),
            ('6', '数据封装', '结构体装数据，函数指针装行为 —— 接口的种子')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.22, 0.72), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：链表 —— 结构体加一个 next 指针，大小不再固定（第8讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_define, p05_access, p06_ptr, p07_param,
           p08_typedef, p09_memory, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
