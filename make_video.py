# -*- coding: utf-8 -*-
"""
视频生成流水线
PPT幻灯片 → 图片导出 + Voicebox语音合成 → moviepy视频拼接

用法：
  python make_video.py --ppt 课件.pptx --output 讲解.mp4 --script script.json
"""

import os
import sys
import json
import time
import argparse
import requests
import subprocess
from pathlib import Path

# moviepy v2.x 导入方式
try:
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# ============================================================
# 配置
# ============================================================
VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "6a1f7579-b2e1-4ec9-98da-febeaa7f325a"  # 刘东良

# ============================================================
# 第1步：PPT导出为图片（通过PowerPoint COM）
# ============================================================
def export_ppt_slides(ppt_path, output_dir):
    """使用PowerPoint COM自动化将PPT每页导出为PNG图片"""
    import pythoncom
    import win32com.client
    
    pythoncom.CoInitialize()  # 初始化COM
    
    ppt_path = os.path.abspath(ppt_path)
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[1/4] 导出PPT幻灯片为图片...")
    print(f"  PPT: {ppt_path}")
    print(f"  输出: {output_dir}")
    
    # 检查是否已有导出的图片（跳过COM）
    existing = sorted(Path(output_dir).glob("slide_*.png")) if Path(output_dir).exists() else []
    if existing:
        print(f"  ✅ 发现已导出图片 {len(existing)} 张，跳过COM导出")
        return [str(p) for p in existing]
    
    # 启动PowerPoint（使用DispatchEx创建新实例）
    try:
        powerpoint = win32com.client.DispatchEx("PowerPoint.Application")
    except Exception as e:
        print(f"  ❌ PowerPoint启动失败: {e}")
        print(f"  💡 建议：手动运行一次导出，或使用其他方式生成图片")
        return None
    
    try:
        # 打开PPT
        presentation = powerpoint.Presentations.Open(ppt_path, WithWindow=False)
        
        slide_count = presentation.Slides.Count
        print(f"  共 {slide_count} 页幻灯片")
        
        image_paths = []
        for i in range(1, slide_count + 1):
            slide = presentation.Slides(i)
            image_path = os.path.join(output_dir, f"slide_{i:02d}.png")
            
            # 导出为PNG（宽度1920，高度1080）
            slide.Export(image_path, "PNG", 1920, 1080)
            image_paths.append(image_path)
            print(f"    第{i}页 → {os.path.basename(image_path)}")
        
        presentation.Close()
        print(f"  ✅ 导出完成，共 {len(image_paths)} 张图片")
        return image_paths
        
    finally:
        powerpoint.Quit()

# ============================================================
# 第2步：通过Voicebox API生成语音
# ============================================================
def generate_speech(text, output_path, language="zh", model_size="0.6B", engine="qwen"):
    """调用Voicebox API生成语音"""
    
    payload = {
        "profile_id": PROFILE_ID,
        "text": text,
        "language": language,
        "model_size": model_size,
        "engine": engine,
        "personality": False,  # 直接TTS，不需要LLM改写
        "normalize": True,
    }
    
    print(f"    生成语音: {text[:30]}...")
    
    # 发送生成请求
    try:
        resp = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        gen_id = data.get("id")
        status = data.get("status", "unknown")
        
        if status == "completed" and data.get("audio_path"):
            # 直接下载音频
            audio_url = f"{VOICEBOX_URL}/history/{gen_id}/export-audio"
            audio_resp = requests.get(audio_url, timeout=30)
            with open(output_path, "wb") as f:
                f.write(audio_resp.content)
            print(f"    ✅ 音频已保存: {os.path.basename(output_path)}")
            return output_path
        elif status == "generating":
            # 需要轮询等待完成
            print(f"    生成中，等待完成...", end="", flush=True)
            for _ in range(60):  # 最多等5分钟
                time.sleep(5)
                try:
                    status_resp = requests.get(f"{VOICEBOX_URL}/history", timeout=10)
                    items = status_resp.json().get("items", [])
                    for item in items:
                        if item.get("id") == gen_id:
                            if item.get("status") == "completed" and item.get("audio_path"):
                                audio_url = f"{VOICEBOX_URL}/history/{gen_id}/export-audio"
                                audio_resp = requests.get(audio_url, timeout=30)
                                with open(output_path, "wb") as f:
                                    f.write(audio_resp.content)
                                print(f" ✅")
                                return output_path
                            elif item.get("status") == "failed":
                                print(f" ❌ 生成失败")
                                return None
                    print(".", end="", flush=True)
                except:
                    print("!", end="", flush=True)
            print(" 超时")
            return None
        else:
            print(f"    ❌ 状态异常: {status}")
            return None
    except Exception as e:
        print(f"    ❌ 请求失败: {e}")
        return None

