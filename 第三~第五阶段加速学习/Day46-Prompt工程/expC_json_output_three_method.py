# -*- coding: utf-8 -*-
"""
### 实验 C：结构化输出——让模型吐能直接用的 JSON（约 1 小时）★★★
"""

# ===== 第一步：导入需要的库 =====
from openai import OpenAI  # openai 官方 SDK（负责发 HTTP 请求给模型）
from dotenv import load_dotenv  # python-dotenv：负责读取 .env 文件
import os  # os：负责读取环境变量
import json

# ===== 第二步：读取 .env 文件 =====
# load_dotenv() 会在当前文件夹找 .env，把里面的 "KEY=值" 读进内存（环境变量）
load_dotenv()

# 提前检查：Key 有没有真的填进去（防止没填就跑，报一堆看不懂的错）
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-在这里"):
    print(
        "❌ 还没填 Key！先打开 .env 文件，把 sk- 开头的 DeepSeek Key 粘贴进去，再运行"
    )
    exit(1)  # 退出程序（1 表示"异常退出"）

# ===== 第三步：创建"客户端" =====
# 客户端 = "连接 DeepSeek 的钥匙串"，后面所有请求都用它发
client = OpenAI(
    api_key=api_key,  # 从 .env 里拿到的 Key
    base_url="https://api.deepseek.com/v1",  # 地址指向 DeepSeek（默认是指向 OpenAI 官网的，必须换）
)

# ===== 第四步：发聊天请求 =====
# messages 是"聊天记录"列表：role=user 表示你说的话，role=assistant 表示模型说的话

# 方法一（纯自然语言）：
# response = client.chat.completions.create(
#     model="deepseek-v4-flash",  # 模型名：注意 deepseek-chat 已于 2026-07-24 停用，现在用 v4-flash（快+便宜）
#     messages=[
#         {
#             "role": "user",
#             "content": "请把这句话的情感判断输出成JSON，包含情感和关键词两个字段：『电池两天就没电，客服也找不到人』",
#         },
#     ],
# )

# 方法二（few-shot 模板）：先给一个标准 JSON 示例，再问
# response = client.chat.completions.create(
#     model="deepseek-v4-flash",  # 模型名：注意 deepseek-chat 已于 2026-07-24 停用，现在用 v4-flash（快+便宜）
#     messages=[
#         {
#             "role": "user",
#             "content": '请把这句话的情感判断输出成JSON，包含情感和关键词两个字段,json示例：{"情感":"正面","关键词":["我喜欢这部电影"]}，情感判断内容:『电池两天就没电，客服也找不到人』',
#         },
#     ],
# )

# 方法三（**response_format，新参数**）
response = client.chat.completions.create(
    model="deepseek-v4-flash",  # 模型名：注意 deepseek-chat 已于 2026-07-24 停用，现在用 v4-flash（快+便宜）
    messages=[
        {
            "role": "user",
            "content": "请把这句话的情感判断输出成JSON，包含情感和关键词两个字段 情感判断内容:『电池两天就没电，客服也找不到人』",
        },
    ],
    response_format={"type": "json_object"},  # ← 强制模型输出合法 JSON
)

# ===== 第五步：打印模型回答 =====
answer = response.choices[0].message.content
print("🤖 DeepSeek 说：")
print(answer)

# 解析json
result = json.loads(answer)
print("情感：", result["情感"])
print("关键词：", result["关键词"])
