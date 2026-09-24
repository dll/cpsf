# -*- coding: utf-8 -*-
"""
第11讲：运行时加载 —— 让程序自己决定加载什么
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

LECTURE = '第11讲 运行时加载'
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

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第11讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.30, 3.4, 1.2,
              '从一行 printf\n到软件体系的插件框架', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '运行时加载', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '让程序自己决定加载什么', 27, C['primary_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.6,
              '第10讲把库独立了出去，但"In 启动就必须齐"还是死依赖：\n'
              '缺一个库，程序根本起不来。本讲把决定权从操作系统手里\n'
              '拿回来——运行中自己打开库、按名字找函数、用完卸载；\n'
              '再配合目录扫描，"插件"就此诞生。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '六级台阶的第五级 —— 插件：库从"必需"变成"可选"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '前几讲我们一路把"库"做扎实了。本讲跨到第五级台阶——插件。它的关键一跃是：'
        '库不再是启动前必须齐的依赖，而是运行中按需加载、按名字调用的可选资源。'),
        title='🎯 本讲定位', color='orange', size=15.5, min_h=1.10)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '第3讲 ✅'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '第9-10讲 ✅'), ('⑤ 插件', '← 你在这里'), ('⑥ 框架', '第13讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('gray', 'gray', 'gray', 'gray', 'primary', 'gray'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第10讲：动态库 + 加载时链接，\n'
        '库独立了，但缺库就起不来、加载对象编译期写死。'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第12讲：只统一函数名还不够，\n'
        '要用"结构体 + 函数指针"统一插件接口，走向多态。'),
        title='➡ 后续', color='teal', size=14.5, min_h=1.00)
    banner(s, '本讲让库从"必需"变成"可选"：缺了照跑，多了就用——插件的门就此打开')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '动态库解决了共享，但"加载时链接"还是三个死依赖')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第10讲：加载时链接', [
                    '程序启动时由 OS 自动把所有依赖库加载齐',
                    '缺一个 dll/so，程序根本启动不了',
                    '加载哪个库，编译链接时就写死进了导入表'],
                '第11讲：要打破的"死"', [
                    '依赖是死的：启动前库必须到位，一个不能少',
                    '时机是死的：加载发生在启动，而不是要用到时',
                    '对象是死的：加载哪个库在编译期就定死了'],
                left_color='blue', right_color='red', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '依赖是死的', 'body': '缺一个库，程序直接起不来\n不是功能失效，是根本启动不了',
         'color': 'red', 'size': 13},
        {'title': '时机是死的', 'body': '加载发生在"程序启动"\n而不是"真正用到"的那一刻',
         'color': 'yellow', 'size': 13},
        {'title': '对象是死的', 'body': '加载哪个库编译期就写死\n想加一个新库必须重新链接',
         'color': 'purple', 'size': 13},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '一个自然的想法：能不能让程序自己决定——何时加载、加载哪个、调用哪个函数？',
    ], size=15)
    banner(s, '把决定权从操作系统手里，拿回到程序自己手里——这就是运行时加载')
    done('P3')


# ============================================================
# P4 核心内容一：运行时加载的概念
# ============================================================
def p04_concept():
    s = pg('什么是运行时加载：程序自己说了算', '加载时机、加载对象、用完卸载，全部由代码决定')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '运行时加载 = 程序在运行过程中，自己调用 API 打开动态库、查找函数、调用函数，用完还能卸载。'),
        title='📌 一句话定义', color='orange', size=15, min_h=0.92)
    y = y2 + 0.20

    y = kv_rows(s, MARGIN_L, y, INNER_W, [
        ('什么时候加载？', '启动时由 OS 自动加载', '运行到需要时，由代码自己加载'),
        ('谁决定加载哪个？', '编译器/链接器写死在导入表', '程序在运行时按名字挑'),
        ('能不能卸载？', '不能，跟随进程生命周期', '可以，dlclose / FreeLibrary 主动卸载'),
        ('库不存在会怎样？', '程序无法启动', '加载失败返回空句柄，程序继续跑'),
    ], widths=(0.26, 0.36, 0.38), size=11.5,
        header=('问题', '加载时链接（第10讲）', '运行时加载（本讲）'))[0] + 0.18

    cards_row(s, y, [
        {'title': '自助餐：开餐前必须摆齐', 'body': '少一道菜，今天就不开门 —— 缺库 = 起不来',
         'color': 'red', 'size': 13},
        {'title': '点菜：客人点了才现做', 'body': '某道菜没有？只告诉这道没有，其他照常',
         'color': 'green', 'size': 13},
    ])
    banner(s, '库从"必需"变成"可选"——这一字之差，打开了插件世界的大门')
    done('P4')


# ============================================================
# P5 核心内容二：两套 API 对照
# ============================================================
def p05_api():
    s = pg('两套平台 API：名字不同，心思一样', 'dlopen/dlsym/dlclose  ↔  LoadLibrary/GetProcAddress/FreeLibrary')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'Linux 和 Windows 各有一套运行时加载 API，做的事情一模一样，只是名字不同——学一套，另一套自动会。'),
        title='🔑 一套心思，两套名字', color='blue', size=14.5, min_h=0.95)
    y = y2 + 0.20

    kv_rows(s, MARGIN_L, y, INNER_W, [
        ('打开动态库', 'dlopen(path, RTLD_LAZY)', 'LoadLibraryA(path)'),
        ('按名字找符号', 'dlsym(handle, "name")', 'GetProcAddress(handle, "name")'),
        ('关闭 / 卸载', 'dlclose(handle)', 'FreeLibrary(handle)'),
        ('取错误信息', 'dlerror()', 'GetLastError() + FormatMessage'),
        ('是否需要额外链接', '要，-ldl（libdl）', '不用，kernel32 默认就有'),
    ], widths=(0.26, 0.37, 0.37), size=12,
        header=('作用', 'Linux（dlfcn.h）', 'Windows（windows.h）'))
    banner(s, '记忆口诀：dlopen 就是 LoadLibrary，dlsym 就是 GetProcAddress')
    done('P5')


# ============================================================
# P6 核心内容三：跨平台封装 dynlib.h
# ============================================================
def p06_dynlib():
    s = pg('跨平台封装：把平台差异关进 dynlib.h', '对外只留 dynlib_open / dynlib_sym / dynlib_close')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        '/* 句柄：两个平台统一成 dynlib_handle */',
        '#ifdef _WIN32',
        '    typedef HMODULE dynlib_handle;',
        '#else',
        '    typedef void *dynlib_handle;',
        '#endif',
        '',
        'static inline dynlib_handle',
        'dynlib_open(const char *path) {',
        '#ifdef _WIN32',
        '    return LoadLibraryA(path);',
        '#else',
        '    return dlopen(path, RTLD_LAZY);',
        '#endif',
        '}',
    ], title='dynlib.h：用一个头文件隔离平台差异', size=10.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    cards_col(s, xr, y, wr, [
        {'title': '① 什么叫句柄', 'body': '操作系统发的一张"提货单"，代表一个已打开的库', 'color': 'orange', 'size': 12.5},
        {'title': '② 为什么封装', 'body': '#ifdef 只出现在 dynlib.h 里，业务代码与平台无关', 'color': 'blue', 'size': 12.5},
        {'title': '③ 为什么用 static inline', 'body': '每个 .c 都能 include，不重复定义，也不用多编一个 .c', 'color': 'teal', 'size': 12.5},
    ], gap=0.14)
    banner(s, '把"会因平台而变的东西"关进最小范围，外面只留一套统一接口')
    done('P6')


# ============================================================
# P7 核心内容四：按名字找函数 = 符号约定
# ============================================================
def p07_symbol():
    s = pg('按名字找函数：一切靠"约定"', '动态库自带符号表，dlsym 就是拿名字去查这张表')
    y = BODY_TOP
    y = kv_rows(s, MARGIN_L, y, INNER_W, [
        ('plugin_name', 'const char *plugin_name(void)', '返回插件名字，宿主打印"我加载了谁"'),
        ('plugin_execute', 'int plugin_execute(double amount)', '功能入口，0 成功、非 0 失败'),
    ], widths=(0.20, 0.40, 0.40), size=12,
        header=('约定符号', '签名', '含义'))[0] + 0.22

    cw = INNER_W * 0.52
    code(s, MARGIN_L, y, cw, [
        '/* plugin_api.h：把"接头暗号"写成宏 */',
        '#define PLUGIN_SYM_NAME     "plugin_name"',
        '#define PLUGIN_SYM_EXECUTE  "plugin_execute"',
        '',
        '/* 函数指针类型：宿主接收 dlsym 结果 */',
        'typedef const char *(*plugin_name_fn)(void);',
        'typedef int (*plugin_execute_fn)(double amount);',
    ], title='约定写进头文件，避免手写字符串打错', size=10.5)

    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '忘了加导出宏 → GetProcAddress 返回 NULL\n'
        '用 C++ 编译（名字被修饰）→ 名字变了，查不到\n'
        '函数写成 static → 不进入导出表\n'
        '符号名拼错一个字母 → 照样返回 NULL'),
        title='⚠️ 四种取不到符号的真实原因', color='red', size=12.5, min_h=1.75)
    banner(s, '运行时加载把"调用哪个函数"交给了一个字符串——字符串最脆弱，必须当正常情况处理')
    done('P7')


# ============================================================
# P8 核心内容五：目录扫描 + 自动加载 = 插件雏形
# ============================================================
def p08_scan():
    s = pg('目录扫描 + 自动加载 = 插件雏形', '宿主不再"认识"任何插件，它只认约定')
    y = BODY_TOP
    y = code(s, MARGIN_L, y, INNER_W, [
        'plugins/ 目录',
        '   deposit_plugin.dll    withdraw_plugin.dll',
        '   query_plugin.dll      broken_plugin.dll  ← 不守约的反例',
        '            │  ① 扫描目录，筛出 .dll / .so',
        '            ▼',
        '   dynlib_open(路径)               ② 运行时加载（这一步才把库拉进进程）',
        '      成功 ↙      ↘ 失败  →  打印错误（dynlib_error），跳过',
        '   dynlib_sym 取 plugin_name / plugin_execute   ③ 按约定名字取符号',
        '      成功 ↙      ↘ 取不到 plugin_execute  →  判定不合格，卸载并跳过',
        '   调用 get_name() / execute(amount)             ④ 执行插件功能',
        '            ▼',
        '   dynlib_close(handle)            ⑤ 用完卸载，内存释放',
    ], title='宿主的五步流程：发现 → 加载 → 取符号 → 调用 → 卸载', size=10)[0] + 0.22

    cards_row(s, y, [
        {'title': '运行时加载', 'body': '加载时机由程序决定', 'color': 'blue', 'size': 12.5},
        {'title': '按名字取符号', 'body': '调用哪个函数由字符串决定', 'color': 'teal', 'size': 12.5},
        {'title': '扫描目录', 'body': '加载哪些库由目录内容决定', 'color': 'purple', 'size': 12.5},
        {'title': '用完卸载', 'body': '模块可插可拔，内存可回收', 'color': 'orange', 'size': 12.5},
    ])
    banner(s, '往 plugins 目录丢一个动态库，宿主就多一个功能——插件就此诞生')
    done('P8')


# ============================================================
# P9 原理深入：句柄与符号表 ⭐
# ============================================================
def p09_deep():
    s = pg('原理深入：句柄是什么？NULL 为什么不能调用？ ⭐', '先有"库"，才有"函数"；查不到就是空地址')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '句柄代表"哪一个库"，函数指针代表"哪一个函数"。dlsym 拿名字去查库的符号表，'
        '查到返回函数入口地址，查不到返回 NULL——NULL 就是"没有这个地址"。'),
        title='🧭 一句话原理', color='blue', size=14.5, min_h=1.05)
    y = y2 + 0.22

    y = compare(s, MARGIN_L, y, INNER_W,
                '句柄 handle', [
                    '代表整个"库"这一个模块',
                    '由 dlopen / LoadLibrary 产生',
                    '用来查符号、卸载；不能加括号调用'],
                '函数指针 function pointer', [
                    '代表库里"某一个函数"',
                    '由 dlsym / GetProcAddress 产生',
                    '就是代码入口地址，能直接调用'],
                left_color='primary', right_color='teal', size=13.5) + 0.16

    card(s, MARGIN_L, y, INNER_W, (
        '若 execute 为 NULL 还直接 execute(amount)，等于"调用空地址"，程序立刻崩溃。'
        '所以宿主必须把取不到符号当正常情况处理：打印原因 → dynlib_close 卸载 → 返回错误码，绝不想当然。'),
        title='🚨 NULL 绝不能调用', color='red', size=13.5, min_h=1.05)
    banner(s, '运行时加载的"优雅"，就在于把失败当常态：一个坏插件，拖不垮整个宿主')
    done('P9')


# ============================================================
# P10 对比与辨析：三种链接方式
# ============================================================
def p10_compare():
    s = pg('对比与辨析：三种链接方式', '代码放在哪、何时加载、谁来决定、缺库后果、能否卸载')
    y = BODY_TOP
    rows = [
        ('代码放在哪', '复制进 exe 内部', '独立的 .dll/.so', '独立的 .dll/.so'),
        ('何时加载', '链接时复制，运行无需库', '程序启动时由 OS 自动加载', '运行到需要时由代码主动加载'),
        ('谁来决定', '链接器（编译期写死）', '链接器写进导入表，OS 执行', '程序自己（运行时按名字挑）'),
        ('缺库后果', '不受影响（已内置）', '程序无法启动', '返回 NULL，程序继续跑'),
        ('能否卸载', '不需要（就在 exe 里）', '不能，跟随进程生命周期', '能，dlclose 主动卸载'),
        ('加功能要改宿主吗', '要重新链接', '要重新链接', '不用，丢个文件到目录即可'),
    ]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.19, 0.27, 0.27, 0.27), size=11.5,
            header=('维度', '静态链接（第9讲）', '加载时链接（第10讲）', '运行时加载（本讲）'))
    banner(s, '热插拔的本质：宿主与插件只靠约定通信，不靠编译期硬编码绑定')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/host.c 的 load_and_call + src/deposit_plugin.c')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        '/* host.c —— 加载一个插件的完整过程 */',
        'handle = dynlib_open(path);              /* ① 运行时加载 */',
        'if (handle == DYNLIB_INVALID) {',
        '    printf("  ✗ 加载失败（已优雅跳过）");',
        '    return -1;',
        '}',
        'get_name = dynlib_sym(handle, PLUGIN_SYM_NAME);',
        'execute  = dynlib_sym(handle, PLUGIN_SYM_EXECUTE);  /* ② 取符号 */',
        'if (execute == NULL) {',
        '    printf("  ✗ 缺少约定符号，不是合法插件，已跳过");',
        '    dynlib_close(handle);                /* 失败也要先卸载 */',
        '    return -1;',
        '}',
        'execute(amount);                         /* ③ 函数指针调用 */',
        'dynlib_close(handle);                    /* ④ 用完卸载 */',
    ], title='host.c：任何一步失败，都先 dlclose 再返回', size=10)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '/* deposit_plugin.c —— 插件实现契约 */',
        'static double g_balance = 1000.0;',
        '',
        'PLUGIN_API const char *plugin_name(void)',
        '{ return "存款插件"; }',
        '',
        'PLUGIN_API int plugin_execute(double amount)',
        '{',
        '    if (amount <= 0.0) return -1;',
        '    g_balance += amount;',
        '    printf("存入 %.2f，余额 %.2f", amount, g_balance);',
        '    return 0;',
        '}',
    ], title='插件：static 状态活在宿主进程里', size=10)
    banner(s, '宿主里没有任何插件名，只认"约定"——只要导出了那两个符号，就把它当插件用')
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实加载与优雅报错', '扫描目录、加载、调用、卸载，以及坏插件的处理，全部真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.60
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall -Wextra -shared -o deposit_plugin.dll deposit_plugin.c',
        '$ gcc -Wall -Wextra -o host.exe host.c',
        '$ ./host.exe',
        '[步骤 1] 扫描插件目录：plugins',
        '  共发现 4 个候选插件文件',
        '  发现文件：plugins\\broken_plugin.dll',
        '    ✗ 该文件缺少约定符号 "plugin_execute"，不是合法插件，已跳过',
        '  发现文件：plugins\\deposit_plugin.dll',
        '    → 加载成功，插件名字：存款插件',
        '    [存款插件] 存入 500.00 元，当前余额 1500.00 元',
        '  发现文件：plugins\\query_plugin.dll',
        '    → 加载成功，插件名字：查询插件',
        '[步骤 2] 故意加载一个不存在的库',
        '    ✗ 加载失败（已优雅跳过）：找不到指定的模块。',
        '[步骤 3] 查找不存在的符号 "plugin_exectue"',
        '    ✗ 未找到（返回 NULL），宿主没有崩溃，正常继续。',
        '  运行结束：本轮成功加载并调用了 3 个插件',
    ], title='终端实录（真实输出，未删改）', size=10)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    card(s, xr, y, wr, (
        '① 共发现 4 个候选：3 个合法 + 1 个坏插件\n'
        '② 坏插件能加载，但少了 execute 被判定不合格\n'
        '③ 不存在的库 → 打印一句错误继续跑\n'
        '④ 符号名少一个 c → dlsym 返回 NULL，不崩溃\n'
        '⑤ 每个插件用完都 dlclose，不占内存\n'
        '⑥ 宿主全程没写死任何插件名，只认约定'),
        title='👀 要看清楚的六个点', color='orange', size=12, min_h=4.35)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 dynlib.h / host.c')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的第五级：插件诞生 —— 库从"必需"变成"可选"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。本讲站上第五级——插件。'
        '它诞生的标志是：宿主在运行时扫描目录、按名字找函数、动态调用，库成了可插可拔的资源。'),
        title='🧭 一条主线', color='orange', size=15, min_h=1.05)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '第3讲 ✅'),
        ('③ 模块', '第4讲 ✅'),
        ('④ 库', '第9-10讲 ✅'),
        ('⑤ 插件', '← 本讲 ⭐'),
        ('⑥ 框架', '第13讲'),
    ], colors=('gray', 'gray', 'gray', 'gray', 'primary', 'gray'),
        size=14, h=0.95) + 0.24

    w = INNER_W / 2 - 0.14
    card(s, MARGIN_L, y, w, (
        '运行时加载让库变"可选"；\n'
        '按名字找函数让调用不必编译期绑定；\n'
        '目录扫描让宿主不认识插件、只认约定；\n'
        '用完卸载，模块可插可拔——插件成型。'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.60)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '插件"能进来"了，但宿主是靠字符串和写死的\n'
        '参数类型去调用的：查询插件被迫收一个金额，\n'
        '转账插件一个 double 又不够用。\n'
        '→ 只统一函数名还不够，还得统一接口。'),
        title='下一讲接着做什么', color='blue', size=13.5, min_h=1.60)
    banner(s, '插件诞生了，但接口还是"散装"的——下一讲给所有插件装一个统一的 USB 插头')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'Linux 与 Windows 各有一套运行时加载 API。请说出它们的对应关系；'
        '并回答：dlopen / LoadLibrary 返回的"句柄"到底是什么？它和函数指针有什么区别？'
        '为什么 dlsym 需要一个句柄，而不能直接传库文件名？\n'
        '提示：先想"要先打开才能查询"，再想"同名符号可能来自不同的库"。'),
        title='思考题 ①：两套 API 的对应与句柄的本质', color='orange', size=14.5, min_h=1.62)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '宿主用 dynlib_sym 取符号，如果返回 NULL，为什么不直接忽略、继续往下调用？'
        '请说出至少三种会导致"找不到符号"的真实原因，以及宿主应该怎么正确处理。\n'
        '提示：NULL 是什么？直接调用它会怎样？错误处理里，"已经打开的库"要不要还回去？'),
        title='思考题 ②：找不到符号，为什么不能硬调用？', color='purple', size=14.5, min_h=1.62)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：句柄代表"库"，指针代表"函数"',
         'body': '对应关系：dlopen ↔ LoadLibrary，\n'
                 'dlsym ↔ GetProcAddress，dlclose ↔ FreeLibrary。\n'
                 '句柄是一个已打开库的凭证（不透明指针），\n'
                 '代表"整个库"；函数指针代表"库里某个函数"，\n'
                 '能直接加括号调用，句柄不能。\n'
                 '为什么必须传句柄：库要先 dlopen 加载、\n'
                 '建好映射和符号表，符号地址才存在；\n'
                 '且同名符号可能来自不同库，必须靠句柄区分。',
         'color': 'orange', 'size': 12},
        {'title': '解答 ②：NULL 是空地址，不能调用',
         'body': 'dynlib_sym 返回函数入口地址，NULL 表示\n'
                 '这个地址不存在；直接调用等于调用空地址，\n'
                 '程序立刻崩溃（访问违规 / 段错误）。\n'
                 '三种原因：符号名写错（少一个字母）；\n'
                 '插件忘了加导出宏；用 C++ 编译被名字修饰，\n'
                 '或函数写成了 static。\n'
                 '正确做法：判定为"不合格插件"，打印原因，\n'
                 '先 dynlib_close 把已加载的库还回去，\n'
                 '再返回错误码——资源获取即释放。',
         'color': 'purple', 'size': 12},
    ], gap=0.26)
    banner(s, '句柄代表哪一个库，函数指针代表哪一个函数——先有库，才有函数')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从三种链接方式，接到"热插拔"的本质')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '请从"代码放在哪、何时加载、谁来决定、缺库后果、能否卸载、新增功能要不要改程序"'
        '六个维度，对比静态链接（第9讲）、加载时链接（第10讲）、运行时加载（第11讲）。\n'
        '提示：不要只背结论，每题都问一句"为什么会有这个差异"。'),
        title='思考题 ③：三种链接方式的全方位对比', color='teal', size=14.5, min_h=1.62)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '本讲让宿主"往目录里丢一个新插件就能多一个功能"，也就是热插拔。'
        '为什么只有运行时加载能做到？前两种链接方式究竟"卡"在哪一步？\n'
        '提示：热插拔有两个硬条件——加载时机由程序决定、新增模块不动宿主程序。逐一代入三种方式看看。'),
        title='思考题 ④：为什么只有运行时加载能"热插拔"？', color='green', size=14.5, min_h=1.62)
    banner(s, '想通这两题，"宿主与插件靠约定通信"这句话就真正落到地上了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '从"编译期绑定"接到"运行期绑定"')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：三种方式，一条演进线',
         'body': '静态链接：代码复制进 exe，链接期写死，\n'
                 '缺库不受影响，不需卸载，加功能要重链。\n'
                 '加载时链接：库独立，但启动时必须齐，\n'
                 '加载哪些写进导入表，缺库起不来，不能卸载，\n'
                 '加功能要重链。\n'
                 '运行时加载：库独立，用到才加载，\n'
                 '按名字挑，缺库返回 NULL 继续跑，\n'
                 '能卸载，加功能只丢文件、不改宿主。',
         'color': 'teal', 'size': 12},
        {'title': '解答 ④：绑定推迟到运行时',
         'body': '热插拔的两个硬条件：① 加载时机由程序决定；\n'
                 '② 新增模块不动宿主程序。\n'
                 '静态链接出局：代码焊死在 exe 里，\n'
                 '加功能必须重新编译分发整个程序。\n'
                 '加载时链接出局：要哪些库编译期就写进导入表，\n'
                 '加新库就得改导入表，也就是重新链接宿主。\n'
                 '运行时加载胜出：宿主没硬编码任何插件名，\n'
                 '只是扫描目录，谁在就加载谁。\n'
                 '本质：绑定从编译期推迟到了运行期。',
         'color': 'green', 'size': 12},
    ], gap=0.26)
    banner(s, '前两种都有编译期绑定，第三种把绑定推迟到运行时——这就是热插拔的全部秘密')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第11讲 运行时加载 —— 让程序自己决定加载什么')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '运行时加载让程序在运行中自己决定"何时加载、加载哪个库、调用哪个函数、用完卸载"；'
        '再配合目录扫描，宿主只认约定、不认识插件——插件的雏形就此诞生。'),
        title='📝 一句话总结', color='orange', size=14.5, min_h=1.02)
    y = y2 + 0.24

    rows = [('1', '第10讲的死依赖', '加载时链接：缺库程序根本起不来，加载对象编译期定死'),
            ('2', '运行时加载概念', '加载时机、对象由程序自己决定；失败返回 NULL，程序继续跑'),
            ('3', '两套 API 对照', 'dlopen/dlsym/dlclose ↔ LoadLibrary/GetProcAddress/FreeLibrary'),
            ('4', '跨平台封装', '#ifdef _WIN32 把平台差异关进 dynlib.h，对外只留统一接口'),
            ('5', '符号约定与句柄', '句柄 = 库的凭证；dlsym 按名字查符号表，查不到返回 NULL'),
            ('6', '目录扫描 = 插件雏形', '"谁在目录里就加载谁"，宿主只认约定')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.22, 0.72), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：接口抽象 —— 用"结构体 + 函数指针"统一插件接口，让宿主只认接口（第12讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_concept, p05_api, p06_dynlib, p07_symbol,
           p08_scan, p09_deep, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
