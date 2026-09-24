# -*- coding: utf-8 -*-
"""
综合篇：从表达式到框架 —— 14 讲一次讲透（24 页）

依赖统一工具箱 tools/ppt_kit.py：
    · 标题单行自适应（R1）——投影时标题绝不换行
    · 容器不叠压、文字不越界、装饰永在底层（R2）——不再"前后不分"
    · 正文对比度 >= 4.5:1，代码一律深底亮字（R3）——投影看得清
每画完一页立刻 done('PN') 质检，有问题直接报错。

输出：docs/课件.pptx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # _work/summary/docs -> 项目根
sys.path.insert(0, os.path.join(PROJ, 'tools'))

from ppt_kit import *          # noqa
from ppt_kit import C, page, card, code, bullets, flow, compare, banner, footer_note, \
    kv_rows, text, panel, rect, audit, save, new_deck, blank, MARGIN_L, INNER_W, \
    BODY_TOP, BODY_BOTTOM, SW, SH, MARGIN_R, TITLE_TOP, fit_size, text_width_in, \
    _put_text, _reg_text, _reg_container, _reset_reg

LECTURE = '综合篇 · 从表达式到框架'
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
                    size=sp.get('size', 16), title_size=sp.get('title_size', 18),
                    min_h=sp.get('min_h', 0.0))
        bottoms.append(b)
    return max(bottoms)


def cards_col(s, x, y, w, specs, gap=0.20, size=13.5):
    for sp in specs:
        b, _ = card(s, x, y, w, sp['body'], title=sp.get('title'),
                    color=sp.get('color', 'orange'), size=sp.get('size', size),
                    title_size=sp.get('title_size', 17),
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
    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '综合篇 / 14 讲串讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.40, 3.5, 1.2,
              '半小时看完\n十四讲的完整演进', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '从表达式到框架', 46, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.05, 7.4, 0.6, '14 讲要点一次讲透', 24, C['primary_dark'])
    rect(slide, 5.35, 3.80, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.05, 7.2, 1.8,
              '这一期不引入新知识，只做一件事：把十四讲串成一条线，\n'
              '看清每一次跃迁解决了什么痛点、留下了什么新问题。\n'
              '从一行 printf，到一台谁都能往上装功能的机器。',
              16, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 主线地图
# ============================================================
def p02_map():
    s = pg('整条路线：六级台阶', '每一级都在做同一件事——把变化从代码里挪到代码外')
    y = BODY_TOP
    y = flow(s, MARGIN_L, y, INNER_W,
             ['表达式', '函数', '模块', '库', '插件', '框架'],
             colors=('blue', 'blue', 'teal', 'teal', 'purple', 'orange'),
             size=15, h=0.72) + 0.24
    y = cards_row(s, y, [
        {'title': '① 语言基础层', 'color': 'blue', 'size': 13, 'min_h': 2.05,
         'body': '第1-8讲：表达式、控制结构、函数、\n多文件、指针、数组、结构体、链表。\n'
                 '回答：怎么把逻辑写清楚、\n把数据组织好。'},
        {'title': '② 库与链接层', 'color': 'teal', 'size': 13, 'min_h': 2.05,
         'body': '第9-11讲：静态库、动态库、\n运行时加载。\n'
                 '回答：写好的代码怎么交到\n别人手上复用。'},
        {'title': '③ 架构思想层', 'color': 'purple', 'size': 13, 'min_h': 2.05,
         'body': '第12-14讲：接口抽象、\n插件框架、完整项目。\n'
                 '回答：别人写的代码怎么插进来\n而不改主程序。'},
    ]) + 0.24
    card(s, MARGIN_L, y, INNER_W, (
        '一句话主线：表达式 → 函数 → 模块 → 库 → 插件 → 框架。'
        '每上一级，改动的波及面就小一圈。'),
        title='🧭 记住这条线', color='orange', size=13.5, min_h=0.95)
    banner(s, '架构演进的全部意义：让"变化"越来越难波及别人')
    done('P2')


# ============================================================
# P3-P16：14 讲要点页（数据驱动，统一版式）
# ============================================================
LECT = [
    # (页号, 标题, 副标题, 要点卡, 代码标题, 代码行, 要点卡2, 遗留卡, banner, accent)
    ('P3', '第1讲 表达式：一行代码里的骨架', '编译四阶段 · 接口/复用/进化三颗种子',
     '一个表达式背后是五个要素：运算符、操作数、优先级、结合性、求值顺序。'
     '源文件变成能跑的程序，要过四道门：预处理、编译、汇编、链接。',
     'hello.c',
     ['#include <stdio.h>',
      'int main(void) {',
      '    printf("Hello, ATM!");',
      '    return 0;',
      '}'],
     ('核心要点', '五个要素决定表达式怎么求值；\n四阶段把源码变成可执行文件。', 'blue'),
     ('埋下的种子', '接口、复用、进化——\n后面十四讲全是它们长出来的。', 'purple'),
     '最小的一行代码里，藏着整门语言的骨架', 'blue'),

    ('P4', '第2讲 控制结构：程序活了', '顺序 / 分支 / 循环 —— 第一个痛点也来了',
     'switch 负责选功能，while 让菜单一直转，余额这个变量保存着程序的状态。'
     '痛点也随之出现：所有逻辑堆在一个循环里，代码一长就成了没人敢碰的屎山。',
     'atm_menu.c',
     ['while (1) {',
      '    show_menu();',
      '    scanf("%d", &choice);',
      '    switch (choice) {',
      '      case 1: deposit(); break;',
      '      case 0: return 0;',
      '    }',
      '}'],
     ('三种结构', '顺序：一步一步往下走\n分支：if-else / switch 做选择\n循环：while / for 做重复', 'blue'),
     ('新痛点', '所有逻辑挤在一个循环里，\n加一个功能要改一大片代码。', 'red'),
     '程序活起来了，但代码开始失控', 'blue'),

    ('P5', '第3讲 函数封装：给逻辑起名字', '命名 · 复用 · 边界 —— 第一次分而治之',
     '把存款、取款、查询各自抽成函数，main 里只剩调度。'
     '参数和返回值就是契约，外面的代码不能随便碰函数里的变量。',
     'atm_func.c',
     ['int deposit(Account *a, double amt) {',
      '    if (amt <= 0) return -1;',
      '    a->balance += amt;',
      '    return 0;',
      '}'],
     ('三个收益', '命名：函数名说明意图\n复用：校验逻辑只写一遍\n边界：参数就是契约', 'teal'),
     ('遗留问题', '函数都在同一个文件里，\n文件越来越长，找东西越来越难。', 'red'),
     '分而治之的第一步：让每段逻辑有名字、有边界', 'teal'),

    ('P6', '第4讲 多文件模块：按职责分家', '头文件声明契约 · 实现文件各管一摊',
     '账务、界面、工具各归各的文件，每块配一个头文件对外声明。'
     '头文件保护防止重复包含，编译隔离让改动只重编一个文件。',
     'account.h',
     ['#ifndef ACCOUNT_H',
      '#define ACCOUNT_H',
      '',
      'double get_balance(int id);',
      'int    deposit(int id, double amt);',
      '',
      '#endif'],
     ('核心收益', '编译隔离：改一个 .c 只重编它自己\n接口与实现彻底分离', 'teal'),
     ('遗留问题', '想复用这些代码，\n还得把源文件拷到别人的工程里。', 'red'),
     '接口和实现第一次分离——插件思想的雏形', 'teal'),

    ('P7', '第5讲 指针：全系列的分水岭', '类型决定步长 · 地址传参 · 函数指针',
     '指针就是地址。int 星号 加一走四个字节，char 星号 加一走一个字节。'
     '想让函数改掉外面的变量，就必须传地址；函数指针则让函数变成可以传递的数据。',
     '指针的两张脸',
     ['void swap(int *a, int *b) {',
      '    int t = *a; *a = *b; *b = t;',
      '}',
      'int (*op)(int, int) = &add;   // 函数指针',
      'int r = op(3, 5);'],
     ('为什么必须传地址', 'C 的函数参数是值传递，\n形参改了，实参纹丝不动。', 'blue'),
     ('为什么要有函数指针', '把函数当数据传来传去，\n它是接口抽象和插件注册的技术底座。', 'purple'),
     '指针是后面所有关卡的钥匙', 'blue'),

    ('P8', '第6讲 数组：一段连续内存', '随机访问是强项 · 长度固定是弱项',
     '数组名在大多数场合会退化成首元素指针，所以下标访问等价于指针加偏移再解引用。'
     '强项是算一下标就能到位，弱项是长度编译时就定死了。',
     'array_atm.c',
     ['int arr[5] = {1, 2, 3, 4, 5};',
      '',
      '// arr[i] 等价于 *(arr + i)',
      'for (int i = 0; i < 5; i++)',
      '    sum += arr[i];'],
     ('强项', '连续内存 + 随机访问，\n下标一算就到位。', 'green'),
     ('弱项', '长度固定，想动态增长\n只能重新分配一块更大的内存。', 'red'),
     '连续与下标，换来速度也换来束缚', 'green'),

    ('P9', '第7讲 结构体：把数据打包', '从平行数组到数据建模',
     '账号、户名、余额原来是三个平行数组，改一个账户要同步改三处。'
     '打包成一个结构体之后，一个账户就是一个整体，传参只传一个指针。',
     'struct_atm.c',
     ['typedef struct {',
      '    int    id;',
      '    char   name[32];',
      '    double balance;',
      '} Account;',
      'acc.id = 1001;        // 变量用点',
      'p->balance += 100;    // 指针用箭头'],
     ('解决了什么', '相关数据不再散落，\n改一个账户只需改一处。', 'green'),
     ('遗留问题', '账户数量还是固定的，\n想随时增删，得换数据结构。', 'red'),
     '打包，是数据建模的开始', 'green'),

    ('P10', '第8讲 链表：随时能长的数据结构', '插入删除只改指针 · 申请与释放必须配对',
     '每个节点带一个 next 指针把自己串起来。插入删除只改指针，不用搬动整块内存，'
     '长度还能随时长。代价是不能随机访问，查找只能逐个走。',
     'linked_atm.c',
     ['typedef struct Node {',
      '    Account      data;',
      '    struct Node *next;',
      '} Node;',
      'n->next = head->next;   // 插入只改指针',
      'head->next = n;'],
     ('相比数组', '长度随时可变，插入删除是常数级，\n代价是查找要逐个走。', 'green'),
     ('必须记住', '每一块申请来的内存\n都要有人还回去，否则泄漏。', 'red'),
     '指针串起来的，不只是节点，还有灵活性', 'green'),

    ('P11', '第9讲 静态库：复用做到了', '归档打包 · 链接期代码复制',
     '把目标文件用归档工具打包成库文件，别人链接时，链接器把用到的代码直接复制进可执行文件。'
     '好处是发布简单，代价是十份拷贝、升级要重编。',
     '构建命令',
     ['$ ar rcs libaccount.a \\',
      '      account.o transaction.o',
      '$ gcc main.o -o atm.exe \\',
      '      -L. -laccount',
      '# 用到的代码被复制进 atm.exe'],
     ('好处', '一个可执行文件走天下，\n不怕缺文件、启动快。', 'green'),
     ('代价', '代码被复制多份，\n库一升级所有程序都要重新链接。', 'red'),
     '复用做到了，共享还没有', 'yellow'),

    ('P12', '第10讲 动态库：共享做到了', '加载时链接 · 换库不用重编主程序',
     '编译成动态库后，程序启动时由加载器把它映射进进程，磁盘上只有一份代码。'
     '升级只要替换库文件，代价是部署必须带着它、版本要对得上。',
     '构建与运行',
     ['__declspec(dllexport)',
      'double get_balance(int id);',
      '$ gcc -shared -o account.dll account.c',
      '$ gcc main.c -o atm.exe -L. -laccount',
      '# 启动时由加载器映射进进程'],
     ('好处', '磁盘内存都共享，\n换库不用重编主程序。', 'green'),
     ('代价', '部署要带 dll，\n版本对不上就打不开。', 'red'),
     '代码终于能被别人复用，但用谁仍写死在编译期', 'yellow'),

    ('P13', '第11讲 运行时加载：不链接也能调用', '装进来 · 取地址 · 调用 —— 插件雏形',
     '用 LoadLibrary 在运行期把库装进来，按名字取出函数地址，转成函数指针就能调用。'
     '主程序编译时根本不需要知道这个库存在，用完还能卸载。',
     'host.c',
     ['HANDLE h = LoadLibrary(',
      '        "deposit_plugin.dll");',
      'create_fn f = (create_fn)',
      '    GetProcAddress(h, "create_plugin");',
      'Plugin *p = f();     // 运行期装进来',
      '// ... 用完 FreeLibrary(h)'],
     ('关键突破', '依赖从编译期推迟到运行期，\n主程序不必知道插件存在。', 'purple'),
     ('遗留问题', '大家各自取地址、各自约定函数名，\n没有统一的契约，很容易对不上。', 'red'),
     '扫一个目录，见到一个装一个', 'purple'),

    ('P14', '第12讲 接口抽象：定一份契约', '结构体 + 函数指针表 —— C 语言的多态',
     '既然插件是别人写的，宿主怎么知道该调它什么？约定一个结构体，里面放一组函数指针。'
     '插件导出创建函数返回这个结构体，宿主只认结构体、不认实现。',
     'plugin_api.h',
     ['typedef struct {',
      '    const char *name;',
      '    const char *version;',
      '    int  (*init)(void);',
      '    int  (*execute)(void *ctx);',
      '    void (*cleanup)(void);',
      '} Plugin;'],
     ('这就是多态', '同一行宿主代码，\n因为拿到不同插件，行为就不一样。', 'purple'),
     ('遗留问题', '加载、卸载、出错处理仍散落在各处，\n谁都可以随便来一发。', 'red'),
     '只认契约，不认实现', 'purple'),

    ('P15', '第13讲 插件框架：控制反转', '生命周期 + 状态机 + 管理器',
     '插件有了完整生命周期：加载、初始化、启动、执行、停止、清理，状态机管着能不能迁移。'
     '框架负责扫目录、注册、分发、卸载，插件只管自己的业务。',
     'framework.c',
     ['UNLOADED -> LOADED -> INITIALIZED',
      '        -> STARTED',
      '        -> STOPPED -> CLEANED',
      '',
      '// 框架：扫目录 / 注册 / 分发 / 卸载',
      '// 插件：只实现自己的业务'],
     ('开闭原则落地', '加功能就加插件，\n主程序一行不改。', 'orange'),
     ('控制反转', '以前你调用库，\n现在框架调用你——别打电话给我们。', 'orange'),
     '框架定骨架，插件填血肉', 'orange'),

    ('P16', '第14讲 完整项目：零件装成机器', '核心稳定 · 插件可插 · 主程序只调度',
     '账务核心是一个动态库，四个插件各管一个业务，主程序扫目录加载插件、按配置生成菜单，'
     '插件缺失还能优雅降级。一行 printf 长成了一台能跑的机器。',
     '运行输出',
     ['$ ./atm_framework.exe',
      '=== 初始化账务核心 ===',
      '=== 扫描插件目录: plugins ===',
      '  [发现] deposit_plugin.dll',
      '  [注册] 存款  v1.0  菜单项 1',
      '  [注册] 取款  v1.0  菜单项 2'],
     ('分层清晰', '核心层稳定，插件层可插，\n主程序只做调度。', 'orange'),
     ('优雅降级', '插件文件删掉，程序照常跑，\n只是菜单少了那一项。', 'green'),
     '十四讲走完：一行 printf 长成一台机器', 'orange'),
]


def lecture_page(tag, title, subtitle, top_body, code_title, code_lines,
                 right1, right2, banner_msg, accent):
    s = pg(title, subtitle)
    y = BODY_TOP
    b, _ = card(s, MARGIN_L, y, INNER_W, top_body,
                title='📌 本讲要点', color=accent, size=13.5, min_h=1.05)
    y = b + 0.22
    cw = 6.05
    code(s, MARGIN_L, y, cw, code_lines, title=code_title, size=13)
    rx = MARGIN_L + cw + 0.30
    rw = INNER_W - cw - 0.30
    cards_col(s, rx, y, rw, [
        {'title': right1[0], 'body': right1[1], 'color': right1[2], 'size': 13.5,
         'min_h': 1.25},
        {'title': right2[0], 'body': right2[1], 'color': right2[2], 'size': 13.5,
         'min_h': 1.25},
    ], gap=0.20)
    banner(s, banner_msg, fill=accent)
    done(tag)


# ============================================================
# P17 六次跃迁对比表
# ============================================================
def p17_ladder():
    s = pg('六次跃迁：变化被挪到了哪里', '每一级，改动的波及面都在变小')
    y = BODY_TOP
    rows = [
        ('表达式 → 函数', '变化从 main 里挪进函数，改动只影响一个函数体'),
        ('函数 → 模块', '变化从函数挪进文件，改动只影响一个编译单元'),
        ('模块 → 库', '变化从源码挪进库，复用者只需要在链接期接上它'),
        ('库 → 运行时加载', '依赖从编译期推迟到运行期，主程序不必知道插件存在'),
        ('加载 → 接口抽象', '用函数指针表定契约，宿主与实现彻底解耦'),
        ('抽象 → 框架', '连调用顺序都交给框架，加功能不改主程序'),
    ]
    b, _ = kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.28, 0.72), size=14,
                   header=('跃迁', '变化被挪到了哪里'), tag='ladder')
    y = b + 0.22
    card(s, MARGIN_L, y, INNER_W, (
        '规律：每一次跃迁，都把"会变的东西"关进更小的笼子。'
        '架构不是设计出来的，是一次次把变化往外挪的结果。'),
        title='📝 一句话规律', color='orange', size=13.5, min_h=0.95)
    banner(s, '波及面越来越小，就是架构越来越好的标志')
    done('P17')


# ============================================================
# P18 同一功能的四种写法
# ============================================================
def p18_evolution():
    s = pg('同一件事的四种写法', '存款功能在四个阶段的样子 —— 功能一样，代价不同')
    y = BODY_TOP
    blocks = [
        ('① 表达式阶段', [
            '// main 里的一段代码',
            'balance = balance + amt;',
            'printf("%.2f", balance);',
            '',
            '改它：动 main，全部重编']),
        ('② 函数阶段', [
            'int deposit(Account *a,',
            '           double amt) {',
            '    a->balance += amt;',
            '    return 0;',
            '}',
            '改它：动一个函数']),
        ('③ 库阶段', [
            '// account.c -> libaccount.a',
            '__declspec(dllexport)',
            'int deposit(int id,',
            '            double amt);',
            '',
            '改它：重编库，再重链主程序']),
        ('④ 插件阶段', [
            '// deposit_plugin.dll',
            'static int execute(void *ctx) {',
            '    return deposit(ctx);',
            '}',
            '',
            '改它：只换一个 dll，不动主程序']),
    ]
    cw = (INNER_W - 0.26) / 2
    ch = 0.40 + 0.36 + 12.5 * 1.42 / 72.0 * 6
    for i, (tt, lines) in enumerate(blocks):
        cx = MARGIN_L + (i % 2) * (cw + 0.26)
        cy = y + (i // 2) * (ch + 0.16)
        code(s, cx, cy, cw, lines, title=tt, size=12.5)
    banner(s, '功能没变，变的是"改一次要付出多大代价"')
    done('P18')


# ============================================================
# P19 三条设计原则
# ============================================================
def p19_principles():
    s = pg('十四讲沉淀的三条原则', '解耦 · 契约先行 · 开闭原则')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '回头看，十四讲其实只教了三件事。它们不是背诵用的口号，'
        '而是每一次跃迁背后真正起作用的东西。'),
        title='📌 为什么是这三条', color='orange', size=14, min_h=0.95)
    y = y2 + 0.24
    y = cards_row(s, y, [
        {'title': '① 解耦', 'color': 'blue', 'size': 13.5, 'min_h': 2.25,
         'body': '依赖接口，不依赖实现。\n'
                 '头文件让调用方看不见实现，\n函数指针表让宿主看不见插件。\n'
                 '好处：换实现，调用方无感。'},
        {'title': '② 契约先行', 'color': 'teal', 'size': 13.5, 'min_h': 2.25,
         'body': '先定好怎么说话，再写实现。\n'
                 '头文件是模块间的契约，\n插件接口是宿主与插件的契约。\n'
                 '好处：双方可以并行开发。'},
        {'title': '③ 开闭原则', 'color': 'purple', 'size': 13.5, 'min_h': 2.25,
         'body': '对扩展开放，对修改关闭。\n'
                 '加功能就加插件，\n主程序一行不改。\n'
                 '好处：老代码越用越稳。'},
    ])
    banner(s, '三条原则一句话：把变化关进笼子里')
    done('P19')


# ============================================================
# P20 运行演示
# ============================================================
def p20_demo():
    s = pg('运行演示：机器真的转起来了', '扫目录加载插件 → 配置化菜单 → 优雅降级')
    y = BODY_TOP
    demo_frame(s, MARGIN_L, y, 8.10, 4.55, title='atm_framework.exe', lines=[
        '$ ./atm_framework.exe',
        '=== 初始化账务核心 ===',
        '  [开户] ID:1001  户名:张三  余额:10000.00',
        '=== 扫描插件目录: plugins ===',
        '  [发现] plugins/deposit_plugin.dll',
        '  [注册] 存款     v1.0   菜单项 1',
        '  [发现] plugins/withdraw_plugin.dll',
        '  [注册] 取款     v1.0   菜单项 2',
        '  [发现] plugins/query_plugin.dll',
        '  [注册] 查询     v1.0   菜单项 3',
        '  [发现] plugins/transfer_plugin.dll',
        '  [注册] 转账     v1.0   菜单项 4',
        '请选择操作: 1',
        '请输入金额: 500',
        '  [成功] 存款 500.00，余额 10500.00',
        '请选择操作: 0',
        '=== 清理插件并退出 ===',
    ])
    rx = MARGIN_L + 8.10 + 0.26
    rw = INNER_W - 8.10 - 0.26
    cards_col(s, rx, y, rw, [
        {'title': '看什么', 'color': 'green', 'size': 13, 'min_h': 1.25,
         'body': '插件是扫目录发现的，\n菜单是注册时生成的。'},
        {'title': '关键在哪', 'color': 'orange', 'size': 13, 'min_h': 1.25,
         'body': '没有一行代码写死\n有哪些功能。'},
        {'title': '再试一次', 'color': 'purple', 'size': 13, 'min_h': 1.25,
         'body': '删掉一个插件 dll 再启动，\n程序照常跑，只是少一项。'},
    ], gap=0.20)
    banner(s, '优雅降级：缺哪个插件，就少哪一项功能，但绝不崩溃')
    done('P20')


# ============================================================
# P21-P24 思考题与解答
# ============================================================
def qa_page(tag, title, subtitle, specs, banner_msg, accent='primary'):
    s = pg(title, subtitle)
    y = BODY_TOP
    y = cards_col(s, MARGIN_L, y, INNER_W, specs, gap=0.24, size=14)
    banner(s, banner_msg, fill=accent)
    done(tag)


def p21_q12():
    qa_page('P21', '思考题 ①②', '先自己想一想，再往下翻', [
        {'title': '① 既然动态库能共享代码，为什么嵌入式和独立小工具还在用静态库？',
         'color': 'blue', 'size': 14, 'min_h': 1.35,
         'body': '提示：想想部署环境你能不能控制，以及"缺一个文件"的代价有多大。'},
        {'title': '② 函数指针表已经能实现多态了，为什么还要设计完整的生命周期和状态机？',
         'color': 'purple', 'size': 14, 'min_h': 1.35,
         'body': '提示：想想插件会失败、会被卸载、会被重复加载的场合。'},
    ], '想清楚这两题，你就懂了库和框架各自的取舍', 'blue')


def p22_a12():
    qa_page('P22', '解答 ①②', '答案不是唯一的，关键是取舍的理由', [
        {'title': '① 静态库 vs 动态库', 'color': 'green', 'size': 13.5, 'min_h': 1.55,
         'body': '静态库换来确定性：没有外部依赖、不会缺文件、启动更快，'
                 '代价是体积大、升级要重编。动态库换来共享和热升级，'
                 '代价是部署复杂、版本要对齐。选哪个，取决于你能不能控制运行环境。'},
        {'title': '② 为什么要有状态机', 'color': 'orange', 'size': 13.5, 'min_h': 1.55,
         'body': '真实系统里插件会加载失败、会被卸载、会被重复加载。'
                 '没有状态机，就会出现"还没初始化就执行"或者"已经卸载还在调用"的崩溃。'
                 '多态解决的是怎么调，状态机解决的是什么时候能调。'},
    ], '能说出取舍的理由，比记住结论更重要', 'green')


def p23_q34():
    qa_page('P23', '思考题 ③④', '最后两道，关于边界与分层', [
        {'title': '③ 框架和库的分界到底在哪里？',
         'color': 'purple', 'size': 14, 'min_h': 1.35,
         'body': '提示：不要看代码长什么样，看谁掌握调用权。'},
        {'title': '④ 要给这台 ATM 加"转账限额"，你改哪一层？',
         'color': 'orange', 'size': 14, 'min_h': 1.35,
         'body': '提示：核心层、插件层、配置层，三选一，说说理由。'},
    ], '这两题测的是你对分层和控制权的直觉', 'purple')


def p24_a34():
    s = pg('解答 ③④ 与全系列总结', '十四讲走完，愿你心里有这条线')
    y = BODY_TOP
    y = cards_col(s, MARGIN_L, y, INNER_W, [
        {'title': '③ 分界在控制权', 'color': 'blue', 'size': 13.5, 'min_h': 1.25,
         'body': '库是你调用它，框架是它调用你。控制权在谁手上，就是分界线。'},
        {'title': '④ 限额属于业务策略', 'color': 'teal', 'size': 13.5, 'min_h': 1.25,
         'body': '应做成配置或独立插件，核心层只提供查询能力，'
                 '不该写死任何业务规则——否则每改一次规则就要动核心。'},
    ], gap=0.22, size=13.5)
    y += 0.10
    card(s, MARGIN_L, y, INNER_W, (
        '十四讲从一个 printf 走到一个可插拔的框架，路只有一条：不断把变化往外挪。'
        '愿你以后写代码时，心里始终有这条线。'),
        title='🎉 全系列一句话', color='orange', size=13.5, min_h=0.95)
    banner(s, '课程结束了，你的架构之路才刚开始')
    done('P24')


# 生成顺序 = 讲解顺序（P1 → P24），与 讲解脚本.json 的 24 段一一对应
p01_cover()
p02_map()
for item in LECT:                      # P3 ~ P16：14 讲要点
    lecture_page(*item)
p17_ladder()
p18_evolution()
p19_principles()
p20_demo()
p21_q12()
p22_a12()
p23_q34()
p24_a34()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页，全部通过质检' % len(prs.slides._sldIdLst))
