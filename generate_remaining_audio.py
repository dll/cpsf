# -*- coding: utf-8 -*-
"""
生成第1讲剩余语音（7-12段）
缩短文本，避免Voicebox CPU推理超时
"""
import json
import time
import requests
import os

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "6a1f7579-b2e1-4ec9-98da-febeaa7f325a"
AUDIO_DIR = r"e:\2026-2027\2026-2027-1\AI化教学创新\AI化教学创新03\01_你好世界\video\_work\audio"

# 缩短版的7-12段讲解词
remaining_scripts = [
    # 第7段（缩短）
    "链接是最关键的一步。你写了printf，但printf的实现在标准库里。链接器负责找到printf的机器码，把它和你的main函数拼到一起，生成可执行文件。",
    # 第8段（缩短）
    "头文件和库文件的区别：头文件是菜单，告诉你有什么菜可以点；库文件是厨房，真正做菜的地方。include包含头文件只是告诉编译器函数名字，真正实现在链接时才从库文件中找来。",
    # 第9段（缩短）
    "从表达式到函数封装，到多文件模块，到静态库，到动态库，到接口抽象，最后到插件框架。每一步演进都是因为前一步不够用了。表达式是起点，但不是终点。",
    # 第10段（缩短）
    "课堂小测：第一题，C语言编译分四个阶段：预处理、编译、汇编、链接。第二题，printf实现在标准库中，不在头文件里。第三题，链接器把你调用的库函数和你的代码拼到一起。",
    # 第11段（缩短）
    "深入思考：为什么C语言设计成编译型？编译型运行快但调试慢，是性能和便利性的权衡。头文件和源文件分离实现了接口与实现分离，这个思想贯穿了整个架构演进。",
    # 第12段（缩短）
    "总结：从一行printf出发，理解了表达式的概念，走过了编译四阶段，揭开了链接的秘密，辨析了头文件和库文件的区别。下一讲我们进入控制结构。感谢观看，下讲再见。",
]

def submit(text):
    payload = {
        "profile_id": PROFILE_ID,
        "text": text,
        "language": "zh",
        "model_size": "0.6B",
        "engine": "qwen",
        "personality": False,
        "normalize": True,
    }
    resp = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json().get("id")

def poll(gen_id, max_wait=300):
    print(f"      等待", end="", flush=True)
    for _ in range(max_wait // 5):
        time.sleep(5)
        try:
            history = requests.get(f"{VOICEBOX_URL}/history", timeout=10).json()
            for item in history.get("items", []):
                if item.get("id") == gen_id:
                    if item.get("status") == "completed":
                        print(f" ✅ ({item.get('duration', 0):.1f}s)")
                        return item
                    elif item.get("status") == "failed":
                        print(f" ❌")
                        return None
            print(".", end="", flush=True)
        except:
            print("!", end="", flush=True)
    print(" 超时")
    return None

def download(gen_id, path):
    resp = requests.get(f"{VOICEBOX_URL}/history/{gen_id}/export-audio", timeout=30)
    with open(path, "wb") as f:
        f.write(resp.content)
    return path

def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    print("生成剩余语音（7-12段，缩短版）...")
    
    for i, text in enumerate(remaining_scripts):
        seg_num = 7 + i
        audio_path = os.path.join(AUDIO_DIR, f"audio_{seg_num:02d}.wav")
        
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 50000:
            print(f"  第{seg_num}段: 已存在({os.path.getsize(audio_path)//1024}KB)，跳过")
            continue
        
        print(f"  第{seg_num}段: {text[:30]}...")
        
        try:
            gen_id = submit(text)
            print(f"      ID: {gen_id}")
        except Exception as e:
            print(f"      ❌ 提交失败: {e}")
            continue
        
        result = poll(gen_id, max_wait=300)
        if result:
            try:
                download(gen_id, audio_path)
                size = os.path.getsize(audio_path)
                print(f"      ✅ 下载: {size//1024}KB")
            except Exception as e:
                print(f"      ❌ 下载失败: {e}")
        else:
            print(f"      ⚠️ 超时，跳过")
    
    # 统计
    audios = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]
    real_audios = [f for f in audios if os.path.getsize(os.path.join(AUDIO_DIR, f)) > 50000]
    print(f"\n完成！共 {len(real_audios)}/{12} 段真实音频")

if __name__ == "__main__":
    main()
