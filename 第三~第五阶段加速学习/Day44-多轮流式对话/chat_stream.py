from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

# 提前检查：Key 有没有真的填进去（防止没填就跑，报一堆看不懂的错）
if not api_key or api_key.startswith("sk-在这里"):
    print(
        "❌ 还没填 Key！先打开 .env 文件，把 sk- 开头的 DeepSeek Key 粘贴进去，再运行"
    )
    exit(1)

# ===== 第三步：创建"客户端" =====
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
messages = [{"role": "user", "content": "你好，我叫小明，我住在北京"}]
response = client.chat.completions.create(
    model="deepseek-v4-flash", messages=messages, stream=True
)

for chunk in response:
    text = chunk.choices[0].delta.content
    if text:  # 不是所有 chunk 都装文字，装文字的才打印。
        print(text, end="")  # 没拿到一小块就立即打印（不换行)
