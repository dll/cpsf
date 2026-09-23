# -*- coding: utf-8 -*-
"""
第5讲：指针 — 用PIL渲染幻灯片图片
匹配系列风格：明亮暖色调、轻松愉快
"""
from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1280, 720
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_work", "images")
os.makedirs(OUT_DIR, exist_ok=True)

# 配色
BG = (247, 249, 252)
TITLE_BAR = (255, 140, 66)
TEXT_DARK = (44, 62, 80)
TEXT_LIGHT = (127, 140, 141)
ACCENT = (78, 205, 196)
RED = (255, 107, 107)
YELLOW = (255, 217, 61)
GREEN = (107, 203, 119)
BLUE = (116, 185, 255)
PURPLE = (162, 155, 254)
CODE_BG = (30, 41, 59)
CODE_FG = (200, 210, 230)

# 字体
def get_font(size, bold=False):
    paths = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_bg(img, draw):
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=BG)
    draw.rectangle([0, 0, WIDTH, 8], fill=TITLE_BAR)

def draw_title(draw, text, y=40):
    font = get_font(36, bold=True)
    draw.text((60, y), text, fill=TITLE_BAR, font=font)
    return y + 50

def draw_text(draw, text, x, y, size=22, color=None, font=None):
    if font is None:
        font = get_font(size)
    if color is None:
        color = TEXT_DARK
    draw.text((x, y), text, fill=color, font=font)
    return y + size + 10

