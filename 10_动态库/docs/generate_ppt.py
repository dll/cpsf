# -*- coding: utf-8 -*-
"""
第10讲：动态库 —— 让多个程序共享同一份代码
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

LECTURE = '第10讲 动态库'
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

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第10讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.30, 3.4, 1.2,
              '从一行 printf\n到软件体系的插件框架', 15, C['primary_dark'], bold=True)

    _put_text(slide, 5.35, 1.95, 7.4, 1.5, '动态库', 66, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.20, 7.4, 0.6, '让多个程序共享同一份代码', 27, C['primary_dark'])
    rect(slide, 5.35, 3.95, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.20, 7.2, 1.6,
              '第9讲把模块打包成静态库，解决了"散装分发"，\n'
              '但代码被"复制"进了每个程序：磁盘占三份、内存占三份、\n'
              '改一个 bug 要重新链接所有程序。本讲让库"独立成文件"，\n'
              'exe 里只留一张导入表，运行时由操作系统加载共享。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)
    done('P1')


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '六级台阶的第四级 —— 库：从"代码复制"走向"代码共享"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '前九讲一路往上搭：表达式、函数、模块，再到静态库。本讲仍在"库"这一级台阶上，'
        '但换了一种打包方式——静态库把代码复制进每个程序，动态库让所有程序共享同一份二进制。'),
        title='🎯 本讲定位', color='orange', size=15.5, min_h=1.10)
    y = y2 + 0.22

    items = [('① 表达式', '第1讲 ✅'), ('② 函数', '第3讲 ✅'), ('③ 模块', '第4讲 ✅'),
             ('④ 库', '← 你在这里'), ('⑤ 插件', '第11-12讲'), ('⑥ 框架', '第13讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('gray', 'gray', 'gray', 'primary', 'gray', 'gray'),
             size=14, h=0.90) + 0.24

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, (
        '第9讲：静态库用 ar rcs 打包 .o，\n'
        '链接时把代码复制进 exe —— 能分发，但三份浪费。'),
        title='⬅ 前置', color='blue', size=14.5, min_h=1.00)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第11讲：运行时加载 dlopen / LoadLibrary，\n'
        '把加载时机从"启动时"推迟到"运行中"，插件就此萌芽。'),
        title='➡ 后续', color='teal', size=14.5, min_h=1.00)
    banner(s, '本讲只做一件事：把库从"复制"改成"共享"——一份代码，大家共用')
    done('P2')


# ============================================================
# P3 上一讲的"痛" → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '静态库解决了打包，却留下"代码复制"的三个后患')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第9讲：静态库已经做到', [
                    'ar rcs 把 account.o / transaction.o 打包成一个文件',
                    '链接时复制目标文件进 exe，运行期不依赖外部文件',
                    '函数天然可见，不需要任何导出宏'],
                '第9讲：留下的三个后患', [
                    '体积大：每个 exe 各含一份库代码，磁盘上 N 份副本',
                    '内存浪费：多进程各自持有一份，物理内存 N 份',
                    '更新麻烦：库修了 bug，所有用过它的程序都要重新链接'],
                left_color='blue', right_color='red', size=14) + 0.06
    y = cards_row(s, y, [
        {'title': '痛点一：体积大', 'body': '10 个程序共用一个 5MB 的库\n磁盘上就多占 45MB 冗余',
         'color': 'red', 'size': 13},
        {'title': '痛点二：内存浪费', 'body': '3 个进程同时跑\n物理内存里是 3 份函数机器码',
         'color': 'yellow', 'size': 13},
        {'title': '痛点三：更新麻烦', 'body': '库修一个 bug\n要把所有程序重新链接一遍',
         'color': 'purple', 'size': 13},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '根因只有一个：链接器把库的代码"复制"到了每个程序里',
    ], size=15)
    banner(s, '本讲把"复制"改成"共享"：库独立成文件，程序共用同一份')
    done('P3')


# ============================================================
# P4 核心内容一：什么是动态库
# ============================================================
def p04_concept():
    s = pg('什么是动态库：独立成文件，运行时加载', '动态库本体 / 导入库 / 导出符号 —— 三个必须分清的概念')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '动态库 = 把多个目标文件链接成一个独立二进制文件，由操作系统在运行时加载、多进程共享。'),
        title='📌 一句话定义', color='orange', size=15, min_h=0.92)
    y = y2 + 0.20

    y = kv_rows(s, MARGIN_L, y, INNER_W, [
        ('Linux', 'libaccount.so', 'so = shared object'),
        ('Windows', 'account.dll', 'dll = dynamic link library'),
        ('macOS', 'libaccount.dylib', 'dylib = dynamic library'),
    ], widths=(0.16, 0.30, 0.54), size=12,
        header=('平台', '动态库文件名', '含义'))[0] + 0.22

    cards_row(s, y, [
        {'title': '动态库本体', 'body': '提供真正的函数机器码\n运行时被映射进进程', 'color': 'orange', 'size': 13},
        {'title': '导入库', 'body': '只有"符号归属"的通讯录\n本身不含代码，链接时用', 'color': 'teal', 'size': 13},
        {'title': '导出符号', 'body': '显式声明哪些函数可被外部调用\n由 ACCOUNT_API 宏标记', 'color': 'blue', 'size': 13},
    ])
    banner(s, '链接时连的是导入库（几 KB 的通讯录），运行时加载的是动态库本体')
    done('P4')


# ============================================================
# P5 核心内容二：编译动态库
# ============================================================
def p05_build():
    s = pg('编译动态库：-fPIC -shared', 'Linux 与 Windows(MinGW) 两套写法，做的事情完全一样')
    y = BODY_TOP
    y = cards_row(s, y, [
        {'title': '-fPIC 位置无关代码', 'body': '库被映射到地址空间的任意位置\n代码不能假设自己的绝对地址',
         'color': 'blue', 'size': 13},
        {'title': '-shared 生成共享库', 'body': '告诉编译器：产物是动态库\n而不是一个可执行文件',
         'color': 'teal', 'size': 13},
    ]) + 0.24

    code(s, MARGIN_L, y, INNER_W, [
        '# Linux：一次编译出 libaccount.so（.so 自带完整符号表，无需导入库）',
        'gcc -Wall -Wextra -fPIC -shared -o libaccount.so account.c transaction.c',
        'gcc -Wall -Wextra -o atm_dynamic main.c -L. -laccount -Wl,-rpath,\'$ORIGIN\'',
        '',
        '# Windows / MinGW：一次编译出 account.dll + 导入库 libaccount.dll.a',
        'gcc -Wall -Wextra -shared -o account.dll account.c transaction.c \\',
        '    -Wl,--out-implib,libaccount.dll.a -DACCOUNT_EXPORTS -DTRANSACTION_EXPORTS',
        'gcc -Wall -Wextra -o atm_dynamic.exe main.c -L. -laccount',
        '',
        '# -DACCOUNT_EXPORTS 让 ACCOUNT_API 展开为 dllexport（导出）',
        '# 不加这个宏编译主程序时，它展开为 dllimport（导入）',
    ], title='build.bat / Makefile 的核心两行', size=11)
    banner(s, 'Linux 一条 -fPIC -shared 就够；MinGW 还要多产一个导入库给链接器用')
    done('P5')


# ============================================================
# P6 核心内容三：加载时链接 —— 链接期
# ============================================================
def p06_iat():
    s = pg('加载时链接：exe 里只有一张导入表', '链接器不复制任何库代码，只留下"欠条清单" IAT')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '动态链接时链接器很"抠门"：它只检查"哪些符号还没定义"，'
        '然后在 exe 里登记一条"我叫过 account_create，它在 account.dll 里"——这就是导入表 IAT。'),
        title='💡 链接器到底做了什么', color='teal', size=14.5, min_h=1.05)
    y = y2 + 0.22

    cw = INNER_W * 0.60
    code(s, MARGIN_L, y, cw, [
        '链接时：链接器只看"有哪些符号没定义"',
        'main.o ──────────┐',
        '                 ├──► 链接器 ──► atm_dynamic.exe',
        'libaccount.dll.a ┘',
        '  ┌──────────────────────────────┐',
        '  │ main() 的机器码                │',
        '  ├──────────────────────────────┤',
        '  │ 导入表 IAT（欠条清单）          │',
        '  │  account_create      → ???    │',
        '  │  transaction_transfer → ???   │',
        '  └──────────────────────────────┘',
    ], title='atm_dynamic.exe 的内部结构', size=11)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    card(s, xr, y, wr, (
        'exe 里没有 account_create 的机器码，\n'
        '只有一张"符号名 → 地址未知"的导入表；\n'
        '地址留给 OS 加载器，启动时才回填。'),
        title='🔑 三个要点', color='orange', size=13, min_h=1.50)
    banner(s, '导入表 IAT = 一张欠条清单：先记下欠谁，运行时再还')
    done('P6')


# ============================================================
# P7 核心内容四：加载时链接 —— 运行期
# ============================================================
def p07_loader():
    s = pg('启动时：操作系统加载器来"还债"', '五个步骤，把库映射进进程并回填地址')
    y = BODY_TOP
    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 映射 exe', '读进新进程\n地址空间'),
        ('② 读导入表', '发现需要\naccount.dll'),
        ('③ 映射 dll', '只读映射进\n同一进程'),
        ('④ 回填 IAT', '真实地址写进导入表'),
        ('⑤ 跳到 main', '开始执行\nmain 函数'),
    ], colors=('blue', 'teal', 'green', 'orange', 'purple'), size=14, h=1.05) + 0.26

    cw = INNER_W * 0.58
    code(s, MARGIN_L, y, cw, [
        '内存视图（三个进程共用一份代码）',
        '',
        '进程A ─┐',
        '进程B ─┼── 虚拟地址各不相同',
        '进程C ─┘   但都指向同一份物理内存',
        '',
        '   [ account.dll 代码段 ]  只读 → 物理内存只有 1 份',
        '   [ 数据段 accounts[]  ]  可写 → 每个进程各 1 份',
        '   共享只读代码省内存，可写数据独立互不干扰',
    ], title='地址空间与物理内存', size=11)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    card(s, xr, y, wr, (
        '共享的是"代码段"（只读，函数机器码不会变，共享无害且省内存）。\n'
        '全局变量 accounts[] 在可写数据段，每个进程各有一份独立副本，'
        '进程 A 给张三加钱，进程 B 的账本不受影响。'),
        title='⚖️ 共享什么，不共享什么', color='orange', size=13, min_h=2.30)
    banner(s, '共享只读代码段省内存；可写数据各自独立——这正是动态库的"共享"能成立的边界')
    done('P7')


# ============================================================
# P8 核心内容五：优缺点与常见坑
# ============================================================
def p08_proscons():
    s = pg('动态库的优缺点与常见坑', '共享省资源，代价是"运行时依赖"和"DLL Hell"')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '优点', [
                    '节省磁盘：全系统只有一份库文件',
                    '节省内存：代码段只读共享，物理内存一份',
                    '便于更新：替换库文件即可，程序无需重链'],
                '缺点', [
                    '运行时依赖：缺 dll/so，程序直接启动不了',
                    'DLL Hell：同一 dll 多版本互相覆盖',
                    '加载开销与调试：启动要重定位，崩溃点可能在库里'],
                left_color='green', right_color='red', size=13.5) + 0.14

    y = cards_row(s, y, [
        {'title': '坑一：缺库起不来', 'body': '把 account.dll 改名\n程序在启动阶段就报错终止',
         'color': 'red', 'size': 12.5},
        {'title': '坑二：DLL Hell', 'body': 'A 要 v1、B 要 v2\n系统却只能留一份',
         'color': 'yellow', 'size': 12.5},
        {'title': '价值：可单独换库', 'body': '只重编 account.dll\n旧 exe 直接生效，无需重链',
         'color': 'green', 'size': 12.5},
    ]) + 0.20
    bullets(s, MARGIN_L, y, INNER_W, [
        '适合：大型系统、多程序共享基础库、插件架构；不适合：单文件小工具、嵌入式裸机',
    ], size=14)
    banner(s, '缺库是"启动失败"而不是"功能失效"——这是动态库最典型的行为特征')
    done('P8')


# ============================================================
# P9 原理深入：代码段只读共享 ⭐
# ============================================================
def p09_share():
    s = pg('原理深入：为什么能省内存？ ⭐', '代码段只读 → 可共享映射；数据段可写 → 每进程独立')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '操作系统把库的只读代码段共享映射给多个进程，可写数据段则用写时复制作各进程独立副本。'),
        title='🧭 一句话原理', color='blue', size=14.5, min_h=1.05)
    y = y2 + 0.22

    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        '同一份 account.dll，三份不同的地址空间：',
        '',
        '        虚拟地址      物理内存',
        '进程A ── 0x7F00 ──┐',
        '进程B ── 0x9A00 ──┼──► [ 代码段 ] 只有 1 份',
        '进程C ── 0xB400 ──┘     （只读、可共享）',
        '',
        '        虚拟地址      物理内存',
        '进程A ── 0x7F10 ──► [ 数据段 A ] 一份',
        '进程B ── 0x9A10 ──► [ 数据段 B ] 一份',
        '进程C ── 0xB410 ──► [ 数据段 C ] 一份',
    ], title='代码共享 vs 数据独立', size=11)

    cards_col(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, [
        {'title': '只读 → 敢共享', 'body': '函数机器码永不改变，多进程指向同一份物理页零风险', 'color': 'green', 'size': 12.5},
        {'title': '可写 → 必须独立', 'body': '若共享，A 改余额会污染 B 的账本，绝不可接受', 'color': 'red', 'size': 12.5},
        {'title': '这就是省内存的来源', 'body': '10 个进程跑同一库，代码段内存仍只有 1 份', 'color': 'orange', 'size': 12.5},
    ], gap=0.14)
    banner(s, '"共享代码、隔离数据"——一条边界，同时解释了省内存和进程互不干扰')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：静态库 vs 动态库', '从打包、链接、运行到更新，逐项对照')
    y = BODY_TOP
    rows = [
        ('打包工具', 'ar rcs 把 .o 打包成 .a', 'gcc -shared 直接产出 .dll/.so'),
        ('链接产物', 'exe 内含库代码', 'exe 内只有导入表 IAT'),
        ('运行时依赖', '无，已内置', '必须有库文件，缺了起不来'),
        ('磁盘占用', '每程序一份（大）', '全系统一份（小）'),
        ('内存占用', '每进程一份', '多进程共享只读代码段'),
        ('启动速度', '快（无加载开销）', '稍慢（要加载 + 重定位 + 回填）'),
        ('库更新', '全部程序重新链接', '替换库文件即可，下次启动生效'),
        ('版本冲突', '无（各自一份）', '有（DLL Hell）'),
        ('典型使用者', '小工具、嵌入式裸机', '系统级库、插件、大型软件'),
    ]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.20, 0.40, 0.40), size=12,
            header=('对比项', '静态库 .a / .lib', '动态库 .so / .dll'))
    banner(s, '一句话记忆：静态库是"复制"，动态库是"共享"')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/account.h 的导出宏 + src/main.c —— 主程序和静态库版几乎一样')
    y = BODY_TOP
    cw = INNER_W * 0.54
    code(s, MARGIN_L, y, cw, [
        '/* account.h —— 导出/导入宏（本讲第一个新知识点） */',
        '#if defined(_WIN32) || defined(_MSC_VER)',
        '    #ifdef ACCOUNT_EXPORTS',
        '        #define ACCOUNT_API __declspec(dllexport)',
        '    #else',
        '        #define ACCOUNT_API __declspec(dllimport)',
        '    #endif',
        '#else',
        '    #define ACCOUNT_API __attribute__((visibility("default")))',
        '#endif',
        'ACCOUNT_API int account_create(const char *name, double bal);',
    ], title='account.h：显式标记哪些函数要导出', size=10.5)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    code(s, xr, y, wr, [
        '/* main.c —— 调用方式与静态库版完全一致 */',
        '#include "account.h"',
        '#include "transaction.h"',
        'int main(void) {',
        '    id1 = account_create("张三", 1000.0);',
        '    transaction_deposit(id1, 500.0);',
        '    transaction_transfer(id1, id3, 300.0);',
        '    account_list_all();',
        '    return 0;',
        '}',
    ], title='main.c：源码几乎没变，变的只是链接方式', size=10.5)

    y2 = y + 11 * 10.5 * 1.42 / 72 + 0.40 + 0.36 + 0.22
    card(s, MARGIN_L, y2, INNER_W, (
        '内部数据与辅助函数用 static 修饰，不会进入导出表——'
        'objdump -p account.dll 只能看到 11 个 account_* / transaction_* 符号，'
        'log_transaction 和 accounts[] 都查不到。'),
        title='🔒 导出是"显式许可"：没标记的符号外部拿不到', color='orange', size=13)
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '编译命令、账户列表、依赖查询、退出码 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.62
    code(s, MARGIN_L, y, cw, [
        '$ gcc -shared -o account.dll account.c transaction.c \\',
        '      -Wl,--out-implib,libaccount.dll.a \\',
        '      -DACCOUNT_EXPORTS -DTRANSACTION_EXPORTS',
        '$ gcc -Wall -Wextra -o atm_dynamic.exe main.c -L. -laccount',
        "$ printf '6\\n0\\n' | ./atm_dynamic.exe",
        '=== ATM动态库版初始化 ===',
        '[开户] ID:1001  户名:张三  余额:1000.00',
        '[转账] 1001 -> 1003  金额:300.00',
        '======== 账户列表 ========',
        '1001     张三               1200.00      活跃',
        '1002     李四               1800.00      活跃',
        '1003     王五               800.00       活跃',
        '总计: 3 个账户',
        '$ objdump -p atm_dynamic.exe | grep "DLL Name"',
        '        DLL Name: account.dll',
        '$ echo $?',
        '0',
    ], title='终端实录（真实输出，未删改）', size=11)

    xr = MARGIN_L + cw + 0.26
    wr = INNER_W - cw - 0.26
    card(s, xr, y, wr, (
        '① 编译一次产出 dll + 导入库\n'
        '② 链接只连导入库，exe 内无库代码\n'
        '③ 开户、转账、列表都来自 account.dll\n'
        '④ exe 只登记了一条 account.dll 依赖\n'
        '⑤ 改名 account.dll → 程序启动即失败\n'
        '⑥ 只重编 account.dll → 旧 exe 立即生效'),
        title='👀 要看清楚的六个点', color='orange', size=12, min_h=4.05)
    banner(s, '片尾有真实运行演示动画，右侧并列展示 account.h / main.c')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '六级台阶的第四级：库 —— 从"复制"到"共享"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。本讲站在第四级"库"上：'
        '静态库让代码能被打包复用，动态库让同一份代码被所有程序共享——'
        '库这一级的两条腿，到这里才站稳。'),
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
    card(s, MARGIN_L, y, w, (
        '静态库解决"可分发"，动态库解决"可共享"；\n'
        'exe 里只留导入表，OS 启动时映射并回填；\n'
        '库能单独升级——这条能力直接喂给了插件。'),
        title='本讲为终点贡献了什么', color='teal', size=13.5, min_h=1.55)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第11讲把"加载时机"从启动推迟到运行中：\n'
        '用到才加载、按名字找函数、用完卸载，\n'
        '再配合目录扫描，插件雏形就此诞生。'),
        title='下一讲接着做什么', color='blue', size=13.5, min_h=1.55)
    banner(s, '库把代码复用了，插件让复用发生在运行中——主线正走向"控制反转"')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '静态库有三个痛点：体积大、内存浪费、更新麻烦。请分别说明每个痛点产生的原因，'
        '以及动态库究竟是怎么解决的。\n'
        '提示：三个痛点的共同根因是同一个动作——"复制"。想清楚动态库在哪里、'
        '用什么手段避开了这个动作。'),
        title='思考题 ①：三个痛点与动态库的解法', color='orange', size=14.5, min_h=1.58)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        'Windows/MinGW 下编译动态库时，-Wl,--out-implib,libaccount.dll.a 是做什么的？'
        '为什么链接主程序时连的是 libaccount.dll.a，而不是 account.dll？\n'
        '提示：链接发生在"编译期"，那时程序还没运行。链接器生成导入表，'
        '需要的到底是"符号索引"还是"函数机器码"？'),
        title='思考题 ②：导入库为什么不是动态库本体？', color='purple', size=14.5, min_h=1.58)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：复制 → 共享',
         'body': '体积大：静态链接把目标文件复制进每个 exe，\n'
                 'N 个程序就 N 份；动态库磁盘只留一份\n'
                 '内存浪费：静态代码各进程独立，N 份内存；\n'
                 '动态库代码段只读，多进程共享同一份物理页\n'
                 '更新麻烦：静态代码已焊死在 exe 里，\n'
                 '修 bug 要重链所有程序；动态库只换库文件\n'
                 '一句话：三个痛点的根因都是"复制"，\n'
                 '动态库用一个字破解——"共享"',
         'color': 'orange', 'size': 12},
        {'title': '解答 ②：链接期不需要机器码',
         'body': '该选项让链接器额外产出一个"导入库"。\n'
                 '导入库很小，不含函数代码，\n'
                 '只记录"哪些符号由哪个 dll 提供"的通讯录。\n'
                 '链接主程序时，链接器只需知道 account_create\n'
                 '等符号的归属，就能生成导入表 IAT，\n'
                 '根本不需要函数机器码，也无需把 dll 装进 exe。\n'
                 '真正加载 account.dll 是运行时 OS 加载器的事；\n'
                 'Linux 的 .so 自带完整符号表，所以无需导入库。',
         'color': 'purple', 'size': 12},
    ], gap=0.26)
    banner(s, '把"编译期"和"运行期"分开看，两个问题都会迎刃而解')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从进程内存，接到"缺库"与"换库"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        'account.c 里有一个 static Account accounts[MAX_ACCOUNTS]; 数组。当两个进程 A 和 B '
        '都加载了同一个 account.dll：①代码和数据在物理内存各有几份？②A 新增账户 B 能看到吗？'
        '③为什么"代码段共享、数据段不共享"是合理的？'),
        title='思考题 ③：两个进程共享同一个 dll', color='teal', size=14.5, min_h=1.58)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '把 account.dll 从目录移走，atm_dynamic.exe 会怎样？请对比"动态链接失败"与'
        '"静态链接"在程序行为上的差异，并解释为什么动态库更新后程序无需重链就能用上新版本。\n'
        '提示：注意区分"启动失败"与"运行后功能失效"这两种完全不同的失败方式。'),
        title='思考题 ④：缺库的后果与免重链的理由', color='green', size=14.5, min_h=1.58)
    banner(s, '想通这两题，你就真正理解"加载时链接"了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '从"共享什么"接到本讲最实用的价值')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：代码一份，数据两份',
         'body': '代码段只读，物理内存只有一份被共享；\n'
                 '数据段可写（accounts[]、next_id 等），\n'
                 'OS 用写时复制作给每进程独立副本。\n'
                 'A 新增账户，B 完全看不到——\n'
                 '两者操作的是各自地址空间里的独立数组。\n'
                 '合理且必需：只读共享无害又省内存；\n'
                 '可写若共享，A 加钱会改到 B 的账本，\n'
                 '绝不可接受。共享数据必须显式用 IPC。',
         'color': 'teal', 'size': 12},
        {'title': '解答 ④：启动失败，但可单独换库',
         'body': '移走 dll 后程序在"启动阶段"就失败：\n'
                 'Windows 报找不到模块，Linux 报加载共享库失败。\n'
                 '不是跑起来后功能失效，而是根本启动不了。\n'
                 '对比：静态链接删掉库照样跑；\n'
                 '动态链接删掉库就起不来。\n'
                 '免重链的原因：exe 里没有库代码，\n'
                 '只有"符号名→地址未知"的导入表；\n'
                 '每次启动 OS 都重新加载当时的库，\n'
                 '把新版函数地址填进 IAT，自然用上新代码。',
         'color': 'green', 'size': 12},
    ], gap=0.26)
    banner(s, '"启动时加载"是限制，也是可单独升级的来源——下一讲把时机再往后推')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第10讲 动态库 —— 让多个程序共享同一份代码')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '库代码放进独立的 .dll/.so，exe 里只留一张导入表；'
        '启动时 OS 把库映射进进程，多进程共享同一份只读代码段——'
        '磁盘和内存双省，还能单独更新库。'),
        title='📝 一句话总结', color='orange', size=14.5, min_h=0.98)
    y = y2 + 0.24

    rows = [('1', '静态库三痛点', '体积大、内存浪费、更新麻烦——根因是"代码复制"'),
            ('2', '动态库概念', '库代码独立成 .dll/.so，运行时加载共享'),
            ('3', '导出宏', 'ACCOUNT_API / TRANSACTION_API，编译库时展开为 dllexport'),
            ('4', '编译命令', 'Linux 用 -fPIC -shared；Windows -shared + 生成导入库'),
            ('5', '加载时链接', 'exe 里只有 IAT，OS 启动时映射库并回填地址'),
            ('6', '共享机制', '代码段只读共享省内存，数据段每进程独立')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=12,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：运行时加载 —— 用 dlopen / LoadLibrary 在运行中打开库、查找函数（第11讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_concept, p05_build, p06_iat, p07_loader,
           p08_proscons, p09_share, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页），全部通过质检' % len(prs.slides._sldIdLst))
