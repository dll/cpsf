# -*- coding: utf-8 -*-
"""
第12讲：接口抽象与插件发现 —— 给所有插件装一个统一的插头
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

LECTURE = '第12讲 接口抽象'
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


def cards_col(s, x, y, w, specs, gap=0.22, size=15):
    for sp in specs:
        b, _ = card(s, x, y, w, sp['body'], title=sp.get('title'),
                    color=sp.get('color', 'orange'), size=sp.get('size', size),
                    title_size=sp.get('title_size', 18),
                    min_h=sp.get('min_h', 0.0))
        y = b + gap
    return y - gap


def code_h(n_lines, size, title=None):
    head = 0.40 if title else 0.0
    return head + 0.36 + size * 1.42 / 72.0 * n_lines


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

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第12讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.55, 3.4, 1.0,
              '从一行 printf\n到软件体系的插件框架', 15, C['purple_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '接口抽象', 62, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.18, 7.4, 0.6, '给所有插件装一个统一插头', 25, C['purple_dark'])
    rect(slide, 5.35, 3.93, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.18, 7.2, 1.6,
              '第11讲学会了 dlopen / dlsym，能加载动态库了，\n'
              '可每个插件的函数名、参数都不一样，调用方要记一堆细节。\n'
              '本讲借 USB 接口的启示，用"结构体 + 函数指针"造一个插座：\n'
              '所有插件都插同一个口，调用方只认接口，不认插件。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '六级台阶的第五级 —— 插件，从"能加载"走到"能统一调用"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '第11讲把动态库在运行时加载了起来，插件有了雏形；但每个插件的函数名和参数都不同，'
        '调用方得一个个记住，耦合度极高。\n'
        '本讲站上第五级——插件，用统一的 Plugin 接口把它们收编：'
        '不管你是什么插件，只要实现同一套方法，就能被一样地调用。'),
        title='🎯 本讲定位', color='purple', size=15.5, min_h=1.15)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '第3讲 ✅'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '第9-10讲 ✅'), ('⑤ 插件', '← 你在这里'), ('⑥ 框架', '第13讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('gray', 'gray', 'gray', 'gray', 'purple', 'gray'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第5讲：函数指针（本讲的零件）\n'
        '第7讲结构体、第8讲链表、第11讲运行时加载'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第13讲：生命周期、插件管理器、配置化菜单\n'
        '在统一接口之上，长出完整的插件框架'),
        title='➡ 后续', color='teal', size=14.5, min_h=1.00)
    banner(s, '本讲把"一根线一根线接"变成"插同一个插座"：接口统一，调用统一')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '第11讲能加载了，但"调用方式不统一"这件事还没解决')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第11讲：已经做到的', [
                    'dlopen 在运行时打开动态库',
                    'dlsym 按名字取到函数地址',
                    '插件第一次"从文件里来"'],
                '第12讲：要补上的', [
                    '定义统一的 Plugin 接口契约',
                    '用结构体 + 函数指针打包行为',
                    '调用方只认接口，不认插件'],
                left_color='blue', right_color='purple', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '痛一：函数名不同', 'body': '存款叫 do_deposit\n查询叫 get_balance',
         'color': 'red', 'size': 13, 'title_size': 15},
        {'title': '痛二：参数不同', 'body': '有的收金额\n有的一个参数都不收',
         'color': 'yellow', 'size': 13, 'title_size': 15},
        {'title': '痛三：返回值不同', 'body': '有的返回 int\n有的返回 double',
         'color': 'orange', 'size': 13, 'title_size': 15},
        {'title': '痛四：要改调用方', 'body': '每来一个新插件\n就得学它的新"插头"',
         'color': 'purple', 'size': 13, 'title_size': 15},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：能加载不等于能复用 —— 插头标准不统一，插上去也没法用',
    ], size=15)
    banner(s, '本讲造一个"USB 接口"：所有插件都实现同一套方法')
    done('P3')


# ============================================================
# P4 核心内容一：函数指针回顾
# ============================================================
def p04_fnptr():
    s = pg('零件回顾：函数指针（第5讲）', '函数在内存里有地址，函数指针存的就是这个地址')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        'int a = 10;',
        'int* p = &a;              /* 普通指针：指向数据 */',
        '',
        'int add(int a, int b) { return a + b; }',
        'int (*fp)(int, int) = add; /* 函数指针：指向函数 */',
        'int r = fp(3, 5);          /* 等价于 add(3,5)，结果 8 */',
    ], title='指针 vs 函数指针', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    y2 = y + code_h(6, 11.5, 'x') + 0.24
    rows = [('回调函数', '把函数当参数传给别人（qsort）'),
            ('多态', '同一接口，不同行为 ← 本讲重点'),
            ('事件处理', '注册回调，事件来了再调'),
            ('策略模式', '运行时切换算法')]
    kv_rows(s, MARGIN_L, y2, INNER_W, rows, widths=(0.18, 0.82), size=12.5,
            header=('用途', '说明'))
    card(s, xr, y, wr, (
        '括号不能少：int (*fp)(int) 是指向函数的指针；'
        'int *fp(int) 是"返回 int 指针的函数"，差一个括号，含义全变。'),
        title='⚠️ 别写错括号', color='red', size=12.5, title_size=14, min_h=1.60)
    banner(s, '一个函数指针能指向一个函数；把一组函数指针装进结构体，就是接口')
    done('P4')


# ============================================================
# P5 核心内容二：结构体 + 函数指针 = 接口
# ============================================================
def p05_iface():
    s = pg('结构体 + 函数指针 = C 语言的接口', '第7讲的结构体打包数据；本讲的结构体打包"行为"')
    y = BODY_TOP
    cw = INNER_W * 0.58
    code(s, MARGIN_L, y, cw, [
        'typedef struct Plugin {',
        '    char name[32];      /* 元数据：插件叫什么 */',
        '    char version[16];',
        '    char description[64];',
        '',
        '    /* 行为：三个函数指针 = 三个接口方法 */',
        '    int  (*init)(struct Plugin* self);',
        '    int  (*execute)(struct Plugin* self, double amount);',
        '    void (*cleanup)(struct Plugin* self);',
        '} Plugin;',
    ], title='plugin.h：统一契约', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '① 从数据封装到行为封装', 'body': '第7讲装的是 id / name / balance\n本讲装的是 init / execute / cleanup',
         'color': 'blue', 'size': 12.5, 'title_size': 14},
        {'title': '② 三个方法就是生命周期', 'body': '加载 → init → execute(可多次)\n→ cleanup → 卸载',
         'color': 'teal', 'size': 12.5, 'title_size': 14},
        {'title': '③ 实现插件 = 填一张表', 'body': 'Plugin deposit = { .name="存款",\n  .execute=deposit_execute, ... };',
         'color': 'orange', 'size': 12.5, 'title_size': 14},
    ], gap=0.14)
    banner(s, '存款、取款、查询功能不同，但"长相"完全一样 —— 这就是契约的价值')
    done('P5')


# ============================================================
# P6 核心内容三：self 指针
# ============================================================
def p06_self():
    s = pg('self 指针：手动版 this', 'C 语言没有编译器帮忙传 this，那就自己传第一个参数')
    y = BODY_TOP
    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        '/* C++：编译器自动隐式传 this */',
        'class DepositPlugin : public Plugin {',
        '    int execute(double amount) {',
        '        balance += amount;   /* this->balance */',
        '    }',
        '};',
        '',
        '/* C：显式把 self 当第一个参数传进去 */',
        'int deposit_execute(Plugin* self, double amount) {',
        '    printf("[%s] 存入 %.2f\\n", self->name, amount);',
        '    return 0;',
        '}',
    ], title='同一个东西，两种写法', size=11)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '为什么要 self', 'body': '插件方法要能访问自己的数据；\nC 没有自动 this，只能手动传。',
         'color': 'purple', 'size': 12.5, 'title_size': 14},
        {'title': '调用时就长这样', 'body': 'p->execute(p, 500.0);\n把一个 p 传两遍：找函数、当参数。',
         'color': 'blue', 'size': 12.5, 'title_size': 14},
        {'title': '和 Python 一样', 'body': 'Python 的 self、C++ 的 this、\nC 的 self 参数，是同一件事。',
         'color': 'teal', 'size': 12.5, 'title_size': 14},
    ], gap=0.14)
    banner(s, 'self 就是"我是谁"：有了它，同一个 execute 才能操作各自的数据')
    done('P6')


# ============================================================
# P7 核心内容四：插件链表管理
# ============================================================
def p07_link():
    s = pg('插件链表：注册 = 头部插入', '衔接第8讲链表 —— 数据结构没变，节点里装的东西变了')
    y = BODY_TOP
    cw = INNER_W * 0.52
    rows = [('第8讲 交易链表', '数据域 amount + 指针域 next'),
            ('第12讲 插件链表', '数据域 Plugin* + 指针域 next'),
            ('注册', '头部插入，O(1)，和链表一模一样'),
            ('查找', '遍历比较 name，O(n)'),
            ('销毁', '遍历 free，逐个释放节点')]
    kv_rows(s, MARGIN_L, y, cw, rows, widths=(0.30, 0.70), size=12,
            header=('对比', '插件链表怎么管理'))

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'typedef struct PluginNode {',
        '    Plugin* plugin;            /* 指向接口 */',
        '    struct PluginNode* next;',
        '} PluginNode;',
        '',
        'int plugin_register(Plugin* p) {',
        '    if (已存在同名插件) return -2;   /* 防重复 */',
        '    PluginNode* n = malloc(sizeof(PluginNode));',
        '    n->plugin = p;',
        '    n->next = plugin_head;   /* 头部插入 O(1) */',
        '    plugin_head = n;  plugin_total++;',
        '    return 0;',
        '}',
    ], title='plugin_atm.c：节点与注册', size=11)
    banner(s, '把插件挂进链表，才有"一批插件"可管；注册与防重复，都是链表的活')
    done('P7')


# ============================================================
# P8 核心内容五：注册机制与目录扫描
# ============================================================
def p08_scan():
    s = pg('从手动注册到目录扫描自动发现', '加插件只丢一个文件，不改一行代码 —— 这就是"发现"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '手动注册的写法是 plugin_register(&deposit_plugin) 一行行写；'
        '每来一个新插件，都要回来改代码。\n'
        '自动发现把它反过来：扫描 plugins 目录，看到 .dll / .so 就加载、取接口、注册进链表。'),
        title='🔎 为什么要"发现"', color='orange', size=14.5, min_h=1.05)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 打开目录', 'opendir / FindFirst'),
        ('② 逐个读文件', '拿到文件名'),
        ('③ 查后缀', '.so / .dll'),
        ('④ 加载取接口', 'dlopen + dlsym'),
        ('⑤ 注册链表', 'plugin_register'),
    ], colors=('blue', 'teal', 'purple', 'orange', 'green'), size=13.5, h=1.00) + 0.24

    code(s, MARGIN_L, y, INNER_W, [
        '/* 约定：每个插件导出 get_plugin，作为"身份标识" —— 第11讲已学 dlopen/dlsym */',
        'if (dlsym(handle, "get_plugin") == NULL) {  /* 没有这个符号，就不是合法插件 */',
        '    printf("不是合法插件，跳过\\n");  dlclose(handle);  return NULL;  }',
    ], title='怎么判断一个文件是合法插件', size=11)
    banner(s, 'VS Code、Eclipse、Photoshop 都是这么发现插件的：扫描固定目录')
    done('P8')


# ============================================================
# P9 原理深入：多态 ⭐
# ============================================================
def p09_poly():
    s = pg('原理深入：同一句调用，为什么行为不同？ ⭐', '运行期绑定 —— 编译期不知道会调谁，运行期看链表里挂了谁')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        '/* 调用方只认接口，完全不知道是谁 */',
        'void plugin_execute_all(double amount) {',
        '    PluginNode* cur = plugin_head;',
        '    while (cur != NULL) {',
        '        cur->plugin->execute(cur->plugin, amount);',
        '        cur = cur->next;   /* 同一句调用，不同插件 */',
        '    }',
        '}',
    ], title='一句 cur->plugin->execute(...) 走天下', size=11.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '① 运行期才决定调谁', 'body': '指针里存的地址是运行期填的，\n编译期无法预先绑定。',
         'color': 'blue', 'size': 12.5, 'title_size': 14},
        {'title': '② 同一调用，不同行为', 'body': '存款 +500、取款 -500、查询只显示，\n调用方一行都没改。',
         'color': 'teal', 'size': 12.5, 'title_size': 14},
        {'title': '③ 这是开闭原则的地基', 'body': '对扩展开放、对修改关闭 ——\n第14讲的框架就长在这上面。',
         'color': 'purple', 'size': 12.5, 'title_size': 14},
    ], gap=0.14)
    banner(s, '多态 = 面向接口编程：代码只依赖"契约"，不依赖"具体是谁"')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：C 语言的接口 vs C++ / Java', 'C++ 的 vtable 本质就是"结构体 + 函数指针"的自动化版本')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                'C++ / Java', [
                    'interface Plugin 声明方法',
                    'class DepositPlugin : Plugin 实现',
                    '编译器自动生成 vtable（函数指针数组）',
                    'this 由编译器隐式传入'],
                'C 语言', [
                    'struct Plugin + 函数指针',
                    '填一张表：.execute = deposit_execute',
                    '手工填函数指针字段，就是那张表',
                    '手动把 self 作为第一个参数'],
                left_color='blue', right_color='purple', size=13.5) + 0.14

    kv_rows(s, MARGIN_L, y, INNER_W, [
        ('接口', 'interface Plugin', 'struct + 函数指针'),
        ('实现', 'class ... : Plugin', '结构体实例填函数指针'),
        ('this / self', '编译器自动传', '手动传第一个参数'),
        ('多态调用', 'plugin->execute(500)', 'plugin->execute(plugin, 500)'),
    ], widths=(0.16, 0.42, 0.42), size=12,
        header=('概念', 'C++ / Java', 'C 语言'))
    banner(s, '区别只在"谁维护那张表"：C 手动填，C++ 编译器自动生成')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/plugin.h 定义契约，src/plugin_atm.c 管理插件')
    y = BODY_TOP
    cw = INNER_W * 0.55
    code(s, MARGIN_L, y, cw, [
        '/* plugin.h —— 统一契约，所有插件都实现它 */',
        'typedef struct Plugin {',
        '    char name[32];       /* 插件名称 */',
        '    char version[16];    /* 版本号 */',
        '    int  (*init)(struct Plugin* self);',
        '    int  (*execute)(struct Plugin* self, double amount);',
        '    void (*cleanup)(struct Plugin* self);',
        '} Plugin;',
        '',
        'typedef struct PluginNode {  /* 链表节点 */',
        '    Plugin* plugin;  struct PluginNode* next;',
        '} PluginNode;',
    ], title='plugin.h：接口 + 链表节点', size=10.5)
    y2 = y + code_h(12, 10.5, 'x') + 0.22
    card(s, MARGIN_L, y2, cw, (
        '一个文件就把"插件长什么样"说清楚了：元数据三个字段，行为三个函数指针。'),
        title='📄 契约只有 8 行', color='teal', size=12.5,
        title_size=14, min_h=0.90)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '/* 三个内置插件，接口统一 */',
        'static Plugin deposit_plugin = {',
        '    .name = "存款", .version = "1.0",',
        '    .description = "向账户存入现金",',
        '    .init = deposit_init,',
        '    .execute = deposit_execute,',
        '    .cleanup = deposit_cleanup,',
        '};',
        '',
        'plugin_register(&deposit_plugin);   /* 注册进链表 */',
        'plugin_register(&withdraw_plugin);',
        'plugin_register(&query_plugin);',
    ], title='plugin_atm.c：填表 + 注册', size=10.5)
    y2 = y + code_h(12, 10.5, 'x') + 0.22
    card(s, xr, y2, wr, (
        '三个插件功能不同，填表的格式完全一样；注册之后，遍历链表就能统一调用。'),
        title='🔌 插头一样的三个插件', color='purple', size=12.5,
        title_size=14, min_h=0.90)
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '命令、注册顺序、多态调用结果，全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.62
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall -o plugin_atm.exe plugin_atm.c',
        '$ ./plugin_atm.exe',
        '=== 插件管理器已初始化 ===',
        '[注册] 插件[存款] v1.0 - 向账户存入现金',
        '[注册] 插件[取款] v1.0 - 从账户取出现金',
        '[注册] 插件[查询余额] v1.0 - 查询账户当前余额',
        '--- 已注册插件列表 (3个) ---',
        '  1. 查询余额   2. 取款   3. 存款',
        '--- 初始化所有插件 ---',
        '  [存款] 初始化完成 v1.0',
        '>>> 使用插件: 存款',
        '  [存款] 存入 500.00 元，余额: 10500.00 元',
        '>>> 使用插件: 取款',
        '  [取款] 取出 200.00 元，余额: 10300.00 元',
        '>>> 使用插件: 查询余额',
        '  [查询余额] 当前余额: 10300.00 元',
    ], title='终端实录（真实输出，节选）', size=10.5)

    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译：一个源文件 + 一个头文件，直接出 exe\n'
        '② 注册：三个插件依次挂入链表，各带名称与描述\n'
        '③ 列表：链表逆序打印，证实注册是头部插入\n'
        '④ 多态：同一句 execute，存款加钱、取款减钱\n'
        '⑤ 查询：同一个接口，行为却完全不同\n'
        '⑥ 收尾：cleanup 逐个清理 → 管理器销毁'
        ),
        title='👀 要看清楚的六个点', color='orange', size=11.5, min_h=4.20)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 plugin.h / plugin_atm.c 源码')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的第五级：插件 —— 统一接口，让插件能被一样地调用')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。'
        '第11讲解决了"插件从哪里来"，本讲解决了"插件怎么被统一调用"——'
        '这是插件台阶真正立住的一步。'),
        title='🧭 一条主线', color='purple', size=15, min_h=1.05)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '第3讲 ✅'),
        ('③ 模块', '第4讲 ✅'),
        ('④ 库', '第9-10讲 ✅'),
        ('⑤ 插件', '← 本讲 ⭐'),
        ('⑥ 框架', '第13讲'),
    ], colors=('gray', 'gray', 'gray', 'gray', 'purple', 'gray'),
        size=14, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '定义了 Plugin 统一契约（init / execute / cleanup）\n'
        '用链表管理一批插件，注册与查找成体系\n'
        '多态调用：调用方只依赖接口'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '还没有框架来管顺序、管菜单、管状态。\n'
        '下一讲把生命周期拆成五个阶段，\n'
        '用状态机与配置化菜单把秩序建立起来 ——\n'
        '统一接口，正是框架能生长的那块地基。'),
        title='下一讲接着做什么', color='blue', size=13.5, min_h=1.55)
    banner(s, '从"一根线一根线接"到"插同一个插座"，插件才算真的能被复用')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '我们是用"结构体 + 函数指针"实现多态的，C++ 用"虚函数"。'
        'C++ 的虚函数底层的虚函数表 vtable 里存的是什么？\n'
        '提示：先想一想 vtable 是不是一个"函数指针数组"；'
        '再比较一下"C 手动填函数指针"和"C++ 编译器自动生成 vtable"，是不是同一件事。'),
        title='思考题 ①：为什么能模拟多态？和 vtable 什么关系', color='orange',
        size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '我们的接口是 execute(Plugin* self, double amount)，金额直接当参数。'
        '可查询插件不需要金额，转账插件又需要目标账户，怎么统一到同一个接口？\n'
        '提示：能不能用 void* 传递通用参数，把各种参数打包成结构体传进来？'
        '这样做接口统一了，代价又是什么？'),
        title='思考题 ②：参数不一样，怎么塞进同一个接口', color='purple',
        size=14.5, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：本质就是同一张表',
         'body': 'vtable 就是一张函数指针数组，\n'
                 '存在对象的内存布局里\n'
                 'C++：编译器自动生成并维护这张表，\n'
                 '程序员只写一个 virtual 关键字\n'
                 'C：程序员手动填函数指针字段\n'
                 '调用时：对象 → 取地址 → 查表 → 调用\n'
                 '两者机制相同，差别只在"谁维护"\n'
                 '所以 C 语言能做面向对象设计',
         'color': 'orange', 'size': 12.5},
        {'title': '解答 ②：用 void* 换统一',
         'body': '方案一：接口改成 execute(self, void* arg)，\n'
                 '存款把 double 装箱传入、查询显式忽略，\n'
                 '转账用结构体一次传多个参数\n'
                 '优点：一个接口适配所有插件\n'
                 '缺点：失去类型安全，转换易出错，\n'
                 '要自己管理参数的生命周期\n'
                 '方案二：参数存进 Plugin 的 user_data，\n'
                 'execute(self) 自己取\n'
                 'Linux 内核与 GStreamer 都这么干',
         'color': 'purple', 'size': 12.5},
    ], gap=0.26)
    banner(s, '接口要统一，参数就得让位给 void* —— 这是灵活性与类型安全之间的取舍')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：插件身份验证，与注册防重复')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '目录扫描时，如果只看后缀 .dll / .so 就当成插件，'
        '用户随手放一个同后缀的文件进来，加载就会出问题。怎么判断一个文件是合法插件？\n'
        '提示：可以让每个插件约定导出一个特殊符号当"身份标识"，'
        '再用 dlsym 去取它；取不到就说明不是插件。'),
        title='思考题 ③：怎么判断一个文件是合法插件', color='teal',
        size=14.5, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        'plugin_register 会先遍历链表，检查插件名是不是已经存在，然后再插入。'
        '为什么非要多做这一步？如果不检查会怎样？\n'
        '提示：同一个插件注册两次，遍历执行 execute 时会发生什么？'
        '目录扫描时同一个文件又会不会被扫到两次？'),
        title='思考题 ④：注册时为什么要检查重复', color='green',
        size=14.5, min_h=1.55)
    banner(s, '这两题想通了，第14讲的框架注册与生命周期就提前入门了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '把"接口"接到下一讲的"框架"')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：约定一个导出符号',
         'body': '每个插件都导出 get_plugin() 作为身份：\n'
                 'Plugin* get_plugin(void) { return &xxx; }\n'
                 '扫描时用 dlsym(handle, "get_plugin") 去取，\n'
                 '返回 NULL 就说明这不是插件，dlclose 跳过\n'
                 '取到之后再校验 init / execute / cleanup\n'
                 '是否为空，接口不完整也不收\n'
                 '这种"约定符号"是插件系统的标准做法，\n'
                 '既挡住了垃圾文件，也挡住了半成品插件',
         'color': 'teal', 'size': 12.5},
        {'title': '解答 ④：防止重复执行与统计错误',
         'body': '不检查重复，同一个插件会有两个节点：\n'
                 '遍历执行时它的 execute 被调用两次，\n'
                 '存款 +500 执行两遍，结果就错了\n'
                 'plugin_total 也会统计偏大，\n'
                 '插件列表里出现重复项，管理混乱\n'
                 '目录扫描更容易重复：软链接、\n'
                 '重扫、多线程并发都会命中同一个文件\n'
                 '所以检查重复是一种防御性编程，\n'
                 '代价是一次 O(n) 遍历，换来系统正确',
         'color': 'green', 'size': 12.5},
    ], gap=0.26)
    banner(s, '接口统一让插件能被批量调用，防御性检查让批量调用不出错')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第12讲 接口抽象与插件发现')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '结构体 + 函数指针 = C 语言的接口；所有插件实现同一契约，用链表统一管理。\n'
        '调用方只认接口、不认实现，同一句 execute 走出不同行为 —— 这就是多态。'),
        title='📝 一句话总结', color='purple', size=14.5, min_h=0.98)
    y = y2 + 0.24

    rows = [('1', '函数指针', '指向函数入口地址的指针，第5讲的零件，本讲用来当接口方法'),
            ('2', '结构体接口', '把多个函数指针打包成 struct Plugin，从数据封装升级为行为封装'),
            ('3', 'self 指针', '手动传的 this；调用写成 p->execute(p, 500.0)'),
            ('4', '插件链表', '注册 = 头部插入 O(1)，查找 = 遍历 O(n)，衔接第8讲链表'),
            ('5', '目录扫描', '扫描 .dll / .so，靠约定导出符号 get_plugin 验证身份'),
            ('6', '多态', '同一句 execute，运行期决定调谁 —— 面向接口编程')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：插件框架架构 —— 生命周期、状态机、配置化菜单（第13讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_fnptr, p05_iface, p06_self, p07_link,
           p08_scan, p09_poly, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
