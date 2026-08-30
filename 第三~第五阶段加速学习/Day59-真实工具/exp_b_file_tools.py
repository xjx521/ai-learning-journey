import os, re
from openai import OpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

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


llm = ChatOllama(model="qwen2.5:7b", base_url="http://127.0.0.1:11434", temperature=0)

agent = create_agent(
    model=llm,
    tools=[save_note, read_note],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，
且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我 ,可用工具[save_note,read_note]""",
)

for q in [
    "帮我把今天学的三个 ReAct 要点：1. Thought→Action→Observation 循环2. 工具返回要模型看得懂3. 失败包装成 Observation 不抛异常记到 note.txt",
    "我刚才记的什么在note.txt文件下查找？",
]:
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": q}]}, stream_mode="values"
    ):
        latest_messages = chunk["messages"][-1]
        if latest_messages.content:
            print(latest_messages.content)
        try:
            if latest_messages.tool_calls:
                print(f"工具调:{[tc["name"] for tc in latest_messages.tool_calls]}")
        except AttributeError as e:
            pass
