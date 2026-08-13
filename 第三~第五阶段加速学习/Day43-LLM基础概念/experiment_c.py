# -*- coding: utf-8 -*-
"""
实验 C：temperature 破坏性实验
同一句 prompt，temperature=0 和 1.5 各跑 5 次，观察输出差异
（相比 call_deepseek.py，只多了：循环 + temperature 参数 + 对照表）
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# ===== 读取 .env =====
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-在这里"):
    print("❌ 还没填 Key！先打开 .env 填好 DeepSeek Key 再运行")
    exit(1)

# ===== 客户端 =====
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",
)

# ===== 关键 1：选 prompt（必须开放题）=====
# 问"1+1=?"不管温度多少都答 2，差异显不出来；冷笑话/写诗这种才有多种答案
prompt = "用一句话给我讲个冷笑话"   # ← 可以自己换成别的开放题

# ===== 关键 2：temperature 加在 create() 里 =====
# results 是个字典：键是温度，值是用来存 5 次回答的列表
results = {0: [], 1.5: []}

for t in [0, 1.5]:                   # 外层循环：先跑温度 0，再跑温度 1.5
    print(f"\n========== temperature = {t} ==========")
    for i in range(5):               # 内层循环：同一种温度跑 5 次
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            temperature=t,           # ← 核心：就这一个参数控制随机性
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        print(f"第{i+1}次：{answer}")
        results[t].append(answer)    # 存进 results[t] 对应的列表
        print("---")
        time.sleep(1)                # 免费额度有速率限制，每次歇 1 秒

# ===== 关键 3：打印对照表（对着填任务单）=====
print("\n\n次数 | temperature=0 | temperature=1.5")
for i in range(5):
    # replace("\n", " ")：把回答里的换行换成空格，让表格整齐
    col0 = results[0][i].replace("\n", " ")
    col15 = results[1.5][i].replace("\n", " ")
    print(f"{i+1} | {col0} | {col15}")
