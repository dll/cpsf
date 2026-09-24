# -*- coding: utf-8 -*-
"""
第13讲：插件框架架构 —— 让框架来调用你
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

LECTURE = '第13讲 插件框架架构'
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

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第13讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.55, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '插件框架架构', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '让框架来调用你', 27, C['primary_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.6,
              '第12讲统一了插件接口，能注册、能发现了，\n'
              '可没人管生命周期、注册靠手动、菜单还硬编码。\n'
              '本讲请一个"管家"：状态机管顺序、管理器管秩序、\n'
              '配置化菜单管扩展——加插件，不改主程序。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '六级台阶的最后一级 —— 框架，第一次出现"控制反转"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '前十二讲，我们一直在"往上搭"：表达式、函数、模块、库、插件，一级比一级抽象。\n'
        '本讲站上第六级——框架。它最特别的地方是：控制流不再只向下走，'
        '框架会在合适的时机，反过来调用你写的插件代码。'),
        title='🎯 本讲定位', color='orange', size=15.5, min_h=1.15)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '第3讲 ✅'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '第9-10讲 ✅'), ('⑤ 插件', '第11-12讲 ✅'), ('⑥ 框架', '← 你在这里')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('teal', 'teal', 'teal', 'teal', 'teal', 'primary'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第12讲：统一 Plugin 接口 + 注册 + 发现\n'
        '第8讲链表、第11讲运行时加载打底'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第14讲：把 dlopen、目录扫描接进来\n'
        '让插件真的"从文件里来"，完成收官'),
        title='➡ 后续', color='teal', size=14.5, min_h=1.00)
    banner(s, '本讲把"插件"拼成一个框架：有生命周期、有秩序、有插槽')
    done('P2')

# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '能注册、能发现了，但还留着三个坑')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第12讲：已经做到的', [
                    '统一 Plugin 接口：init / execute / cleanup',
                    '能注册、能发现：链表统一管理插件',
                    '有统一插座，各种插件能被一样地调用'],
                '第13讲：要补上的', [
                    '五阶段生命周期：多了 start / stop',
                    '状态机：状态不对就拒绝，错误挡在门口',
                    '配置化菜单：注册即挂载，加功能不改主程序'],
                left_color='blue', right_color='green', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '坑一：生命周期无人管', 'body': '3 阶段全靠调用方自觉\n顺序错、漏调用、重复释放都会炸',
         'color': 'red', 'size': 13},
        {'title': '坑二：注册靠手动', 'body': '忘记 plugin_register()\n编译通过、功能静默消失',
         'color': 'purple', 'size': 13},
        {'title': '坑三：菜单硬编码', 'body': 'printf 一行行写、switch 一个个 case\n加功能 = 改主程序三处',
         'color': 'orange', 'size': 13},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：加一个插件就要改主程序，正是开闭原则最反对的事',
    ], size=15)
    banner(s, '本讲用一个框架，同时填掉这三个坑')
    done('P3')


# ============================================================
# P4 核心内容一：五阶段生命周期
# ============================================================
def p04_lifecycle():
    s = pg('五阶段生命周期：从 3 阶段到 5 阶段', 'init 是进货，start 是开门营业，stop 是打烊，cleanup 是清算关店')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '第12讲只有三步：init → execute → cleanup。问题在于"分配了资源"和"对外提供服务"'
        '被压成同一件事，中间没有回旋余地。本讲把 lifecycle 拆成五段，把这两件事分开。'),
        title='📌 为什么要多出两步', color='orange', size=15, min_h=1.05)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('init', '准备资源\n只做一次'),
        ('start', '对外服务\n只做一次'),
        ('execute', '核心业务\n可反复调用'),
        ('stop', '停止服务\n只做一次'),
        ('cleanup', '释放资源\n只做一次'),
    ], colors=('blue', 'teal', 'orange', 'purple', 'gray'), size=15, h=1.05) + 0.24

    card(s, MARGIN_L, y, INNER_W, (
        'ATM 开机要加载 4 个插件：存款 init 成功、取款 init 失败。只有 3 阶段时，系统就卡在'
        '"一半可用"的尴尬里，失败插件占着资源却没有回滚时机。\n'
        '拆出 start 后变成两阶段提交：全部 init 成功 → 才允许全部 start，任何一步失败都能整体中止。'),
        title='💡 四插件里有一个初始化失败，怎么办？', color='red', size=14.5, min_h=1.30)
    banner(s, 'init 是"准备好了"，start 是"开始服务"——两种状态，必须分开')
    done('P4')


# ============================================================
# P5 核心内容二：生命周期状态机
# ============================================================
def p05_state():
    s = pg('生命周期状态机：六种状态，管住顺序', 'UNLOADED → LOADED → INITIALIZED → STARTED → STOPPED → CLEANED')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '管理器就是守着这张图：状态不对就拒绝，并把原因说清楚。\n'
        '失败不升状态 —— 会被后续的 start_all 自然跳过，失败会自己"传染"到下一个阶段。'),
        title='🧭 六个状态，一条单向链', color='blue', size=14.5, min_h=1.05)
    y = y2 + 0.24

    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        'typedef enum {',
        '    PLUGIN_UNLOADED = 0,   /* 未加载 */',
        '    PLUGIN_LOADED,         /* 已加载（已注册到管理器） */',
        '    PLUGIN_INITIALIZED,    /* 已初始化（init 成功） */',
        '    PLUGIN_STARTED,        /* 已启动（start 成功，可执行） */',
        '    PLUGIN_STOPPED,        /* 已停止（stop 成功） */',
        '    PLUGIN_CLEANED         /* 已清理（cleanup 成功） */',
        '} PluginState;',
        '/* 迁移：UNLOADED -> LOADED -> ... -> CLEANED -> UNLOADED */',
    ], title='framework.h：状态枚举（契约，不可改）', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'if (p->state != PLUGIN_LOADED) {',
        '    /* 状态前置校验：状态不对，不放行 */',
        '    printf("  [%s] 跳过：状态 %s\\n",',
        '           p->name, state_name(p->state));',
        '} else if (p->init(p) == 0) {',
        '    p->state = PLUGIN_INITIALIZED;  /* 升状态 */',
        '}',
    ], title='init_all() 的核心：先看状态，再放行', size=11)
    banner(s, '状态机是框架的守门人：不合规矩的操作，当场拒绝并说明理由')
    done('P5')


# ============================================================
# P6 核心内容三：插件管理器
# ============================================================
def p06_manager():
    s = pg('插件管理器：给插件请一个"管家"', '链表 + 批量操作 + 查找执行 —— 对应 C++ 的 PluginManager 类')
    y = BODY_TOP
    cw = INNER_W * 0.50
    rows = [('manager_register(p)', '注册插件：挂插件链表 + 挂菜单项'),
            ('manager_init_all()', '批量初始化：LOADED → INITIALIZED'),
            ('manager_start_all()', '批量启动：INITIALIZED → STARTED'),
            ('manager_stop_all()', '批量停止：STARTED → STOPPED'),
            ('manager_cleanup_all()', '批量清理：STOPPED → CLEANED'),
            ('manager_find / execute', '按名字查找、执行（要求 STARTED）'),
            ('manager_destroy()', '释放链表：CLEANED → UNLOADED')]
    kv_rows(s, MARGIN_L, y, cw, rows, widths=(0.44, 0.56), size=11.5,
            header=('manager_* 接口', '职责与状态变化'))

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'static PluginNode* g_plugin_head = NULL;  /* 链表头 */',
        'static PluginNode* g_plugin_tail = NULL;  /* 尾插 O(1) */',
        'static int         g_plugin_count = 0;',
        '',
        'node->plugin = p;   node->next = NULL;',
        'if (g_plugin_tail == NULL) {          /* 空链表 */',
        '    g_plugin_head = node;  g_plugin_tail = node;',
        '} else {                              /* 尾插 */',
        '    g_plugin_tail->next = node;  g_plugin_tail = node;',
        '}',
        'g_plugin_count++;',
    ], title='链表实现：头尾指针 + 计数（第8讲链表的延续）', size=11.5)
    card(s, xr, y + 11 * 11.5 * 1.42 / 72 + 0.40 + 0.36 + 0.20, wr, (
        '第12讲头插顺序相反；本讲用尾指针，依然 O(1) 且保序。'),
        title='⚖️ 设计取舍：要顺序，也要性能', color='purple', size=12.5)
    done('P6')


# ============================================================
# P7 核心内容四：扩展点设计
# ============================================================
def p07_ext():
    s = pg('扩展点设计：插件能挂在哪里？', '框架好不好用，就看它留了多少"插槽"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '扩展点就是框架预留的"插槽"：插件把自己的钩子插进去，框架照着槽位统一回调。'),
        title='🔌 什么是扩展点', color='teal', size=15, min_h=1.05)
    y = y2 + 0.24

    cw = INNER_W * 0.54
    rows = [('菜单项', 'menu_id + menu_label + 菜单链表', '✅ 已实现'),
            ('命令', 'manager_find() + manager_execute()', '✅ 已实现'),
            ('事件', '插件注册回调，框架按时机回调', '🔜 第14讲')]
    kv_rows(s, MARGIN_L, y, cw, rows, widths=(0.18, 0.58, 0.24),
            size=11.5, header=('扩展点', '载体', '本讲状态'))

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'static Plugin transfer_plugin = {',
        '    .name = "转账",',
        '    .menu_id = 4,          /* ← 只填这两个字段 */',
        '    .menu_label = "转账",',
        '    .init = transfer_init, .start = transfer_start,',
        '    .execute = transfer_execute,',
        '    .stop = transfer_stop, .cleanup = transfer_cleanup,',
        '};',
    ], title='插件只负责填表，不负责描述菜单', size=11)
    banner(s, '同一批插件，能被菜单调用、被命令行调用、被将来的 Web API 调用')
    done('P7')


# ============================================================
# P8 核心内容五：配置化菜单
# ============================================================
def p08_menu():
    s = pg('配置化菜单：菜单项就是链表节点', '第8讲链表的核心应用 —— 注册即挂载、卸载即摘除')
    y = BODY_TOP
    cw = INNER_W * 0.46
    code(s, MARGIN_L, y, cw, [
        'typedef struct MenuItem {',
        '    int  id;                 /* 菜单编号 */',
        '    char label[40];          /* 菜单文字 */',
        '    Plugin* plugin;          /* 关联的插件 */',
        '    struct MenuItem* next;   /* 下一个菜单项 */',
        '} MenuItem;',
    ], title='菜单项节点 = 链表节点', size=12.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '和普通链表唯一的不同，是多了 plugin 指针 —— 它把"用户看到的一行字"和"背后干活的插件"挂在一起。\n'
        '有了它，菜单处理就退化成纯粹的"查表 + 多态"。'),
        title='🔑 关键就是那个 plugin 指针', color='orange', size=13.5, min_h=2.05)
    y += 6 * 12.5 * 1.42 / 72 + 0.40 + 0.36 + 0.24

    compare(s, MARGIN_L, y, INNER_W,
            '第2讲：硬编码（功能写死在主程序）', [
                'printf("1. 存款\\n"); printf("2. 取款\\n");',
                'switch (choice) { case 1: deposit(); break; }',
                '加"转账"要改三处：打印、分支、编号'],
            '第13讲：配置化（数据驱动）', [
                '遍历链表显示：while (cur) { ... cur = cur->next; }',
                'menu_handle() 查表加多态，再调 manager_execute()',
                '加"转账"改 0 处：插件自带编号与菜单文字'],
            left_color='red', right_color='green', size=13)
    banner(s, '菜单不长在代码里，它长在链表里 —— 谁注册，谁就在里面')
    done('P8')


# ============================================================
# P9 原理深入：开闭原则 ⭐
# ============================================================
def p09_ocp():
    s = pg('原理深入：加插件，为什么可以不改主程序？ ⭐', '对扩展开放，对修改关闭 —— 开闭原则在 C 里的落地')
    y = BODY_TOP
    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        'int menu_handle(int choice, double amount) {',
        '    MenuItem* cur = g_menu_head;',
        '    while (cur != NULL) {',
        '        if (cur->id == choice) {',
        '            return manager_execute(cur->plugin->name, amount);',
        '        }                       /* 查表 + 多态：编译期不知道是谁 */',
        '        cur = cur->next;',
        '    }',
        '    return -1;              /* 没有这个编号的功能 */',
        '}',
    ], title='数一数这里面有几个 case：答案是 0 个', size=12)
    cards_col(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, [
        {'title': '支柱① 函数指针 = 多态', 'body': '编译期不知道会调用谁\n运行期看链表里挂的是谁', 'color': 'blue', 'size': 13},
        {'title': '支柱② 链表 = 数据驱动', 'body': '代码表达"怎么处理"\n数据表达"处理什么"', 'color': 'teal', 'size': 13},
        {'title': '支柱③ 稳定契约', 'body': 'framework.h 冻结语义\n扩展才能在契约上生长', 'color': 'purple', 'size': 13},
    ], gap=0.14)
    banner(s, '三次改动全是"新增"：新文件、加声明、加注册 —— 加功能零改动主程序')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：库 vs 框架，谁调用谁？', '控制反转（IoC）是框架和库的分界线')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '库（Library）', [
                    '你调用库：主程序是导演，指挥每一步',
                    '控制权在你手上，调用链一目了然',
                    '典型代表：libc、libaccount.a、json-c'],
                '框架（Framework）', [
                    '框架调用你：主程序只是启动器',
                    '控制权在框架手上，时机由状态机决定',
                    '典型代表：Qt、Spring、VS Code、本讲 framework'],
                left_color='blue', right_color='purple', size=14) + 0.16

    rows = [('加功能', '改 3 处（打印 / 分支 / 编号）', '改 0 处（插件自带 id 与 label）'),
            ('删功能', '容易残留"死分支"', 'menu_remove(id) 一句摘掉'),
            ('运行开销', '零开销', '多一次 O(n) 遍历，n 很小可忽略'),
            ('出错风险', '编号重复、漏改才报错', '编号重复会被 menu_add 拒绝并说明原因'),
            ('适合场景', '功能极少且几乎不变的小工具', '功能会持续增长、需要常加功能')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.14, 0.42, 0.44),
            size=12, header=('维度', '硬编码 switch', '配置化链表'))
    banner(s, "Don't call us, we'll call you. —— 别来找我们，我们会找你")
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/framework.c 与 src/main.c —— 注册即挂菜单，主程序只剩三行')
    y = BODY_TOP
    cw = INNER_W * 0.58
    code(s, MARGIN_L, y, cw, [
        'int manager_register(Plugin* p) {',
        '    if (p == NULL) return -1;              /* 关卡1：空指针 */',
        '    if (p->execute == NULL) return -1;     /* 关卡2：不是合法插件 */',
        '    /* 关卡3：重名拒绝；malloc 节点 + 尾插 + g_plugin_count++ */',
        '    p->state = PLUGIN_LOADED;              /* UNLOADED -> LOADED */',
        '    if (p->menu_id != 0) {',
        '        menu_add(p->menu_id, p->menu_label, p);  /* 注册即挂菜单 */',
        '    }',
        '    return 0;',
        '}',
    ], title='framework.c：注册即挂载（四道关卡都带"人话"提示）', size=11.5)
    card(s, MARGIN_L, y + 10 * 11.5 * 1.42 / 72 + 0.40 + 0.36 + 0.22, cw, (
        '六阶段的注册、初始化、启动、执行、停止、清理，'
        '主程序一行都没提 —— 它只说了"开始""运行""停止"。'),
        title='📊 状态闭环', color='green', size=13)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'int main(void)',
        '{',
        '    framework_start();  /* 初始化+注册+init+start */',
        '    framework_run();    /* 显示菜单 + 交互循环 */',
        '    framework_stop();   /* stop+cleanup+destroy */',
        '    return 0;',
        '}',
    ], title='main.c：通篇没有"存款""取款"', size=11.5)
    demo_frame(s, xr, y + 7 * 11.5 * 1.42 / 72 + 0.40 + 0.36 + 0.22, wr, 1.60,
               title='启动顺序（真实输出节选）',
               lines=['manager_init → menu_init',
                      '[注册] 存款 (状态: LOADED)',
                      '      └─ 菜单项已挂载： 1. 存款',
                      '-- start_all 完成：启动 4 个插件 --'])
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '命令、菜单、拒绝原因、退出码 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.60
    code(s, MARGIN_L, y, cw, [
        "$ gcc -Wall -o plugin_framework.exe framework.c atm_state.c \\",
        "      plugin_deposit.c plugin_withdraw.c plugin_query.c \\",
        "      plugin_transfer.c main.c",
        "$ printf '1\\n1\\n500\\n0\\n' | ./plugin_framework.exe",
        '=== 插件管理器已初始化（插件链表为空）===',
        '[注册] 存款 v1.1 - 向账户存入现金  (状态: LOADED)',
        '        └─ 菜单项已挂载： 1. 存款',
        '--- init_all 成功 4 个 / start_all 启动 4 个 ---',
        '========== ATM 主菜单（共 4 项，全部来自插件）==========',
        '  1. 存款   2. 取款   3. 查询余额   4. 转账   0. 退出',
        '请选择功能编号: 请输入金额（查询类请输入 0）:',
        '  [存款] 存入     1.00 元，余额 10001.00 元',
        '  [菜单] 无效选择：没有编号 500 的功能',
        '[框架] 输入流已结束，自动退出',
        '=== 菜单已销毁（释放 4 个菜单项节点）===',
        '=== 框架已安全关闭 ===',
        '$ echo $?   →   0',
    ], title='终端实录（真实输出，未删改）', size=11.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 注册即挂菜单：4 个插件各带一行菜单\n'
        '② 批量启动：init_all 成功 4 个 → start_all 启动 4 个\n'
        '③ 菜单来自链表：4 项全是插件挂上来的\n'
        '④ 编号 500 不存在 → 被 menu_handle 拦下，程序没崩\n'
        '⑤ 安全关闭：stop → cleanup → destroy\n'
        '⑥ 退出码 0：资源和链表全部回收，状态闭环'),
        title='👀 要看清楚的六个点', color='orange', size=12.5, min_h=4.35)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 framework.h / framework.c')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的最后一级：框架 —— 控制反转第一次真正登场')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。前五级都是"你调用别人"，'
        '只有第六级反过来：框架反过来调用你的代码 —— 这就是控制反转（IoC）。'),
        title='🧭 一条主线', color='orange', size=15, min_h=1.05)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '第3讲 ✅'),
        ('③ 模块', '第4讲 ✅'),
        ('④ 库', '第9-10讲 ✅'),
        ('⑤ 插件', '第11-12讲 ✅'),
        ('⑥ 框架', '← 本讲 ⭐'),
    ], colors=('gray', 'gray', 'gray', 'gray', 'gray', 'primary'),
        size=14, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '状态机管住生命周期顺序\n管理器管住注册与批量调度\n配置化菜单管住扩展点\n'
        '主程序从 60 行瘦到 3 行'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第14讲把 dlopen 与目录扫描接进来，\n'
        '连"有哪些插件"都不再由代码决定 ——\n'
        '那时控制反转才真正完整，整条主线收官。'),
        title='最后一讲接着做什么', color='blue', size=13.5, min_h=1.55)
    banner(s, '前五级是你调用世界，第六级是世界调用你 —— 这就是架构')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'init 成功后插件其实已经"能用"了，为什么还要多一个 start？'
        '我们的框架里，init 只申请资源，start 才对外提供服务。\n'
        '提示：想想 ATM 开机加载 4 个插件、其中一个 init 失败会怎样；'
        '再想想"暂停服务但保留状态"，3 阶段模型能不能表达？'),
        title='思考题 ①：init 与 start 为什么要分开？', color='orange', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '配置化之后加功能不用改主程序了，但这套方案是"免费"的吗？'
        '多了一个结构体、五个函数、一条链表，这些代价花得值不值？\n'
        '提示：从代码复杂度、可读性、运行开销、出错风险四个角度分析；'
        '再想想什么情况下反而应该老老实实写 switch。'),
        title='思考题 ②：配置化菜单的收益与代价', color='purple', size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：准备与服务，两种状态',
         'body': 'init 是"进货"，start 是"开门营业"\n'
                 '只有 3 阶段时，4 个插件有一个失败，\n'
                 '系统卡在"一半可用"，还没法回滚\n'
                 '拆出 start 后可两阶段提交：\n'
                 '全部 init 成功，才允许全部 start\n'
                 '多了 stop 这一级台阶，服务可暂停，\n'
                 'cleanup 不可逆 —— 可逆与不可逆分开',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ②：不是更高级，是换自由',
         'body': '收益：扩展性（改 0 处主程序）、\n'
                 '一致性（显示与处理共用一份数据）、\n'
                 '编号冲突被 menu_add 自动拒绝\n'
                 '代价：多一个结构体 + 5 个函数、\n'
                 '可读性下降（要逐个插件看 menu_id）、\n'
                 'O(n) 遍历、调试链变长\n'
                 '反而该硬编码：功能极少且稳定、\n'
                 '菜单项上千需哈希、二级菜单与权限',
         'color': 'purple', 'size': 12.5},
    ], gap=0.26)
    banner(s, '判断标准只有一条：这个菜单会持续增长吗？')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从 C 语言的开闭原则，接到框架与库的分界')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '有人说："开闭原则是面向对象的东西，C 语言没有继承多态，谈不了开闭原则。"\n'
        '本讲却做到"加转账插件零改动主程序"。提示：函数指针算不算多态？'
        '链表算不算"把结构交给数据"？framework.h 为什么必须冻结语义？'),
        title='思考题 ③：开闭原则在 C 语言中如何落地？', color='teal', size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '第12讲的 main() 有 60 多行，手动注册、手动 init、手动执行、手动清理；'
        '第13讲只剩三行 framework_start / run / stop。\n'
        '提示：这中间省掉的到底是什么？"控制权"从谁手上，交到了谁手上？'
        '再想想好莱坞那句 Don\'t call us, we\'ll call you。'),
        title='思考题 ④：框架与库的本质区别', color='green', size=14.5, min_h=1.55)
    banner(s, '这两题想通了，第14讲的完整项目就提前入门了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '把今天的"框架"接到最后一讲的总收官')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：三根支柱，能做但更费手',
         'body': '① 函数指针 = 多态：menu_handle 里\n'
                 '   编译期不知道会调哪个函数，\n'
                 '   运行期看链表挂了谁 —— 运行期绑定\n'
                 '② 链表 = 数据驱动：功能清单存进链表，\n'
                 '   代码说"怎么处理"，数据说"处理什么"\n'
                 '③ 稳定契约：framework.h 冻结语义\n'
                 '代价：无编译期检查、无访问控制、\n'
                 '手动 malloc/free。Linux 内核、\n'
                 'Redis、Nginx 都是这么干的',
         'color': 'teal', 'size': 12.5},
        {'title': '解答 ④：调用方向的反转',
         'body': '库是"你调用它"，框架是"它调用你"——\n'
                 '控制权在谁手上，就是分界线\n'
                 '第12讲 main() 是导演，60 多行手动调度\n'
                 '第13讲 main() 只是启动器，三行交权\n'
                 '反转发生在哪：控制流从 main 进入框架，\n'
                 '又从框架折返回你写的插件代码\n'
                 'main → framework_start → manager_init_all\n'
                 '        → 插件 init()   ← 折返，这就是反转\n'
                 '本讲还是静态注册，第14讲才完全体',
         'color': 'green', 'size': 12.5},
    ], gap=0.26)
    banner(s, '框架把秩序收上去，把自由留给了插件')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第13讲 插件框架架构 —— 让框架来调用你')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '状态机管生命周期，管理器管秩序，配置化菜单管扩展 —— 把控制权收归框架，加插件不改主程序。'),
        title='📝 一句话总结', color='orange', size=14.5, min_h=0.98)
    y = y2 + 0.24

    rows = [('1', '五阶段生命周期', 'init → start → execute(可多次) → stop → cleanup，init 准备、start 营业'),
            ('2', '状态机', 'UNLOADED → LOADED → INITIALIZED → STARTED → STOPPED → CLEANED'),
            ('3', '插件管理器', 'manager_* 系列：链表 + 批量 init/start/stop/cleanup + find/execute'),
            ('4', '扩展点设计', '菜单项 / 命令 / 事件，本质都是"链表 + 回调"'),
            ('5', '配置化菜单', '菜单项 = 链表节点；注册即挂载、卸载即摘除；menu_handle 零 switch'),
            ('6', '框架 vs 库', '库是你调用它，框架是它调用你 —— 控制反转 IoC')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：完整项目与全系列总结 —— 把 dlopen、目录扫描接进框架（第14讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_lifecycle, p05_state, p06_manager, p07_ext,
           p08_menu, p09_ocp, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
