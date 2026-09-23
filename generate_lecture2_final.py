# -*- coding: utf-8 -*-
"""
第2讲视频生成脚本
策略：前6段用Voicebox（您的声纹），后6段用Windows TTS
"""
import os, sys, json, time, requests
import pyttsx3
from PIL import Image
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_video import export_ppt_slides, create_silent_audio

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "6a1f7579-b2e1-4ec9-98da-febeaa7f325a"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "02_控制结构")
SCRIPT_PATH = os.path.join(BASE, "video", "讲解脚本.json")
PPT_PATH = os.path.join(BASE, "docs", "课件.pptx")
WORK_DIR = os.path.join(BASE, "video", "_work")
IMAGE_DIR = os.path.join(WORK_DIR, "images")
IMAGE_SMALL_DIR = os.path.join(WORK_DIR, "images_small")
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
OUTPUT_PATH = os.path.join(BASE, "video", "讲解.mp4")

def voicebox_generate(text, audio_path):
    """用Voicebox生成语音"""
    payload = {"profile_id": PROFILE_ID, "text": text, "language": "zh",
               "model_size": "0.6B", "engine": "qwen", "personality": False, "normalize": True}
    try:
        resp = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=30)
        resp.raise_for_status()
        gen_id = resp.json().get("id")
        print(f"      ID: {gen_id}")
        # 轮询等待
        for _ in range(48):  # 最多4分钟
            time.sleep(5)
            try:
                history = requests.get(f"{VOICEBOX_URL}/history", timeout=10).json()
                for item in history.get("items", []):
                    if item.get("id") == gen_id:
                        if item.get("status") == "completed":
                            audio_resp = requests.get(f"{VOICEBOX_URL}/history/{gen_id}/export-audio", timeout=30)
                            with open(audio_path, "wb") as f:
                                f.write(audio_resp.content)
                            print(f"      ✅ ({item.get('duration', 0):.1f}s)")
                            return True
                        elif item.get("status") == "failed":
                            print(f"      ❌")
                            return False
                print(".", end="", flush=True)
            except:
                print("!", end="", flush=True)
        print(" 超时")
        return False
    except Exception as e:
        print(f"      ❌ {e}")
        return False

def tts_generate(text, audio_path):
    """用Windows TTS生成语音"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for v in voices:
        if 'chinese' in v.name.lower() or 'zh' in v.id.lower() or 'huihui' in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 160)
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    return os.path.getsize(audio_path) > 10000

def main():
    print("=" * 60)
    print("  第2讲视频生成")
    print("=" * 60)
    
    # 读取脚本
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        scripts = json.load(f)
    print(f"共 {len(scripts)} 段讲解词")
    
    # Step 1: 导出PPT图片
    print("\n[1/4] 导出PPT图片...")
    images = export_ppt_slides(PPT_PATH, IMAGE_DIR)
    if not images:
        print("❌ PPT导出失败")
        return
    
    # Step 2: 生成语音（前6段Voicebox，后6段TTS）
    print(f"\n[2/4] 生成语音...")
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_paths = []
    
    for i, text in enumerate(scripts):
        audio_path = os.path.join(AUDIO_DIR, f"audio_{i+1:02d}.wav")
        
        # 已存在且大于100KB则跳过
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 100000:
            print(f"  第{i+1}段: 已存在({os.path.getsize(audio_path)//1024}KB)，跳过")
            audio_paths.append(audio_path)
            continue
        
        print(f"  第{i+1}段: {text[:30]}...")
        
        if i < 6:
            # 前6段用Voicebox
            print(f"      [Voicebox]")
            success = voicebox_generate(text, audio_path)
            if not success:
                print(f"      回退到TTS")
                tts_generate(text, audio_path)
        else:
            # 后6段用TTS
            print(f"      [TTS]")
            tts_generate(text, audio_path)
        
        size = os.path.getsize(audio_path) // 1024
        print(f"      大小: {size}KB")
        audio_paths.append(audio_path)
    
    # Step 3: 缩小图片 + 合成视频
    print(f"\n[3/4] 合成视频...")
    os.makedirs(IMAGE_SMALL_DIR, exist_ok=True)
    
    clips = []
    total_dur = 0
    for i in range(len(images)):
        # 缩小图片到1280x720
        small_path = os.path.join(IMAGE_SMALL_DIR, f"slide_{i+1:02d}.png")
        img = Image.open(images[i])
        img = img.resize((1280, 720), Image.LANCZOS)
        img.save(small_path, 'PNG')
        
        audio = AudioFileClip(audio_paths[i])
        dur = audio.duration
        total_dur += dur
        img_clip = ImageClip(small_path, duration=dur).with_audio(audio)
        clips.append(img_clip)
        print(f"  第{i+1}页: {dur:.1f}s")
    
    print(f"  总时长: {total_dur:.1f}s ({total_dur/60:.1f}分钟)")
    
    print("  拼接中...")
    final = concatenate_videoclips(clips, method="compose")
    
    print("  导出视频...")
    final.write_videofile(OUTPUT_PATH, fps=10, codec="libx264", audio_codec="aac", bitrate="800k", logger=None)
    
    for c in clips:
        c.close()
    final.close()
    
    # Step 4: 验证
    print(f"\n[4/4] 验证...")
    size = os.path.getsize(OUTPUT_PATH) / (1024*1024)
    print(f"  ✅ 视频生成完成: {size:.1f} MB")
    print(f"\n{'='*60}")
    print(f"🎉 第2讲视频生成完成！")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
