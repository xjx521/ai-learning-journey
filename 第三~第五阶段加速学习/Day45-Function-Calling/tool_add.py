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


# 1. 定义工具元信息（给模型看的 JSON Schema）
tools = [
    {
        "type": "function",  # 固定写法：这是个"函数工具"
        "function": {
            "name": "add",  # ← 工具名（模型调用时用这个名字
            "description": "两个整数相加",  # ← 描述：模型靠它决定"要不要用这个工具"
            "parameters": {  # 参数说明（JSON Schema 格式）
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个加数"},
                    "b": {"type": "integer", "description": "第二个加数"},
                },
                "required": ["a", "b"],  # 必填参数
            },
        },
    }
]

# 2. 本地真实执行的函数（代码负责动手，模型只发调用请求）


def add(a: int, b: int) -> int:
    return a + b


client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

messages = [{"role": "user", "content": "3 加 5 等于几？"}]
msg = send_messages(messages)  # 发送请求 这里msg是Pydantic对象

if msg.tool_calls:  # 判断模型是否调用
    print("✅ 模型发起工具调用")

    # 把模型调用信息发给上下文
    # 1. 模型下单：assistant 消息里有一条带 id（订单号）的 tool_calls。

    messages.append(msg.model_dump())  # 这里msg是Pydantic对象 必须转换成字典

    # 循环处理所有工具调用
    for tool_call in msg.tool_calls:
        name = tool_call.function.name
        args = json.loads(
            tool_call.function.arguments
        )  # 提取模型发送的工具内部参数 文字（字符串）转成字典

        # 本地执行工具
        # 2. 你执行工具：算出 8。
        if name == "add":
            result = add(args["a"], args["b"])

        # 3. 你把结果塞回去给模型：tool 消息里写 tool_call_id = 刚才那个订单号，意思是——"这个结果是那个单子的"。
        # 把结果添加回prompt
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": str(result),  # content必须是字符串
            }
        )

    # 所有工具执行完成后 只一次重新提交给大模型输出自然语言回答
    msg = send_messages(messages)
    print("AI回答：", msg.content)
