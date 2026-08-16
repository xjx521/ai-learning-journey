# -*- coding: utf-8 -*-
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)

# max_tokens：限制"模型这次最多输出几个 token"
# 设 10 就是想看它"话说到一半被掐断"
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "好"}],
    max_tokens=10,  # ← 关键参数：故意设小，制造截断
)

msg = response.choices[0].message
print("输出内容：", repr(msg.content))  # repr 能看见末尾有没有被切断
print(
    "finish_reason:", response.choices[0].finish_reason
)  # stop=正常结束 / length=被 max_tokens 掐断
