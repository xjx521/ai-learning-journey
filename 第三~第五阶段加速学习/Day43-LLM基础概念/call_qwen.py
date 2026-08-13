# -*- coding: utf-8 -*-
"""
实验 B：第一次调用通义千问大模型
目标：用 Python 调一次通义千问，让它打印自我介绍
原理：通义千问对外提供"OpenAI 兼容接口"，所以直接用 openai 官方库，
      只要把地址（base_url）换成阿里云的就行。
"""

# ===== 第一步：导入需要的库 =====
from openai import OpenAI  # openai 官方 SDK（负责发 HTTP 请求给模型）
from dotenv import load_dotenv  # python-dotenv：负责读取 .env 文件
import os  # os：负责读取环境变量

# ===== 第二步：读取 .env 文件 =====
# load_dotenv() 会在当前文件夹找 .env，把里面的 "KEY=值" 读进内存（环境变量）
load_dotenv()

# 提前检查：Key 有没有真的填进去（防止没填就跑，报一堆看不懂的错）
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key or api_key.startswith("sk-在这里"):
    print("❌ 还没填 Key！先打开 .env 文件，把 sk- 开头的 Key 粘贴进去，再运行")
    exit(1)  # 退出程序（1 表示"异常退出"）

# ===== 第三步：创建"客户端" =====
# 客户端 = "连接通义千问的钥匙串"，后面所有请求都用它发
client = OpenAI(
    api_key=api_key,  # 从 .env 里拿到的 Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 地址指向阿里云（默认是指向 OpenAI 官网的，必须换）
)

# ===== 第四步：发聊天请求 =====
# messages 是"聊天记录"列表：role=user 表示你说的话，role=assistant 表示模型说的话
response = client.chat.completions.create(
    model="qwen3.8-max",  # 用哪个模型：qwen-plus 性价比均衡（qwen-turbo 更快更便宜）
    messages=[
        {"role": "user", "content": "你好，介绍一下你自己"},
    ],
)

# ===== 第五步：打印模型回答 =====
# 回答藏在 response.choices[0].message.content 里（第一次返回结果的文本）
answer = response.choices[0].message.content
print("🤖 通义千问说：")
print(answer)
