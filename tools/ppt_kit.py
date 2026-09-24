# -*- coding: utf-8 -*-
"""
ppt_kit.py —— 课件 PPT 统一工具箱（全系列共用）
================================================

【为什么需要它】
  早期课件用"手工摆放形状"的做法，导致三类硬伤：
    1) 标题过长时自动换行，投影时标题占两行、压住副标题；
    2) 装饰大图/色块压在卡片和文字上（前后不分），内容被吞掉；
    3) 代码块用"浅色字 + 浅色底"，投影仪下几乎看不清。
  本工具箱把排版收进代码，任何页面都由它生成，从根上避免上述问题。

【三条硬规矩（audit() 会逐页检查并报错）】
  R1 标题单行    —— 标题字号自动收缩到"单行放得下"，绝不换行
  R2 层级分明    —— 容器（卡片/代码块/横幅）之间不许重叠，正文不许越过底线，
                    文字一律后画（永远在装饰之上）
  R3 对比度达标  —— 所有正文与底色的对比度 ≥ 4.5:1（投影友好），
                    代码块一律深底亮字

【版式分区】13.333 x 7.5 英寸（16:9）
  0.00 ~ 0.10  顶部主色条
  0.34 ~ 1.34  标题区（标题 + 副标题 + 分隔线）
  1.52 ~ 6.28  正文区（所有内容必须在此区间内）
  6.44 ~ 7.02  要点横幅（可选，单行）
  7.08 ~ 7.50  页脚（讲次标签 / 页码）
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import ImageFont

# ============================================================
# 一、常量
# ============================================================
SW, SH = 13.333, 7.5           # 幻灯片尺寸（英寸）

MARGIN_L = 0.60
MARGIN_R = 0.60
INNER_W = SW - MARGIN_L - MARGIN_R          # 12.133

BAR_H = 0.10                    # 顶部色条
TITLE_TOP = 0.34
TITLE_H = 0.70
SUBTITLE_TOP = 1.08
SUBTITLE_H = 0.28
DIVIDER_Y = 1.44

BODY_TOP = 1.56
BODY_BOTTOM = 6.28              # 正文底线，容器不许越过
BANNER_TOP = 6.44
BANNER_H = 0.58
FOOTER_TOP = 7.08

FONT_R = 'C:/Windows/Fonts/msyh.ttc'       # 微软雅黑
FONT_B = 'C:/Windows/Fonts/msyhbd.ttc'     # 微软雅黑 Bold
FONT_C = 'C:/Windows/Fonts/consola.ttf'    # Consolas（代码）

FONT_NAME_R = '微软雅黑'
FONT_NAME_C = 'Consolas'

# 投影友好配色：色值只用于"面"（色块/条），文字一律用 *_dark 或 ink
C = {
    'bg':          'FFFFFF',
    'ink':         '1F2937',   # 正文（最深）
    'ink2':        '475569',   # 次级
    'ink3':        '7C8A9C',   # 弱化
    'line':        'DCE3EC',

    'primary':     'F97316',   # 主色（橙）
    'primary_dark':'C2410C',
    'teal':        '0D9488',
    'teal_dark':   '0F766E',
    'blue':        '2563EB',
    'blue_dark':   '1D4ED8',
    'red':         'DC2626',
    'red_dark':    'B91C1C',
    'green':       '16A34A',
    'green_dark':  '15803D',
    'purple':      '7C3AED',
    'purple_dark': '6D28D9',
    'pink':        'DB2777',
    'pink_dark':   'BE185D',
    'yellow':      'F59E0B',
    'yellow_dark': 'B45309',

    # 卡片浅底（配 ink 深字，对比度充足）
    'card_orange': 'FFF1E6',
    'card_teal':   'E4F6F4',
    'card_blue':   'E8F1FF',
    'card_red':    'FDECEF',
    'card_purple': 'F1EAFE',
    'card_green':  'E8F8EF',
    'card_yellow': 'FFF6E0',
    'card_gray':   'F1F5F9',

    # 代码块（深底亮字）
    'code_bg':     '0F172A',
    'code_head':   '1E293B',
    'code_ink':    'E6EDF7',
    'code_kw':     'FDBA74',
    'code_str':    '86EFAC',
    'code_cmt':    '9FB0C9',
    'code_num':    '7DD3FC',
    'code_fn':     'C4B5FD',
}

# 卡片浅底 -> 强调色 的配套表
CARD_PAIRS = {
    'orange': ('card_orange', 'primary', 'primary_dark'),
    'teal':   ('card_teal',   'teal',    'teal_dark'),
    'blue':   ('card_blue',   'blue',    'blue_dark'),
    'red':    ('card_red',    'red',     'red_dark'),
    'purple': ('card_purple', 'purple',  'purple_dark'),
    'green':  ('card_green',  'green',   'green_dark'),
    'yellow': ('card_yellow', 'yellow',  'yellow_dark'),
    'gray':   ('card_gray',   'ink3',    'ink'),
    'pink':   ('card_red',    'pink',    'pink_dark'),
}

# 需要"白字压面"时，必须用这些深一号的实色（对比度 ≥ 4.5，投影才看得清）
# 亮色只用于装饰块/细条（不承载文字）
SOLID = {
    'primary': 'C2410C', 'orange': 'C2410C',
    'teal':    '0F766E', 'blue':   '1D4ED8',
    'red':     'B91C1C', 'green':  '15803D',
    'purple':  '6D28D9', 'pink':   'BE185D',
    'yellow':  'B45309', 'ink3':   '475569',
    'gray':    '475569',
}


def solid(key):
    """取"可承载白字的实色"。"""
    return C.get(SOLID.get(key, key), SOLID.get(key, key))

# ============================================================
# 二、文本测量（用真实字体度量，保证"不换行/不溢出"可验证）
# ============================================================
_font_cache = {}


def _font(path, size):
    key = (path, int(round(size)))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, int(round(size)))
    return _font_cache[key]


SAFETY = 1.06       # 实测：PowerPoint 渲染比 PIL 度量略宽，留 6% 余量


def text_width_in(text, size, bold=False):
    """文本在给定字号下的宽度（英寸，含安全余量）。字号单位 pt，1pt = 1/72 in。"""
    f = _font(FONT_B if bold else FONT_R, size)
    return f.getlength(text) / 72.0 * SAFETY


def code_width_in(text, size):
    f = _font(FONT_C, size)
    return f.getlength(text) / 72.0 * SAFETY


def wrap_text(text, size, width_in, bold=False, mono=False):
    """按像素真实宽度做贪心折行（中文可任意断行），返回行列表。"""
    meas = (lambda s: code_width_in(s, size)) if mono else (lambda s: text_width_in(s, size, bold))
    limit = width_in
    out = []
    for para in str(text).split('\n'):
        if para == '':
            out.append('')
            continue
        cur = ''
        for ch in para:
            if meas(cur + ch) <= limit:
                cur += ch
            else:
                out.append(cur)
                cur = ch
        out.append(cur)
    return out


def n_lines(text, size, width_in, bold=False, mono=False):
    return len(wrap_text(text, size, width_in, bold, mono))


def text_height_in(text, size, width_in, bold=False, line_spacing=1.30, mono=False):
    """文本所需高度（英寸），含行距。"""
    return n_lines(text, size, width_in, bold, mono) * size * line_spacing / 72.0


def fit_size(text, width_in, start=40, min_size=20, bold=True, step=1):
    """标题自适应：返回"单行放得下"的最大字号。"""
    s = start
    while s > min_size:
        if text_width_in(text, s, bold) <= width_in:
            return s
        s -= step
    return min_size


# ============================================================
# 三、对比度（R3）
# ============================================================
def _lum(hex6):
    r, g, b = (int(hex6[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    l1, l2 = _lum(fg), _lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# ============================================================
# 四、内部：本页元素登记表（供 audit 检查层级与溢出）
# ============================================================
_REG = []       # 容器：dict(kind,x,y,w,h,tag)
_TEXTS = []     # 文字：dict(x,y,w,h,text,size,bold,color,parent_bg,tag)


_stage = {'slide': None, 'content_start': 0, 'banner_start': None}


def _reset_reg():
    _REG.clear()
    _TEXTS.clear()


def _center_content():
    """把正文内容在正文区内垂直居中，避免"上挤下空"的观感。"""
    slide = _stage.get('slide')
    if slide is None or not _REG:
        return
    cand = [r for r in _REG if r['kind'] not in ('banner',)]
    if not cand:
        return
    bottom = max(r['y'] + r['h'] for r in cand)
    gap = BODY_BOTTOM - bottom
    if gap < 0.55:
        return
    delta = gap / 2.0
    end = _stage['banner_start'] if _stage['banner_start'] is not None else len(slide.shapes)
    start = _stage['content_start']
    for shp in list(slide.shapes)[start:end]:
        if shp.top is not None:
            shp.top = Emu(int(shp.top + Inches(delta)))
    for coll in (_REG, _TEXTS):
        for it in coll:
            it['y'] += delta


def _reg_container(kind, x, y, w, h, tag=''):
    _REG.append({'kind': kind, 'x': x, 'y': y, 'w': w, 'h': h, 'tag': tag})


def _reg_text(x, y, w, h, text, size, bold, color, parent_bg, tag=''):
    _TEXTS.append({'x': x, 'y': y, 'w': w, 'h': h, 'text': text, 'size': size,
                   'bold': bold, 'color': color, 'bg': parent_bg, 'tag': tag})


# ============================================================
# 五、底层绘制原语
# ============================================================
def _rgb(hex6):
    return RGBColor.from_string(hex6.upper())


def _no_shadow(shape):
    """关掉 PowerPoint 默认阴影（阴影会让"前后不分"）"""
    try:
        spPr = shape._element.spPr
        from pptx.oxml.ns import qn
        el = spPr.find(qn('a:effectLst'))
        if el is None:
            from lxml import etree
            el = etree.SubElement(spPr, qn('a:effectLst'))
    except Exception:
        pass


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, radius=None, shape=MSO_SHAPE.RECTANGLE):
    """画一个矩形/圆角矩形。fill/line 传十六进制字符串或 None。"""
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(fill)
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = _rgb(line)
        shp.line.width = Pt(line_w)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    return shp


def panel(slide, x, y, w, h, fill='card_gray', line=None, radius=0.06, tag='panel'):
    return rect(slide, x, y, w, h, fill=C.get(fill, fill),
                line=C.get(line, line) if line else None,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)


def _put_text(slide, x, y, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT,
              line_spacing=1.30, anchor=MSO_ANCHOR.TOP, font_name=None, italic=False,
              space_after=0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = str(text).split('\n')
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        if space_after:
            p.space_after = Pt(space_after)
        run = p.add_run()
        run.text = ln
        f = run.font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = _rgb(color)
        f.name = font_name or FONT_NAME_R
    return tb


def text(slide, x, y, w, txt, size=18, color=None, bold=False, align=PP_ALIGN.LEFT,
         line_spacing=1.30, h=None, parent_bg='bg', tag='text', anchor=MSO_ANCHOR.TOP):
    """正文文字。h=None 时按真实测量自动定高，杜绝溢出。"""
    color = color or C['ink']
    need = text_height_in(txt, size, w, bold, line_spacing)
    hh = need if h is None else h
    _put_text(slide, x, y, w, hh, txt, size, color, bold, align, line_spacing, anchor)
    _reg_text(x, y, w, hh, txt, size, bold, color, parent_bg, tag)
    return y + hh


# ============================================================
# 六、页面骨架
# ============================================================
def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    return prs


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def page(prs, title, subtitle=None, label=None, page_no=None, accent='primary'):
    """
    建一页并画好骨架：白底 + 顶部色条 + 单行标题 + 副标题 + 分隔线 + 页脚。
    返回 slide。
    """
    _reset_reg()
    slide = blank(prs)
    _stage['slide'] = slide
    _stage['banner_start'] = None

    # 1) 背景（最先画，永远在最底层）
    rect(slide, 0, 0, SW, SH, fill=C['bg'])
    rect(slide, 0, 0, SW, BAR_H, fill=C[accent])

    # 2) 标题徽标 + 标题（单行自适应）
    rect(slide, MARGIN_L, TITLE_TOP + 0.06, 0.50, 0.50, fill=C[accent],
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.22)

    tx = MARGIN_L + 0.72
    tw = SW - tx - MARGIN_R
    size = fit_size(title, tw, start=38, min_size=22, bold=True)
    _put_text(slide, tx, TITLE_TOP + 0.06, tw, TITLE_H, title, size, C['ink'], bold=True)
    _reg_text(tx, TITLE_TOP + 0.06, tw, TITLE_H, title, size, True, C['ink'], 'bg', 'TITLE')

    if subtitle:
        sub_size = 15 if text_width_in(subtitle, 15) <= tw else 13
        _put_text(slide, tx + 0.02, SUBTITLE_TOP, tw, SUBTITLE_H, subtitle, sub_size, C['ink2'])
        _reg_text(tx + 0.02, SUBTITLE_TOP, tw, SUBTITLE_H, subtitle, sub_size, False, C['ink2'], 'bg', 'SUBTITLE')

    rect(slide, MARGIN_L, DIVIDER_Y, INNER_W, 0.02, fill=C['line'])

    # 4) 页脚
    if label:
        _put_text(slide, MARGIN_L, FOOTER_TOP, INNER_W * 0.7, 0.30, label, 11, C['ink3'])
    if page_no:
        no = len(prs.slides._sldIdLst) if page_no == 'auto' else page_no
        _put_text(slide, SW - MARGIN_R - 1.2, FOOTER_TOP, 1.2, 0.30,
                  str(no), 11, C['ink3'], align=PP_ALIGN.RIGHT)
    _stage['content_start'] = len(slide.shapes)   # 骨架之后画的都算"正文内容"
    return slide


def banner(slide, msg, fill='primary', size=16):
    """底部要点横幅（正文区之下的独立层，绝不与正文重叠）。"""
    if _stage.get('slide') is slide:
        _stage['banner_start'] = len(slide.shapes)
    y = BANNER_TOP
    rect(slide, MARGIN_L, y, INNER_W, BANNER_H, fill=solid(fill),
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.20)
    _reg_container('banner', MARGIN_L, y, INNER_W, BANNER_H, 'banner')
    inner_w = INNER_W - 0.6
    s = size
    while s > 12 and text_width_in(msg, s, True) > inner_w:
        s -= 1
    _put_text(slide, MARGIN_L + 0.3, y + 0.10, inner_w, BANNER_H - 0.2, msg, s,
              'FFFFFF', bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _reg_text(MARGIN_L + 0.3, y + 0.10, inner_w, BANNER_H - 0.2, msg, s, True, 'FFFFFF',
              SOLID[fill], 'BANNER')


def footer_note(slide, msg):
    """底线之外留给横幅时，用一行小字结论（放在正文区内最后一行）。"""
    y = BODY_BOTTOM - 0.42
    rect(slide, MARGIN_L, y, INNER_W, 0.40, fill=C['card_orange'],
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.25)
    _reg_container('note', MARGIN_L, y, INNER_W, 0.40, 'note')
    s = 15
    while s > 11 and text_width_in(msg, s, True) > INNER_W - 0.5:
        s -= 1
    _put_text(slide, MARGIN_L + 0.25, y + 0.06, INNER_W - 0.5, 0.28, msg, s,
              C['primary_dark'], bold=True, align=PP_ALIGN.CENTER)
    _reg_text(MARGIN_L + 0.25, y + 0.06, INNER_W - 0.5, 0.28, msg, s, True,
              C['primary_dark'], 'card_orange', 'NOTE')
    return y


# ============================================================
# 七、常用内容块（全部自动定高，返回底部 y）
# ============================================================
def card(slide, x, y, w, body, title=None, color='orange', size=16, title_size=18,
         min_h=0.0, pad=0.20, tag='card', line_spacing=1.32):
    """
    浅底卡片：左侧强调色条 + 可选标题 + 正文。高度按真实测量自动撑开。
    返回 (bottom_y, height)
    """
    bg_key, accent_key, dark_key = CARD_PAIRS[color]
    inner_w = w - pad * 2 - 0.06
    h = pad * 2
    if title:
        th = text_height_in(title, title_size, inner_w, True, 1.25)
        h += th + 0.08
    bh = text_height_in(body, size, inner_w, False, line_spacing) if body else 0
    h += bh
    h = max(h, min_h)

    panel(slide, x, y, w, h, fill=bg_key, tag=tag)
    _reg_container('card', x, y, w, h, tag)
    rect(slide, x, y, 0.055, h, fill=C[accent_key])       # 左侧色条

    cy = y + pad
    if title:
        th = text_height_in(title, title_size, inner_w, True, 1.25)
        _put_text(slide, x + pad, cy, inner_w, th, title, title_size, C[dark_key], bold=True,
                  line_spacing=1.25)
        _reg_text(x + pad, cy, inner_w, th, title, title_size, True, C[dark_key], bg_key, tag + ':t')
        cy += th + 0.08
    if body:
        _put_text(slide, x + pad, cy, inner_w, bh, body, size, C['ink'], line_spacing=line_spacing)
        _reg_text(x + pad, cy, inner_w, bh, body, size, False, C['ink'], bg_key, tag + ':b')
    return y + h, h


CODE_KW = ('int', 'char', 'double', 'float', 'void', 'return', 'if', 'else', 'while', 'for',
           'switch', 'case', 'break', 'continue', 'struct', 'typedef', 'static', 'const',
           'sizeof', 'include', 'define', 'free', 'malloc', 'NULL', 'true', 'false', 'bool',
           'extern', 'unsigned', 'long', 'short', 'do', 'default', 'enum', 'union')


def code(slide, x, y, w, lines, title=None, size=13.5, tag='code'):
    """
    深底代码块（R3：深底亮字，投影清晰）。行首简单着色。
    返回 (bottom_y, height)
    """
    pad = 0.18
    line_h = size * 1.42 / 72.0
    head_h = 0.40 if title else 0.0
    h = head_h + pad * 2 + line_h * len(lines)

    rect(slide, x, y, w, h, fill=C['code_bg'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    _reg_container('code', x, y, w, h, tag)
    if title:
        rect(slide, x, y, w, head_h, fill=C['code_head'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.10)
        _put_text(slide, x + pad, y + 0.06, w - pad * 2, head_h - 0.12, title, size + 1,
                  C['code_kw'], bold=True, anchor=MSO_ANCHOR.MIDDLE)
        _reg_text(x + pad, y + 0.06, w - pad * 2, head_h - 0.12, title, size + 1, True,
                  C['code_kw'], 'code_head', tag + ':t')

    ty = y + head_h + pad * 0.6
    for i, ln in enumerate(lines):
        color = C['code_ink']
        s = ln.strip()
        if s.startswith('//') or s.startswith('/*') or s.startswith('*') or s.startswith('#'):
            color = C['code_cmt']
        elif any(s.startswith(k + ' ') or s.startswith(k + '(') or s.startswith(k + ';')
                 for k in ('int', 'char', 'double', 'void', 'return', 'typedef', 'struct', 'static')):
            color = C['code_kw']
        _put_text(slide, x + pad, ty + i * line_h, w - pad * 2, line_h, ln, size, color,
                  font_name=FONT_NAME_C)
        _reg_text(x + pad, ty + i * line_h, w - pad * 2, line_h, ln, size, False, color,
                  'code_bg', tag + ':l%d' % i)
    return y + h, h


def kv_rows(slide, x, y, w, rows, widths=(0.30, 0.70), size=15, header=None, tag='kv'):
    """
    表格式列表（用形状+文字手绘，避免 pptx 表格默认样式在投影下发灰）。
    rows: [(左, 右), ...]
    返回 (bottom_y, height)
    """
    row_h = max(0.42, size * 1.5 / 72.0 + 0.20)
    h = row_h * len(rows)
    if header:
        h += row_h
    cur = y
    if header:
        rect(slide, x, cur, w, row_h, fill=solid('primary'))
        _reg_container('kvhead', x, cur, w, row_h, tag)
        cx = x
        for i, cell in enumerate(header):
            cw = w * widths[i]
            _put_text(slide, cx + 0.14, cur + 0.04, cw - 0.24, row_h - 0.08, cell, size,
                      'FFFFFF', bold=True, anchor=MSO_ANCHOR.MIDDLE)
            _reg_text(cx + 0.14, cur + 0.04, cw - 0.24, row_h - 0.08, cell, size, True,
                      'FFFFFF', SOLID['primary'], tag + ':h%d' % i)
            cx += cw
        cur += row_h
    for r, row in enumerate(rows):
        fill = C['card_gray'] if r % 2 == 0 else C['bg']
        rect(slide, x, cur, w, row_h, fill=fill)
        _reg_container('kvrow', x, cur, w, row_h, tag)
        cx = x
        for i, cell in enumerate(row):
            cw = w * widths[i]
            col = C['ink'] if i == 0 else C['ink']
            _put_text(slide, cx + 0.14, cur + 0.04, cw - 0.24, row_h - 0.08, cell,
                      size, col, bold=(i == 0), anchor=MSO_ANCHOR.MIDDLE)
            _reg_text(cx + 0.14, cur + 0.04, cw - 0.24, row_h - 0.08, cell, size, i == 0,
                      col, 'card_gray' if r % 2 == 0 else 'bg', tag + ':r%d%d' % (r, i))
            cx += cw
        cur += row_h
    return cur, h


def bullets(slide, x, y, w, items, size=17, color='ink', bullet='▸', tag='bullets',
            gap=0.10, bold_head=False):
    """无序列表（首行可加粗），返回 bottom_y。"""
    cur = y
    for it in items:
        if isinstance(it, tuple):
            head, rest = it
            txt = f'{bullet} {head} {rest}'
        else:
            txt = f'{bullet} {it}'
        h = text_height_in(txt, size, w, False, 1.34)
        _put_text(slide, x, cur, w, h, txt, size, C[color], line_spacing=1.34)
        _reg_text(x, cur, w, h, txt, size, False, C[color], 'bg', tag)
        cur += h + gap
    return cur


def flow(slide, x, y, w, items, colors=('blue', 'teal', 'purple', 'orange', 'green'),
         size=14, h=0.78, tag='flow'):
    """
    横向箭头流程（等宽分栏）。高度按文字实测自动增高，返回 bottom_y。
    """
    n = len(items)
    gap = 0.34
    cw = (w - gap * (n - 1)) / n
    # 先按最长的一栏算出需要的行高
    need = h
    for it in items:
        t = it if isinstance(it, str) else it[0]
        sub = None if isinstance(it, str) else it[1]
        th = text_height_in(t, size, cw - 0.24, True, 1.25)
        sh = text_height_in(sub, size - 2, cw - 0.20, False, 1.28) if sub else 0
        need = max(need, 0.10 + th + 0.10 + sh + 0.12)
    h = need
    for i, it in enumerate(items):
        ck = colors[i % len(colors)]
        cx = x + i * (cw + gap)
        rect(slide, cx, y, cw, h, fill=solid(ck), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
        _reg_container('flow', cx, y, cw, h, tag)
        t = it if isinstance(it, str) else it[0]
        sub = None if isinstance(it, str) else it[1]
        s_ = size
        while s_ > 9 and text_width_in(t, s_, True) > cw - 0.24:
            s_ -= 1
        th = text_height_in(t, s_, cw - 0.24, True, 1.25)
        ty = y + (h - th - (text_height_in(sub, s_ - 2, cw - 0.20, False, 1.28) if sub else 0)) / 2
        if sub:
            sh = text_height_in(sub, s_ - 2, cw - 0.20, False, 1.28)
            _put_text(slide, cx + 0.10, ty, cw - 0.20, th, t, s_, 'FFFFFF', bold=True,
                      align=PP_ALIGN.CENTER, line_spacing=1.25)
            _put_text(slide, cx + 0.10, ty + th + 0.08, cw - 0.20, sh, sub, s_ - 2, 'FFFFFF',
                      align=PP_ALIGN.CENTER, line_spacing=1.28)
            _reg_text(cx + 0.10, ty + th + 0.08, cw - 0.20, sh, sub, s_ - 2, False, 'FFFFFF',
                      SOLID[ck], tag + ':s%d' % i)
        else:
            _put_text(slide, cx + 0.10, ty, cw - 0.20, th, t, s_, 'FFFFFF', bold=True,
                      align=PP_ALIGN.CENTER, line_spacing=1.25, anchor=MSO_ANCHOR.MIDDLE)
        _reg_text(cx + 0.10, ty, cw - 0.20, th, t, s_, True, 'FFFFFF', SOLID[ck], tag + ':t%d' % i)
        if i < n - 1:
            rect(slide, cx + cw + 0.03, y + h / 2 - 0.13, gap - 0.06, 0.26,
                 fill=C['ink3'], shape=MSO_SHAPE.RIGHT_ARROW)
    return y + h


def compare(slide, x, y, w, left_title, left_items, right_title, right_items,
            left_color='red', right_color='green', size=15, tag='cmp', row_h=None):
    """
    左右对照（表头 + 条目）。自动定高，返回 bottom_y。
    """
    gap = 0.36
    cw = (w - gap) / 2
    hy = 0.46
    rect(slide, x, y, cw, hy, fill=solid(left_color), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18)
    rect(slide, x + cw + gap, y, cw, hy, fill=solid(right_color), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18)
    _reg_container('cmphead', x, y, cw, hy, tag)
    _reg_container('cmphead', x + cw + gap, y, cw, hy, tag)
    for cx, t in ((x, left_title), (x + cw + gap, right_title)):
        s_ = 17
        while s_ > 11 and text_width_in(t, s_, True) > cw - 0.4:
            s_ -= 1
        _put_text(slide, cx + 0.2, y + 0.06, cw - 0.4, hy - 0.12, t, s_, 'FFFFFF', bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _reg_text(cx + 0.2, y + 0.06, cw - 0.4, hy - 0.12, t, s_, True, 'FFFFFF',
                  SOLID[left_color if cx == x else right_color], tag + ':h')

    # 条目：逐行对齐，行高按两列中最长的那条算
    n = max(len(left_items), len(right_items))
    cur = y + hy + 0.06
    for i in range(n):
        lt = left_items[i] if i < len(left_items) else ''
        rt = right_items[i] if i < len(right_items) else ''
        lh = max(text_height_in(lt, size, cw - 0.42, False, 1.30) if lt else 0,
                 text_height_in(rt, size, cw - 0.42, False, 1.30) if rt else 0)
        lh = max(lh, row_h or 0)
        for cx, t, ck in ((x, lt, left_color), (x + cw + gap, rt, right_color)):
            if not t:
                continue
            _put_text(slide, cx + 0.20, cur, cw - 0.40, lh,
                      '· ' + t, size, C['ink'], line_spacing=1.30)
            _reg_text(cx + 0.20, cur, cw - 0.40, lh, '· ' + t, size, False, C['ink'], 'bg',
                      tag + ':i%d' % i)
            d = rect(slide, cx + 0.06, cur + 0.05, 0.075, lh - 0.10, fill=C[ck])
        cur += lh + 0.06
    return cur + 0.04


def demo_frame(slide, x, y, w, h, title='运行效果', lines=None, note=None, tag='demo'):
    """
    片尾"运行演示/截图"占位画框：一个深色终端窗口 + 说明。
    lines: 终端里逐行显示的内容（静态版；视频里会做成打字动画）
    """
    pad = 0.16
    rect(slide, x, y, w, h, fill=C['code_bg'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    _reg_container('demo', x, y, w, h, tag)
    rect(slide, x, y, w, 0.40, fill=C['code_head'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    _put_text(slide, x + pad, y + 0.06, w - pad * 2, 0.28, title, 13, C['code_kw'], bold=True)
    _reg_text(x + pad, y + 0.06, w - pad * 2, 0.28, title, 13, True, C['code_kw'], 'code_head', tag + ':t')
    if lines:
        lh = 12.5 * 1.5 / 72.0
        for i, ln in enumerate(lines):
            col = C['code_ink']
            if ln.startswith('>') or ln.startswith('$'):
                col = C['code_str']
            _put_text(slide, x + pad, y + 0.50 + i * lh, w - pad * 2, lh, ln, 12.5, col,
                      font_name=FONT_NAME_C)
            _reg_text(x + pad, y + 0.50 + i * lh, w - pad * 2, lh, ln, 12.5, False, col,
                      'code_bg', tag + ':l%d' % i)
    if note:
        _put_text(slide, x + pad, y + h - 0.34, w - pad * 2, 0.28, note, 12, C['code_cmt'])
        _reg_text(x + pad, y + h - 0.34, w - pad * 2, 0.28, note, 12, False, C['code_cmt'],
                  'code_bg', tag + ':n')
    return y + h


# ============================================================
# 八、质检（R1/R2/R3 逐页核对）
# ============================================================
def _overlap(a, b, tol=0.02):
    ix = min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x'])
    iy = min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y'])
    if ix <= tol or iy <= tol:
        return 0.0
    return ix * iy


def audit(prs, deck_name='', raise_on_error=True):
    """
    对已生成的每一页做检查（需在 page()/各绘制函数调用之后、切页之前调用）。
    返回 issue 列表；raise_on_error=True 时有问题直接抛异常，避免生成坏 PPT。
    """
    _center_content()
    issues = []
    for i, r in enumerate(_REG):
        if r['kind'] == 'banner':
            continue
        if r['y'] + r['h'] > BODY_BOTTOM + 0.02:
            issues.append(f"[R2 越界] {r['kind']}:{r['tag']} 底边 {r['y']+r['h']:.2f} > 正文底线 {BODY_BOTTOM}")
        if r['y'] < BODY_TOP - 0.02:
            issues.append(f"[R2 越界] {r['kind']}:{r['tag']} 顶边 {r['y']:.2f} < 正文顶线 {BODY_TOP}")
        if r['x'] < MARGIN_L - 0.02 or r['x'] + r['w'] > SW - MARGIN_R + 0.02:
            issues.append(f"[R2 越界] {r['kind']}:{r['tag']} 横向超出安全边距")

    for i in range(len(_REG)):
        for j in range(i + 1, len(_REG)):
            a, b = _REG[i], _REG[j]
            if a['tag'] == b['tag']:
                continue
            ov = _overlap(a, b)
            if ov > 0.03:
                issues.append(f"[R2 叠压] {a['kind']}:{a['tag']} 与 {b['kind']}:{b['tag']} 重叠 {ov:.2f} in²")

    for t in _TEXTS:
        need = text_height_in(t['text'], t['size'], t['w'], t['bold'], 1.32)
        if need > t['h'] + 0.03:
            issues.append(f"[溢出] {t['tag']} 文字需要 {need:.2f}in，框高仅 {t['h']:.2f}in：「{t['text'][:18]}」")
        _ls = wrap_text(t['text'], t['size'], t['w'], t['bold'])
        if len(_ls) > 1 and len(_ls[-1].strip()) <= 3:
            issues.append(f"[孤儿行] {t['tag']} 折行后末行只剩「{_ls[-1].strip()}」：「{t['text'][:20]}」")
        if t['tag'] == 'TITLE':
            if n_lines(t['text'], t['size'], t['w'], True) > 1:
                issues.append(f"[R1 标题换行] 「{t['text']}」在 {t['size']}pt 下超过 {t['w']:.2f}in")
        if contrast_ratio(t['color'], C.get(t['bg'], t['bg'])) < 4.5:
            issues.append(f"[R3 对比度] {t['tag']} 「{t['text'][:14]}」 {t['color']} on {t['bg']} = "
                          f"{contrast_ratio(t['color'], C.get(t['bg'], t['bg'])):.2f} < 4.5")
    if issues and raise_on_error:
        raise AssertionError(f"{deck_name} 质检未通过（{len(issues)} 项）：\n  - " + "\n  - ".join(issues[:20]))
    return issues


def save(prs, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    prs.save(path)
    print(f'PPT 已生成：{path}（{len(prs.slides.__iter__.__self__._sldIdLst)} 页）')
    return path
