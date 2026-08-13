from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key or api_key.startswith("st-在这里"):
    print(
        "❌ 还没填 Key！先打开 .env 文件，把 sk- 开头的 DeepSeek Key 粘贴进去，再运行"
    )
    exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

messages = [{"role": "system", "content": "你是客服小助手，回答必须简短，不超过20个字"}]

for i in range(5):
    response = client.chat.completions.create(
        model="deepseek-v4-flash", messages=messages
    )
    answer = response.choices[0].message.content
    print(f"第{i+1}次回答:", answer)
    print("上下文总长度：", len(messages))
    messages.append(
        {"role": "system", "content": "你是客服小助手，回答必须简短，不超过20个字"}
    )
    print("=" * 50)
    time.sleep(1)
    if i >= 3:  # 连问两句 以下是破坏性实验只传user
        response = client.chat.completions.create(
            model="deepseek-v4-flash", messages=messages
        )
        answer = response.choices[0].message.content
        print(f"第{i+1}次回答:", answer)
        print("上下文总长度：", len(messages))
        messages.append(
            {"role": "user", "content": "你是客服小助手，回答必须简短，不超过20个字"}
        )
        print("=" * 50)
        time.sleep(1)
