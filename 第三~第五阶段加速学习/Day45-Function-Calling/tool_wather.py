from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print(
        "❌ 还没填 Key！先打开 .env 文件，把 sk- 开头的 DeepSeek Key 粘贴进去，再运行"
    )
    exit(1)


def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=tools,
    )
    return response.choices[0].message


def get_weather(city):
    return fake_db.get(city)


client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

fake_db = {"北京": "晴，28℃", "上海": "小雨，25℃"}
messages = [{"role": "user", "content": "北京今天天气怎么样"}]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名称"}},
                "required": ["city"],  # 必填字段
            },
        },
    }
]

msg = send_messages(messages)  # msg是pydantic对象

if msg.tool_calls:
    print("✅ 模型发起工具调用")

    # 大模型发送请求
    messages.append(msg.model_dump())
    for tool_call in msg.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)  # 获取参数 字符串转字典

        if name == "get_weather":
            result = get_weather(args["city"])

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": result,
            }
        )

    msg = send_messages(messages)
    print("AI回答：", msg.content)
