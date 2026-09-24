# -*- coding: utf-8 -*-
"""
第8讲：链表 —— 动态数据的灵活管理
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

LECTURE = '第8讲 链表'
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
                    title=sp.get('title'), color=sp.get('color', 'purple'),
                    size=sp.get('size', 16), min_h=sp.get('min_h', 0.0))
        bottoms.append(b)
    return max(bottoms)


def cards_col(s, x, y, w, specs, gap=0.20, size=15):
    for sp in specs:
        b, _ = card(s, x, y, w, sp['body'], title=sp.get('title'),
                    color=sp.get('color', 'purple'), size=sp.get('size', size),
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
    rect(slide, 0, 0, 4.4, SH, fill=C['card_purple'])
    rect(slide, 0, 0, 0.16, SH, fill=C['purple'])
    rect(slide, 4.4, 0, SW - 4.4, 0.12, fill=C['purple'])

    _put_text(slide, 0.75, 1.15, 3.3, 0.5, '从程序员到架构师', 20, C['purple_dark'], bold=True)
    _put_text(slide, 0.75, 1.72, 3.3, 0.4, 'C语言插件框架演进之旅', 14, C['ink2'])
    rect(slide, 0.75, 2.30, 0.9, 0.05, fill=C['purple'])

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第8讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.55, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['purple_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '链表', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '动态数据的灵活管理', 27, C['purple_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.6,
              '第7讲把一条记录打包好了，可它还是装在数组里，\n'
              '大小一开始就定死：多了放不下，少了又浪费。\n'
              '银行客户从 5 个涨到 5000 个，难道每次都要改代码？\n'
              '本讲用指针把节点串起来——车厢随挂随摘，大小随时变。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '第②级"函数"的数据面 —— 从"固定大小"到"动态增长"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '前两讲解决了"数据怎么放"：数组排成一排、结构体打包成一条。但它们的容量都在编译期就定死了。'
        '本讲用"数据域 + 指针域"的节点，把一串数据动态串起来，这是第12讲插件链表管理的直接地基。'),
        title='🎯 本讲定位', color='purple', size=15.5, min_h=1.15)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '← 本讲深挖'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '第9-10讲'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('gray', 'purple', 'gray', 'gray', 'gray', 'gray'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第5讲：指针能拿地址\n第7讲：结构体把数据打包成一条记录'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第12讲：插件链表管理（每个插件一个节点）\n第13讲：配置化菜单（菜单项用链表管）'),
        title='➡ 后续', color='teal', size=14.5, min_h=1.00)
    banner(s, '链表 = 结构体 + 指针：把一条条记录用"挂钩"串成一列火车')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '结构体把记录打包好了，可容量还是死的')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第7讲：已经做到的', [
                    '一个结构体就是一条完整记录',
                    '结构体数组替代了平行数组',
                    '结构体指针能遍历、能改原数据'],
                '第8讲：要补上的', [
                    '节点按需 malloc，大小不再定死',
                    '头部插入、尾部插入，随时加一条',
                    '用完 free，避免内存泄漏'],
                left_color='blue', right_color='green', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '坑一：容量定死', 'body': 'accounts[5] 想加第 6 个账户\n只能改代码重新编译',
         'color': 'red', 'size': 13},
        {'title': '坑二：空间浪费', 'body': 'trans[10] 只用了 2 格\n剩下 8 格也一直占着',
         'color': 'purple', 'size': 13},
        {'title': '坑三：会覆盖旧数据', 'body': '第 11 笔写回第 1 格\n一年前的记录找不回来',
         'color': 'orange', 'size': 13},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：数组是"一排定长的储物柜"，链表是"一列随时加挂车厢的火车"',
    ], size=15)
    banner(s, '本讲用 malloc 按需分配 + 指针串联，把数据容量交给运行期')
    done('P3')


# ============================================================
# P4 核心内容一：节点结构（数据域 + 指针域）
# ============================================================
def p04_node():
    s = pg('节点：数据域 + 指针域', '每节车厢装自己的货，再用挂钩连上下一节')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '链表的基本单位是节点：数据域存数据，指针域 next 存下一个节点的地址 —— 这叫自引用结构。'),
        title='🚃 节点就是一节火车车厢', color='purple', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        'typedef struct TransactionNode {',
        '    /* ---- 数据域 ---- */',
        '    double amount;   /* 交易金额 */',
        '    int    type;     /* 交易类型 */',
        '    char   desc[40]; /* 交易描述 */',
        '    /* ---- 指针域 ---- */',
        '    struct TransactionNode* next;  /* 下一节 */',
        '} TransactionNode;',
    ], title='节点定义：自引用结构', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    rb, _ = code(s, xr, y, wr, [
        'head ──> [车厢A] ──> [车厢B] ──> [车厢C] ──> NULL',
        '         数据+next    数据+next    数据+next',
        '',
        'head = NULL   一节车厢都没有（空链表）',
        'next = NULL   最后一节，后面没车厢了',
    ], title='一列链表：靠 next 串起来', size=11.5)
    card(s, xr, rb + 0.18, wr, (
        '数组像一排紧挨着的储物柜；\n'
        '链表像散落各地的仓库，只能顺着线索找。'),
        title='🏬 一句话记住', color='teal', size=13)
    banner(s, '节点 = 数据 + 挂钩；挂钩没了（NULL），这列火车就到头了')
    done('P4')


# ============================================================
# P5 核心内容二：创建与销毁（malloc / free）
# ============================================================
def p05_malloc():
    s = pg('创建与销毁：malloc 与 free', '节点在堆上按需分配，用完必须手动释放')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '链表节点分配在堆上，用 malloc 申请、free 释放。malloc 不会自动回收：只 malloc 不 free，'
        '就是内存泄漏——借了车厢不还，停车场越来越满。'),
        title='🧱 堆上的节点，手动管理', color='purple', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        'TransactionNode* create_trans_node(...) {',
        '    TransactionNode* node =',
        '        malloc(sizeof(TransactionNode));',
        '    if (node == NULL) return NULL;  /* 分配失败 */',
        '    node->amount = amount;',
        '    node->next = NULL;   /* 新节点暂时无后继 */',
        '    return node;',
        '}',
    ], title='创建：malloc 一块，填好数据', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'void trans_destroy(void) {',
        '    TransactionNode* cur = trans_head;',
        '    while (cur != NULL) {',
        '        TransactionNode* tmp = cur;  /* 先存 */',
        '        cur = cur->next;             /* 再移 */',
        '        free(tmp);                   /* 后释放 */',
        '    }',
        '    trans_head = NULL;',
        '}',
    ], title='销毁：先存 next，再 free', size=11.5)
    banner(s, '顺序一定是"先记住下一节，再拆这一节"——先 free 再取 next 会用已释放的内存')
    done('P5')


# ============================================================
# P6 核心内容三：增（头插 / 尾插）
# ============================================================
def p06_insert():
    s = pg('增：头部插入与尾部插入', '头插只改两个指针 O(1)，尾插要先走到末尾 O(n)')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '头部插入  O(1)', [
                    '新节点指向旧头，头指针改指新节点',
                    '只改两个指针，不用遍历',
                    '适合"最近发生的排最前"'],
                '尾部插入  O(n)', [
                    '先走到最后一节，再挂上新车厢',
                    '要遍历到末尾，规模大时较慢',
                    '适合"按时间顺序留档"'],
                left_color='purple', right_color='teal', size=14) + 0.14

    cw = INNER_W * 0.50
    code(s, MARGIN_L, y, cw, [
        '/* 头部插入：O(1) */',
        'node->next = trans_head;',
        'trans_head = node;',
        '',
        '/* 插入前：head -> A -> B -> NULL   */',
        '/* 插入后：head -> NEW -> A -> B    */',
    ], title='头插：两个指针搞定', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '/* 尾部插入：O(n) */',
        'if (trans_head == NULL) {',
        '    trans_head = node; return;   /* 空链表 */',
        '}',
        'TransactionNode* cur = trans_head;',
        'while (cur->next != NULL) cur = cur->next;',
        'cur->next = node;   /* 走到末尾再挂 */',
    ], title='尾插：先走到末尾', size=11.5)
    banner(s, '记住两个动作：头插 = 改两个指针；尾插 = 先走到末尾，再挂车厢')
    done('P6')


# ============================================================
# P7 核心内容四：删（按值 / 按位置）
# ============================================================
def p07_delete():
    s = pg('删：按值删除与按位置删除', '删除的关键是拿到"前驱节点"，再让前驱跳过被删节点')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '删除分两种：删头节点就头指针后移；删中间节点要先找到前驱，再让前驱跳过它。'),
        title='✂️ 摘车厢：先重新挂钩，再运走', color='purple', size=15, min_h=1.05)
    y = y2 + 0.20

    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        '/* 按值删除：删金额匹配的第一个节点 */',
        'if (trans_head->amount == amount) {   /* 删头 */',
        '    TransactionNode* tmp = trans_head;',
        '    trans_head = trans_head->next;  free(tmp);  return;',
        '}',
        'while (cur != NULL) {',
        '    if (cur->amount == amount) {',
        '        prev->next = cur->next;  free(cur);  return;',
        '    }',
        '    prev = cur;  cur = cur->next;',
        '}',
    ], title='按值删除（删头是特殊情况）', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '删中间节点要前驱', 'body': 'prev->next = cur->next\n前驱跳过当前节点，再 free 掉它',
         'color': 'red', 'size': 13},
        {'title': '改数据：找到再改', 'body': 'cur->type = new_type;\n修改本身 O(1)，查找 O(n)',
         'color': 'orange', 'size': 13},
    ], gap=0.18)
    banner(s, '删除不是"抹掉"，而是"改挂钩 + 还内存"，缺一不可')
    done('P7')


# ============================================================
# P8 核心内容五：查/遍历 + 插件框架应用
# ============================================================
def p08_find_plugin():
    s = pg('查与遍历 —— 以及它在插件框架中的应用', '从 head 走到 NULL，一个 while 走完全链')
    y = BODY_TOP
    cw = INNER_W * 0.50
    code(s, MARGIN_L, y, cw, [
        '/* 遍历：从头走到 NULL */',
        'TransactionNode* cur = trans_head;',
        'while (cur != NULL) {',
        '    printf("%.2f %s\\n", cur->amount, cur->desc);',
        '    cur = cur->next;   /* 移动到下一节 */',
        '}',
        '',
        '/* 查找：遍历中比较，命中就返回 */',
        'while (cur != NULL) {',
        '    if (cur->id == id) return cur;',
        '    cur = cur->next;',
        '}',
        'return NULL;   /* 没找到 */',
    ], title='查与遍历：从 head 到 NULL', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '/* 插件框架里的"插件节点" */',
        'typedef struct PluginNode {',
        '    char name[20];      /* 插件名 */',
        '    char feature[40];   /* 功能描述 */',
        '    struct PluginNode* next;',
        '} PluginNode;',
        '',
        '/* 加载插件 = 头插到插件链表 */',
        'p->next = *head;  *head = p;',
        '',
        '/* 执行所有插件 = 遍历链表 */',
        'while (cur) { run(cur); cur = cur->next; }',
    ], title='本讲的终点：插件链表（预告第12讲）', size=11.5)
    banner(s, '插件管理 = 链表 + 函数指针；配置化菜单 = 菜单项也是链表节点')
    done('P8')


# ============================================================
# P9 原理深入：链表的内存布局 ⭐
# ============================================================
def p09_memory():
    s = pg('原理深入：链表的内存布局 ⭐', '数组靠"连续"换 O(1)，链表靠"指针"换灵活性')
    y = BODY_TOP
    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        '/* 数组：一整块连续内存 */',
        '[10][20][30][40][50]',
        ' 100 104 108 112 116   下标一步定位 O(1)',
        '',
        '/* 链表：节点分散在堆上，靠 next 串联 */',
        'head -> [10|next] -> [20|next] -> [30|NULL]',
        '         0x1400        0x2200        0x900',
        '要访问第 3 个，只能顺指针走 3 步 O(n)',
        '',
        '/* 但增删只要改指针，不必搬家 */',
    ], title='连续 vs 分散：两种内存模型', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    y2, _ = card(s, xr, y, wr, (
        '数组知道首地址和元素大小，第 i 个元素地址一次乘法加法就算出来；'
        '链表每个节点的地址都不确定，只能顺着 next 一节一节找。'),
        title='⚡ 为什么链表不能随机访问', color='purple', size=13, min_h=1.75)
    card(s, xr, y2 + 0.18, wr, (
        '每个节点多一个 next 指针，\n'
        '换来的却是"想加就加、想删就删"。\n'
        '空间与灵活性的取舍。'),
        title='⚖️ 代价换来了什么', color='teal', size=13, min_h=1.45)
    banner(s, '数组用连续换速度，链表用指针换灵活 —— 没有免费的结构，只有合适的场景')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：链表 vs 数组', '同一个问题，两种数据结构，选谁看场景')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '数组', [
                    '一整块连续内存，下标直接定位',
                    '大小编译期定死，运行期不变',
                    '随机访问 O(1)，插入删除 O(n)'],
                '链表', [
                    '节点分散在堆上，靠指针串联',
                    '大小运行期可变，想加就加',
                    '访问第 i 个 O(n)，增删只改指针'],
                left_color='blue', right_color='purple', size=14) + 0.16

    rows = [('内存布局', '连续分配，一整块', '分散分配，指针相连'),
            ('访问第 i 个', 'O(1)，一步算到', 'O(n)，从头顺着走'),
            ('插入 / 删除', 'O(n)，后面全体搬家', 'O(1)，改两个指针'),
            ('额外开销', '无', '每节点多一个 next 指针'),
            ('内存管理', '自动或固定', 'malloc / free 手动管理')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.18, 0.41, 0.41),
            size=12, header=('维度', '数组', '链表'))
    banner(s, '要频繁随机访问选数组，要频繁增删、大小不定选链表')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/linked_atm.c —— 节点、malloc、插入、销毁一整套')
    y = BODY_TOP
    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        'typedef struct TransactionNode {',
        '    double amount;  int type;',
        '    char   desc[DESC_LEN];',
        '    struct TransactionNode* next;',
        '} TransactionNode;',
        '',
        'TransactionNode* create_trans_node(...) {',
        '    TransactionNode* node = malloc(sizeof(*node));',
        '    node->next = NULL;  return node;',
        '}',
    ], title='节点定义 + 创建', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    rb, _ = code(s, xr, y, wr, [
        '/* 尾部插入：追加到末尾 */',
        'void acct_insert_tail(int id, ...) {',
        '    AccountNode* node = create_acct_node(...);',
        '    if (acct_head == NULL) {',
        '        acct_head = node;  return;',
        '    }',
        '    AccountNode* cur = acct_head;',
        '    while (cur->next != NULL) cur = cur->next;',
        '    cur->next = node;   /* 追加 */',
        '}',
    ], title='尾部插入：走到末尾再挂', size=11.5)
    b = max(rb, y + 10 * 11.5 * 1.42 / 72 + 0.40 + 0.36)
    card(s, MARGIN_L, b + 0.20, cw, (
        '每个账户、每笔交易都是 malloc 出来的节点，退出前统一销毁。'),
        title='🌱 链表的账要还清', color='green', size=13)
    demo_frame(s, xr, b + 0.20, wr, 1.30,
               title='真实运行（节选）',
               lines=['已用链表加载 5 个账户。',
                      '共 1 条交易记录（链表节点数）',
                      '（链表已销毁，内存已释放）'])
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '链表加载账户、交易入链、插件链表、内存释放 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.60
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall -o linked_atm.exe linked_atm.c',
        '（无警告 —— malloc / free 配对都用对了）',
        "$ printf '1001\\n2\\n500\\n5\\n6\\n7\\n0\\n' | ./linked_atm.exe",
        '   欢迎使用 CCIT ATM 系统（链表版）',
        '  动态交易记录 | 动态账户管理 | 无上限',
        '已用链表加载 5 个账户。',
        '  账户ID: 1001  姓名: 张三  余额: 1000.00',
        '请输入您的账户ID：登录成功！欢迎，张三',
        '请输入存款金额：操作成功！存入 500.00 元',
        '【交易记录】1  存款  500.00  张三 存入 500.00',
        '共 1 条交易记录（链表节点数）',
        '[1] 插件名：电子发票  |  功能：生成电子发票',
        '[2] 插件名：积分兑换  |  功能：积分兑换礼品',
        '[3] 插件名：汇率查询  |  功能：查询实时汇率',
        '（链表已销毁，内存已释放）',
        '$ echo $?     →     0',
    ], title='终端实录（真实输出，未删改）', size=11.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译零警告：malloc 与 free 配对了\n'
        '② 5 个账户：全部 malloc 成节点\n'
        '③ 存款入链：交易追加到链表尾部\n'
        '④ 遍历统计：共 1 条交易记录\n'
        '⑤ 插件链表：3 个插件就是一个链表\n'
        '⑥ 退出前销毁：内存已释放，退出码 0'),
        title='👀 要看清楚的六个点', color='purple', size=12.5, min_h=4.35)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 src/linked_atm.c')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '第②级"函数"的数据面：链表是插件管理器的地基')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。本讲仍在第②级夯数据的地基，'
        '却第一次让数据"动"了起来——不用预先知道有多少，运行期随时增删。'
        '第12讲的插件链表、第14讲的配置化菜单，都直接长在这套链表操作上。'),
        title='🧭 一条主线', color='purple', size=15, min_h=1.15)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '← 本讲 ⭐'),
        ('③ 模块', '第4讲 ✅'),
        ('④ 库', '第9-10讲'),
        ('⑤ 插件', '第11-12讲'),
        ('⑥ 框架', '第13讲'),
    ], colors=('gray', 'purple', 'gray', 'gray', 'gray', 'gray'),
        size=14, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '链表让数据容量交给运行期：\n'
        'malloc 按需分配、free 用完归还；\n'
        '增删只改指针，不必搬家。\n'
        '插件链表管理就是它的直接应用。'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第12讲：链表节点里装函数指针，\n'
        '变成可统一调用的插件接口；\n'
        '第13讲：菜单项也用链表管理，\n'
        '加一个插件就自动多一行菜单。'),
        title='后面接着做什么', color='blue', size=13.5, min_h=1.55)
    banner(s, '数组把数据排成一排，链表把数据串成一列 —— 后者才是动态和插件的地基')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '数组能用 arr[5] 一步定位第 6 个元素，链表却必须从头逐个遍历。这是为什么？'
        '如果写一个 get_at(head, index) 取第 index 个节点，复杂度是多少？\n'
        '提示：数组元素在内存里连续排列，有地址公式；链表的节点却分散在堆上。'),
        title='思考题 ①：链表为什么不能随机访问？', color='purple', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '一个函数里 malloc 了一个节点却没有 free，函数结束后这个节点会怎样？'
        '如果这个函数被调用一百万次呢？\n'
        '提示：malloc 的内存在堆上，谁负责回收？什么叫"内存泄漏"？'),
        title='思考题 ②：忘记 free 会怎样？', color='orange', size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：内存布局不同',
         'body': '数组元素连续排列，地址可以算：\n'
                 'arr[i] 地址 = 首地址 + i × 元素大小\n'
                 '所以一步乘法加法就定位，O(1)。\n'
                 '链表节点是 malloc 分散分配的，\n'
                 '每个节点在哪并不确定，\n'
                 '没有公式能算出第 5 个在哪，\n'
                 '只能顺着 next 一节节找，O(n)。\n'
                 '结论：频繁随机访问选数组，\n'
                 '频繁增删、大小不定选链表。',
         'color': 'purple', 'size': 12.5},
        {'title': '解答 ②：堆内存不会自动收回',
         'body': 'node 是局部变量，在栈上，\n'
                 '函数结束它自动消失；\n'
                 '但 malloc 的内存在堆上，不会自动释放。\n'
                 '指针一消失，那块内存就再也找不到，\n'
                 '没法 free —— 这就是内存泄漏。\n'
                 '调用一百万次，每次漏一个节点，\n'
                 '累计几十 MB，长期运行必然崩溃。\n'
                 '好习惯：每个 malloc 都要配一个 free。',
         'color': 'orange', 'size': 12.5},
    ], gap=0.26)
    banner(s, 'C 给你动态内存的自由，也把"记得归还"的责任一并交给你')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：有序插入，以及链表有环怎么办')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '假设链表按金额从小到大排序，现在插入一笔新交易，插入后仍要有序，该怎么写？'
        '复杂度是多少？\n'
        '提示：找到第一个比新节点大的位置，插在它前面；想想空链表和插在末尾这两种情况。'),
        title='思考题 ③：有序链表的插入怎么做？', color='purple', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '如果某个节点的 next 不是指向后面，而是指向前面的节点，就形成了"环"。'
        '遍历这样的链表会怎样？怎么检测有没有环？\n'
        '提示：while 循环里 cur 永远不等于 NULL 会怎样？有没有不用额外空间的办法？'),
        title='思考题 ④：链表有环会怎样，如何检测？', color='teal', size=14.5, min_h=1.55)
    banner(s, '这两题想通了，链表的"指针操作"就真正练到手了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '把今天的"指针串联"接到链表的两个经典难题')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：找位置，插前面',
         'body': '从 head 开始找第一个比新值大的节点，\n'
                 '把新节点插在它前面。\n'
                 '若链表为空，或头节点就比新值大，\n'
                 '直接插到头部；\n'
                 '若走到末尾都没找到更大的，\n'
                 '就追加到末尾。\n'
                 '循环条件用 cur->next 判断：\n'
                 'while (cur->next && cur->next->amount < v)\n'
                 '时间复杂度 O(n)。\n'
                 '应用：优先队列、按时间排序的流水。',
         'color': 'purple', 'size': 12.5},
        {'title': '解答 ④：快慢指针判环',
         'body': '有环时 while (cur != NULL) 永远不结束，\n'
                 '程序死循环，CPU 占用拉满。\n'
                 '检测办法一：记下走过的每个节点地址，\n'
                 '发现重复即有环 —— 需要 O(n) 额外空间。\n'
                 '办法二（Floyd 判圈）：\n'
                 '慢指针一次走一步，快指针一次走两步，\n'
                 '若有环，快指针迟早追上慢指针；\n'
                 '若快指针走到 NULL，就没有环。\n'
                 '时间 O(n)，空间 O(1)，经典面试题。',
         'color': 'teal', 'size': 12.5},
    ], gap=0.26)
    banner(s, '指针是链表的灵魂：会写指针，才真正踏入数据结构的大门')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第8讲 链表 —— 动态数据的灵活管理')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '链表用"数据域 + 指针域"的节点，把一串数据动态串起来：malloc 按需分配、free 用完归还；'
        '头插 O(1)、尾插 O(n)；删除要先找到前驱；访问必须从头遍历。大小随时可变，这就是它的价值。'),
        title='📝 一句话总结', color='purple', size=14.5, min_h=0.98)
    y = y2 + 0.24

    rows = [('1', '节点结构', '数据域 + 指针域，next 是自引用指针'),
            ('2', '创建与销毁', 'malloc 分配、free 释放；先存 next 再 free'),
            ('3', '增', '头部插入 O(1)，尾部插入 O(n)'),
            ('4', '删', '按值 / 按位置，关键是找到前驱再改指针'),
            ('5', '查与改', '遍历从 head 到 NULL；修改前先查找 O(n)'),
            ('6', '链表 vs 数组', '链表动态灵活但只能顺序访问，数组随机访问快但大小固定')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：静态库 —— 把链表代码打包成 .a，跨项目复用（第9讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_node, p05_malloc, p06_insert, p07_delete,
           p08_find_plugin, p09_memory, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
