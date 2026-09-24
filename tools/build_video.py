# -*- coding: utf-8 -*-
"""
build_video.py —— 全系列讲解视频流水线（字幕 + 语音 + 内容 + 鼠标 同步）

解决了旧流水线的四个问题：
  1) 没有字幕            → 按标点切分讲解词，逐句烧录（硬字幕），同时另存 .srt
  2) 语音与画面不同步     → 每一段幻灯片严格对应一段配音，段落边界就是换页时机
  3) 没有鼠标            → 每段有一个"看点坐标"，鼠标带缓动移动到该点并点击，
                            移动节奏与该段配音时长严格对齐
  4) 片尾没有演示          → 最后一段支持"终端演示"模式：用真实程序输出做打字动画，
                            右侧并列展示源码/命令截图

用法：
    python tools/build_video.py <讲次目录> [--voice clone|tts|auto] [--fps 12]
例：
    python tools/build_video.py "01_你好世界" --voice clone

音频查找顺序：
    <讲次>/video/audio_clone/audio_NN.wav   （克隆音，优先）
    <讲次>/video/_work/audio/audio_NN.wav   （历史音频）
    <讲次>/video/audio_tts/audio_NN.wav     （语音合成，可用 --voice tts 生成）

可选配置：<讲次>/video/video_meta.json
    {
      "cursor": [[x_ratio, y_ratio], ...],   # 每段的鼠标落点（0~1 相对坐标）
      "click_at": [0.55, ...],               # 每段点击发生的时间比例
      "demo_segments": [11],                 # 走"终端演示"模式的段号
      "demo_terminal": ["$ gcc ...", "..."], # 演示终端里逐行打出的内容
      "demo_shots": ["src/hello.c", "..."],  # 右侧展示的截图/源码文件
      "demo_title": "运行演示"
    }
未提供时自动生成一份合理的默认配置（落点沿内容区做规律分布）。
"""
import argparse
import glob
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from _pipelock import acquire as _lock_acquire          # noqa: E402
# 讲稿的两种写法 + "念法→真实写法"的还原，统一放在 subtitle_text，
# 供 build_video / tts_batch / 校验脚本共用。
from subtitle_text import narration, show_text          # noqa: E402,F401

W, H = 1920, 1080
FPS = 12
FONT_R = 'C:/Windows/Fonts/msyh.ttc'
FONT_B = 'C:/Windows/Fonts/msyhbd.ttc'
FONT_C = 'C:/Windows/Fonts/consola.ttf'

FFMPEG = shutil.which('ffmpeg') or 'ffmpeg'
FFPROBE = shutil.which('ffprobe') or 'ffprobe'

# 配色（与 ppt_kit 一致）
INK = (31, 41, 55)
ORANGE = (194, 65, 12)
DARK = (15, 23, 42)

DEFAULT_ZOOM = 0.010      # 极轻微推近；逐帧亚像素变化，绝不做"隔帧跳变"
DEFAULT_JOBS = 5          # 分段并行渲染的进程数（留出 CPU 给并行的语音克隆）


