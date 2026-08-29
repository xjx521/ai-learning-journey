import re
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def parse_city(raw):
    """校验避免多任务问题传入json导致查不到天气"""
    raw = raw.strip()
    try:  # 1) 先试 JSON
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return next(iter(obj.values()))
    except Exception:
        pass
    if "=" in raw:  # 2) 再试 key=value
        raw = raw.split("=", 1)[1]
    return raw.strip().strip('"').strip("'")  # 3) 去引号


def get_weather(raw):
    city = parse_city(raw)
    table = {"北京": "晴 28℃", "上海": "雨 24℃", "广州": "多云 30℃"}
    if (
        city not in table
    ):  # ✅**生产正确做法：捕获异常，把异常信息包装成字符串赋值给`observation`，追加进 messages 给模型看，不要向外抛。**
        raise KeyError(f"没有{city}天气数据")
    return table[city]


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
            try:
                Observation = tool_func(tool_input)
            except Exception as e:
                # 捕获全部异常，包装为Observation，不要raise！
                Observation = f"工具执行出错{e}"

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
