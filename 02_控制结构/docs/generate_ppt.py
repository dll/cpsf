# -*- coding: utf-8 -*-
"""
第2讲：控制结构 —— 让程序会判断、会循环
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
    BODY_TOP, BODY_BOTTOM, SW, MARGIN_R, TITLE_TOP, fit_size, text_width_in, \
    _put_text, _reg_text, _reg_container, _reset_reg

LECTURE = '第2讲 控制结构'
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


def cards_col(s, x, y, w, specs, gap=0.22):
    """纵向堆叠卡片，返回底部 y。"""
    for sp in specs:
        b, _ = card(s, x, y, w, sp['body'], title=sp.get('title'),
                    color=sp.get('color', 'orange'), size=sp.get('size', 15),
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
    rect(slide, 0, 0, 4.4, SH, fill=C['card_teal'])            # 左侧冷色带
    rect(slide, 0, 0, 0.16, SH, fill=C['teal'])
    rect(slide, 4.4, 0, SW - 4.4, 0.12, fill=C['teal'])

    _put_text(slide, 0.75, 1.15, 3.3, 0.5, '从程序员到架构师', 20, C['teal_dark'], bold=True)
    _put_text(slide, 0.75, 1.72, 3.3, 0.4, 'C语言插件框架演进之旅', 14, C['ink2'])
    rect(slide, 0.75, 2.30, 0.9, 0.05, fill=C['teal'])

    _put_text(slide, 0.75, 2.70, 3.3, 0.5, '第2讲 / 共 14 讲', 18, C['ink2'], bold=True)
    _put_text(slide, 0.75, 5.60, 3.4, 0.9,
              '从一行 printf\n到软件体系的插件框架', 15, C['teal_dark'], bold=True)

    _put_text(slide, 5.35, 2.05, 7.4, 1.5, '控制结构', 72, C['ink'], bold=True)
    _put_text(slide, 5.35, 3.35, 7.4, 0.6, '顺序 · 分支 · 循环', 26, C['teal_dark'])
    rect(slide, 5.35, 4.10, 6.4, 0.03, fill=C['line'])
    _put_text(slide, 5.35, 4.35, 7.2, 1.4,
              '一行 printf 只会从上到下走一遍，\n'
              '现实程序却要"看情况办事、重复干活"。\n'
              '三种基本结构，就是给程序装上判断与循环的骨架。',
              17, C['ink2'], line_spacing=1.5)
    PAGES.append(slide)


# ============================================================
# P2 知识图谱位置
# ============================================================
def p02_map():
    s = pg('知识图谱：本讲站在哪里', '控制结构是表达式与函数之间那道必修的门槛')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '上一讲的表达式，是程序里最小的"砖块"；本讲的控制结构，就是把这些砖块搭成房子的"骨架"。\n'
        '没有骨架，程序只能从上到下走一遍；有了骨架，程序才会看情况办事、才会重复干活。'),
        title='🎯 本讲定位', color='teal', size=16, min_h=1.10)
    y = y2 + 0.22

    items = [('表达式', '第1讲 ✅'), ('控制结构', '← 你在这里'), ('函数', '第3讲'),
             ('模块', '第4讲'), ('库', '第9-10讲'), ('插件', '第11-12讲'), ('框架', '第13-14讲')]
    y = flow(s, MARGIN_L, y, INNER_W, items,
             colors=('teal', 'primary', 'gray', 'gray', 'gray', 'gray', 'gray'),
             size=14, h=0.86) + 0.22

    w = INNER_W / 2 - 0.14
    y3, _ = card(s, MARGIN_L, y, w, '表达式：能算出一个值的代码片段\n本讲直接站在它的肩膀上',
                 title='⬅ 前置', color='blue', size=15, min_h=0.95)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, '函数封装：把逻辑封成名字\n控制结构就是函数体的骨架',
         title='➡ 后续', color='teal', size=15, min_h=0.95)
    footer_note(s, '本讲让程序"会判断、会循环"，为第3讲把逻辑封成函数做准备')
    done('P2')


# ============================================================
# P3 上一讲的痛 → 本讲要解决什么
# ============================================================
def p03_pain():
    s = pg('上一讲的"痛"，本讲要解决什么', '只有顺序结构，程序就只会"一路走到黑"')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                '第1讲：只有顺序结构', [
                    '代码从上到下，一行一行执行',
                    '用户输入不同，也只能走同一条路',
                    '同样的事要重复，只能照抄很多遍',
                    '做完一件事，程序就退出了'],
                '第2讲：补上分支与循环', [
                    '顺序结构保留，作为默认执行方式',
                    '分支结构：if-else / switch 选路径',
                    '循环结构：while / for 重复执行',
                    '程序能停在菜单里，等用户下命令'],
                left_color='red', right_color='green', size=14) + 0.04
    y = cards_row(s, y, [
        {'title': '需求一：看情况办事', 'body': '输入 1 查余额、输入 2 存款\n→ 需要分支结构', 'color': 'blue', 'size': 14},
        {'title': '需求二：重复地干活', 'body': '同一段逻辑要跑很多次\n→ 需要循环结构', 'color': 'teal', 'size': 14},
        {'title': '需求三：别做完就跑', 'body': '交易完回到菜单接着用\n→ 循环里再套分支', 'color': 'purple', 'size': 14},
    ]) + 0.24
    bullets(s, MARGIN_L, y, INNER_W, [
        '一句话：本讲要学的，就是把"看情况"和"重复干"这两件事写进代码',
    ], size=15)
    banner(s, '从"一路走到黑"，到"会拐弯、会转圈"')
    done('P3')


# ============================================================
# P4 什么是控制结构
# ============================================================
def p04_what():
    s = pg('什么是控制结构？', '控制代码"执行顺序"的语法 —— 只有三种基本结构')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '控制结构，就是决定"代码先走哪一行、要不要回头再走"的语法。\n'
        '想象你在开车：一直直行、在岔路口选一条、围着广场绕圈 —— 正好对应三种结构。'),
        title='🚗 一个开车的比喻', color='orange', size=16, min_h=1.10)
    y = y2 + 0.24

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('顺序', '一直往前开\n默认的执行方式'),
        ('分支', '岔路口选一条\n看条件决定走哪'),
        ('循环', '围着广场绕圈\n重复做同一件事'),
    ], colors=('blue', 'purple', 'teal'), size=16, h=1.02) + 0.26

    card(s, MARGIN_L, y, INNER_W, (
        '不管程序多复杂，拆到最后都是这三种结构的组合 —— 这是已经被数学证明过的结论。'),
        title='🧩 一句话结论', color='green', size=15, min_h=0.95)
    banner(s, '顺序 · 分支 · 循环：程序世界的三块乐高积木')
    done('P4')


# ============================================================
# P5 顺序结构
# ============================================================
def p05_seq():
    s = pg('顺序结构：从上到下，一行一行执行', '最基本、也是代码默认的执行方式')
    y = BODY_TOP
    code(s, MARGIN_L, y, INNER_W, [
        'printf("========================================\\n");   // ① 打印上分隔线',
        'printf("       欢迎使用 CCIT ATM 系统\\n");        // ② 打印欢迎语',
        'printf("========================================\\n");   // ③ 打印下分隔线',
        'printf("\\n");                                        // ④ 打印一个空行',
    ], title='顺序结构示例：ATM 欢迎界面（src/atm_menu.c）', size=14)
    y += 4 * 14 * 1.42 / 72 + 0.40 + 0.36 + 0.30

    y = bullets(s, MARGIN_L, y, INNER_W, [
        '四行 printf，谁在前谁先执行，不跳、不回头',
        '这就是"顺序结构"：代码写着什么顺序，就跑什么顺序',
        '它是另外两种结构的"底色"——分支和循环里，每一段仍然是顺序执行',
    ], size=15) + 0.10

    card(s, MARGIN_L, y, INNER_W, (
        '顺序结构不需要任何关键字，它就是"默认"。—— 你写的每一行普通代码，都是顺序结构。'),
        title='💡 记住这一点', color='blue', size=15, min_h=0.95)
    banner(s, '顺序结构是地板：分支和循环，都站在它上面')
    done('P5')


# ============================================================
# P6 分支结构 if-else
# ============================================================
def p06_if():
    s = pg('分支结构：if-else 让程序会判断', '条件为真走一条路，为假走另一条路')
    y = BODY_TOP
    cw = INNER_W * 0.56
    code(s, MARGIN_L, y, cw, [
        'if (amount <= 0) {',
        '    printf("取款金额必须大于0！\\n");',
        '}',
        'else if (amount > balance) {',
        '    printf("余额不足！\\n");',
        '}',
        'else {',
        '    balance = balance - amount;',
        '    printf("取款成功！\\n");',
        '}',
    ], title='取款时的三重判断（src/atm_menu.c）', size=13)
    cards_col(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, [
        {'title': '① 金额 ≤ 0', 'body': '金额不合法\n直接报错', 'color': 'red', 'size': 14},
        {'title': '② 金额 > 余额', 'body': '余额不足\n拒绝取款', 'color': 'orange', 'size': 14},
        {'title': '③ 其他情况', 'body': '正常取款\n余额相应减少', 'color': 'green', 'size': 14},
    ], gap=0.16)
    y += 10 * 13 * 1.42 / 72 + 0.40 + 0.36 + 0.28
    bullets(s, MARGIN_L, y, INNER_W, [
        'if 从上往下逐个判断，谁先为真就进谁的门，后面的分支不再执行',
    ], size=15)
    banner(s, 'if-else 是"万能分支"：范围、组合条件，它都管')
    done('P6')


# ============================================================
# P7 分支结构 switch 与 case 穿透
# ============================================================
def p07_switch():
    s = pg('分支结构：switch 多选一 与 case 穿透', '一个值对应多个选项，比 if-else 更整齐')
    y = BODY_TOP
    cw = INNER_W * 0.58
    code(s, MARGIN_L, y, cw, [
        'switch (choice) {',
        '    case 1:                    // 查询余额',
        '        printf("【查询余额】\\n");',
        '        break;                 // 跳出 switch',
        '    case 2:                    // 存款',
        '        ...',
        '    case 0:                    // 退出',
        '        running = 0;',
        '        break;',
        '    default:                   // 都不匹配',
        '        break;',
        '}',
    ], title='ATM 菜单：一个 choice 对应多个 case', size=12)
    cards_col(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, [
        {'title': '⚠️ break 的作用', 'body': 'break = 跳出 switch，\n不再往下走', 'color': 'red', 'size': 13.5},
        {'title': '⚠️ 忘了 break？', 'body': '会从匹配的 case 一路往下执行，\n这叫"case 穿透"', 'color': 'orange', 'size': 13.5},
    ], gap=0.16)
    y += 12 * 12 * 1.42 / 72 + 0.40 + 0.36 + 0.24
    code(s, MARGIN_L, y, INNER_W, [
        'switch (x) { case 1: printf("A"); case 2: printf("B"); break; }',
        '// 若 x == 1，屏幕输出 "AB" —— 穿透了！每个 case 后面都要记得加 break',
    ], size=12)
    banner(s, 'switch 管"多选一"，但每个 case 后面必须加 break')
    done('P7')


# ============================================================
# P8 循环结构 while / for
# ============================================================
def p08_loop():
    s = pg('循环结构：让代码重复执行', 'while 靠条件驱动 ｜ for 靠计数器驱动')
    y = BODY_TOP
    cw = INNER_W / 2 - 0.14
    code(s, MARGIN_L, y, cw, [
        'int running = 1;',
        'while (running) {',
        '    // 显示菜单 / 读取输入',
        '    // 用户选退出：running = 0;',
        '}',
    ], title='while：条件为真就一直转', size=13)
    code(s, MARGIN_L + cw + 0.28, y, cw, [
        'for (int i = 1; i <= 3; i++) {',
        '    printf("第 %d 次\\n", i);',
        '}',
        '// 初始化；条件；更新 —— 三件套',
    ], title='for：计数器驱动，跑固定次数', size=13)
    y += 5 * 13 * 1.42 / 72 + 0.40 + 0.36 + 0.26

    y = cards_row(s, y, [
        {'title': 'while 适合', 'body': '不知道要跑多少次\n菜单循环、等用户输入', 'color': 'teal', 'size': 14},
        {'title': 'for 适合', 'body': '知道要跑多少次\n计数、遍历 N 个元素', 'color': 'blue', 'size': 14},
        {'title': '共同前提', 'body': '循环条件最终要能变假\n否则就是"死循环"', 'color': 'red', 'size': 14},
    ]) + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        'ATM 主循环：用 running 当开关，用户选"退出"时把它设为 0，循环自然结束',
    ], size=15)
    banner(s, '循环的力量，来自一句"什么时候停下来"')
    done('P8')


# ============================================================
# P9 原理深入：三种结构嵌套 ⭐
# ============================================================
def p09_nest():
    s = pg('原理深入：三种结构如何"嵌套"成程序 ⭐', '大结构套小结构 —— 这就是程序的组织方式')
    y = BODY_TOP
    cw = INNER_W * 0.60
    code(s, MARGIN_L, y, cw, [
        'main()',
        '├─ 顺序：定义 balance / choice / running',
        '├─ 顺序：打印欢迎界面',
        '└─ while (running)        ← 循环',
        '   ├─ 顺序：显示菜单',
        '   ├─ 顺序：读取用户输入',
        '   └─ switch (choice)     ← 分支',
        '      ├─ case 1 查余额（顺序）',
        '      ├─ case 3 取款（再套 if-else）',
        '      └─ case 0 退出（running = 0）',
    ], title='ATM 程序的骨架：循环里套分支，分支里再套顺序', size=12)
    cards_col(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, [
        {'title': '① 最外层', 'body': 'while 循环，\n让菜单反复出现', 'color': 'teal', 'size': 13.5},
        {'title': '② 中间层', 'body': 'switch 分支，\n按选择走不同路', 'color': 'purple', 'size': 13.5},
        {'title': '③ 最内层', 'body': '顺序 + 更小的 if\n处理具体业务', 'color': 'blue', 'size': 13.5},
    ], gap=0.14)
    y += 10 * 12 * 1.42 / 72 + 0.40 + 0.36 + 0.24
    card(s, MARGIN_L, y, INNER_W, (
        'Böhm 和 Jacopini 在 1966 年证明：任何程序都能只用顺序、分支、循环表达出来。\n'
        '所以现代语言都有这三种结构 —— 它们足够表达一切，又足够简单，这就是"结构化程序设计"。'),
        title='📐 结构化程序设计的根基', color='orange', size=14.5)
    banner(s, '三种结构 + 层层嵌套 = 任何复杂程序的全部积木')
    done('P9')


# ============================================================
# P10 对比与辨析
# ============================================================
def p10_compare():
    s = pg('对比与辨析：怎么选对结构？', 'if 还是 switch？while 还是 for？')
    y = BODY_TOP
    y = compare(s, MARGIN_L, y, INNER_W,
                'if-else', ['判断范围：大于、小于、区间',
                            '判断多个条件的组合',
                            '条件各式各样、彼此不同'],
                'switch', ['根据一个值多选一',
                           '选项整齐排列，一目了然',
                           '选项超过 3 个时更清晰'],
                left_color='blue', right_color='purple', size=14) + 0.14
    rows = [('判断范围 / 条件组合', '用 if-else，灵活'),
            ('一个变量多选一（菜单）', '用 switch，整齐'),
            ('不知道要循环多少次', '用 while，条件驱动'),
            ('知道要循环多少次', '用 for，计数器驱动'),
            ('循环条件要能被改变', '否则会死循环，务必检查')]
    y2, _ = kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.46, 0.54), size=14,
                    header=('场景', '推荐用法'))
    y = y2 + 0.22
    bullets(s, MARGIN_L, y, INNER_W, [
        '选哪个的标准只有一条：哪种写法让人更容易看懂',
    ], size=15)
    banner(s, '语法是工具，清晰才是目的')
    done('P10')


# ============================================================
# P11 ATM 实战：本讲源码
# ============================================================
def p11_source():
    s = pg('ATM 实战：本讲源码', 'src/atm_menu.c —— 三种结构在同一份代码里同台')
    y = BODY_TOP
    code(s, MARGIN_L, y, INNER_W, [
        'double balance = 1000.0;   int choice = 0;   int running = 1;   // 变量定义',
        'printf("  欢迎使用 CCIT ATM 系统\\n");        // ① 顺序结构：从上到下',
        'while (running)                              // ② 循环结构：反复显示菜单',
        '{',
        '    scanf("%d", &choice);                    // 读取用户选择',
        '    switch (choice)                          // ③ 分支结构：按 choice 分流',
        '    {',
        '        case 1:  printf("余额为：%.2f 元\\n", balance);  break;   // 查询余额',
        '        case 2:  /* 存款逻辑 */                          break;   // 存款',
        '        case 3:  /* 取款逻辑：里面还有 if-else */         break;   // 取款',
        '        case 0:  running = 0;                           break;   // 退出循环',
        '        default: break;                                          // 其它输入',
        '    }',
        '}',
    ], title='core 骨架（节选自 src/atm_menu.c，完整含注释）', size=12)
    banner(s, '一份 main，把顺序、分支、循环三种结构全用上了')
    done('P11')


# ============================================================
# P12 运行演示
# ============================================================
def p12_run():
    s = pg('运行演示：真实编译与运行', '编译命令、菜单交互、退出码 —— 全部来自真实运行')
    y = BODY_TOP
    cw = INNER_W * 0.55
    code(s, MARGIN_L, y, cw, [
        '$ gcc -Wall atm_menu.c -o atm_menu.exe',
        '$ ./atm_menu.exe',
        '========================================',
        '       欢迎使用 CCIT ATM 系统',
        '========================================',
        '-------- 主菜单 --------',
        '  1. 查询余额    2. 存款    3. 取款',
        '请输入您的选择：1',
        '【查询余额】',
        '您当前的账户余额为：1000.00 元',
        '请输入您的选择：0',
        '感谢使用 CCIT ATM 系统，再见！',
        '$ echo $?',
        '0',
    ], title='终端实录（真实输出）', size=11.5)
    card(s, MARGIN_L + cw + 0.26, y, INNER_W - cw - 0.26, (
        '① 编译期：gcc -Wall 检查语法，有错就停在这步\n'
        '② 运行期：菜单反复出现 —— 循环在起作用\n'
        '③ 输入 1：只走查询那条路 —— 分支在起作用\n'
        '④ 输入 0：running 置 0，循环结束\n'
        '⑤ 退出码 0：程序正常结束'),
        title='👀 要看清楚的五个点', color='orange', size=13.5, min_h=3.40)
    y += 14 * 11.5 * 1.42 / 72 + 0.40 + 0.36 + 0.26
    bullets(s, MARGIN_L, y, INNER_W, [
        '片尾会放一段真实的编译 + 运行演示动画：命令怎么敲、菜单怎么转、退出码怎么读',
    ], size=15)
    banner(s, '看得见的运行结果，是最好的老师')
    done('P12')


# ============================================================
# P13 本讲在主线上的位置 ⭐
# ============================================================
def p13_ladder():
    s = pg('本讲在主线上的位置 ⭐', '控制结构，是"函数体的骨架"')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '六级台阶：表达式 → 函数 → 模块 → 库 → 插件 → 框架。\n'
        '本讲落在"函数"这一级的前面 —— 函数体里写的，正是顺序、分支、循环这些控制结构。'),
        title='🧭 一条主线', color='orange', size=15.5, min_h=1.05)
    y = y2 + 0.22

    y = flow(s, MARGIN_L, y, INNER_W, [
        ('① 表达式', '第1讲 ✅'),
        ('② 函数', '本讲为它铺路'),
        ('③ 模块', '第4讲'),
        ('④ 库', '第9-10讲'),
        ('⑤ 插件', '第11-12讲'),
        ('⑥ 框架', '第13-14讲'),
    ], colors=('teal', 'primary', 'gray', 'gray', 'gray', 'gray'),
        size=14, h=1.05) + 0.24

    w = INNER_W / 2 - 0.14
    cards_col(s, MARGIN_L, y, w, [
        {'title': '本讲贡献了什么', 'body': '让程序会判断、会循环\n有了骨架，逻辑才装得进函数', 'color': 'teal', 'size': 14},
    ], gap=0.0)
    card(s, MARGIN_L + INNER_W / 2 + 0.14, y, w, (
        '第3讲把今天这三段逻辑封成\n独立的函数，重复的代码就能只写一遍'),
        title='下一讲接着做什么', color='blue', size=14)
    banner(s, '本讲让程序会判断、会循环，为第3讲把逻辑封成函数做准备')
    done('P13')


# ============================================================
# P14 思考题 ①②
# ============================================================
def p14_q12():
    s = pg('思考题 ①②', '先自己想，再看下一页的参考解答')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '我们已经学了顺序、分支、循环三种结构。ATM 程序里，它们并不是各管一段，而是层层套在一起：\n'
        '最外层是 while，里面是 switch，switch 的某个 case 里又藏着 if-else。\n'
        '想一想：为什么"只用三种结构"就能拼出任意复杂的程序？这种嵌套，到底解决了一个什么问题？'),
        title='思考题 ①：为什么三种结构"够用"？', color='orange', size=15, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '在 switch 里，如果某个 case 忘写 break，程序会从匹配处一直往下执行，直到遇到 break —— 这叫"case 穿透"。\n'
        '有人说它是设计缺陷，有人说它能被巧妙利用。\n'
        '提示：想想多个 case 能不能共用同一段代码；再想想，忘了写 break 时，这个 bug 好不好查？'),
        title='思考题 ②：case 穿透，是 bug 还是特性？', color='purple', size=15, min_h=1.55)
    banner(s, '带着问题翻页，比直接看答案收获大得多')
    done('P14')


# ============================================================
# P15 思考题 ①② 参考解答
# ============================================================
def p15_a12():
    s = pg('思考题 ①② 参考解答', '看看你的思路和参考答案差在哪')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ①：结构少，但可以嵌套',
         'body': '顺序、分支、循环是三种"原子"，\n'
                 '嵌套就是"原子套原子"，组合无限\n'
                 'ATM：while 里 switch，switch 里 if\n'
                 '这是 Böhm-Jacopini 定理的结论：\n'
                 '三种结构足以表达一切计算逻辑\n'
                 '把它们拆开，任何程序都不会更复杂',
         'color': 'orange', 'size': 13},
        {'title': '解答 ②：弊大于利的"历史特性"',
         'body': '能用：多个 case 共用一段代码\n'
                 '（case 1: case 2: 同一句 break;）\n'
                 '是坑：99% 是忘了写 break，很难查\n'
                 'Java / C# / Go 都已禁止隐式穿透\n'
                 '结论：除非明确要用穿透，\n'
                 '否则每个 case 后面都要加 break',
         'color': 'purple', 'size': 13},
    ], gap=0.26)
    banner(s, '简单规则 + 层层嵌套 = 复杂而清晰的程序')
    done('P15')


# ============================================================
# P16 思考题 ③④
# ============================================================
def p16_q34():
    s = pg('思考题 ③④', '两题进阶：从循环的边界，接到结构化思想')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '循环能不能停下来，全看循环条件会不会从"真"变成"假"。ATM 里是用户选了退出，把 running 设成 0。\n'
        '如果条件永远为真，程序就会一直转下去 —— 这就是"死循环"。\n'
        '提示：想一想 while (1) 什么时候不算 bug？循环变量忘了更新会怎样？怎么快速判断一个循环会不会停？'),
        title='思考题 ③：循环靠什么结束？死循环怎么来的？', color='teal', size=15, min_h=1.55)
    y = y2 + 0.26
    card(s, MARGIN_L, y, INNER_W, (
        '我们常说"顺序、分支、循环是程序的三种基本结构"，这句话其实来自一个数学结论，而不是经验总结。\n'
        '它是谁、在哪一年证明的？为什么当年的 goto 语句会引起那么大的争论？\n'
        '提示：这个思想，和我们后面要学的函数、模块、分层架构，是不是一脉相承？'),
        title='思考题 ④：结构化程序设计，是谁提出来的？', color='green', size=15, min_h=1.55)
    banner(s, '这两题想通了，第3讲函数封装就提前入门了')
    done('P16')


# ============================================================
# P17 思考题 ③④ 参考解答
# ============================================================
def p17_a34():
    s = pg('思考题 ③④ 参考解答', '把今天的"循环"和"结构化"，接到后面的函数与架构')
    y = BODY_TOP
    cards_row(s, y, [
        {'title': '解答 ③：条件是唯一的刹车',
         'body': 'while / for 都要"条件最终变假"\n'
                 'for：忘写 i++，i 永远小于上限 → 死循环\n'
                 'while：忘改循环变量 → 条件永远为真\n'
                 '排查法：盯住"条件里的变量"在哪里被改\n'
                 'while (1) 不算 bug：当循环里一定有\n'
                 'break / return 或退出条件时，它是惯用法',
         'color': 'teal', 'size': 13},
        {'title': '解答 ④：一次数学证明，一场范式革命',
         'body': 'Böhm 与 Jacopini，1966 年证明：\n'
                 '任何程序都可用顺序、分支、循环表达\n'
                 '1968 年 Dijkstra 发表《goto 有害论》，\n'
                 '推动"结构化程序设计"普及\n'
                 '与架构的关系：本质是"执行路径要清晰"\n'
                 '函数、模块、分层，都是更高层的结构化',
         'color': 'green', 'size': 13},
    ], gap=0.26)
    banner(s, '越往上层走，越是在"结构化"——只是结构越来越大')
    done('P17')


# ============================================================
# P18 小结与预告
# ============================================================
def p18_summary():
    s = pg('小结与预告', '第2讲 控制结构 —— 让程序会判断、会循环')
    y = BODY_TOP
    y2, _ = card(s, MARGIN_L, y, INNER_W, (
        '顺序让代码跑起来，分支让代码有选择，循环让代码有力量；三种结构层层嵌套，就能搭出任何程序。'),
        title='📝 一句话总结', color='orange', size=15)
    y = y2 + 0.24

    rows = [('1', '顺序结构', '从上到下，一行一行执行，不需要关键字'),
            ('2', 'if-else 分支', '灵活的条件判断，适合范围与条件组合'),
            ('3', 'switch 分支', '简洁的多选一，每个 case 后面记得加 break'),
            ('4', 'while 循环', '不知道次数时用，条件驱动，注意别死循环'),
            ('5', 'for 循环', '知道次数时用，计数器驱动，注意更新变量'),
            ('6', '嵌套与结构化', '三种结构嵌套组合，可表达一切程序（Böhm-Jacopini）')]
    kv_rows(s, MARGIN_L, y, INNER_W, rows, widths=(0.06, 0.20, 0.74), size=13,
            header=('#', '知识点', '关键句'))
    banner(s, '下一讲：函数封装 —— 让代码有名字、能复用（第3讲）')
    done('P18')


for fn in (p01_cover, p02_map, p03_pain, p04_what, p05_seq, p06_if, p07_switch,
           p08_loop, p09_nest, p10_compare, p11_source, p12_run, p13_ladder,
           p14_q12, p15_a12, p16_q34, p17_a34, p18_summary):
    fn()

out = os.path.join(HERE, '课件.pptx')
save(prs, out)
print('共 %d 页（封面 1 页 + 正文 17 页）' % len(prs.slides._sldIdLst))
