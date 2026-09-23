# -*- coding: utf-8 -*-
"""
批量生成第2-6讲视频
策略：Windows TTS + PPT图片 + imageio-ffmpeg直接合成
比moviepy更快、内存更省
"""
import os, sys, json, glob, gc, shutil, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))

# 使用完整版ffmpeg（非TRAE精简版）
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

LECTURES = [
    {"dir": "02_控制结构",   "title": "第2讲"},
    {"dir": "03_函数封装",   "title": "第3讲"},
    {"dir": "04_多文件编程", "title": "第4讲"},
    {"dir": "05_指针",       "title": "第5讲"},
    {"dir": "06_数组",       "title": "第6讲"},
]

# ============================================================
# TTS引擎（每次新建，避免COM卡死）
# ============================================================
def tts_generate(text, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for v in voices:
        name_lower = v.name.lower()
        if 'chinese' in name_lower or 'zh' in v.id.lower() or 'huihui' in name_lower:
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 150)
    engine.save_to_file(text, path)
    engine.runAndWait()
    engine.stop()
    del engine
    return os.path.exists(path) and os.path.getsize(path) > 5000

# ============================================================
# PPT导出图片
# ============================================================
def export_images(ppt_path, img_dir):
    os.makedirs(img_dir, exist_ok=True)
    existing = sorted(glob.glob(os.path.join(img_dir, "slide_*.png")))
    if len(existing) >= 8:
        return existing

    import win32com.client, pythoncom
    pythoncom.CoInitialize()
    ppt = win32com.client.DispatchEx('PowerPoint.Application')
    try:
        pres = ppt.Presentations.Open(os.path.abspath(ppt_path), WithWindow=False)
        paths = []
        for i in range(1, pres.Slides.Count + 1):
            p = os.path.join(img_dir, f"slide_{i:02d}.png")
            pres.Slides(i).Export(p, 'PNG', 1280, 720)
            paths.append(p)
        pres.Close()
        return paths
    except Exception as e:
        print(f"  PPT导出失败: {e}")
        return None
    finally:
        ppt.Quit()

# ============================================================
# ffmpeg合成单段视频（图片+音频→视频段）
# ============================================================
def make_segment(img_path, audio_path, out_path):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
        return True
    cmd = [
        FFMPEG, '-y',
        '-loop', '1', '-framerate', '10', '-i', img_path,
        '-i', audio_path,
        '-c:v', 'libx264', '-tune', 'stillimage',
        '-c:a', 'aac', '-b:a', '128k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        '-r', '10',
        out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"    ffmpeg error: {r.stderr[-200:] if r.stderr else 'unknown'}")
    return r.returncode == 0

