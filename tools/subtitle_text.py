# -*- coding: utf-8 -*-
"""
subtitle_text.py —— 把"给 TTS 念的稿子"还原成"给人看的字幕"

讲解稿为了让人声念得准，会把代码里的符号写成中文读法：
    美元问号 / 星号p / 反斜杠n / arr方括号i / acc 点 id / p 箭头 id / void 星号 …
念出来没问题，但**字幕照抄就看不懂，也和投影页面上的真实代码对不上**。
所以字幕一律用还原后的写法：
    echo $? / *p / \\n / arr[i] / acc.id / p->id / void * …

设计原则：**宁可少改，也不要改错**。
只还原"百分之百确定是符号"的写法；像"引号、分号、括号"这种在句子里
当普通名词用的，保持原样（反而更好读）。

用法：
    from subtitle_text import narration, show_text, to_display
"""
import re


def narration(entry):
    """
    一段讲解稿，支持两种写法：
        "……"                             —— 念的和字幕一样
        {"say": "……", "show": "……"}       —— 分开写（say 给配音，show 给字幕）
    返回 (say, show)
    """
    if isinstance(entry, dict):
        say = entry.get('say') or entry.get('text') or ''
        show = entry.get('show') or ''
        return say, show
    return entry, ''


def show_text(entry):
    """字幕文本：作者显式写了 show 就照用；否则把念法还原成真实写法。"""
    say, show = narration(entry)
    return show if show else to_display(say)


# ------------------------------------------------------------
# 规则表
# ------------------------------------------------------------
# "零"在这些词里不是数字 0，先保护起来
_ZERO_KEEP = ['零件', '零散', '零基础', '零等待', '零配置', '零拷贝', '零成本', '零依赖']

# 念法和写法一对一，直接换
_PLAIN = [
    ('美元问号', '$?'),
    ('美元符', '$'),
    ('反斜杠n', '\\n'),
    ('反斜杠0', '\\0'),
    ('反斜杠t', '\\t'),
    ('反斜杠', '\\'),
    ('点斜杠', './'),
    ('下划线', '_'),
    ('加加', '++'),          # C 加加 / arr 加加
]

_CN_DIGIT = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
             '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100, '千': 1000}
_CN_NUM = '零一二三四五六七八九十百千'
_NAMECH = r'[A-Za-z_][A-Za-z_0-9]*'
_IDXCH = r'[A-Za-z_0-9]+|[' + _CN_NUM + r']+'

# 顺序很重要：先长后短、先具体后笼统
_RULES = [
    # void 星号 -> void *（声明里的指针）
    (re.compile(r'\b(void|char|int|short|long|float|double|unsigned|signed|struct)\s*星号'),
     lambda m: '%s *' % m.group(1)),
    # 星号括号arr加i -> *(arr+i)
    (re.compile(r'星号\s*括号\s*(%s)\s*加\s*([A-Za-z_0-9]+)' % _NAMECH),
     lambda m: '*(%s+%s)' % (m.group(1), m.group(2))),
    # 括号arr加i -> (arr+i)
    (re.compile(r'括号\s*(%s)\s*加\s*([A-Za-z_0-9]+)' % _NAMECH),
     lambda m: '(%s+%s)' % (m.group(1), m.group(2))),
    # 星号p / 星号 p -> *p
    (re.compile(r'星号\s?(%s)' % _NAMECH), lambda m: '*' + m.group(1)),
    # 用星号 / 比星号高 -> 用 * / 比 * 高
    (re.compile(r'星号'), lambda m: '*'),
    # 取地址a -> &a（单独说"取地址"这个操作名时保持不变）
    (re.compile(r'取地址\s*(%s)' % _NAMECH), lambda m: '&' + m.group(1)),
    # 加 -Wall -> -Wall
    (re.compile(r'加\s*(-{1,2}[A-Za-z][A-Za-z0-9_-]*)'), lambda m: m.group(1)),
    # arr方括号i / arr 方括号一百 / arr方括号i方括号j -> arr[i] / arr[100] / arr[i][j]
    (re.compile(r'(%s)(\]?)\s*方括号\s*(%s)' % (_NAMECH, _IDXCH)),
     lambda m: '%s%s[%s]' % (m.group(1), m.group(2), cn_to_num(m.group(3)))),
    (re.compile(r'\]\s*方括号\s*(%s)' % _IDXCH), lambda m: '][%s]' % cn_to_num(m.group(1))),
    # 括号…括号 里包的是短代码片段 -> 加回真括号
    (re.compile(r'括号([^，。；：！？、（）]{1,20}?)括号'), lambda m: '(%s)' % m.group(1)),
    # C ++ -> C++
    (re.compile(r'([A-Za-z0-9])\s*\+\+'), lambda m: m.group(1) + '++'),
    # acc 点 id -> acc.id；p 箭头 id -> p->id；(*p) 点 id -> (*p).id
    (re.compile(r'([A-Za-z_0-9\)\]]+)\s*点\s*(%s)' % _NAMECH), lambda m: '%s.%s' % (m.group(1), m.group(2))),
    (re.compile(r'([A-Za-z_0-9\)\]]+)\s*箭头\s*(%s)' % _NAMECH), lambda m: '%s->%s' % (m.group(1), m.group(2))),
    (re.compile(r'\)\s*点'), lambda m: ').'),
]


