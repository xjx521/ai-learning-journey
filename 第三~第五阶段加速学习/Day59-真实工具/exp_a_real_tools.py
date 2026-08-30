import re
import datetime
import requests
from openai import OpenAI
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


# ---------- 工具 1：系统时间（真实，不写死） ----------
@tool(description="获取真实时间 返回一个字符串")
def get_time() -> str:
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


@tool(description="获取真实天气 返回一个字符串")
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
@tool(description="计算两个数的和，参数 a 和 b")
def get_add(a, b):
    return f"{a}+{b}={a+b}"


llm = ChatOllama(model="qwen2.5:7b", base_url="http://127.0.0.1:11434", temperature=0)

agent = create_agent(
    model=llm,
    tools=[get_time, get_weather, get_add],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，
且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我""",
)


for q in ["现在几点了？", "北京天气怎么样？", "3+5 等于几？"]:
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": q}]}, stream_mode="values"
    ):
        latest_message = chunk["messages"][-1]
        if latest_message.content:
            print("AI回答:", latest_message.content)
        try:
            if latest_message.tool_calls:
                print(f"工具调： {[tc["name"] for tc in latest_message.tool_calls]}")
        except AttributeError as e:
            pass
