import re
import datetime
import requests
from openai import OpenAI
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


# ---------- 工具 1：系统时间（真实，不写死） ----------


def get_time(_=None) -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# ---------- 工具 2：真实天气（调 HTTP API） ----------
def getcode(city: str):
    """获取真实经纬度 改成普通函数 get_weather才能正常调用 不然只能工具调用"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "zh", "format": "json"}

    try:
        resp = requests.get(url, params=params, timeout=10)  #  超时 10 秒，别让它无限等
        resp.raise_for_status()  # 判断 HTTP 响应状态码 非 2xx 就抛异常
        data = resp.json()
        if not data.get("results"):
            return None
        loc = data["results"][0]
        return loc["latitude"], loc["longitude"], loc.get("country")
    except Exception as e:
        return f"地理编码解析失败：{e}"


def get_weather(raw_city: str) -> str:
    """获取真实天气"""
    # ① 输入归一化：剥掉 Action Input 可能带的前缀/引号/JSON
    city = raw_city.strip().strip('"').strip("'")  # 过滤引号
    if "=" in city:
        city = city.split("=", 1)[1].strip().strip('"').strip('"')  # 过滤=
    geo = getcode(city)
    if isinstance(geo, str):  # geocode 返回了出错信息
        return geo
    if geo is None:
        return f"找不到{city}的经纬度，请检查城市名"  # ② 查映射表，查不到 → 返回"模型看得懂的失败信息"而不是抛异常
    lat, lon, country = geo
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        cw = resp.json()["current_weather"]
        temp, wind = cw["temperature"], cw["windspeed"]
        return f"{city}({country})当前温度 {temp}°C，风速 {wind} km/h"
    except Exception as e:
        return f"查询天气失败:{e}"


# ---------- 工具 3：纯计算（保留，无副作用） ----------
def get_add(a, b):
    return f"{a}+{b}={a+b}"


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
                return f"工具执行出错：{e}"
        messages.append({"role": "assistant", "content": reply})
        messages.append(
            {
                "role": "user",
                "content": f"Observation: {Observation}\n请根据观察结果继续。",
            }
        )

    return "达到最大迭代次数，强制停止。"


SYSTEM = """你是 ReAct 智能体。可用工具（Action 必须原样写英文工具名）：
1. get_time —— 获取当前系统时间，无参数，Action Input 写 none
2. get_weather —— 查城市实时天气，Action Input 只写城市名，例：北京
3. get_add —— 两数相加，Action Input 写逗号分隔，例：3,5

每轮严格按此格式输出，且只输出一个 Action 后立即停止：
Thought: 你的思考
Action: 工具名
Action Input: 参数

【禁止】你自己编写 Observation，Observation 由我提供给你。
拿到足够 Observation 后再输出：
Thought: ...
Final Answer: ..."""
TOOLS = {"get_time": get_time, "get_weather": get_weather, "get_add": get_add}

for q in ["现在几点？", "北京天气怎么样？", "3+5 等于几？"]:
    print("=" * 40)
    print(run_agent(q))