# ============================================================
# ffmpeg拼接多段视频（concat demuxer）
# ============================================================
def concat_segments(seg_paths, out_path):
    """使用ffmpeg concat demuxer拼接视频段"""
    list_file = os.path.join(os.path.dirname(out_path), "_concat_list.txt")
    with open(list_file, 'w', encoding='utf-8') as f:
        for p in seg_paths:
            ap = os.path.abspath(p).replace('\\', '/')
            f.write(f"file '{ap}'\n")

    cmd = [
        FFMPEG, '-y',
        '-f', 'concat', '-safe', '0',
        '-i', list_file,
        '-c', 'copy',
        out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    os.remove(list_file)
    if r.returncode != 0:
        # concat copy失败时尝试重新编码
        print("  concat copy失败，尝试重新编码...")
        cmd2 = [
            FFMPEG, '-y',
            '-f', 'concat', '-safe', '0',
            '-i', list_file,
            '-c:v', 'libx264', '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            out_path
        ]
        # 重新创建list文件（上面已删除）
        with open(list_file, 'w', encoding='utf-8') as f:
            for p in seg_paths:
                ap = os.path.abspath(p).replace('\\', '/')
                f.write(f"file '{ap}'\n")
        r = subprocess.run(cmd2, capture_output=True, text=True, timeout=300)
        os.remove(list_file)
        if r.returncode != 0:
            print(f"  ffmpeg error: {r.stderr[-200:] if r.stderr else 'unknown'}")
            return False
    return True

# ============================================================
# 生成一讲的完整视频
# ============================================================
def make_lecture_video(lecture):
    ldir = os.path.join(BASE, lecture["dir"])
    ppt_path = os.path.join(ldir, "docs", "课件.pptx")
    script_path = os.path.join(ldir, "video", "讲解脚本.json")
    work_dir = os.path.join(ldir, "video", "_work")
    img_dir = os.path.join(work_dir, "images")
    audio_dir = os.path.join(work_dir, "audio")
    seg_dir = os.path.join(work_dir, "segments")
    output_path = os.path.join(ldir, "video", "讲解.mp4")

    print(f"\n{'='*50}")
    print(f"  {lecture['title']} 视频生成")
    print(f"{'='*50}")

    # Step 1: 导出PPT图片
    print("[1/4] 导出PPT图片...")
    images = export_images(ppt_path, img_dir)
    if not images:
        print("  [FAIL] 图片导出失败，跳过")
        return False
    print(f"  [OK] {len(images)} 张图片")

    # Step 2: 生成语音
    print("[2/4] 生成语音(TTS)...")
    with open(script_path, "r", encoding="utf-8") as f:
        scripts = json.load(f)
    os.makedirs(audio_dir, exist_ok=True)
    audio_paths = []
    for i, text in enumerate(scripts):
        path = os.path.join(audio_dir, f"audio_{i+1:02d}.wav")
        if os.path.exists(path) and os.path.getsize(path) > 30000:
            print(f"  第{i+1}段: 已存在({os.path.getsize(path)//1024}KB)，跳过")
            audio_paths.append(path)
            continue
        print(f"  第{i+1}段: {text[:30]}...", end=" ", flush=True)
        if tts_generate(text, path):
            print(f"[OK {os.path.getsize(path)//1024}KB]")
        else:
            print("[FAIL]")
        audio_paths.append(path)

    # Step 3: 逐段合成
    n = min(len(images), len(audio_paths))
    print(f"[3/4] 逐段合成视频（{n}段）...")
    os.makedirs(seg_dir, exist_ok=True)
    # 清理旧的段文件
    for old in glob.glob(os.path.join(seg_dir, "seg_*.mp4")):
        os.remove(old)
    seg_paths = []
    for i in range(n):
        seg_path = os.path.join(seg_dir, f"seg_{i+1:02d}.mp4")
        print(f"  第{i+1}/{n}段...", end=" ", flush=True)
        if make_segment(images[i], audio_paths[i], seg_path):
            sz = os.path.getsize(seg_path) // 1024
            print(f"[OK {sz}KB]")
            seg_paths.append(seg_path)
        else:
            print("[FAIL]")

    # Step 4: 拼接
    print("[4/4] 拼接最终视频...")
    if concat_segments(seg_paths, output_path):
        size = os.path.getsize(output_path) / (1024*1024)
        print(f"  [OK] {lecture['title']}视频完成: {size:.1f} MB")
        # 清理段文件
        shutil.rmtree(seg_dir, ignore_errors=True)
        return True
    else:
        print("  [FAIL] 拼接失败")
        return False

# ============================================================
# 主函数
# ============================================================
def main():
    print(f"批量生成第2-6讲视频（TTS + ffmpeg合成）")
    print(f"ffmpeg: {FFMPEG}")
    results = {}
    for lec in LECTURES:
        ldir = os.path.join(BASE, lec["dir"])
        script_path = os.path.join(ldir, "video", "讲解脚本.json")
        if not os.path.exists(script_path):
            print(f"\n[SKIP] {lec['title']}讲解脚本不存在")
            continue
        try:
            ok = make_lecture_video(lec)
        except Exception as e:
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()
            ok = False
        results[lec["title"]] = "[OK]" if ok else "[FAIL]"
        gc.collect()

    print(f"\n{'='*50}")
    print("批量视频生成结果：")
    for title, status in results.items():
        print(f"  {title}: {status}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