# ============================================================
# 基础工具
# ============================================================
def audio_duration(path):
    out = subprocess.run([FFPROBE, '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except Exception:
        return 0.0


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(f, s):
    return f.getlength(s)


def wrap_cjk(s, f, max_w):
    out, cur = [], ''
    for ch in s:
        if text_w(f, cur + ch) <= max_w:
            cur += ch
        else:
            out.append(cur)
            cur = ch
    if cur:
        out.append(cur)
    return out


def split_subtitles(text, max_chars=24):
    """把一段讲解词切成字幕块：先按标点断句，过长再按字数切。"""
    import re
    parts = [p for p in re.split(r'(?<=[。！？；])', text) if p.strip()]
    chunks = []
    for p in parts:
        p = p.strip()
        while len(p) > max_chars * 1.6:
            cut = p.rfind('，', 0, int(max_chars * 1.2))
            if cut < max_chars * 0.6:
                cut = int(max_chars * 1.1)
            chunks.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        if p:
            chunks.append(p)
    # 相邻过短的块合并
    merged = []
    for c in chunks:
        if merged and len(merged[-1]) + len(c) <= max_chars * 1.35:
            merged[-1] += c
        else:
            merged.append(c)
    return merged


def ease(t):
    """缓入缓出"""
    return 3 * t * t - 2 * t * t * t


_cursor_cache = {}


def cursor(size=40):
    if size in _cursor_cache:
        return _cursor_cache[size]
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    k = size / 40.0
    pts = [(4 * k, 2 * k), (4 * k, 30 * k), (11 * k, 23 * k), (16 * k, 35 * k),
           (21 * k, 32 * k), (16 * k, 21 * k), (26 * k, 20 * k)]
    # 阴影
    d.polygon([(x + 2, y + 2) for x, y in pts], fill=(0, 0, 0, 90))
    d.polygon(pts, fill=(255, 255, 255, 255), outline=(20, 20, 20, 255))
    _cursor_cache[size] = img
    return img


def draw_subtitle(frame, text, f_sub, bottom_pad=64):
    """在画面底部画一条硬字幕（半透明圆角底 + 白字）。"""
    d = ImageDraw.Draw(frame, 'RGBA')
    lines = wrap_cjk(text, f_sub, W - 380)
    lh = f_sub.size + 14
    box_h = lh * len(lines) + 26
    y0 = H - bottom_pad - box_h
    x0, x1 = 190, W - 190
    d.rounded_rectangle([x0, y0, x1, y0 + box_h], radius=14, fill=(17, 24, 39, 205))
    for i, ln in enumerate(lines):
        tw = text_w(f_sub, ln)
        d.text(((W - tw) / 2, y0 + 13 + i * lh), ln, font=f_sub, fill=(255, 255, 255))


def draw_progress(frame, ratio):
    d = ImageDraw.Draw(frame, 'RGBA')
    d.rectangle([0, H - 7, W, H], fill=(40, 48, 62, 120))
    d.rectangle([0, H - 7, int(W * ratio), H], fill=(249, 115, 22, 235))


# ============================================================
# 分段渲染
# ============================================================
def encode_frames(frame_iter, out_mp4, audio, fps=FPS, tempo=1.0):
    """
    把逐帧图像直接通过管道喂给 ffmpeg（不落盘中间帧）。
    中间无声视频固定复用同一个文件名、不删除——沙箱对"批量删除"有拦截，
    每段删一次文件会累积到阈值后中断整批任务。
    """
    # 关键：临时文件名必须跟本段绑定。并行渲染时若多个进程共用一个名字，
    # 会互相覆盖，产出时长被截断的分段（曾导致第3段只有 14 秒而不是 24 秒）。
    silent = out_mp4 + '.silent.mp4'
    p = subprocess.Popen(
        [FFMPEG, '-y', '-loglevel', 'error',
         '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(fps),
         '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
         '-threads', '2',     # 并行渲染时留给同伴；单段也够用，避免线程超售反而变慢
         '-pix_fmt', 'yuv420p', '-r', str(fps), silent],
        stdin=subprocess.PIPE)
    for fr in frame_iter:
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError('ffmpeg 编码失败')
    cmd = [FFMPEG, '-y', '-loglevel', 'error', '-i', silent, '-i', audio]
    if abs(tempo - 1.0) > 1e-3:
        cmd += ['-filter:a', 'atempo=%.4f' % tempo]
    cmd += ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', out_mp4]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_mp4



def render_segment(slide_png, chunks, duration, out_mp4, audio, cursor_path, click_at,
                   fps=FPS, tmpdir=None, seed=0, tempo=1.0, zoom=DEFAULT_ZOOM):
    """
    渲染一段：幻灯片 + 鼠标缓动 + 硬字幕 → 无声 mp4，再与音频合成。
    cursor_path: [(t0_ratio, x, y), ...] 鼠标关键帧（0~1 相对坐标）

    zoom：极轻微推近的幅度。**逐帧亚像素变换**（仿射系数是浮点），
          上一版为了省算力只对偶数帧做整数裁剪缩放，结果画面每两帧跳一次，
          投影/播放时就是肉眼可见的"抖"。这里改成每帧都做、且不取整。
    """
    base = Image.open(slide_png).convert('RGB')
    if base.size != (W, H):
        base = base.resize((W, H), Image.LANCZOS)

    n = max(2, int(round(duration * fps)))
    f_sub = font(FONT_B, 40)
    cur_img = cursor(44)

    # 字幕时间轴：按字数分配
    total_chars = sum(len(c) for c in chunks) or 1
    tl, t = [], 0.0
    for c in chunks:
        seg = duration * len(c) / total_chars
        tl.append((c, t, t + seg))
        t += seg
    if tl:
        tl[-1] = (tl[-1][0], tl[-1][1], duration)

    def gen():
        for fi in range(n):
            tt = fi / fps
            ratio = fi / (n - 1.0)
            frame = base.copy()

            # 极轻微推近：每帧都用浮点仿射变换（亚像素），画面平滑不抖
            if zoom > 0:
                inv = 1.0 / (1.0 + zoom * ratio)      # 1 → 略小于 1，缓慢推进
                frame = frame.transform(
                    (W, H), Image.AFFINE,
                    (inv, 0.0, (W - W * inv) / 2.0,
                     0.0, inv, (H - H * inv) / 2.0),
                    resample=Image.BILINEAR)

            # 字幕
            cur_txt = ''
            for c, a, b in tl:
                if a <= tt < b:
                    cur_txt = c
                    break
            if cur_txt:
                draw_subtitle(frame, cur_txt, f_sub)

            # 鼠标：在关键帧之间缓动
            px, py = cursor_path[0][1], cursor_path[0][2]
            for i in range(len(cursor_path) - 1):
                t0, x0, y0 = cursor_path[i]
                t1, x1, y1 = cursor_path[i + 1]
                if t0 <= ratio <= t1:
                    k = ease((ratio - t0) / max(1e-6, (t1 - t0)))
                    px, py = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
                    break
            else:
                if ratio > cursor_path[-1][0]:
                    px, py = cursor_path[-1][1], cursor_path[-1][2]

            cx, cy = int(px * W), int(py * H)
            # 点击涟漪
            if click_at is not None and abs(ratio - click_at) < 0.10:
                dt = abs(ratio - click_at) / 0.10
                r = int(16 + 46 * dt)
                d = ImageDraw.Draw(frame, 'RGBA')
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          outline=(249, 115, 22, int(200 * (1 - dt))), width=5)

            frame.paste(cur_img, (cx, cy), cur_img)
            draw_progress(frame, ratio)
            yield frame

    return encode_frames(gen(), out_mp4, audio, fps, tempo)


def render_demo_segment(slide_png, chunks, duration, out_mp4, audio,
                        term_lines, shot_paths, title='运行演示', fps=FPS, tmpdir=None,
                        tempo=1.0):
    """
    片尾演示段：幻灯片做背景，上面盖一个"终端窗口"逐行打字，
    右侧并列展示源码/命令的截图卡片。
    """
    base = Image.open(slide_png).convert('RGB').resize((W, H), Image.LANCZOS)
    if base.size != (W, H):
        base = base.resize((W, H), Image.LANCZOS)

    n = max(2, int(round(duration * fps)))
    f_sub = font(FONT_B, 40)
    # 终端行含中文（如"=== 初始化账务核心 ==="），Consolas 没有中文字形，
    # 会渲染成一排豆腐块 —— 必须用中文字体（微软雅黑）。
    f_term = font(FONT_R, 24)
    f_title = font(FONT_B, 24)
    f_shot = font(FONT_R, 15)      # 源码卡片含中文注释，必须用中文字体

    # 终端窗口几何
    tw, th = 1150, 745
    tx, ty = 68, 168

    # 右侧截图卡片：取真实存在的文件
    shots = []
    for p in (shot_paths or [])[:2]:
        fp = p if os.path.isabs(p) else os.path.join(ROOT, p)
        if os.path.exists(fp):
            shots.append(fp)

    # 终端逐行打字的时间点
    total_chars = sum(len(l) for l in term_lines) or 1
    type_span = duration * 0.82
    marks, acc = [], 0
    for l in term_lines:
        marks.append((acc / total_chars * type_span, l))
        acc += len(l) + 3

    # 字幕时间轴
    total_sub = sum(len(c) for c in chunks) or 1
    tl, t = [], 0.0
    for c in chunks:
        tl.append((c, t, t + duration * len(c) / total_sub))
        t += duration * len(c) / total_sub
    if tl:
        tl[-1] = (tl[-1][0], tl[-1][1], duration)

    def gen():
        for fi in range(n):
            tt = fi / fps
            frame = base.copy()
            d = ImageDraw.Draw(frame, 'RGBA')
            # 底页要彻底盖住：半透明遮罩会让幻灯片文字透出来，和终端叠在一起很脏
            d.rectangle([0, 0, W, H], fill=(255, 255, 255, 255))

            d.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=14, fill=(15, 23, 42, 255))
            d.rounded_rectangle([tx, ty, tx + tw, ty + 46], radius=14, fill=(30, 41, 59, 255))
            d.text((tx + 20, ty + 10), title, font=f_title, fill=(253, 186, 116))
            for i, col in enumerate([(239, 68, 68), (245, 158, 11), (34, 197, 94)]):
                d.ellipse([tx + tw - 96 + i * 26, ty + 15, tx + tw - 82 + i * 26, ty + 29], fill=col)

            shown = [line for mark, line in marks if tt >= mark]
            partial = ''
            for i, (mark, line) in enumerate(marks):
                nxt = marks[i + 1][0] if i + 1 < len(marks) else duration * 0.95
                if mark <= tt < nxt:
                    k = (tt - mark) / max(1e-6, (nxt - mark))
                    partial = line[:max(1, int(len(line) * min(1.0, k * 1.6)))]
                    break

            ly = ty + 66
            for line in shown[-16:]:
                col = (134, 239, 172) if line.startswith('$') or line.startswith('>') else (230, 237, 247)
                d.text((tx + 22, ly), line, font=f_term, fill=col)
                ly += 32
            if partial:
                d.text((tx + 22, ly), partial, font=f_term, fill=(230, 237, 247))
                if int(tt * 2) % 2 == 0:
                    pw = text_w(f_term, partial)
                    d.rectangle([tx + 24 + pw, ly + 2, tx + 24 + pw + 13, ly + 26], fill=(230, 237, 247))

            sx, sy, sw, sh = tx + tw + 34, ty, W - (tx + tw) - 102, 352
            for i, sp in enumerate(shots):
                y = sy + i * (sh + 24)
                d.rounded_rectangle([sx, y, sx + sw, y + sh], radius=12, fill=(241, 245, 249, 255),
                                    outline=(203, 213, 225, 255))
                d.text((sx + 14, y + 8), os.path.basename(sp), font=f_title, fill=ORANGE)
                try:
                    txt = open(sp, encoding='utf-8', errors='ignore').read().split('\n')[:13]
                except Exception:
                    txt = []
                for j, line in enumerate(txt):
                    d.text((sx + 14, y + 48 + j * 19), line[:62], font=f_shot, fill=INK)

            for c, a, b in tl:
                if a <= tt < b:
                    draw_subtitle(frame, c, f_sub)
                    break
            draw_progress(frame, fi / (n - 1.0))
            yield frame

    return encode_frames(gen(), out_mp4, audio, fps, tempo)


