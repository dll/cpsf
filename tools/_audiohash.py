# -*- coding: utf-8 -*-
"""
_audiohash.py —— 给每段配音配一个"文本指纹"，防止配音和讲解稿对不上

踩过的坑：讲解稿改过之后，旧的 audio_NN.wav 还在原地，
流水线会"看到文件就跳过"，于是成片里出现**一半新稿、一半旧稿**的配音。

做法：生成音频时，同时写一个同名的 .txt，内容是该段"念稿"的 sha1 前 16 位。
以后判断"要不要重新生成"时：
    · 没有 .txt（历史遗留音频） → 视为可用（不强制重跑）
    · 有 .txt 且和当前讲稿一致   → 可用
    · 有 .txt 但和当前讲稿不一致 → **必须重新生成**

用法：
    from _audiohash import hash_text, is_fresh, write_stamp
"""
import hashlib
import os

MIN_BYTES = 100 * 1024


def hash_text(say):
    return hashlib.sha1(say.encode('utf-8')).hexdigest()[:16]


def stamp_path(wav):
    return os.path.splitext(wav)[0] + '.txt'


def is_fresh(wav, say, min_bytes=MIN_BYTES, script_path=None):
    """
    音频存在、大小合格、且内容确实是当前这版讲稿念出来的。

    判据优先级：
      1. 有指纹（.txt）  → 指纹必须等于当前讲稿
      2. 没有指纹        → 退化为比时间：音频必须比讲解脚本新。
                           讲稿一改，脚本 mtime 就变新，旧配音自然被判为过期。
                           （早期版本这里直接返回 True，结果旧配音被当成新的跳过，
                             成片里出现"一半新稿一半旧稿"。）
    """
    if not os.path.exists(wav) or os.path.getsize(wav) < min_bytes:
        return False
    sp = stamp_path(wav)
    if not os.path.exists(sp):
        if not script_path or not os.path.exists(script_path):
            return True                  # 无从判断，按可用处理
        try:
            return os.path.getmtime(wav) > os.path.getmtime(script_path)
        except Exception:
            return True
    try:
        with open(sp, encoding='utf-8') as f:
            return f.read().strip() == hash_text(say)
    except Exception:
        return True


def write_stamp(wav, say):
    try:
        with open(stamp_path(wav), 'w', encoding='utf-8') as f:
            f.write(hash_text(say))
    except Exception:
        pass
