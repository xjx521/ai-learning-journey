# ============================================================================
# Day60 实验B：手写 ReAct 多工具协同
# 本脚本的"灵魂"是那 8 处 🔧 改动 —— 每一处都在补一道"契约缝"。
# 手写 ReAct 的全部痛点可收成四道缝，恰好是框架版（create_agent / @tool）内置解决的东西：
#   缝①·参数怎么传  → 手写统一"单字符串契约"自己 split 解析；框架用 @tool 签名 + tool calling 结构化参数
#   缝②·Observation → 手写要防模型自编（stop= 硬截）；框架是真实返回值，模型碰不到
#   缝③·出错怎么办  → 手写 except 没写好就 return 打断循环；框架有重试/回传/并行
#   缝④·终止逻辑    → 手写用正则抠 Final Answer 优先级；框架由 LangGraph 状态机接管
# 代码里 🔧 改点②~⑧ 标注了每处改动对应哪道缝，对照学习笔记 Day60 食用。
# ============================================================================
import re, os
import datetime
import requests
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes")
os.makedirs(NOTES_DIR, exist_ok=True)  # 只允许模型写这个目录

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
    # 🔧 改点②【缝①·参数怎么传】输入归一化：模型填的 Action Input 形态不可控
    #    （可能带引号 "北京"、可能带 key= 前缀 city=北京、甚至 JSON）。手写版没有
    #    框架的"结构化参数校验"，只能靠手动 strip / split 把脏输入归一成干净城市名。
    city = raw_city.strip().strip('"').strip("'")  # 剥外层引号
    if "=" in city:
        city = (
            city.split("=", 1)[1].strip().strip('"').strip("'")
        )  # 若带了 key= 前缀，只取等号后的值
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


def _safe_path(filename: str) -> str:
    """把文件名规范化并强制落在 NOTES_DIR 内，挡 ../../ 路径穿越 —— 你填
    提示：os.path.basename() 只取最后一段 + os.path.join(NOTES_DIR, basename)"""
    filename = filename.strip()  # 去空格
    # 🔧 改点③【缝③·出错怎么办】路径安全护栏：手写版没有框架的"参数校验/异常自动回传"，
    #    必须自己用正则早退挡住危险输入。正则 r"\.\.|[/\\:]" 一次性挡三类：
    #    ① ".." 目录穿越  ② / \ 路径分隔符（linux/win）  ③ ":" 冒号——专门防 NTFS 数据流
    #    （note.txt:xxx 会被写成 ADS 隐藏流）和盘符 D:
    if re.search(r"\.\.|[/\\:]", filename):
        raise ValueError(f"非法文件名：{filename!r}")

    # ① 剥掉路径只剩文件名（挡住 ../ 穿越）——
    basename = os.path.basename(filename)

    # ② 拼回 NOTES_DIR ——
    path = os.path.join(NOTES_DIR, basename)

    # ③ 返回绝对路径 ——
    return os.path.abspath(path=path)


def save_note(raw: str) -> str:
    """手写React Raw单字符串契约：note.txt||内容 把多字符传入工具内再解析"""
    if "||" not in raw:
        return "参数格式错，请写：文件名||内容"
    filename, content = raw.split("||", 1)
    # 🔧 改点④【缝①·参数怎么传】再剥一层：模型常给文件名加 filename= / filename: 前缀
    #    （它把"参数名"也写进来了）。手写单字符串契约下，只能手动 re.sub 吃掉这个前缀。
    filename = re.sub(r"^\s*filename\s*[=:]\s*", "", filename.strip())
    try:
        path = _safe_path(filename)
    except ValueError as e:
        return str(e)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
    except Exception as e:
        return f"文件写入失败:{e}"
    return f"已保存到{path}，共{len(content.strip())}字"


def get_add(raw: str) -> str:
    parts = [x for x in re.split(r"[,，+\s]+", raw.strip()) if x]
    if len(parts) != 2:
        return f"参数格式错，请写 3,5 这种，收到：{raw}"
    a, b = float(parts[0]), float(parts[1])
    return f"{a}+{b}={a+b}"