# ============================================================
# 主流程
# ============================================================
def _render_task(task):
    """
    渲染一个分段（供多进程并行调用）。
    单讲 18 段串行要 40 多分钟，20 核机器上并行跑能把整批时间压到 1/4 左右。
    """
    (seg_out, slide, chunks, dur_eff, audio, is_demo, cursor_path, click,
     demo_lines, demo_shots, demo_title, fps, tempo, zoom) = task
    if is_demo:
        render_demo_segment(slide, chunks, dur_eff, seg_out, audio,
                            demo_lines, demo_shots, demo_title, fps=fps, tempo=tempo)
    else:
        render_segment(slide, chunks, dur_eff, seg_out, audio, cursor_path, click,
                       fps=fps, tempo=tempo, zoom=zoom)
    return seg_out


def default_meta(nseg):
    """默认鼠标落点：沿内容区做规律分布（避免"鼠标乱飘"）。"""
    anchors = [(0.50, 0.55), (0.30, 0.42), (0.70, 0.42), (0.50, 0.62),
               (0.26, 0.62), (0.74, 0.62), (0.50, 0.36), (0.34, 0.52),
               (0.66, 0.52), (0.50, 0.70), (0.30, 0.36), (0.70, 0.36)]
    cur = [anchors[i % len(anchors)] for i in range(nseg)]
    return {'cursor': cur, 'click_at': [0.55] * nseg, 'demo_segments': []}