def generate_all_audio(scripts, output_dir):
    """为所有脚本生成语音"""
    os.makedirs(output_dir, exist_ok=True)
    audio_paths = []
    
    print(f"\n[2/4] 生成语音（共{len(scripts)}段）...")
    for i, text in enumerate(scripts):
        audio_path = os.path.join(output_dir, f"audio_{i+1:02d}.wav")
        
        # 如果音频已存在且非空，跳过
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            print(f"  第{i+1}段: 已存在，跳过")
            audio_paths.append(audio_path)
            continue
        
        print(f"  第{i+1}段: {text[:40]}...")
        result = generate_speech(text, audio_path)
        if result:
            audio_paths.append(result)
        else:
            print(f"    ⚠️ 语音生成失败，使用空白音频代替")
            # 创建一个2秒的静音音频作为fallback
            create_silent_audio(audio_path, 2.0)
            audio_paths.append(audio_path)
    
    print(f"  ✅ 语音生成完成，共 {len(audio_paths)} 段")
    return audio_paths

def create_silent_audio(path, duration):
    """创建静音WAV文件作为fallback"""
    import wave
    import struct
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    with wave.open(path, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for _ in range(num_samples):
            wav.writeframes(struct.pack('<h', 0))

# ============================================================
# 第3步：合成视频（图片 + 音频 → 视频）
# ============================================================
def make_video(image_paths, audio_paths, output_path, fps=24):
    """将图片和音频合成为视频"""
    print(f"\n[3/4] 合成视频...")
    print(f"  图片: {len(image_paths)} 张")
    print(f"  音频: {len(audio_paths)} 段")
    print(f"  输出: {output_path}")
    
    clips = []
    total_duration = 0
    
    for i, (img_path, audio_path) in enumerate(zip(image_paths, audio_paths)):
        # 获取音频时长
        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
        except:
            duration = 3.0  # 默认3秒
            audio_clip = None
        
        # 创建图片视频片段
        img_clip = ImageClip(img_path, duration=duration)
        
        # 如果有音频，添加音频
        if audio_clip:
            img_clip = img_clip.with_audio(audio_clip)
        
        clips.append(img_clip)
        total_duration += duration
        print(f"  第{i+1}页: {duration:.1f}s")
    
    print(f"  总时长: {total_duration:.1f}s ({total_duration/60:.1f}分钟)")
    
    # 拼接所有片段
    print(f"  拼接视频片段...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 导出视频
    print(f"  导出视频...")
    final_video.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )
    
    # 清理
    for clip in clips:
        clip.close()
    final_video.close()
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  ✅ 视频生成完成: {file_size:.1f} MB")
    return output_path

# ============================================================
# 第4步：验证视频
# ============================================================
def verify_video(video_path):
    """验证视频文件"""
    print(f"\n[4/4] 验证视频...")
    if not os.path.exists(video_path):
        print(f"  ❌ 视频文件不存在")
        return False
    
    size = os.path.getsize(video_path)
    if size < 10000:
        print(f"  ❌ 视频文件太小 ({size} bytes)")
        return False
    
    print(f"  ✅ 视频验证通过")
    print(f"  文件: {video_path}")
    print(f"  大小: {size / (1024 * 1024):.1f} MB")
    return True

# ============================================================
# 主流程
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="PPT视频生成工具")
    parser.add_argument("--ppt", required=True, help="PPT文件路径")
    parser.add_argument("--output", required=True, help="输出视频路径")
    parser.add_argument("--script", help="讲解脚本JSON文件（包含每页的讲解词）")
    parser.add_argument("--skip-audio", action="store_true", help="跳过语音生成（使用静音）")
    parser.add_argument("--workdir", default=None, help="工作目录（临时文件）")
    args = parser.parse_args()
    
    ppt_path = args.ppt
    output_path = args.output
    
    # 工作目录
    if args.workdir:
        workdir = args.workdir
    else:
        workdir = os.path.join(os.path.dirname(output_path), "_video_work")
    os.makedirs(workdir, exist_ok=True)
    
    image_dir = os.path.join(workdir, "images")
    audio_dir = os.path.join(workdir, "audio")
    
    # 加载讲解脚本
    if args.script and os.path.exists(args.script):
        with open(args.script, "r", encoding="utf-8") as f:
            scripts = json.load(f)
        if isinstance(scripts, dict) and "scripts" in scripts:
            scripts = scripts["scripts"]
    else:
        # 如果没有脚本，用文件名作为占位
        scripts = None
    
    # Step 1: 导出PPT图片
    image_paths = export_ppt_slides(ppt_path, image_dir)
    
    # Step 2: 生成语音
    if scripts and not args.skip_audio:
        audio_paths = generate_all_audio(scripts, audio_dir)
    else:
        # 跳过语音，用静音
        print(f"\n[2/4] 跳过语音生成，使用静音")
        audio_paths = []
        for i, img in enumerate(image_paths):
            audio_path = os.path.join(audio_dir, f"audio_{i+1:02d}.wav")
            create_silent_audio(audio_path, 3.0)
            audio_paths.append(audio_path)
        print(f"  ✅ 生成 {len(audio_paths)} 个静音文件")
    
    # 确保图片和音频数量匹配
    if len(image_paths) != len(audio_paths):
        print(f"  ⚠️ 图片({len(image_paths)})和音频({len(audio_paths)})数量不匹配")
        n = min(len(image_paths), len(audio_paths))
        image_paths = image_paths[:n]
        audio_paths = audio_paths[:n]
    
    # Step 3: 合成视频
    make_video(image_paths, audio_paths, output_path)
    
    # Step 4: 验证
    verify_video(output_path)
    
    print(f"\n{'='*50}")
    print(f"🎉 视频生成完成！")
    print(f"   {output_path}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