def read_note(filename: str) -> str:
    """读文件：不存在返回友好提示而不是报错"""
    # 🔧 改点④【缝①·参数怎么传】与 save_note 同理：剥掉模型可能带的 filename= / filename: 前缀
    filename = re.sub(r"^\s*filename\s*[=:]\s*", "", filename.strip())
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


def get_poem(topic):
    return f"模拟工具get_poem，输入主题：{topic}"


def get_stock(code):
    return f"模拟工具get_stock，股票代码：{code}"


def get_news(keyword):
    return f"模拟工具get_news，关键词：{keyword}"


def get_calc_sqrt(num):
    return f"模拟工具get_calc_sqrt，输入数字：{num}"


def get_translate(text):
    return f"模拟工具get_translate，输入文本：{text}"


def call_llm(messages):
    """调模型，返回回复文本（复用 Day43 写法）"""
    resp = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=messages,
        temperature=0,
        stop=[
            "Observation:"
        ],  # 🔧 改点⑦【缝②·Observation 从哪来】物理保险：模型一旦开始写 "Observation:"
        #    就被硬截断，杜绝它自编观察结果（Day60 exp_a 那次它编了 2023 年的天气，就是少了这行）。
        #    框架版根本不需要这行——Observation 是真实工具返回值，模型碰不到。
    )
    return resp.choices[0].message.content


def run_agent(question, max_iterations=20):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    for step in range(max_iterations):
        reply = call_llm(messages)
        print(f"[step{step}] {reply}")

        # 🔧 改点⑤【缝④·终止逻辑】正则抠 Action：(\w+) 抓工具名，(.+) 抓整段输入。
        #    原 (\S+) 会漏掉带空格/引号的内容（如 city="北京" 被截成 city="北京"），
        #    故改 (.+) 贪心匹配整行，避免输入被截断。
        m = re.search(r"Action:\s*(\w+)\s*Action Input:\s*(.+)", reply)
        if m is None:
            # 🔧 改点⑧【缝④·终止逻辑】"没解析到 Action"≠"该继续"。手写版最容易漏的坑：
            #    模型已经给了 Final Answer（要收尾了），却因没匹配到 Action 被当成"格式错误"继续空转。
            #    所以这里先判 Final Answer，命中就直接 return 收尾；否则才提醒它按格式来。
            if "Final Answer" in reply:
                return reply
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
            # 🔧 改点⑥【缝③·出错怎么办】工具抛异常时，绝不能 return 打断循环（那会让整个 Agent 崩掉）。
            #    把异常包成 Observation 喂回模型，让它自己换参数重试——这正是框架"错误回传"的手写等价物。
            try:
                Observation = tool_func(tool_input)
            except Exception as e:
                Observation = f"工具执行出错：{e}，请检查参数格式后重试"
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
4. read_note —— 读取文件里存的笔记。Action Input 直接写文件名，例：note.txt
5. save_note —— 写入文件。Action Input 直接写「文件名||内容」，不要加 filename= 前缀，例：note.txt||北京天气晴
6.. get_poem(topic)：根据主题生成一首古诗，参数为诗歌主题
7. get_stock(code)：查询股票实时价格，参数为股票代码
8. get_news(keyword)：查询关键词相关新闻，参数为新闻关键词
9. get_calc_sqrt(num)：计算数字平方根，参数为待计算数字
10. get_translate(text)：把文本翻译成英文，参数为待翻译文本
每轮严格按此格式输出，且只输出一个 Action 后立即停止：
Thought: 你的思考
Action: 工具名
Action Input: 参数

【禁止】你自己编写 Observation，Observation 由我提供给你。
拿到足够 Observation 后再输出：
Thought: ...
Final Answer: ..."""
TOOLS = {
    "get_time": get_time,
    "get_weather": get_weather,
    "get_add": get_add,
    "read_note": read_note,
    "save_note": save_note,
    "get_poem": get_poem,
    "get_stock": get_stock,
    "get_news": get_news,
    "get_calc_sqrt": get_calc_sqrt,
    "get_translate": get_translate,
}

for q in ["帮我查北京天气，然后把天气记到 note.txt", "我刚才记的什么？"]:
    print("=" * 40)
    print(run_agent(q))
