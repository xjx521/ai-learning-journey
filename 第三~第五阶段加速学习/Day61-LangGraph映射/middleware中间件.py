from langchain.agents import create_agent, AgentState
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents.middleware import (
    before_agent,
    before_model,
    after_agent,
    after_model,
    wrap_model_call,
    wrap_tool_call,
)
from langgraph.runtime import Runtime


@tool(description="查询天气 city传入城市名")
def get_weather(city: str):
    return f"{city}天气:晴天"


@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before_agent]agent启动前，并附带{len(state["messages"])}消息")


@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after_agent]agent启动后，并附带{len(state["messages"])}消息")


@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before_model]模型启动前，并附带{len(state["messages"])}消息")


@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after_model]模型启动后，并附带{len(state["messages"])}消息")


@wrap_model_call
def model_call_hook(request, handler):
    print("模型调用啦")
    return handler(request)  # handler 是"接着调用模型"的函数，要用 () 调用，不是 []


@wrap_tool_call
def monitor_tool(request, handler):
    print(f"工具执行：{request.tool_call["name"]}")
    print(f"工具执行参数：{request.tool_call["args"]}")
    return handler(request)  # 必须把 handler 结果传下去，否则工具节点拿到 None


llm = ChatOllama(model="qwen2.5:7b", base_url="http://127.0.0.1:11434", temperature=0)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    middleware=[
        log_before_agent,
        log_before_model,
        log_after_agent,
        log_after_model,
        model_call_hook,
        monitor_tool,
    ],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，
且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我""",
)


for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "惠州天气怎么样?"}]}, stream_mode="values"
):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print("AI回答:", latest_message.content)
    try:
        if latest_message.tool_calls:
            print(f"工具调： {[tc["name"] for tc in latest_message.tool_calls]}")
    except AttributeError as e:
        pass