def find_audio(vdir, i, prefix='audio_', only=None):
    subs = (only,) if only else ('audio_clone', 'audio_tts', '_work/audio')
    for sub in subs:
        p = os.path.join(vdir, sub, '%s%02d.wav' % (prefix, i))
        if os.path.exists(p) and os.path.getsize(p) > 40 * 1024:
            return p
    return None


def pick_audio_dir(vdir, nseg, forced=None):
    """
    配音来源必须"成套"——不能出现前 10 段克隆音、后 8 段合成音的混音视频
    （上一轮有残留任务就是这样，做出了 7 分钟、半克隆半合成的第2讲）。
    做法：按优先级挑第一个"nseg 段全齐"的目录；一个都不齐就返回缺失清单。

    返回 (sub_dir 或 None, 缺失的段号列表)
    """
    subs = (forced,) if forced else ('audio_clone', 'audio_tts', '_work/audio')
    best = None
    for sub in subs:
        miss = [i + 1 for i in range(nseg) if not find_audio(vdir, i + 1, only=sub)]
        if not miss:
            return sub, []
        if best is None or len(miss) < len(best[1]):
            best = (sub, miss)
    return None, (best[1] if best else list(range(1, nseg + 1)))



def _pick_dir(hits):
    """
    同名编号可能有遗留目录（例如 02_函数封装 是旧编号遗留，现行的第2讲是 02_控制结构）。
    优先级：有 讲解脚本.json 的 > 有 课件.pptx 的 > 其余，避免跑到废弃目录上。
    """
    for probe in (os.path.join('video', '讲解脚本.json'), os.path.join('docs', '课件.pptx')):
        good = [h for h in hits if os.path.exists(os.path.join(h, probe))]
        if good:
            return sorted(good)[0]
    return sorted(hits)[0]

