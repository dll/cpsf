# -*- coding: utf-8 -*-
"""
第2讲视频生成脚本
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from make_video import export_ppt_slides, generate_speech, make_video, verify_video, create_silent_audio
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(BASE_DIR, "02_控制结构", "video", "讲解脚本.json")
PPT_PATH = os.path.join(BASE_DIR, "02_控制结构", "docs", "课件.pptx")
WORK_DIR = os.path.join(BASE_DIR, "02_控制结构", "video", "_work")
IMAGE_DIR = os.path.join(WORK_DIR, "images")
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
OUTPUT_PATH = os.path.join(BASE_DIR, "02_控制结构", "video", "讲解.mp4")

def generate_all_audio():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        scripts = json.load(f)
    
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_paths = []
    
    print(f"\n[2/4] 生成语音（共{len(scripts)}段）...")
    for i, text in enumerate(scripts):
        audio_path = os.path.join(AUDIO_DIR, f"audio_{i+1:02d}.wav")
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            print(f"  第{i+1}段: 已存在，跳过")
            audio_paths.append(audio_path)
            continue
        print(f"  第{i+1}段: {text[:30]}...")
        result = generate_speech(text, audio_path)
        if result:
            audio_paths.append(result)
        else:
            create_silent_audio(audio_path, 3.0)
            audio_paths.append(audio_path)
    return audio_paths

def main():
    print("=" * 60)
    print("  第2讲视频生成流水线")
    print("=" * 60)
    
    image_paths = export_ppt_slides(PPT_PATH, IMAGE_DIR)
    if not image_paths:
        print("❌ PPT图片导出失败")
        return
    
    audio_paths = generate_all_audio()
    make_video(image_paths, audio_paths, OUTPUT_PATH)
    verify_video(OUTPUT_PATH)
    
    print(f"\n{'='*60}")
    print(f"🎉 第2讲视频生成完成！")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
