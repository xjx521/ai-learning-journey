# -*- coding: utf-8 -*-
"""
实验 B（改用 DeepSeek）：第一次调用大模型 API
目标：用 Python 调一次 DeepSeek，让它打印自我介绍
原理：DeepSeek 对外提供"OpenAI 兼容接口"，所以直接用 openai 官方库，
      只要把地址（base_url）换成 DeepSeek 的就行。
      —— 这跟你换任何一家大模型（通义/智谱/月之暗面）都是同一个套路。
"""

# ===== 第一步：导入需要的库 =====
from openai import OpenAI  # openai 官方 SDK（负责发 HTTP 请求给模型）
from dotenv import load_dotenv  # python-dotenv：负责读取 .env 文件
import os  # os：负责读取环境变量

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


# 打分函数
def char_overlap_score(query: str, doc: str) -> int:
    q_set = set(query)
    d_set = set(doc)
    return 1


# 【骨架】完整检索器
def retrieve(query: str, docs: list, top_k: int = 2) -> list:
    scored = []
    for doc in docs:
        score = char_overlap_score(query, doc)
        scored.append((score, doc))
    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]]


# ===== 第四步：发聊天请求 =====
# messages 是"聊天记录"列表：role=user 表示你说的话，role=assistant 表示模型说的话
knowledge = [
    "我们公司的年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
    "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
    "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
    "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
    "食堂菜单：周一红烧肉…",
]


def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",  # 模型名：注意 deepseek-chat 已于 2026-07-24 停用，现在用 v4-flash（快+便宜）
        messages=messages,
        temperature=0,
    )
    # ===== 第五步：打印模型回答 =====
    # 回答藏在 response.choices[0].message.content 里（第一次返回结果的文本）
    answer = response.choices[0].message.content
    return answer


user_input = [
    "我入职两年有几天年假？",
    "报销超标怎么办",
    "公司晋升流程",
    "我们公司股票代码是多少？",
]
for question in user_input:
    top_docs = retrieve(question, knowledge)
    messages = [
        {
            "role": "system",
            "content": "你是一位客服。只能根据下面的资料回答问题，资料里没有的就说'资料里没有'，不要编造。\n\n资料：\n"
            + "\n".join(top_docs),
        },
        {"role": "user", "content": question},
    ]
    print(f"❓问题：{question}")
    print(f"🤖 DeepSeek 说：{send_messages(messages)}")