def resolve_lecture(key):
    """
    把命令行参数解析成讲次目录。
    Windows/Git Bash 下命令行传中文会乱码，所以这里支持用 ASCII 编号：
        "01" / "1" / "01_你好世界" 都可以
    """
    key = str(key).strip()
    if os.path.isdir(key):
        return os.path.abspath(key)
    cand = os.path.join(ROOT, key)
    if os.path.isdir(cand):
        return cand
    num = key.zfill(2) if key.isdigit() else key
    hits = [d for d in glob.glob(os.path.join(ROOT, '*'))
            if os.path.isdir(d) and os.path.basename(d).startswith(num[:2]) and '_' in os.path.basename(d)]
    hits = [d for d in hits if os.path.basename(d)[:2] == num[:2]]
    if len(hits) >= 1:
        return _pick_dir(hits)
    raise SystemExit('找不到讲次目录：%s' % key)


def build(lecture_dir, voice='auto', fps=FPS, only=None, audio_dir=None, out_name=None,
          jobs=DEFAULT_JOBS):
    # 流水线互斥：避免"上一轮会话的残留循环"和新任务同时写同一批产物
    if not _lock_acquire('build_video'):
        return None
    ldir = resolve_lecture(lecture_dir) if not os.path.isabs(lecture_dir) else lecture_dir
    name = os.path.basename(ldir.rstrip('\\/'))
    vdir = os.path.join(ldir, 'video')
    img_dir = os.path.join(vdir, '_work', 'v6images')
    if not glob.glob(os.path.join(img_dir, 'slide_*.png')):
        img_dir = os.path.join(vdir, '_work', 'images')

    script = json.load(open(os.path.join(vdir, '讲解脚本.json'), encoding='utf-8'))
    slides = sorted(glob.glob(os.path.join(img_dir, 'slide_*.png')))
    meta_p = os.path.join(vdir, 'video_meta.json')
    meta = json.load(open(meta_p, encoding='utf-8')) if os.path.exists(meta_p) else default_meta(len(script))

    print('=' * 62)
    print('  %s  讲解视频' % name)
    print('  幻灯片 %d 张 ｜ 讲解词 %d 段 ｜ %d fps' % (len(slides), len(script), fps))
    print('=' * 62)

    n = min(len(slides), len(script))
    if only:
        idxs = [int(x) - 1 for x in str(only).split(',')]
    else:
        idxs = list(range(n))
        # 硬门禁：配音必须成套。否则会做出"前 10 段克隆音 + 后 8 段合成音"
        # 或者缺段的半截视频（上一轮残留任务真做出过 7 分钟的第2讲）。
        sub_dir, missing = pick_audio_dir(vdir, n, audio_dir)
        if sub_dir is None:
            print('  [拒绝生成] 配音不齐全，最近的目录 %s 还缺第 %s 段。'
                  % (audio_dir or 'audio_clone/audio_tts', missing))
            print('  请先用 tools/run_clone.py 或 tools/tts_batch.py 补齐，再合成视频。')
            return None
        audio_dir = sub_dir
        print('  配音来源：%s（%d/%d 段齐全）' % (sub_dir, n, n))

    # 时长控制：验收区间 5~9 分钟（用户明确要求）。超过 9 分钟则全片轻微提速
    # （atempo 只改语速、不改变音调），上限 1.18 倍，保证听感自然。
    durs = {}
    for i in idxs:
        a = find_audio(vdir, i + 1, only=audio_dir)
        if a:
            durs[i] = audio_duration(a)
    total = sum(durs.values())
    # 时长控制：验收区间 5~13 分钟。只有超过 13 分钟才轻微提速（atempo 不改音调），
    # 否则保留配音的自然语速 —— 语速被拉快听起来会不清楚。
    target = 780.0                  # 13 分钟
    tempo = min(1.15, total / target) if total > target else 1.0
    if tempo > 1.0:
        print('  总时长 %.1f 分钟 > 13 分钟 → 全片轻微提速 %.2f 倍，预计 %.1f 分钟'
              % (total / 60, tempo, total / tempo / 60))

    seg_dir = os.path.join(vdir, '_work', 'segments_v6')
    os.makedirs(seg_dir, exist_ok=True)
    segs = []
    timeline = []
    t_cursor = 0.0

    # 先把所有分段的任务组装好（顺序即最终拼接顺序），再决定串行还是并行渲染
    seg_meta = []          # [(idx, chunks, dur_eff), ...] 用于字幕时间轴
    tasks = []
    for i in idxs:
        audio = find_audio(vdir, i + 1, only=audio_dir)
        if not audio:
            print('  [跳过] 第%d段 缺少音频' % (i + 1))
            continue
        dur = durs.get(i) or audio_duration(audio)
        dur_eff = dur / tempo          # 提速后的实际时长，帧数与字幕轴都按它算
        # 字幕用"真实写法"（与投影页面上的代码/符号一致），配音仍用原稿
        chunks = split_subtitles(show_text(script[i]))
        seg_out = os.path.join(seg_dir, 'seg_%02d.mp4' % (i + 1))

        is_demo = (i + 1) in meta.get('demo_segments', [])
        if is_demo:
            path, click = None, None
            demo_lines = meta.get('demo_terminal') or ['$ ./demo']
            demo_shots = meta.get('demo_shots') or []
            demo_title = meta.get('demo_title', '运行演示')
        else:
            target = meta['cursor'][i] if i < len(meta.get('cursor', [])) else (0.5, 0.55)
            path = [(0.0, 0.62, 0.80), (0.22, target[0], target[1]), (1.0, target[0], target[1])]
            click = meta.get('click_at', [None] * n)[i] if i < len(meta.get('click_at', [])) else 0.55
            demo_lines = demo_shots = demo_title = None

        tasks.append((seg_out, slides[i], chunks, dur_eff, audio, is_demo, path, click,
                      demo_lines, demo_shots, demo_title, fps, tempo,
                      float(meta.get('zoom', DEFAULT_ZOOM))))
        seg_meta.append((i, seg_out, chunks, dur_eff, dur, is_demo, os.path.basename(audio)))

    if not tasks:
        print('  [失败] 没有任何可合成的片段')
        return None

    def _seg_ok(m):
        """已存在的分段若时长对得上就直接复用，省掉重复渲染。"""
        _i, seg_out, _c, dur_eff, _d, _demo, _a = m
        if not os.path.exists(seg_out) or os.path.getsize(seg_out) < 50 * 1024:
            return False
        try:
            return abs(audio_duration(seg_out) - dur_eff) <= 0.8
        except Exception:
            return False

    reuse = [m for m in seg_meta if _seg_ok(m)]
    todo = [t for t, m in zip(tasks, seg_meta) if m not in reuse]
    if reuse:
        print('  复用已合格分段 %d 段，需渲染 %d 段' % (len(reuse), len(todo)))

    if jobs and jobs > 1 and len(todo) > 1:
        from concurrent.futures import ProcessPoolExecutor
        print('  并行渲染 %d 段（%d 进程）…' % (len(todo), jobs))
        with ProcessPoolExecutor(max_workers=jobs) as ex:
            list(ex.map(_render_task, todo))
    else:
        for t in todo:
            _render_task(t)

    # ---- 质量闸：每段成片时长必须和它的配音时长对得上 ----
    # 并行渲染一旦出岔子（临时文件抢名、进程被杀），分段会被悄悄截断，
    # 拼接出来的成片就会出现"字幕还在、声音已经没了"的错位。
    def _bad_segments():
        out = []
        for (i, seg_out, chunks, dur_eff, dur, is_demo, aname), t in zip(seg_meta, tasks):
            if not os.path.exists(seg_out) or os.path.getsize(seg_out) < 50 * 1024:
                out.append((i, t, '文件缺失或过小'))
                continue
            try:
                real = audio_duration(seg_out)
            except Exception:
                real = 0.0
            if abs(real - dur_eff) > 0.8:
                out.append((i, t, '实际 %.2fs ≠ 应得 %.2fs' % (real, dur_eff)))
        return out

    bad = _bad_segments()
    if bad:
        print('  [质检] %d 段时长不符，改为串行重渲染：' % len(bad))
        for i, t, why in bad:
            print('     第%02d段 %s' % (i + 1, why))
            try:
                _render_task(t)
            except Exception as e:
                print('     第%02d段 重渲染异常：%s' % (i + 1, e))
    bad2 = _bad_segments()
    if bad2:
        print('  [失败] 以下分段仍然不达标，已中止拼接：%s'
              % [i + 1 for i, t, why in bad2])
        return None

    segs = []
    for (i, seg_out, chunks, dur_eff, dur, is_demo, aname) in seg_meta:
        print('  第%02d段%s %.1fs  %s' % (i + 1, ' [演示]' if is_demo else '', dur, aname))
        segs.append(seg_out)
        # 字幕时间轴（累计）
        csum = sum(len(c) for c in chunks) or 1
        for c in chunks:
            d = dur_eff * len(c) / csum
            timeline.append((t_cursor, t_cursor + d, c))
            t_cursor += d

    if not segs:
        print('  [失败] 没有任何可合成的片段')
        return None

    lst = os.path.join(seg_dir, '_concat.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for p in segs:
            f.write("file '%s'\n" % os.path.abspath(p).replace('\\', '/'))
    out = os.path.join(vdir, out_name or '讲解.mp4')
    if only and not out_name:
        out = os.path.join(vdir, '_work', '试片.mp4')
        print('  [提示] 带 --only 属试片，输出到 _work/试片.mp4，不覆盖正式成片')
    r = subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                        '-i', lst, '-c', 'copy', out], capture_output=True, text=True)
    if r.returncode != 0:
        r = subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                            '-i', lst, '-c:v', 'libx264', '-crf', '20', '-c:a', 'aac', out],
                           capture_output=True, text=True)
    if r.returncode != 0:
        print('  [失败] 拼接出错：', r.stderr[-300:])
        return None

    # 外挂字幕（试片就配试片的字幕，别把正式成片的 .srt 冲掉）
    def ts(x):
        hh, mm = int(x // 3600), int((x % 3600) // 60)
        ss, ms = int(x % 60), int((x - int(x)) * 1000)
        return '%02d:%02d:%02d,%03d' % (hh, mm, ss, ms)
    srt = os.path.splitext(out)[0] + '.srt'
    with open(srt, 'w', encoding='utf-8') as f:
        for k, (a, b, c) in enumerate(timeline, 1):
            f.write('%d\n%s --> %s\n%s\n\n' % (k, ts(a), ts(b), c))

    size = os.path.getsize(out) / 1024 / 1024
    print('-' * 62)
    print('  ✅ 视频完成：%s（%.1f MB，%.1f 分钟）' % (out, size, t_cursor / 60))
    print('  ✅ 字幕文件：%s（%d 条）' % (srt, len(timeline)))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('lecture')
    ap.add_argument('--voice', default='auto', choices=['auto', 'clone', 'tts'])
    ap.add_argument('--fps', type=int, default=FPS)
    ap.add_argument('--only', default=None, help='只做指定段，如 11,12')
    ap.add_argument('--audio-dir', default=None,
                    help='只在这个子目录里找音频（audio_clone / audio_tts / _work/audio）')
    ap.add_argument('--out', default=None, help='输出文件名（默认 讲解.mp4）')
    ap.add_argument('--jobs', type=int, default=DEFAULT_JOBS,
                    help='分段并行渲染的进程数，1 表示串行（默认 %d）' % DEFAULT_JOBS)
    a = ap.parse_args()
    build(a.lecture, a.voice, a.fps, a.only, a.audio_dir, a.out, a.jobs)
