from langchain.agents import create_agent

# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool(description="获取体重 返回一个整数 单位是kg")
def get_weight() -> int:
    return 60


@tool(description="获取身高 返回一个整数 单位厘米2")
def get_height() -> int:
    return 170


# ✅替换为本地Ollama，不要ChatTongyi
llm = ChatOllama(model="qwen2.5:7b", base_url="http://127.0.0.1:11434", temperature=0)

agent = create_agent(
    model=llm,
    # model=ChatTongyi(model="qwen2.5:7b"),
    tools=[get_weight, get_height],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，
且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我""",
)

# res=agent.invoke({"messages": [{"role": "user", "content": "算算我的BMI值是多少"}]})
# print(res)
# 流式输出
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "算算我的BMI值是多少"}]},
    stream_mode="values",
):
    latest_messages = chunk["messages"][-1]
    if latest_messages.content:
        print(type(latest_messages).__name__, latest_messages.content)
    try:
        if latest_messages.tool_calls:
            print(f"工具调： {[tc["name"] for tc in latest_messages.tool_calls]}")
    except AttributeError as e:
        pass