def cn_to_num(s):
    """中文数字转阿拉伯数字（一百→100、十五→15、三百二十→320、一百零五→105）。"""
    if not s or any(c not in _CN_DIGIT for c in s):
        return s
    if not any(c in '十百千' for c in s):
        return ''.join(str(_CN_DIGIT[c]) for c in s)
    section, num = 0, 0
    for c in s:
        v = _CN_DIGIT[c]
        if v < 10:
            num = v
        elif v == 10:
            section += (num or 1) * 10
            num = 0
        else:                                   # 100 / 1000
            section += (num or 1) * v
            num = 0
    return str(section + num)


def to_display(text):
    s = text

    for k in _ZERO_KEEP:
        s = s.replace(k, '\x00' + k[1:])

    for a, b in _PLAIN:
        s = s.replace(a, b)

    # 规则要过两遍：括号/点号这类会互相解锁（括号星号p括号点id）
    for _ in range(3):
        prev = s
        for rx, rep in _RULES:
            s = rx.sub(rep, s)
        if s == prev:
            break

    for cn, ar in {'一': '1', '二': '2', '两': '2', '三': '3', '四': '4',
                   '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}.items():
        s = s.replace('输入' + cn, '输入 ' + ar)

    s = s.replace('零', '0')

    # 中英/中数之间补细空格，避免"0警告""输入 2存款"这种粘连
    s = re.sub(r'([0-9])(?=[\u4e00-\u9fff])', r'\1 ', s)
    s = re.sub(r'(?<=[\u4e00-\u9fff])([0-9])', r' \1', s)
    # 单独出现的 * 前后补空格，别和汉字粘在一起（"用*，" -> "用 *，"、"void *传" -> "void * 传"）
    s = re.sub(r'(?<=[\u4e00-\u9fff])\*(?=[，。；：！？、\s])', ' *', s)
    s = re.sub(r'\*(?=[\u4e00-\u9fff])', '* ', s)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s+([，。；：！？、）」』】])', r'\1', s)
    s = re.sub(r'([（「『【])\s+', r'\1', s)

    s = s.replace('\x00', '零')
    return s.strip()


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    tests = [
        '第一条命令用 gcc 加 -Wall 编译，零警告；最后 echo 美元问号，读出退出码是零。',
        '第二个是解引用，用星号，读作星号p，意思是按着地址找上门。星号p 等于一百。',
        '写括号星号p括号点id必须加括号太啰嗦，C 就提供了箭头这个语法糖。',
        '所以 p 箭头 id 和括号星号p括号点id完全等价。acc 点 id，用点。',
        '星号p点id会被当成星号括号p点id括号。箭头就是括号星号p括号点的语法糖。',
        '为什么 arr 方括号一百能一步到位？arr方括号i方括号j 表示第i行第j列。',
        '把接口改成 void 星号传通用参数；C 加加由编译器自动生成。',
        '字符串以反斜杠0结尾；语言把最小的零件做成可拼装的。',
    ]
    for t in tests:
        print('  念：', t)
        print('  字幕：', to_display(t))
        print()