def wrap_text(text, font, max_width):
    """中文文本换行"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = font.getbbox(test)
        w = bbox[2] - bbox[0]
        if w > max_width and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return lines

def draw_code_block(draw, code_lines, x, y, w, h):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=CODE_BG)
    font = get_font(18)
    cy = y + 15
    for line in code_lines:
        for sub in wrap_text(line, font, w - 40):
            draw.text((x + 20, cy), sub, fill=CODE_FG, font=font)
            cy += 26
        cy += 2

def save_slide(img, idx):
    path = os.path.join(OUT_DIR, f"slide_{idx:02d}.png")
    img.save(path)
    print(f"  Slide {idx}: {os.path.getsize(path)//1024}KB")

# ============================================================
# 12张幻灯片
# ============================================================
slides = []

def slide_01_cover():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, WIDTH, HEIGHT], fill=(255, 248, 240))
    d.rectangle([0, 0, WIDTH, 8], fill=TITLE_BAR)
    # 标题
    f = get_font(48, bold=True)
    d.text((WIDTH//2 - 280, 220), "第5讲：指针", fill=TITLE_BAR, font=f)
    f2 = get_font(36, bold=True)
    d.text((WIDTH//2 - 380, 300), "打通任督二脉", fill=TEXT_DARK, font=f2)
    f3 = get_font(22)
    d.text((WIDTH//2 - 240, 380), "从程序员到架构师 · C语言插件框架演进之旅", fill=TEXT_LIGHT, font=f3)
    d.text((WIDTH//2 - 100, 430), "第5讲 / 共14讲", fill=TEXT_LIGHT, font=f3)
    # 装饰
    d.ellipse([200, 500, 260, 560], fill=ACCENT)
    d.ellipse([580, 510, 630, 560], fill=RED)
    d.ellipse([900, 500, 950, 550], fill=YELLOW)
    return img

def slide_02_knowledge_map():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "知识图谱位置")
    code = [
        "函数封装（第3讲）──→ 多文件编程（第4讲）",
        "     ↓ 全局变量太危险...",
        "     ↓",
        "  指针（第5讲）← 你在这里",
        "     ↓ 指针能用，但参数太多...",
        "     ↓",
        "  数组与字符串（第6讲）──→ 结构体（第7讲）──→ 链表（第8讲）",
        "     ↓",
        "  函数指针（第12讲）──→ 插件框架（第13讲）──→ 完整项目（第14讲）",
    ]
    draw_code_block(d, code, 80, 110, 1120, 420)
    y = 560
    d.text((80, y), "前置知识：函数封装（参数传递、返回值）、多文件编程（全局变量的问题）", fill=TEXT_LIGHT, font=get_font(18))
    d.text((80, y+30), "后续关联：数组、结构体、链表、函数指针（插件框架的核心）", fill=TEXT_LIGHT, font=get_font(18))
    return img

def slide_03_memory():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "什么是指针？—— 从内存说起")
    f = get_font(22)
    lines = [
        "程序运行时，数据存在内存（RAM）里。内存就像一栋超大的酒店：",
        "",
        "• 酒店有很多房间，每个房间有房间号（地址）",
        "• 每个房间可以住客人（存储数据）",
        "• 找某个人，不需要知道他叫什么，只要知道房间号就行",
    ]
    for line in lines:
        y = draw_text(d, line, 60, y, 22, TEXT_DARK, f)
    code = [
        "内存酒店",
        "┌──────────────────────────────────────┐",
        "│  地址 0x7FFF0000  │  值 = 1000.0  │  ← balance 住在这",
        "├──────────────────────────────────────┤",
        "│  地址 0x7FFF0008  │  值 = ???     │  ← 别的变量",
        "├──────────────────────────────────────┤",
        "│  地址 0x7FFF0010  │  值 = ???     │",
        "├──────────────────────────────────────┤",
        "│  ...                                  │",
        "└──────────────────────────────────────┘",
    ]
    draw_code_block(d, code, 60, 320, 1160, 350)
    return img

def slide_04_pointer_def():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "指针就是'房间号'")
    f = get_font(22)
    y = draw_text(d, "指针是一种特殊的变量，它存的不是普通数据，而是另一个变量的地址。", 60, y, 22, TEXT_DARK, f)
    y += 10
    code = [
        "普通变量 balance：",
        "  名字：balance",
        "  地址：0x7FFF0000（酒店房间号）",
        "  值：1000.0（房间里住的人）",
        "",
        "指针变量 p_balance：",
        "  名字：p_balance",
        "  地址：0x7FFF0020（指针自己也有房间）",
        "  值：0x7FFF0000（存的是 balance 的房间号！）",
    ]
    draw_code_block(d, code, 60, 170, 560, 420)
    # 右侧比喻
    d.rounded_rectangle([660, 170, 1220, 590], radius=8, fill=(255, 248, 240))
    y2 = 190
    d.text((680, y2), "比喻：", fill=TITLE_BAR, font=get_font(22, True))
    y2 += 40
    lines = [
        "• balance 是一个保险箱，里面装着 1000 块钱",
        "• p_balance 是一张纸条，上面写着",
        "  '保险箱在 0x7FFF0000 号房间'",
        "• 拿着纸条，就能找到保险箱，",
        "  打开看里面多少钱",
        "",
        "价值：",
        "• 不用全局变量，函数也能修改",
        "  调用者的变量",
    ]
    for line in lines:
        d.text((680, y2), line, fill=TEXT_DARK, font=f)
        y2 += 35
    return img

def slide_05_operators():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "取地址（&）和解引用（*）")
    code = [
        "double balance = 1000.0;",
        "double *p_balance;           // 声明指针",
        "",
        "p_balance = &balance;         // 取地址：获取 balance 的地址",
        "                              // p_balance 现在存的是 0x7FFF0000",
        "",
        "printf(\"%p\\n\", p_balance);  // 打印地址：0x7FFF0000",
        "printf(\"%lf\\n\", *p_balance); // 解引用：通过地址取值 → 1000.0",
        "",
        "*p_balance = 2000.0;         // 通过指针修改 balance 的值",
        "printf(\"%lf\\n\", balance);   // balance 现在是 2000.0",
    ]
    draw_code_block(d, code, 60, 110, 700, 560)
    # 右侧要点
    d.rounded_rectangle([790, 110, 1220, 670], radius=8, fill=(255, 248, 240))
    y2 = 130
    points = [
        ("& 取地址", RED),
        ("获取变量的内存地址", TEXT_DARK),
        ("", None),
        ("* 解引用", GREEN),
        ("通过地址访问/修改变量", TEXT_DARK),
        ("", None),
        ("口诀：", TITLE_BAR),
        ("& 是'问门牌号'", TEXT_DARK),
        ("* 是'推门进去'", TEXT_DARK),
    ]
    for text, color in points:
        if color:
            d.text((810, y2), text, fill=color, font=get_font(22, color==RED or color==GREEN or color==TITLE_BAR))
        y2 += 35
    return img

def slide_06_pointer_param():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "指针作为函数参数")
    f = get_font(22)
    y = draw_text(d, "C语言的参数传递是值传递——传的是副本，不是原件。", 60, y, 22, TEXT_DARK, f)
    y = draw_text(d, "函数里修改参数，不会影响外面的变量。", 60, y, 22, TEXT_LIGHT, f)
    y += 10
    code = [
        "// 值传递：改不了外面的变量",
        "void try_double(double x) {",
        "    x *= 2;  // 只改了副本",
        "}",
        "",
        "// 指针传递：能改外面的变量",
        "void do_double(double *p) {",
        "    *p *= 2;  // 通过地址改原件",
        "}",
        "",
        "double balance = 1000.0;",
        "try_double(balance);           // balance 还是 1000.0",
        "do_double(&balance);            // balance 变成 2000.0",
    ]
    draw_code_block(d, code, 60, 200, 1160, 450)
    return img

def slide_07_pointer_array():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "指针与数组")
    f = get_font(22)
    y = draw_text(d, "数组名就是首元素地址，可以用指针操作数组。", 60, y, 22, TEXT_DARK, f)
    y += 10
    code = [
        "double arr[5] = {10, 20, 30, 40, 50};",
        "double *p = arr;  // p 指向 arr[0]",
        "",
        "// 三种等价的访问方式",
        "printf(\"%lf\\n\", arr[2]);     // 30.0  下标",
        "printf(\"%lf\\n\", *(p + 2));   // 30.0  指针偏移",
        "printf(\"%lf\\n\", *(arr + 2)); // 30.0  数组名当指针",
        "",
        "// 指针遍历数组",
        "for (double *q = arr; q < arr + 5; q++) {",
        "    printf(\"%lf \", *q);  // 10 20 30 40 50",
        "}",
    ]
    draw_code_block(d, code, 60, 190, 1160, 460)
    return img

def slide_08_memory_model():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "内存模型简图")
    # 左：全局变量版
    d.rounded_rectangle([60, 110, 600, 670], radius=8, fill=(255, 240, 240))
    d.text((80, 130), "全局变量版（第3讲）", fill=RED, font=get_font(24, True))
    lines = [
        "┌─────────────────────┐",
        "│  全局区             │",
        "│  g_balance = 1000.0  │ ← 所有函数都能直接访问",
        "│  g_count = 0        │",
        "└─────────────────────┘",
        "",
        "  deposit()  → g_balance += 100",
        "  withdraw() → g_balance -= 50",
        "  query()    → 看 g_balance",
        "",
        "  问题：谁都能改，出了bug不知道",
        "  谁改的，函数带着全局变量",
        "  一起搬，不好复用",
    ]
    font = get_font(18)
    cy = 175
    for line in lines:
        d.text((80, cy), line, fill=TEXT_DARK, font=font)
        cy += 24
    # 右：指针版
    d.rounded_rectangle([640, 110, 1220, 670], radius=8, fill=(240, 255, 240))
    d.text((660, 130), "指针版（第5讲）", fill=GREEN, font=get_font(24, True))
    lines2 = [
        "┌─────────────────────┐",
        "│  main的栈帧          │",
        "│  balance = 1000.0   │ ← 只有main能直接访问",
        "│  count = 0           │",
        "└─────────────────────┘",
        "",
        "  deposit(&balance)   → 通过指针修改",
        "  withdraw(&balance)  → 通过指针修改",
        "  query(balance)      → 只读副本",
        "",
        "  优点：谁改的一目了然",
        "  函数只传参数，到哪都能用",
    ]
    cy = 175
    for line in lines2:
        d.text((660, cy), line, fill=TEXT_DARK, font=font)
        cy += 24
    return img

def slide_09_atm_compare():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "ATM指针版对比")
    f = get_font(20)
    y = draw_text(d, "用指针消灭 ATM 程序中的全局变量 —— 从'公共牧场'到'钥匙授权'", 60, y, 20, TEXT_DARK, f)
    y += 10
    # 对比表格
    d.rounded_rectangle([60, y, 1220, y+40], radius=4, fill=TITLE_BAR)
    d.text((80, y+8), "对比项", fill=(255,255,255), font=get_font(20, True))
    d.text((350, y+8), "全局变量版（第3讲）", fill=(255,255,255), font=get_font(20, True))
    d.text((800, y+8), "指针版（第5讲）", fill=(255,255,255), font=get_font(20, True))
    y += 45
    rows = [
        ("余额在哪", "全局区，谁都能看见", "main的局部变量"),
        ("谁能改", "所有函数", "只有main授权的函数"),
        ("出了问题", "不知道谁改的", "看谁拿了地址就知道"),
        ("函数复用", "带着全局变量一起搬", "只传参数，到哪都能用"),
    ]
    for i, (k, v1, v2) in enumerate(rows):
        bg_color = (250, 250, 250) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([60, y, 1220, y+40], fill=bg_color)
        d.text((80, y+8), k, fill=TEXT_DARK, font=get_font(18, True))
        d.text((350, y+8), v1, fill=RED, font=get_font(18))
        d.text((800, y+8), v2, fill=GREEN, font=get_font(18))
        y += 42
    d.text((60, y+10), "指针的价值：在不使用全局变量的前提下，让函数能修改调用者的变量。", fill=TITLE_BAR, font=get_font(20, True))
    return img

def slide_10_func_pointer():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "函数指针 —— 插件框架的种子")
    f = get_font(22)
    y = draw_text(d, "指针不仅能指向数据，还能指向函数！", 60, y, 22, TEXT_DARK, f)
    y = draw_text(d, "函数在内存中也有地址，可以用指针保存和调用。", 60, y, 22, TEXT_LIGHT, f)
    y += 10
    code = [
        "// 声明函数指针",
        "double (*operation)(double, double);",
        "",
        "// operation 可以指向任何 (double, double) -> double 的函数",
        "operation = add;      // 指向加法函数",
        "operation = subtract; // 指向减法函数",
        "",
        "// 通过函数指针调用（和直接调用效果一样）",
        "double result = operation(100.0, 50.0);",
        "",
        "// 这就是插件框架的雏形：",
        "// 不写死调用哪个函数，运行时决定！",
    ]
    draw_code_block(d, code, 60, 210, 1160, 440)
    return img

def slide_11_thinking():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "思考题")
    f = get_font(22)
    questions = [
        "1. 为什么说指针是C语言最强大的特性之一？",
        "   提示：想想指针能做什么其他特性做不到的事",
        "",
        "2. 全局变量和指针参数，各自解决什么问题？",
        "   提示：一个图方便但有风险，一个图安全但需传递",
        "",
        "3. 数组名和指针有什么区别？",
        "   提示：数组名是常量，sizeof结果不同",
        "",
        "4. 函数指针为什么是插件框架的基础？",
        "   提示：运行时决定调用哪个函数 = 动态扩展",
        "",
        "5. & 和 * 是互逆操作吗？验证你的想法。",
        "   提示： *&balance == balance ?  &*p == p ?",
    ]
    for q in questions:
        y = draw_text(d, q, 60, y, 20, TEXT_DARK, f)
    return img

def slide_12_summary():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    draw_bg(img, d)
    y = draw_title(d, "小结")
    f = get_font(22)
    points = [
        "指针 = 地址 = 内存中的'门牌号'",
        "",
        "& 取地址：获取变量的门牌号",
        "* 解引用：拿着门牌号推门进去",
        "",
        "指针参数：不用全局变量，函数也能改调用者的变量",
        "指针与数组：数组名就是首元素地址，指针可以遍历",
        "",
        "函数指针：指向函数的指针，插件框架的种子",
        "",
        "演进路线：",
        "  表达式 → 控制结构 → 函数 → 多文件 → 指针 → 数组",
        "  → 结构体 → 链表 → 静态库 → 动态库 → 接口抽象",
        "  → 函数指针 → 插件框架 → 完整项目",
        "",
        "下一讲：数组与字符串 —— 一排连续的保险箱",
    ]
    for p in points:
        y = draw_text(d, p, 60, y, 20, TEXT_DARK, f)
    return img

# ============================================================
# 生成所有幻灯片
# ============================================================
print("渲染第5讲幻灯片图片...")
creators = [
    slide_01_cover, slide_02_knowledge_map, slide_03_memory,
    slide_04_pointer_def, slide_05_operators, slide_06_pointer_param,
    slide_07_pointer_array, slide_08_memory_model, slide_09_atm_compare,
    slide_10_func_pointer, slide_11_thinking, slide_12_summary,
]

for i, creator in enumerate(creators):
    img = creator()
    save_slide(img, i + 1)

print(f"完成！共{len(creators)}张图片")
