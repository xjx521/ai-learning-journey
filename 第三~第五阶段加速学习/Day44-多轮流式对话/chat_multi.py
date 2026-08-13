from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 提前检查：Key 有没有真的填进去（防止没填就跑，报一堆看不懂的错）
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key.startswith("sk-在这里"):
    print(
        "❌ 还没填 Key！先打开 .env 文件，把 sk- 开头的 DeepSeek Key 粘贴进去，再运行"
    )
    exit(1)  # 退出程序（1表示异常退出）

# ===== 第三步：创建"客户端" =====
# 客户端 = "连接 DeepSeek 的钥匙串"，后面所有请求都用它发
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

# ===== 第四步：发聊天请求 =====
# messages 是"聊天记录"列表：role=user 表示你说的话，role=assistant 表示模型说的话
messages = [{"role": "user", "content": "你好，我叫小明，我住在北京"}]
response1 = client.chat.completions.create(
    model="deepseek-v4-flash", messages=messages
)  # client.chat.completions.create调用对话大模型的标准入口函数

answer1 = response1.choices[0].message.content  # 非流式拿回答
print("第1轮：", answer1)

# ==========================================
# 👇 多轮对话的全部秘密： messages是个越来越长的列表，每次请求把它整个发出去，模型答完把它 append 进去再接下一句。
# ==========================================

# 把模型的回答"记进"对话记录（模型说的话，role 是 assistant）
messages.append({"role": "assistant", "content": answer1})

# # 再加你第二句话（你说的，role 是 user）
messages.append({"role": "user", "content": "我叫什么名字？我住在哪？"})

# 整个对话记录重发一遍 → 模型能看到全部上下文
response2 = client.chat.completions.create(
    model="deepseek-v4-flash", messages=messages  # 这次 messages 有 3 条了
)
answer2 = response2.choices[0].message.content
print("第2轮：", answer2)
