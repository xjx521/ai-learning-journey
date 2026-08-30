import re, os
import datetime
import requests
from openai import OpenAI
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes")
os.makedirs(NOTES_DIR, exist_ok=True)  # 只允许模型写这个目录


def _safe_path(filename: str) -> str:
    """把文件名规范化并强制落在 NOTES_DIR 内，挡 ../../ 路径穿越 —— 你填
    提示：os.path.basename() 只取最后一段 + os.path.join(NOTES_DIR, basename)"""
    filename = filename.strip()  # 去空格
    if re.search(
        r"\.\.|[/\\]", filename
    ):  # 0. 正则早退：挡住 .. 和任何形式的路径分隔符（含裸 ".." 穿越）
        raise ValueError(f"非法文件名：{filename!r}")

    # ① 剥掉路径只剩文件名（挡住 ../ 穿越）——
    basename = os.path.basename(filename)

    # ② 拼回 NOTES_DIR ——
    path = os.path.join(NOTES_DIR, basename)

    # ③ 返回绝对路径 ——
    return os.path.abspath(path=path)


@tool(
    description="把内容写入 notes 目录下的文件。"
    "filename 必须和用户说的文件名【完全一致】，不要自行改名/新建/加扩展名；"
    "content 是【要保存的实际文字】，不要填你的思考过程。"
)  # 把工具描述写死约束 第一次测试时出现read_note创建新文件
def save_note(filename: str, content: str) -> str:
    """写文件：返回"模型看得懂"的成功/失败信息"""
    try:
        path = _safe_path(filename)
    except ValueError as e:
        return str(e)

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return f"文件写入失败:{e}"

    return f"已保存到{path},内容{len(content)}"


@tool(description="读取notes目录下某个文件内容，参数 filename=文件名")
def read_note(filename: str) -> str:
    """读文件：不存在返回友好提示而不是报错"""
    try:
        path = _safe_path(filename)
    except ValueError as e:
        return str(e)

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"文件{path}不存在"


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
    tools=[get_time, get_weather, get_add, save_note, read_note],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，
且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我""",
)


for q in ["现在几点了？", "首尔天气怎么样？", "3+5 等于几？"]:
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
