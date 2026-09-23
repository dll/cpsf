# -*- coding: utf-8 -*-
"""
Voicebox语音批量生成脚本
提交生成请求 → 轮询等待 → 下载音频
"""

import os
import json
import time
import requests

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "6a1f7579-b2e1-4ec9-98da-febeaa7f325a"

def submit_generation(text, language="zh"):
    """提交语音生成请求，返回任务ID"""
    payload = {
        "profile_id": PROFILE_ID,
        "text": text,
        "language": language,
        "model_size": "0.6B",
        "engine": "qwen",
        "personality": False,
        "normalize": True,
    }
    resp = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("id")

def poll_status(gen_id, max_wait=600):
    """轮询等待生成完成，返回音频路径"""
    print(f"    等待中", end="", flush=True)
    for i in range(max_wait // 5):
        time.sleep(5)
        try:
            history = requests.get(f"{VOICEBOX_URL}/history", timeout=10).json()
            for item in history.get("items", []):
                if item.get("id") == gen_id:
                    status = item.get("status")
                    if status == "completed":
                        print(f" ✅ ({item.get('duration', 0):.1f}s)")
                        return item
                    elif status == "failed":
                        print(f" ❌")
                        return None
            print(".", end="", flush=True)
        except:
            print("!", end="", flush=True)
    print(" 超时")
    return None

def download_audio(gen_id, output_path):
    """下载生成的音频文件"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    resp = requests.get(f"{VOICEBOX_URL}/history/{gen_id}/export-audio", timeout=30)
    with open(output_path, "wb") as f:
        f.write(resp.content)
    return output_path

def generate_all_audio(script_path, audio_dir):
    """从脚本文件生成所有语音"""
    with open(script_path, "r", encoding="utf-8") as f:
        scripts = json.load(f)
    
    os.makedirs(audio_dir, exist_ok=True)
    audio_paths = []
    
    print(f"  共 {len(scripts)} 段讲解词")
    
    for i, text in enumerate(scripts):
        audio_path = os.path.join(audio_dir, f"audio_{i+1:02d}.wav")
        
        # 已存在且大于10KB（非静音）则跳过
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 10240:
            # 检查是否是真实语音（大于150KB说明有内容）
            if os.path.getsize(audio_path) > 150000:
                print(f"  第{i+1}段: 已存在({os.path.getsize(audio_path)//1024}KB)，跳过")
                audio_paths.append(audio_path)
                continue
        
        print(f"  第{i+1}段: {text[:30]}...")
        
        # 提交生成请求
        try:
            gen_id = submit_generation(text)
            print(f"    任务ID: {gen_id}")
        except Exception as e:
            print(f"    ❌ 提交失败: {e}")
            audio_paths.append(audio_path)  # 用占位
            continue
        
        # 轮询等待完成
        result = poll_status(gen_id, max_wait=600)
        if result:
            # 下载音频
            try:
                download_audio(gen_id, audio_path)
                size = os.path.getsize(audio_path)
                print(f"    ✅ 下载完成: {size//1024}KB")
                audio_paths.append(audio_path)
            except Exception as e:
                print(f"    ❌ 下载失败: {e}")
                audio_paths.append(audio_path)
        else:
            print(f"    ⚠️ 生成失败，稍后用静音替代")
            audio_paths.append(audio_path)
    
    return audio_paths

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python voicebox_batch.py <脚本.json> <音频输出目录>")
        sys.exit(1)
    
    script_path = sys.argv[1]
    audio_dir = sys.argv[2]
    
    print(f"脚本: {script_path}")
    print(f"输出: {audio_dir}")
    
    audio_paths = generate_all_audio(script_path, audio_dir)
    print(f"\n完成！共 {len(audio_paths)} 段音频")
