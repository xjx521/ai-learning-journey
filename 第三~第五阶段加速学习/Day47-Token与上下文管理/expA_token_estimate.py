# -*- coding: utf-8 -*-
"""
### 实验 A：用近似方法数 token（约 1 小时）★
"""

import re


def count_tokens(text):
    """
    估算一段文本的 token 数（近似方法）。
    规则自己定，写清楚规则就行，不用追求精确。
    """
    count_chinese = len(
        re.findall(r"[一-鿿]", text)
    )  # TODO 1: 统计中文字符数量（提示：逐个字符判断 ord(ch) > 127 或用正则 [一-鿿] 只数汉字）

    count_english = len(
        re.findall(r"[a-zA-Z]+", text)
    )  # TODO 2: 统计英文单词数量（提示：text.split() 后数"纯英文的"）

    count_symbol = len(
        re.sub(r"[一-鿿a-zA-Z]", "", text)
    )  # TODO 3: 数标点 / emoji（提示：非中英文的符号）

    total_token = (
        count_chinese * 1.5 + count_english * 1.3 + count_symbol * 1
    )  # TODO 4: 按规则加权求和返回：中文×1.5 + 英文×1.3 + 符号×1

    return round(total_token, 1)  # 保留1位小数


texts = [
    "Hello, world! This is a test.",  # 英文短句
    "你好，世界。这是一段中文测试。",  # 中文短句
    "def add(a, b):\n    return a + b",  # 代码
    "，。！？,;:😀👍",  # 标点 / emoji
]

for t in texts:
    print(f"{t!r} → {count_tokens(t)} tokens")
