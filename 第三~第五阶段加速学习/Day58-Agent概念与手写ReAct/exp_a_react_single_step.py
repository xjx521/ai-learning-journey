from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def get_weather(city) -> str:
    return f"{city}的天气是晴天"


system = """你是能调用工具的助手。需要查资料时，严格按照这个格式输出：
Thought: 你的推理过程
Action: 工具名
Action Input: 工具参数
如果已经知道答案，输出：Final Answer: 最终答案

可用工具：
- get_weather(city)：查询城市天气，参数=城市名，例如 get_weather(北京)
"""

reply = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "北京今天天气怎么样"},
    ],
    temperature=0,
    # ✅重点：删掉 tools=tools！纯文本ReAct不要这个参数
)

print(reply.choices[0].message.content)
