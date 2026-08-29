import re
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def get_weather(raw):
    city = raw.split("=", 1)[-1].strip().strip('"').strip("'")  # 剥掉 city= 和引号
    table = {"北京": "晴 28℃", "上海": "雨 24℃", "广州": "多云 30℃"}
    return table.get(city, f"没有 {city} 的天气数据")  # 查不到返回提示而不是报错


def add(a, b):
    return f"{a}+{b}={a+b}"


def get_policy(keyword):
    policies = {"报销": "出差住宿每晚500元，超标自理", "年假": "满一年5天，满三年10天"}
    return policies.get(keyword, "没有这个政策")


TOOLS = {"get_weather": get_weather, "add": add, "get_policy": get_policy}

SYSTEM = """你是能调用工具的助手。需要工具时输出：
Thought: 你的推理过程
Action: 工具名
Action Input: 工具参数
知道答案时输出：Final Answer: 最终答案
可用工具：get_weather(city) / add(a,b) / get_policy(keyword)"""


def call_llm(messages):
    """调模型，返回回复文本（复用 Day43 写法）"""
    resp = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=messages,
        temperature=0,
    )
    return resp.choices[0].message.content


def run_agent(question, max_iterations=5):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    for step in range(max_iterations):
        reply = call_llm(messages)
        print(f"[step{step}] {reply}")
        # ① 有最终答案 → 结束循环
        if "Final Answer" in reply:
            return reply
        # ② 正则解析 Action 和 Action Input
        m = re.search(r"Action:\s*(\w+)\s*Action Input:\s*(\S+)", reply)
        if m is None:
            # ③ 没解析出 Action → 提醒模型按格式来，别直接崩
            messages.append({"role": "assistant", "content": reply})
            messages.append(
                {
                    "role": "user",
                    "content": "请按格式输出 Action 和 Action Input，或给出 Final Answer。",
                }
            )
            continue
        tool_name, tool_input = m.groups()
        tool_func = TOOLS.get(tool_name)
        if tool_func is None:
            Observation = f"没有{tool_name}工具"
        else:
            Observation = tool_func(tool_input)
        messages.append({"role": "assistant", "content": reply})
        messages.append(
            {
                "role": "user",
                "content": f"Observation: {Observation}\n请根据观察结果继续。",
            }
        )
    return "达到最大迭代次数，强制停止。"


# 跑两个任务：
print("=" * 40)
print(run_agent("北京天气怎么样？"))  # 单步：查一次天气
print("=" * 40)
print(run_agent("北京天气怎么样？适不适合户外跑步？"))  # 多步：查天气 + 再推理
