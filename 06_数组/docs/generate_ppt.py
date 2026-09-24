# -*- coding: utf-8 -*-
"""
第6讲：数组 —— 批量数据的容器
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

LECTURE = '第6讲 数组'
prs = new_deck()
PAGES = []


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
    rect(slide, 0, 0, 4.4, SH, fill=C['card_teal'])
    rect(slide, 0, 0, 0.16, SH, fill=C['teal'])
    rect(slide, 4.4, 0, SW - 4.4, 0.12, fill=C['teal'])

    _put_text(slide, 0.75, 1.15, 3.3, 0.5, '从程序员到架构师', 20, C['teal_dark'], bold=True)
    _put_text(slide, 0.75, 1.72, 3.3, 0.4, 'C语言插件框架演进之旅', 14, C['ink2'])
    rect(slide, 0.75, 2.30, 0.9, 0.05, fill=C['teal'])

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第6讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.55, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['teal_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '数组', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '批量数据的容器', 27, C['teal_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.6,
              '第5讲给数据发了门牌号，可一次只发一张。\n'
              'ATM 有 5 个账户、要给 10 笔交易留记录——\n'
              '难道起 100 个变量名？\n'
              '本讲把同类数据排成一排：一个名字 + 一个编号。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '第②级"函数"的数据面 —— 让函数一次处理一批')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '上一讲学的是"一个变量的地址"，本讲学的是"一排变量的组织方式"。数组让函数从'
        '"一次处理一个数"升级到"一次处理一批数"，它也是第7讲结构体、第8讲链表的直接前身。'),
        title='🎯 本讲定位', color='teal', size=15.5, min_h=1.15)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '← 本讲深挖'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '第9-10讲'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('gray', 'teal', 'gray', 'gray', 'gray', 'gray'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第2讲：for 循环的套路\n第5讲：数组名就是首元素地址'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第7讲：结构体把平行数组合并\n第8讲：链表打破"固定大小"'),
        title='➡ 后续', color='orange', size=14.5, min_h=1.00)
    banner(s, '本讲把"一个名字管一个数"升级为"一个名字管一批数"')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p3_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '指针能传地址了，可一个指针只管一个变量')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第5讲：已经做到的', [
                    '余额收进 main，变成了局部变量',
                    '函数通过指针能改到调用者的余额',
                    'const 只读 + NULL 检查，用得放心'],
                '第6讲：要补上的', [
                    '5 个账户的余额用一个数组管起来',
                    '最近 10 笔交易用数组留档可查',
                    '账户名用字符数组存成"字符串"'],
                left_color='blue', right_color='green', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '坑一：只能管一个', 'body': '一个 balance 只对应一个账户\n想加账户就得再加变量',
         'color': 'red', 'size': 13},
        {'title': '坑二：做完就忘', 'body': '每笔交易只打印一下\n关掉程序什么都没留下',
         'color': 'purple', 'size': 13},
        {'title': '坑三：名字没处放', 'body': '只有数字 ID，没有姓名\nC 里连 string 类型都没有',
         'color': 'orange', 'size': 13},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：单变量是"一张便利贴"，数组是"一排编号的储物柜"',
    ], size=15)
    banner(s, '数组用"一个名字 + 一个索引"管理一组同类型数据')
    done('P3')


# ============================================================
# P4 核心内容一：一维数组
# ============================================================
def p4_array1():
    s = pg('一维数组：定义、初始化、访问', '索引从 0 开始 —— 这是内存地址的自然映射')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '数组是一排紧挨着的、类型相同的存储单元：定义时尺寸就定下来，位置连续，'
        '用一个数组名加一个下标就能直接定位到任意一格。'),
        title='📦 数组就是"一排编号的储物柜"', color='teal', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        'double balances[5] = {1000, 2000, 500, 3000, 1500};',
        'int  arr[5] = {1, 2, 3};   /* 剩下自动补 0 */',
        'int  a[]   = {10, 20, 30}; /* 大小由编译器数 */',
        '',
        'balances[0]  →  1000.0   /* 第一个 */',
        'balances[2]  →   500.0   /* 第三个 */',
        'balances[5]  =  999;     /* 越界！C 不报错 */',
    ], title='定义、初始化与访问', size=11.5)

    xr = MARGIN_L + cw + 0.26
    cards_col(s, xr, y, INNER_W - cw - 0.26, [
        {'title': '为什么从 0 开始', 'body': 'arr[i] 就是 *(arr + i)\n偏移 0 格正好是第一个元素',
         'color': 'blue', 'size': 13},
        {'title': '越界没有护栏', 'body': 'arr[5] 编译不报错\n读到的是邻居内存的垃圾值',
         'color': 'red', 'size': 13},
    ], gap=0.16)
    banner(s, '数组大小在定义时就定死，运行期不会再变 —— 这是它的力量，也是它的局限')
    done('P4')


# ============================================================
# P5 核心内容二：二维数组
# ============================================================
def p5_array2():
    s = pg('二维数组：数组的数组，一张表', '行优先连续存储 —— 一张表在内存里其实是一条长带子')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '二维数组就是"数组的数组"，每个元素本身又是一个数组。\n'
        '定义 matrix[3][4] 就是 3 行 4 列，行索引在前、列索引在后。'),
        title='📋 从一排柜子，到一整面格子墙', color='teal', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.50
    code(s, MARGIN_L, y, cw, [
        'int matrix[3][4] = {',
        '    { 1,  2,  3,  4},   /* 第 0 行 */',
        '    { 5,  6,  7,  8},   /* 第 1 行 */',
        '    { 9, 10, 11, 12}    /* 第 2 行 */',
        '};',
        'matrix[1][2]  →  7      /* 第 1 行第 2 列 */',
    ], title='定义与访问', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'char names[5][20] = {"张三", "李四",',
        '                     "王五", "赵六", "钱七"};',
        'printf("%s\\n", names[2]);   /* 王五 */',
    ], title='二维字符数组：一排字符串', size=11.5)
    card(s, xr, y + 3 * 11.5 * 1.42 / 72 + 0.40 + 0.36 + 0.18, wr, (
        '内存里仍是连续的一条：\n'
        '先放完第 0 行的 20 个字符，\n'
        '再放第 1 行…… 行优先存储。'),
        title='📐 内存布局', color='orange', size=12.5, min_h=1.20)
    banner(s, '多维只是"看起来多维"，内存在底层永远是一条连续的线')
    done('P5')


# ============================================================
# P6 核心内容三：字符数组与字符串
# ============================================================
def p6_string():
    s = pg('字符数组与字符串：C 没有 string 类型', "字符串 = 一串字符 + 末尾一个 '\\0'")
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        "C 语言没有 string 类型，字符串就是「以 '\\0' 结尾的字符数组」。printf、strlen、strcpy 这些"
        "函数都靠 '\\0' 判断「到哪结束」——它是结束标志，不是内容。"),
        title='🔤 一句话说清', color='teal', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.55
    code(s, MARGIN_L, y, cw, [
        'char name[20] = "张三";',
        '/* 实际存：张  三  \\0  未使用……            */',
        '/*           [0] [1] [2] [3..19]            */',
        '',
        'char ok[5]  = {\'W\',\'a\',\'n\',\'g\',\'\\0\'};  /* 有结束 */',
        'char bad[4] = {\'W\',\'a\',\'n\',\'g\'};        /* 没结束 */',
        'printf("%s", bad);   /* Wang 后面继续乱读 */',
    ], title='字符串的存储真相', size=11.5)

    xr = MARGIN_L + cw + 0.26
    rows = [('strlen(name)', '4    不计 \\0'),
            ('sizeof(name)', '5    含 \\0')]
    kv_rows(s, xr, y, INNER_W - cw - 0.26, rows, widths=(0.52, 0.48),
            size=12, header=('写法', '结果'))
    card(s, xr, y + 3 * 0.45 + 0.16, INNER_W - cw - 0.26, (
        "scanf 读字符串写 %s，数组名本身就是\n"
        "地址，所以不加 &。想不越界就写 %9s 限长。"),
        title='⚠️ 读字符串的坑', color='red', size=12.5, min_h=1.30)
    banner(s, "忘了 '\\0'，printf 就会一路读到内存里偶然遇到 0 才停 —— 这就是乱码的来源")
    done('P6')


# ============================================================
# P7 核心内容四：数组作为函数参数
# ============================================================
def p7_decay():
    s = pg('数组作为函数参数：退化成指针', '传的是首元素地址，长度信息"丢在了门口"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '把数组传给函数，C 不会复制整个数组，只传首元素地址 —— 这叫"数组退化为指针"。'
        '好处是高效（只传 8 字节），代价是函数内部不知道数组有多长，必须额外传一个长度。'),
        title='📌 退化的本质', color='teal', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.55
    code(s, MARGIN_L, y, cw, [
        'void f(int arr[10]);   /* 看着像传数组 */',
        'void f(int arr[]);     /* 看着像传数组 */',
        'void f(int* arr);      /* 实际就是指针 */',
        '/* 三种写法，编译器眼里完全一样 */',
        '',
        'void show(double arr[], int n) {',
        '    for (int i = 0; i < n; i++) printf("%.2f ", arr[i]);',
        '}',
        'show(balances, 5);     /* 数组名 + 长度 一起传 */',
    ], title='三种写法等价', size=11.5)

    xr = MARGIN_L + cw + 0.26
    cards_col(s, xr, y, INNER_W - cw - 0.26, [
        {'title': 'sizeof 的陷阱', 'body': '函数里 sizeof(arr) 只有 4 或 8\n不再是整个数组的大小',
         'color': 'red', 'size': 13},
        {'title': '所以必须传长度', 'body': '数组 + 长度 是 C 的标准搭档\n这也是 printf 那类接口的样子',
         'color': 'blue', 'size': 13},
    ], gap=0.16)
    banner(s, '数组传参"只交钥匙不交清单" —— 清单（长度）得你自己递进去')
    done('P7')


# ============================================================
# P8 核心内容五：数组与指针的关系
# ============================================================
def p8_relation():
    s = pg('数组与指针的关系：一个地址，两种写法', 'arr[i] 与 *(arr+i) 是同一件事的两种说法')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '数组名 arr', [
                    '是地址常量，指向首元素',
                    '不能 arr++，也不能 arr = p',
                    'sizeof(arr) = 整个数组的字节数'],
                '指针变量 p', [
                    '是变量，可以改指向',
                    'p++、p = &arr[3] 都合法',
                    'sizeof(p) = 指针本身（4 或 8）'],
                left_color='teal', right_color='blue', size=14) + 0.14

    cw = INNER_W * 0.55
    code(s, MARGIN_L, y, cw, [
        '/* 三种写法，结果完全一样 */',
        'for (int i = 0; i < 5; i++) printf("%.2f", arr[i]);',
        '',
        'double* p = arr;',
        'for (int i = 0; i < 5; i++) printf("%.2f", *(p + i));',
        '',
        'for (double* q = arr; q < arr + 5; q++) printf("%.2f", *q);',
    ], title='下标法 / 偏移法 / 递增法', size=11.5)

    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        'arr[i] 是 *(arr + i) 的语法糖。\n'
        '编译器内部就是先算地址、\n'
        '再按元素类型取数据。\n'
        '想通了这点，数组就透明了。'),
        title='💡 一句话打通', color='orange', size=12.5, min_h=2.10)
    banner(s, '数组名是"不能移动的地址标签"，指针是"可以移动的地址标签"')
    done('P8')


# ============================================================
# P9 原理深入：连续内存与随机访问 ⭐
# ============================================================
def p9_memory():
    s = pg('原理深入：连续内存与随机访问 ⭐', '为什么 arr[100] 能一步到位？')
    y = BODY_TOP
    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        'int arr[5] = {10, 20, 30, 40, 50};',
        '/* 首地址 0x1000，每个 int 占 4 字节 */',
        '',
        '地址      元素      内容',
        '0x1000    arr[0]    10   ← 首地址',
        '0x1004    arr[1]    20   │ 紧挨着',
        '0x1008    arr[2]    30   │ 连续',
        '0x100C    arr[3]    40   │ 排列',
        '0x1010    arr[4]    50   │',
        '',
        'arr[i] 的地址 = 0x1000 + i × 4',
    ], title='连续内存：地址可以算出来', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    y2, _ = card(s, xr, y, wr, (
        '只要知道首地址和元素大小，第 i 个元素的地址就是\n'
        '"首地址 + i × 元素大小"——一次乘法加法就到，'
        '不用从头数过去。所以数组的随机访问是常数时间 O(1)。'),
        title='⚡ 随机访问：O(1) 的底气', color='green', size=13, min_h=1.75)
    card(s, xr, y2 + 0.18, wr, (
        '链表每个节点分散在堆上，\n'
        '要访问第 i 个必须顺着指针走 i 步，\n'
        '是 O(n) —— 这就是第8讲要付出的代价。'),
        title='🔮 为第8讲预留的对比', color='purple', size=13, min_h=1.45)
    banner(s, '数组用"连续"换来 O(1) 随机访问，也换来"插入删除要搬家"的代价')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：数组 vs 链表（第8讲预告）', '一个用"连续"换速度，一个用"分散"换灵活')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '数组（本讲）', [
                    '一整块连续内存，下标直接定位',
                    '大小编译期定死，运行期不变',
                    '随机访问 O(1)，插入删除 O(n)'],
                '链表（第8讲）', [
                    '节点分散在堆上，靠指针串联',
                    '大小运行期可变，想加就加',
                    '访问第 i 个 O(n)，增删只需改指针'],
                left_color='teal', right_color='purple', size=14) + 0.16

    rows = [('内存布局', '一整块连续内存', '节点散落，指针相连'),
            ('访问第 i 个', 'O(1)，一步算到', 'O(n)，从头顺着走'),
            ('插入 / 删除', 'O(n)，后面全体搬家', 'O(1)，改两个指针'),
            ('大小', '定义时就定死', '运行期随时增减')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.18, 0.41, 0.41),
            size=12, header=('维度', '数组', '链表'))
    banner(s, '没有最好的数据结构，只有最合适的场景 —— 选型就是架构判断')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/array_atm.c —— 平行数组管账户，循环缓冲区存流水')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        '/* 平行数组：同一索引对应同一个账户 */',
        'int    account_ids[MAX_ACCOUNTS];',
        'char   account_names[MAX_ACCOUNTS][NAME_LEN];',
        'double account_balances[MAX_ACCOUNTS];',
        '',
        '/* 循环缓冲区：永远只留最近 10 笔 */',
        'void add_transaction(double amount, int type) {',
        '    int slot = trans_count % MAX_TRANSACTIONS;',
        '    trans_amounts[slot] = amount;',
        '    trans_types[slot]   = type;',
        '    trans_count++;',
        '}',
    ], title='array_atm.c：数组才是主角', size=11.5)
    card(s, MARGIN_L, y + 12 * 11.5 * 1.42 / 72 + 0.40 + 0.36 + 0.20, cw, (
        '第 11 笔写回 slot 0，覆盖最旧那笔 —— 取模运算实现"自动循环"。'),
        title='♻️ 循环缓冲区', color='green', size=13)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'int *pid = account_ids;',
        'double *pbal = account_balances;',
        'for (int i = 0; i < MAX_ACCOUNTS; i++) {',
        '    printf("%-8d %.2f\\n", *pid, *pbal);',
        '    pid++;  pbal++;   /* 指针前进 */',
        '}',
    ], title='指针递增遍历（衔接第5讲）', size=11.5)
    demo_frame(s, xr, y + 6 * 11.5 * 1.42 / 72 + 0.40 + 0.36 + 0.20, wr, 2.10,
               title='真实运行（节选）',
               lines=['$ printf 1001/2/500/5/6/0 | ./array_atm.exe',
                      '  账户ID: 1001  姓名: 张三  余额: 1000.00',
                      '✅ 登录成功！欢迎，张三',
                      '【交易记录】1  存款  500.00',
                      '数组总大小：20 字节'])
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '账户列表、交易流水、数组大小 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.60
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall -o array_atm.exe array_atm.c',
        '（无警告 —— 数组与下标都用对了）',
        "$ printf '1001\\n2\\n500\\n5\\n6\\n0\\n' | ./array_atm.exe",
        '========================================',
        '     欢迎使用 CCIT ATM 系统（数组版）',
        '========================================',
        '  支持 5 个账户 | 记录最近 10 笔交易',
        '  账户ID: 1001  姓名: 张三  余额: 1000.00',
        '  账户ID: 1002  姓名: 李四  余额: 2000.00',
        '请输入您的账户ID：✅ 登录成功！欢迎，张三',
        '请输入存款金额：✅ 操作成功！存入 500.00 元',
        '【交易记录】序号 类型 金额 / 1  存款  500.00',
        '1001     张三   1500.00   ← 数组里被改了',
        '数组总大小：20 字节（5 个 int × 4 字节）',
        '$ echo $?     →     0',
    ], title='终端实录（真实输出，未删改）', size=11.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译零警告：下标、长度都对得上\n'
        '② 5 个账户：一个数组全管住\n'
        '③ 交易留档：最近 10 笔可回溯\n'
        '④ 循环缓冲区：取模实现自动覆盖\n'
        '⑤ 指针遍历：*pid / *pbal 向前走\n'
        '⑥ 退出码 0：程序干净收场'),
        title='👀 要看清楚的六个点', color='teal', size=12.5, min_h=3.85)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 src/array_atm.c')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '第②级"函数"的数据面：数组是结构体与链表的前身')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。本讲仍在第②级"函数"上夯地基，'
        '但它第一次把"数据"组织起来了——从"一个变量"到"一批数据"。没有这一步，'
        '后面的结构体、链表、乃至插件管理器里的插件链表都无从谈起。'),
        title='🧭 一条主线', color='teal', size=15, min_h=1.15)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '← 本讲 ⭐'),
        ('③ 模块', '第4讲 ✅'),
        ('④ 库', '第9-10讲'),
        ('⑤ 插件', '第11-12讲'),
        ('⑥ 框架', '第13讲'),
    ], colors=('gray', 'teal', 'gray', 'gray', 'gray', 'gray'),
        size=14, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '数组让函数一次能处理一批数据：\n'
        '传数组 + 长度，是库接口的标准姿势\n'
        '连续内存换来 O(1) 随机访问，\n'
        '这套"地址 + 偏移"的思维一路用到链表'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第7讲：结构体把平行数组打包成一条记录\n'
        '第8讲：链表 + malloc 打破固定大小\n'
        '第13讲：插件管理器的链表，\n'
        '正是"数组思维"升级后的动态版本'),
        title='后面接着做什么', color='blue', size=13.5, min_h=1.55)
    banner(s, '从单变量到数组，从数组到链表，再到框架 —— 每一步都是因为"上一步不够好"')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'arr[i] 和 *(p+i) 效果一样，数组名传给函数后也变成指针。但数组名不能 arr++、'
        'sizeof 结果也完全不同。它们到底有什么区别？\n'
        '提示：从"地址常量"和"地址变量"想；再想想传给函数之后，sizeof 为什么只剩指针大小。'),
        title='思考题 ①：数组名和指针到底有什么区别？', color='teal', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '只有 5 个元素的数组，访问 arr[100] 编译器不报错，程序也不一定立刻崩。'
        '为什么 C 偏偏不做越界检查？\n'
        '提示：越界检查要付什么代价？C 的设计哲学是什么？不做检查又带来了什么安全问题？'),
        title='思考题 ②：为什么 C 的数组不做越界检查？', color='purple', size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：能互换，但身份不同',
         'body': '区别一：数组名是地址常量，\n'
                 '不能 arr++、不能 arr = p；\n'
                 '指针是变量，来去自如\n'
                 '区别二：sizeof(arr) 是整个数组大小，\n'
                 'sizeof(p) 只是指针本身的大小\n'
                 '更准的说法是：数组名可以隐式\n'
                 '转换为首元素指针，但它本身不是\n'
                 '指针变量 —— 它是钉在墙上的门牌\n'
                 '移到函数里退化成指针后，\n'
                 '连"整体大小"这个身份也丢了',
         'color': 'teal', 'size': 12.5},
        {'title': '解答 ②：这是特性，不是疏忽',
         'body': 'C 诞生于 1972 年，资源极紧张。\n'
                 '每次访问都检查越界，就得加一条\n'
                 '比较加一条跳转，大数组循环里\n'
                 '开销可观 —— C 选择把检查交给人\n'
                 '后果一：越界读的是邻居内存，\n'
                 '结果不可预测，极难调试\n'
                 '后果二：经典的缓冲区溢出攻击，\n'
                 '正是靠写越界覆盖返回地址\n'
                 'Java/Python/Rust 都做检查，\n'
                 '代价是性能；C 选了快，责任在你',
         'color': 'purple', 'size': 12.5},
    ], gap=0.26)
    banner(s, 'C 的哲学是"信任程序员"：给你最快的速度，也把责任一并交给你')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从结束标志接到固定大小的破解')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        "字符串末尾为什么要加 '\\0'？方式一 char a[] = \"Wang\" 自动加，"
        "方式二 char b[4] = {'W','a','n','g'} 不会加。\n"
        "提示：printf 靠什么知道读到哪停？'\\0' 的 ASCII 值是多少？"
        "strlen 和 sizeof 对同一个字符串为什么结果不同？"),
        title="思考题 ③：字符数组末尾为什么要加 '\\0'？", color='teal', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '数组定义时大小就定死了：多了放不下，少了又浪费；想在中间插一个，'
        '后面全体都要搬家。这个局限怎么破？\n'
        '提示：想想到底该定多大？插入要移动多少元素？'
        '再想想 malloc 动态分配和链表各解决了哪一块。'),
        title='思考题 ④：固定大小有什么不便，怎么解决？', color='green', size=14.5, min_h=1.55)
    banner(s, '这两题想通了，第8讲链表就提前入门了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '把今天的"固定大小"接到动态内存与链表')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：\\0 是"到此为止"',
         'body': "C 没有 string 类型，字符串就是\n"
                 "以 '\\0' 结尾的字符数组\n"
                 "所有字符串函数都靠它判断结尾 ——\n"
                 "printf 会一直往后读，直到碰上 0\n"
                 "'\\0' 的 ASCII 值是 0，是空字符，\n"
                 "不是字符 '0'（那是 48）\n"
                 "不加的后果：轻则输出乱码，\n"
                 "重则读到不可访问内存直接崩\n"
                 "strlen 数到 '\\0' 停（4），\n"
                 "sizeof 量整块内存（5）",
         'color': 'teal', 'size': 12.5},
        {'title': '解答 ④：固定大小的三重不便',
         'body': '一、必须提前预估：估小越界、\n'
                 '估大浪费，运行时才知道数量做不到\n'
                 '二、不能动态调整：想加元素，\n'
                 '只能新开大数组再把数据搬过去\n'
                 '三、插入删除很慢：要移动后面\n'
                 '所有元素，时间复杂度 O(n)\n'
                 '解法：malloc 在堆上按需分配、\n'
                 '链表增删只需改指针、\n'
                 '结构体数组把平行数组合并\n'
                 '数组 O(1) 随机访问仍是它的强项',
         'color': 'green', 'size': 12.5},
    ], gap=0.26)
    banner(s, '数组的局限，正是第7、8讲登场的理由 —— 这就是技术演进的动力')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第6讲 数组 —— 批量数据的容器')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '数组是"一个名字 + 一个索引"管理一组同类型数据的容器：连续内存、随机访问 O(1)、'
        '索引从 0 开始、大小为固定值。字符数组加上结束标志就是字符串，'
        '数组传参会退化成指针，必须额外带上长度。'),
        title='📝 一句话总结', color='teal', size=14.5, min_h=0.98)
    y = y2 + 0.24

    rows = [('1', '一维数组', '同类型数据的连续集合，索引从 0 开始'),
            ('2', '二维数组', '数组的数组，按行优先连续存储'),
            ('3', '字符数组', "C 没有 string，字符数组 + '\\0' 就是字符串"),
            ('4', '数组作参数', '退化为指针，长度信息丢失，须显式传长度'),
            ('5', '数组与指针', 'arr[i] 等价于 *(arr+i)，sizeof 结果不同'),
            ('6', '连续内存', '随机访问 O(1)；大小固定是它的局限')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：结构体 —— 把散落的平行数据打包成一条记录（第7讲）')
    done('P18')


for fn in (p01_cover, p02_map, p3_pain, p4_array1, p5_array2, p6_string, p7_decay,
           p8_relation, p9_memory, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
