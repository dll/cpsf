# -*- coding: utf-8 -*-
"""
第1讲视频生成脚本
读取讲解脚本JSON → 逐段生成语音 → 合成最终视频
"""

import os
import json
import time
import requests
import sys

# 导入make_video的函数
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from make_video import export_ppt_slides, generate_speech, make_video, verify_video, create_silent_audio

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "6a1f7579-b2e1-4ec9-98da-febeaa7f325a"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(BASE_DIR, "01_你好世界", "video", "讲解脚本.json")
PPT_PATH = os.path.join(BASE_DIR, "01_你好世界", "docs", "课件.pptx")
WORK_DIR = os.path.join(BASE_DIR, "01_你好世界", "video", "_work")
IMAGE_DIR = os.path.join(WORK_DIR, "images")
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
OUTPUT_PATH = os.path.join(BASE_DIR, "01_你好世界", "video", "讲解_v5.mp4")

def generate_all_audio_from_script():
    """从讲解脚本生成所有语音"""
    # 读取脚本
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        scripts = json.load(f)
    
    print(f"\n[2/4] 从脚本生成语音（共{len(scripts)}段）...")
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    audio_paths = []
    for i, text in enumerate(scripts):
        audio_path = os.path.join(AUDIO_DIR, f"audio_{i+1:02d}.wav")
        
        # 已存在且非空则跳过
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            print(f"  第{i+1}段: 已存在({os.path.getsize(audio_path)//1024}KB)，跳过")
            audio_paths.append(audio_path)
            continue
        
        print(f"  第{i+1}段: {text[:30]}...")
        result = generate_speech(text, audio_path)
        if result:
            audio_paths.append(result)
            print(f"    ✅ 完成 ({os.path.getsize(audio_path)//1024}KB)")
        else:
            print(f"    ⚠️ 失败，用静音代替")
            create_silent_audio(audio_path, 3.0)
            audio_paths.append(audio_path)
    
    return audio_paths

def main():
    print("=" * 60)
    print("  第1讲视频生成流水线")
    print("=" * 60)
    
    # Step 1: 导出PPT图片
    image_paths = export_ppt_slides(PPT_PATH, IMAGE_DIR)
    if not image_paths:
        print("❌ PPT图片导出失败")
        return
    
    # Step 2: 从脚本生成语音
    audio_paths = generate_all_audio_from_script()
    
    # Step 3: 合成视频
    make_video(image_paths, audio_paths, OUTPUT_PATH)
    
    # Step 4: 验证
    verify_video(OUTPUT_PATH)
    
    print(f"\n{'='*60}")
    print(f"🎉 第1讲视频生成完成！")
    print(f"   {OUTPUT_PATH}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
