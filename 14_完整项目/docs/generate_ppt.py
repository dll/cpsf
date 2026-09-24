# -*- coding: utf-8 -*-
"""
第14讲：完整项目与全系列总结 —— 收官之讲
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

LECTURE = '第14讲 完整项目与全系列总结'
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

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第14讲 / 共 14 讲 · 收官', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.40, 3.5, 1.2,
              '把 14讲的零件\n装成一台能跑的机器', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '完整项目与全系列总结', 46, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.05, 7.4, 0.6, '把一行 printf 变成一台可插拔的 ATM', 24, C['primary_dark'])
    rect(slide, 5.35, 3.80, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.05, 7.2, 1.8,
              '前十三讲，我们把零件一件件造齐：表达式、函数、模块、库、插件。\n'
              '这一讲做两件事——先把零件装成一台真正能编译、能运行的机器，\n'
              '再把整条演进路线收回到一张图里：六级台阶、控制反转、设计模式。\n'
              '十四讲走完，你会看清：架构不是写出来的，是一级一级长出来的。',
              16, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 全系列14讲知识地图
# ============================================================
def p02_map():
    s = pg('全系列14讲知识地图', '三层技术线 · 一条复用主线 —— 你在最后一格')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '语言基础层（第1-8讲）造零件 → 库与链接层（第9-11讲）让代码被别人复用 → '
        '架构思想层（第12-14讲）让代码被"别人写的代码"扩展。\n'
        '横着看是三条独立的技术线，竖着看是层层供料，最后一讲把它们焊成一台机器。'),
        title='🧭 一张图看完全系列', color='orange', size=14.5, min_h=1.02)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲'), ('② 控制结构', '第2讲'), ('③ 函数封装', '第3讲'), ('④ 多文件', '第4讲'),
        ('⑤ 指针', '第5讲'), ('⑥ 数组', '第6讲'), ('⑦ 结构体', '第7讲'), ('⑧ 链表', '第8讲'),
    ], colors=('teal',) * 8, size=12.5, h=0.78) + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('⑨ 静态库', '第9讲  代码复制一份'),
        ('⑩ 动态库', '第10讲  共享同一份'),
        ('⑪ 运行时加载', '第11讲  dlopen 按需装载'),
    ], colors=('blue', 'blue', 'blue'), size=13.5, h=0.78) + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('⑫ 接口抽象', '第12讲  结构体 + 函数指针'),
        ('⑬ 插件框架', '第13讲  生命周期 + 管理器'),
        ('⑭ 完整项目 ★', '第14讲  装成一台机器 ← 你在这里'),
    ], colors=('purple', 'purple', 'primary'), size=13.5, h=0.78)
    banner(s, '14 讲不是 14 个孤立知识点，是一条"复用范围不断扩大"的演进线')
    done('P2')


# ============================================================
# P3 目标：一个可插拔的 ATM 系统
# ============================================================
def p03_goal():
    s = pg('本讲目标：一个可插拔的 ATM 系统', '需求只有两句话，第二句才是真正的门槛')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '第一句：做一个 ATM，有存款 / 取款 / 查询余额 / 转账四项功能。\n'
        '第二句：增加第五项功能时，不改主程序一行代码——不用 include、不用 switch、不问有几个功能。'),
        title='📌 两句话需求', color='orange', size=13.5, title_size=15)
    y = y2 + 0.22

    rows = [('统一接口', '第12讲', '所有插件长得一样，框架用同一行代码调用它们'),
            ('五阶段生命周期', '第13讲', 'init→start→execute→stop→cleanup，顺序由框架管'),
            ('运行时加载', '第11讲', '插件是一个个 .dll 文件，扫目录后按需装载'),
            ('数据共享', '第10讲', '主程序和所有插件看到同一份账户数据'),
            ('配置化菜单', '第8讲', '菜单项由插件自己声明，主程序零硬编码'),
            ('优雅降级', '本讲新增', '某个插件加载失败，框架照常启动，只少一项功能')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.19, 0.13, 0.68), size=11.5,
            header=('约束', '来自', '这一条在说什么'))
    banner(s, '要满足第二句话，功能只能以"插件"的形态，在运行时从外部装进来')
    done('P3')


# ============================================================
# P4 完整项目：四层架构
# ============================================================
def p04_arch():
    s = pg('完整项目：四层架构，依赖单向向下', '每一层只认下一层的接口，不认识下一层的实现')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '主程序 → 框架 → 插件 → 账务核心，四层单向依赖。'
        '主程序只认识 framework.h；框架只认识 Plugin 接口；插件只认识 account.h。'),
        title='🏛 四层，一条依赖方向', color='blue', size=14.5, min_h=0.98)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 主程序', 'atm_framework.exe\n只有三行'),
        ('② 框架', '管理器 + 菜单\n+ 动态加载器'),
        ('③ 插件', 'plugins/*.dll\n可无限增加'),
        ('④ 账务核心', 'atmcore.dll\n全局唯一一份数据'),
    ], colors=('primary', 'teal', 'blue', 'purple'), size=14, h=1.00) + 0.22

    cards_row(s, y, [
        {'title': '账务数据必须共享', 'body': '每个 DLL 的全局变量各存一份。\n若把 account.c 编进四个插件，\n"存款"存的 500 元就在它自己那份\naccounts[] 里，"查询"读的还是 10000。',
         'color': 'red', 'size': 12.5, 'title_size': 15, 'min_h': 1.55},
        {'title': '目录即架构', 'body': 'plugin.h 放在 src 根目录\n→ 它是所有模块的共同契约。\nplugins/ 与 framework.c 平级\n→ 插件是外挂，不是框架的一部分。',
         'color': 'teal', 'size': 12.5, 'title_size': 15, 'min_h': 1.55},
        {'title': '平台差异关进接口', 'body': 'LoadLibrary 与 dlopen 完全不同。\n把差异关进 dynamic_loader.c，\n框架主体就一行 #ifdef 都没有\n→ 凡"会变的东西"都关进一个接口。',
         'color': 'purple', 'size': 12.5, 'title_size': 15, 'min_h': 1.55},
    ])
    banner(s, '抽象不是为了好写，是为了让数据只有一个真相')
    done('P4')


# ============================================================
# P5 完整项目：目录结构
# ============================================================
def p05_tree():
    s = pg('完整项目：目录结构', '看目录就能读出架构 —— 谁和谁平级，谁被单独列出')
    y = BODY_TOP
    cw = INNER_W * 0.58
    code(s, MARGIN_L, y, cw, [
        '14_完整项目/src/',
        '├── plugin.h              统一插件接口（契约）',
        '├── framework.h/.c         框架：管理器 + 菜单 + 入口',
        '├── dynamic_loader.h/.c    跨平台加载封装',
        '├── account.h/.c           账户模块（编进 atmcore.dll）',
        '├── transaction.h/.c       流水链表（编进 atmcore.dll）',
        '├── main.c                 入口：登记回退 + 三段式',
        '├── plugins/',
        '│   ├── deposit_plugin.c   存款插件',
        '│   ├── withdraw_plugin.c  取款插件',
        '│   ├── query_plugin.c     查询插件',
        '│   └── transfer_plugin.c  转账插件',
        '├── build.bat / Makefile   一键构建（三步走）',
        '├── atmcore.dll            共享账务核心（产物）',
        '└── atm_framework.exe      主程序（产物）',
    ], title='目录树：一眼看出谁依赖谁', size=10.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '契约在根部', 'body': 'plugin.h 不在 plugins/ 里，\n而在 src/ 根目录——它是共同契约。',
         'color': 'orange', 'size': 12.5, 'min_h': 1.12},
        {'title': '插件与框架平级', 'body': 'plugins/ 与 framework.c 同一层，\n说明插件是"外挂"，不是框架内部实现。',
         'color': 'teal', 'size': 12.5, 'min_h': 1.12},
        {'title': '被复用者单独列出', 'body': 'account / transaction 独立成组，\n它们是被复用的一方，不是主程序的内部实现。',
         'color': 'blue', 'size': 12.5, 'min_h': 1.12},
    ], gap=0.22)
    banner(s, '好的目录结构会说话：它把"谁稳定、谁易变、谁被谁复用"写在脸上')
    done('P5')


# ============================================================
# P6 完整项目：插件接口
# ============================================================
def p06_interface():
    s = pg('完整项目：插件接口 plugin.h', '结构体打包的不是数据，是"行为"')
    y = BODY_TOP
    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        'typedef struct Plugin {',
        '    char name[32];        /* 名称（唯一标识） */',
        '    char version[16];     /* 版本号 */',
        '    int  menu_id;         /* 菜单编号 */',
        '    char menu_label[40];  /* 菜单文字 */',
        '    int  need_amount;     /* 1=框架先读金额 */',
        '',
        '    int  (*init)(struct Plugin* self);',
        '    int  (*start)(struct Plugin* self);',
        '    int  (*execute)(struct Plugin*, double amount);',
        '    int  (*stop)(struct Plugin* self);',
        '    void (*cleanup)(struct Plugin* self);',
        '',
        '    void* user_data;      /* 私有数据 */',
        '    PluginState state;    /* 运行时状态 */',
        '} Plugin;',
    ], title='plugin.h：C 语言手搓的一张虚函数表', size=10.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '① 打包的是行为，不是数据',
         'body': '第7讲结构体打包数据，本讲打包行为。\nC 没有 class，但有函数指针——\n于是自己手搓一张虚函数表（vtable）。',
         'color': 'orange', 'size': 12.5, 'title_size': 15, 'min_h': 1.28},
        {'title': '② 一个 need_amount 省掉一个 switch',
         'body': '转账要"目标账户 + 金额"两个参数，\n统一接口只能传一个 double。\n接口保持最小公约数，插件自己声明需要什么。',
         'color': 'teal', 'size': 12.5, 'title_size': 15, 'min_h': 1.28},
        {'title': '③ 状态存在插件自己身上',
         'body': 'state 是给代码判断用的：\nif (p->state != PLUGIN_STARTED) continue;\n一句就挡住所有"没启动却想执行"的调用。',
         'color': 'purple', 'size': 12.5, 'title_size': 15, 'min_h': 1.28},
    ], gap=0.18)
    banner(s, '主程序通篇没有"存款""取款"，也没有一处 strcmp(p->name, "转账")')
    done('P6')


# ============================================================
# P7 完整项目：动态加载 + 优雅降级
# ============================================================
def p07_degrade():
    s = pg('动态加载 + 优雅降级：坏插件不许拖垮框架', '能力可以退化，体验不能退化')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '扫描目录 → dll_load → dll_symbol("get_plugin") → 拿 Plugin* → manager_register。\n'
        '任何一步失败都只影响当前这个文件：打印原因，然后继续扫下一个。'),
        title='🔌 加载路径：五步走，每步都有退路', color='teal', size=14.5, min_h=0.98)
    y = y2 + 0.24

    cw = INNER_W * 0.46
    code(s, MARGIN_L, y, cw, [
        'DllHandle dll_load(const char *path, char *err, size_t len);',
        'void     *dll_symbol(DllHandle h, const char *name);',
        'void      dll_unload(DllHandle h);',
        'const char *dll_extension(void);   /* ".dll" 或 ".so" */',
        'int       dll_scan_dir(const char *dir, const char *ext,',
        '                       DllFileCallback cb, void *user);',
    ], title='dynamic_loader.h：平台差异关进一个接口', size=10.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    rows = [('防线①', 'dll_load 失败 → 打印系统错误原因，跳过该文件'),
            ('防线②', '无 get_plugin 符号 → 卸载并跳过，计入"非插件"'),
            ('防线③', 'get_plugin() 返回空 → 卸载并跳过'),
            ('防线④', '功能缺失 → 启用 main.c 登记的内置实现兜底')]
    kv_rows(s, xr, y, wr, rows, widths=(0.20, 0.80), size=11.5,
            header=('四级防线', '触发条件与处理'))
    banner(s, '不是"我处理了异常"，而是"我能说清楚发生了什么"——这才是工程代码')
    done('P7')


# ============================================================
# P8 完整项目：配置化菜单
# ============================================================
def p08_menu():
    s = pg('完整项目：配置化菜单', '菜单不是数组，是链表 —— 这就是"零改动扩展"的秘诀')
    y = BODY_TOP
    cw = INNER_W * 0.44
    code(s, MARGIN_L, y, cw, [
        'typedef struct MenuItem {',
        '    int  id;                 /* 菜单编号 */',
        '    char label[40];          /* 菜单文字 */',
        '    Plugin* plugin;          /* 关联插件 */',
        '    struct MenuItem* next;   /* 下一个菜单项 */',
        '} MenuItem;',
    ], title='菜单项节点 = 链表节点 + 一个 plugin 指针', size=11)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '和普通链表唯一的不同，是多了 plugin 指针——它把"用户看到的一行字"和"背后干活的插件"挂在一起。\n'
        '有了它，菜单处理就退化成纯粹的"查表 + 多态"。\n'
        'menu_add 用有序插入：注册即挂载、卸载即摘除；'
        '加载顺序是 存款→查询→转账→取款，菜单却是 1 存款→2 取款→3 查询→4 转账。'),
        title='🔑 关键就是那个 plugin 指针', color='orange', size=12.5, min_h=2.05)
    y += 6 * 11 * 1.42 / 72 + 0.40 + 0.36 + 0.24

    compare(s, MARGIN_L, y, INNER_W,
            '第2讲：硬编码（功能写死在主程序）', [
                'printf 一行行写菜单，switch 一个个 case 分发',
                '加"转账"要改三处：打印、分支、编号分配',
                '菜单顺序 = 代码里的书写顺序，改功能必改主程序'],
            '第14讲：配置化（数据驱动）', [
                '遍历链表显示菜单，menu_find 查表 + 多态调用',
                '加"转账"改 0 处：插件自带 menu_id 与 menu_label',
                '菜单顺序 = id 排序，与插件加载顺序完全无关'],
            left_color='red', right_color='green', size=12.5)
    banner(s, '菜单不长在代码里，它长在链表里 —— 谁注册，谁就在里面')
    done('P8')


# ============================================================
# P9 关键代码走读
# ============================================================
def p09_source():
    s = pg('关键代码走读', '状态机守门 + 注册即挂菜单 + 主程序只剩三行')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        'while (cur != NULL) {',
        '    Plugin* p = cur->plugin;',
        '    if (p->state != PLUGIN_INITIALIZED) continue;  /* 状态守门 */',
        '    p->state = PLUGIN_STARTED;                     /* 升状态：已启动 */',
        '    if (p->menu_id != 0) {                         /* 插件自己声明菜单 */',
        '        menu_add(p->menu_id, p->menu_label, p);    /* 注册即挂载 */',
        '    }',
        '    ok++;',
        '    cur = cur->next;',
        '}',
    ], title='framework.c：manager_start_all() 的核心', size=10.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        'int main(void)',
        '{',
        '    framework_start();   /* 加载 + 注册 + init + start */',
        '    framework_run();     /* 菜单交互循环 */',
        '    framework_stop();    /* stop + cleanup + 卸载 */',
        '    return 0;',
        '}',
    ], title='main.c：通篇没有"存款""取款"', size=10.5)
    card(s, xr, y + 7 * 10.5 * 1.42 / 72 + 0.40 + 0.36 + 0.24, wr, (
        'Plugin 结构体 = 元数据 + 五个函数指针，\n'
        'C 语言用"结构体 + 函数指针"手搓了一张虚函数表。\n'
        '主程序只做两件事：登记兜底方案、把控制权交给框架。\n'
        '从第2讲的几十行 switch，瘦到今天的三行。'),
        title='plugin.h：把控制权交出去', color='orange', size=12, min_h=2.20)
    banner(s, '主程序少掉的全是"调度代码"——这就是控制反转最直观的度量方式')
    done('P9')


# ============================================================
# P10 真实运行输出
# ============================================================
def p10_output():
    s = pg('真实运行输出：终端实录', 'printf \'1\\n1\\n500\\n0\\n\' | ./atm_framework.exe（未删改，仅省去重复菜单）')
    y = BODY_TOP
    code(s, MARGIN_L, y, INNER_W, [
        "$ printf '1\\n1\\n500\\n0\\n' | ./atm_framework.exe",
        '=== 初始化账务核心 ===',
        '  [开户] ID:1001  户名:张三  余额:10000.00',
        '=== 扫描插件目录: plugins ===',
        '  [发现] plugins\\deposit_plugin.dll',
        '  [注册] 存款     v1.0  menu=1  向当前账户存入现金',
        '  [注册] 查询     v1.0  menu=3  查询余额与交易流水',
        '  [注册] 转账     v1.0  menu=4  在当前账户与目标账户之间转账',
        '  [注册] 取款     v1.0  menu=2  从当前账户取出现金',
        '  [结果] 扫描 4 个文件：成功 4，失败 0，非插件 0',
        '  [OK]   [存款] 已由动态库提供，不使用内置实现',
        '=== 框架启动完成，菜单项 5 个 ===',
        '  1. 存款   2. 取款   3. 查询余额   4. 转账   9. 插件列表   0. 退出',
        '请选择操作: 请输入金额:   [存款] 账户:1001(张三)  金额:1.00  余额:10001.00',
        '请选择操作:   [错误] 无效的菜单编号: 500',
        '  [管理器] 已释放 4 个插件节点     [菜单] 已释放 1 个菜单项',
        '  [卸载] plugins\\deposit_plugin.dll',
        '=== 框架已安全关闭，再见！===    $ echo $?  ->  0',
    ], title='终端实录（真实输出，节选）', size=10.5)
    banner(s, '片尾有真实运行演示动画：逐行打字 + 右侧并列展示 main.c / framework.c')
    done('P10')


# ============================================================
# P11 运行演示 + 优雅降级实测
# ============================================================
def p11_demo():
    s = pg('运行演示：优雅降级实测', '故意弄坏一个插件，看框架怎么不崩')
    y = BODY_TOP
    y = cards_row(s, y, [
        {'title': '① 插件来自文件', 'body': '[发现] plugins\\deposit_plugin.dll\n插件是从目录里扫出来的，\n不是编译进代码的。',
         'color': 'teal', 'size': 12.5, 'min_h': 1.22},
        {'title': '② 加载有统计', 'body': '[结果] 成功 4，失败 0，非插件 0\n加载过程有账可算，\n失败绝不会静默发生。',
         'color': 'blue', 'size': 12.5, 'min_h': 1.22},
        {'title': '③ 菜单是攒出来的', 'body': '菜单 5 项 = 4 个插件 + 1 个内置项\n主程序一行菜单都没写，\n挂上去的还有摘下来的路径。',
         'color': 'purple', 'size': 12.5, 'min_h': 1.22},
    ]) + 0.24

    demo_frame(s, MARGIN_L, y, INNER_W, 2.34, title='降级实测：删掉 plugins/transfer_plugin.dll', lines=[
        '$ rm plugins/transfer_plugin.dll      # 故意删掉转账插件',
        '  [结果] 扫描 3 个文件：成功 3，失败 0，非插件 0',
        '  [OK]   [存款] 已由动态库提供，不使用内置实现',
        '  [降级] [转账] 未从 plugins/ 加载到，启用内置实现',
        '  [注册] 转账     v1.0  menu=4  在当前账户与目标账户之间转账',
        '=== 框架启动完成，菜单项 5 个 ===',
    ], note='菜单仍是 5 项，转账照常可用 —— 能力退化，体验不退化')
    banner(s, '片尾演示用真实输出做打字动画，右侧同步展示真实源码文件')
    done('P11')


# ============================================================
# P12 全系列知识树串联
# ============================================================
def p12_tree():
    s = pg('全系列知识树：三条线，拧成一股绳', '横着看是三条技术线，竖着看是层层供料')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '没有第8讲的链表，就没有插件链表和菜单链表；没有第5讲的函数指针，就没有 Plugin 接口；'
        '没有第10讲的动态库，就没有 atmcore.dll。14 讲，没有一讲是"学过就扔"的。'),
        title='🌳 每一讲都在为终点供料', color='orange', size=14.5, min_h=1.00)
    y = y2 + 0.22

    y = cards_row(s, y, [
        {'title': '语言基础层（第1-8讲）', 'body': '表达式 · 控制结构 · 函数 · 多文件\n指针 · 数组 · 结构体 · 链表\n提供"零件"：值 · 逻辑 · 数据 · 连接',
         'color': 'teal', 'size': 12.5, 'title_size': 15, 'min_h': 1.45},
        {'title': '库与链接层（第9-11讲）', 'body': '静态库 → 动态库 → 运行时加载\nar / .dll 共享 / dlopen 按需\n回答同一个问题：怎么让代码被复用',
         'color': 'blue', 'size': 12.5, 'title_size': 15, 'min_h': 1.45},
        {'title': '架构思想层（第12-14讲）', 'body': '接口抽象 → 插件框架 → 完整项目 ★\n结构体+函数指针 / 生命周期 / 装配\n回答：怎么被"别人写的代码"扩展',
         'color': 'purple', 'size': 12.5, 'title_size': 15, 'min_h': 1.45},
    ]) + 0.22

    code(s, MARGIN_L, y, INNER_W, [
        '复用范围：函数内复用 → 文件内复用 → 项目内复用 → 进程内复用 → 系统级复用',
        '          第1-2讲        第3讲         第4讲        第9-10讲        第11-14讲',
        '          一个值         一段逻辑      一组功能     一份二进制       一个生态',
    ], title='贯穿全系列的那条主线：复用范围，一级一级往外扩', size=11)
    banner(s, '复用的范围，就是架构的高度')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的终点：从"你调用世界"到"世界调用你"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架，每上一级，复用范围就往外扩一圈。'),
        title='🧭 六级台阶，一套度量：复用范围', color='orange', size=14.5, min_h=0.98)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1-2讲'),
        ('② 函数', '第3讲'),
        ('③ 模块', '第4讲'),
        ('④ 库', '第9-10讲'),
        ('⑤ 插件', '第11-12讲'),
        ('⑥ 框架', '第13-14讲 ⭐'),
    ], colors=('teal', 'teal', 'blue', 'blue', 'purple', 'primary'),
        size=13.5, h=0.90) + 0.22

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '① 表达式：让我这一行能用上\n'
        '② 函数：让同一文件里能用上\n'
        '③ 模块：让同一项目里能用上\n'
        '④ 库：让别的项目能用上\n'
        '⑤ 插件：让运行中的系统能用上\n'
        '⑥ 框架：让别人写的东西能用上'),
        title='六级台阶都在回答同一个问题', color='teal', size=12.5,
        title_size=15, min_h=1.92)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '本讲把前十三讲的全部零件装配到位：\n'
        '· 运行时加载让"有哪些功能"由文件决定\n'
        '· 共享库让所有插件看到同一份数据\n'
        '· 优雅降级让坏插件拖不垮整个系统\n'
        '· 控制反转从局部走向完整'),
        title='本讲为终点贡献了什么', color='orange', size=12.5,
        title_size=15, min_h=1.92)
    banner(s, '每上一级，我能控制的东西少一点，能容纳的东西多一点')
    done('P13')


# ============================================================
# P14 设计模式入门：C 语言里的四个影子
# ============================================================
def p14_pattern():
    s = pg('设计模式入门：C 语言里的四个影子', '这些模式，你其实已经在无意中用过了')
    y = BODY_TOP
    rows = [('策略', '把"算法"抽出来，运行时换一个', 'p->execute()：同一行代码，换插件就换行为'),
            ('工厂', '不直接 new，交给一个函数去造', 'get_plugin() 是插件工厂的统一入口符号'),
            ('观察者', '主体状态变了，通知一批订阅者', 'manager_start_all() 遍历链表逐个回调'),
            ('模板方法', '骨架固定，可变步骤留给使用者', '五阶段生命周期：框架定序，插件填步')]
    y = kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.14, 0.42, 0.44), size=12,
                header=('模式', '一句话定义', '本系列里的 C 语言长相'))[0] + 0.24

    cards_row(s, y, [
        {'title': '模式不是额外要学的东西', 'body': '设计模式在 C++ / Java 里是"模式"，在 C 里只能自己手搓——\n'
                                                 '但你是一步步走过来的，不是背过来的。\n'
                                                 '解决真实问题时，你自然会走到这些路上。',
         'color': 'teal', 'size': 12.5, 'min_h': 1.30},
        {'title': '模板方法：框架定流程，插件填步骤', 'body': '框架规定死的骨架：init → start → execute… → stop → cleanup，\n'
                                                       '插件只填每一步"做什么"；状态机还强制了顺序。\n'
                                                       '想跳过 init 直接 start？状态机当场拒绝。',
         'color': 'orange', 'size': 12.5, 'min_h': 1.30},
    ], gap=0.26)
    banner(s, '设计模式不是额外要学的东西，它是你解决问题时自然走上的路')
    done('P14')


# ============================================================
# P15 思考题 ①②
# ============================================================
def p15_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '本讲的降级策略覆盖的都是"加载阶段"的失败。但如果插件已经成功加载并启动，'
        '在 execute() 执行到一半时空指针解引用、数组越界直接崩溃（Windows 访问违例 / Linux SIGSEGV），'
        '整个进程会立刻挂掉。\n'
        '提示：进程内的段错误，框架到底能不能接住？如果能，代价是什么？'
        '想想"进程隔离"这条路要付出什么。'),
        title='思考题 ①：插件崩溃了，框架该怎么办？', color='red', size=14, min_h=1.72)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '假设新来一个"报表"插件，它必须在"查询"和"取款"都启动成功之后才能工作；'
        '如果它先启动，调用 transaction_print_history() 时数据还没准备好。'
        '而本讲的 manager_start_all() 只是顺序遍历链表，不关心任何依赖。\n'
        '提示：依赖关系本质是一张有向图，"启动顺序"是什么？谁来检测循环依赖？停机的顺序又该怎样？'),
        title='思考题 ②：插件之间有依赖关系，怎么保证启动顺序正确？', color='purple', size=14, min_h=1.72)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P15')


# ============================================================
# P16 思考题 ①② 参考解答
# ============================================================
def p16_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：分级防御，只有进程隔离能真兜住',
         'body': '残酷事实：进程内的段错误，框架接不住。\n'
                 'execute() 与框架同进程同线程，\n'
                 '插件越界写内存，可能连账务数据一起踩坏。\n'
                 '第一级 进程内（只防软错误）：\n'
                 '  参数校验 + 返回值协议 + 看门狗超时。\n'
                 '第二级 进程隔离（真解决，代价大）：\n'
                 '  插件跑独立进程，IPC 通信，崩了就重启它。\n'
                 '第三级 工程手段：插件过审、分级目录、\n'
                 '  版本归档回滚、崩溃现场写日志。',
         'color': 'red', 'size': 12, 'title_size': 15, 'min_h': 3.30},
        {'title': '解答 ②：把隐式约定变成显式数据',
         'body': '第一步 把依赖变成可声明的数据：\n'
                 '  Plugin 里加 depends_on[] + dep_count。\n'
                 '第二步 启动前做一次拓扑排序：\n'
                 '  入度为 0 的先启动，每启动一个解锁一批；\n'
                 '  队列空了还有没启动的 → 存在循环依赖，报错。\n'
                 '第三步 处理"被依赖插件加载不到"：\n'
                 '  严格 / 宽松 / 回退三种策略；\n'
                 '  本讲的"内置实现兜底"天然适合回退策略。\n'
                 '第四步 停止要逆序（A→B→C 就 C→B→A），\n'
                 '  中途失败要按启动逆序回滚。',
         'color': 'purple', 'size': 12, 'title_size': 15, 'min_h': 3.30},
    ], gap=0.26)
    banner(s, '架构的本质就是：你愿意为哪种失败，付出什么代价')
    done('P16')


# ============================================================
# P17 思考题 ③④
# ============================================================
def p17_q34():
    s = pg('思考题 ③④', '两题进阶：配置化的边界，与库/框架的分界线')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '本讲项目里同时存在"配置化"和"硬编码"，而且硬编码是有意为之：'
        '插件目录写死为 "plugins"、入口符号写死为 "get_plugin"、生命周期写死五步，'
        '但功能清单、菜单编号、need_amount 又全是配置化的。\n'
        '提示：判断标准是什么？"会变、且变化来自使用者"与"稳定、且变化只能来自开发者"该怎么分？'),
        title='思考题 ③：配置化和硬编码，边界到底在哪？', color='teal', size=14, min_h=1.72)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '同一个项目里两者同时存在：atmcore.dll 是库（插件主动调用它的 account_* 函数）；'
        'framework.c 是框架（框架反过来调插件的 init/execute）。'
        '那分界线到底划在哪？\n'
        '提示：从"控制权在谁手上""谁定义流程谁定义步骤""依赖方向""价值来源与代价"四个角度层层深入；'
        '最后想想两者是对立的，还是分层共存的。'),
        title='思考题 ④：框架和库的本质区别到底是什么？', color='green', size=14, min_h=1.72)
    banner(s, '这两题想通了，你就从"会写代码"走到了"会做设计"')
    done('P17')


# ============================================================
# P18 思考题 ③④ 参考解答 + 小结收尾
# ============================================================
def p18_a34():
    s = pg('思考题 ③④ 参考解答 + 全系列收尾', '把今天的项目，接到整条架构主线上')
    y = BODY_TOP
    y = cards_row(s, y, [
        {'title': '解答 ③：契约硬编码，策略配置化',
         'body': '一条尺子：会变、且变化来自使用者 → 配置化；\n'
                 '稳定、且变化只能来自开发者 → 硬编码。\n'
                 '配置化：功能清单、菜单文字、need_amount。\n'
                 '硬编码：插件目录 "plugins"（部署约定）、\n'
                 '  入口符号 "get_plugin"（ABI 契约）、生命周期五步。\n'
                 '三条细则：契约硬编码策略配置化；变化频率\n'
                 '差一个数量级的东西别放一处；算清配置化成本账。\n'
                 '该反过来硬编码时：功能极少且稳定、性能极敏感、\n'
                 '  必须编译期校验。',
         'color': 'teal', 'size': 11.5, 'title_size': 15, 'min_h': 2.95},
        {'title': '解答 ④：控制权在谁手上，就是分界',
         'body': '第一层：库是你调用它，框架是它调用你（IoC）。\n'
                 '第二层：谁定义"流程"谁定义"步骤"——库不拒绝你\n'
                 '  调用，框架会拒绝你没按它的流程走。\n'
                 '第三层：依赖方向相反。应用 → 库；\n'
                 '  插件 → 框架契约，而框架不依赖任何具体插件。\n'
                 '第四层：库复用代码，框架复用结构；\n'
                 '  用库学 API，用框架交控制权。\n'
                 '第五层：两者不对立，是分层共存——\n'
                 '  对插件而言，框架是"调用我的"，库是"我调用的"。',
         'color': 'green', 'size': 11.5, 'title_size': 15, 'min_h': 2.95},
    ], gap=0.26) + 0.22

    card(s, MARGIN_L, y, INNER_W, (
        '一句话总结：把一行 printf，变成一台"谁都能往上装功能、主程序不用改"的机器——这就是架构。'),
        title='📝 全系列一句话', color='orange', size=13, min_h=1.00)
    banner(s, '🎉 全系列完 —— 感谢同行。课程结束了，你的架构之路才刚开始。')
    done('P18')


for fn in (p01_cover, p02_map, p03_goal, p04_arch, p05_tree, p06_interface, p07_degrade,
           p08_menu, p09_source, p10_output, p11_demo, p12_tree, p13_ladder,
           p14_pattern, p15_q12, p16_a12, p17_q34, p18_a34):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
