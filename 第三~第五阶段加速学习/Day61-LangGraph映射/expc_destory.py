from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_ollama import ChatOllama


class AgentState(TypedDict):
    messages: list[BaseMessage]


llm = ChatOllama(model="qwen2.5:7b", base_url="http://localhost:11434")

# 改成这个会触发死循环测试：永远返回提示让模型继续调用工具
# def get_weather(city: str) -> str:
#     return "出错，请重新调用get_weather工具"


def get_weather(city: str) -> str:
    mock_data = {"北京": "晴 28℃", "上海": "小雨 24℃"}
    return mock_data.get(city, f"没有{city}的天气数据")


TOOLS = {"get_weather": get_weather}
llm_with_tools = llm.bind_tools(list(TOOLS.values()))


def llm_node(state: AgentState):
    resp = llm_with_tools.invoke(state["messages"])
    return {"messages": [resp]}


def tools_node(state: AgentState):
    last_msg = state["messages"][-1]
    tool_msgs = []
    for tc in last_msg.tool_calls:
        name = tc["name"]
        args = tc["args"]
        call_id = tc["id"]
        func = TOOLS.get(name)
        if not func:
            content = f"错误：不存在工具 {name}"
        else:
            try:
                content = func(**args)
            except Exception as e:
                content = f"工具执行异常：{str(e)}"
        tool_msgs.append(ToolMessage(content=content, tool_call_id=call_id))
    return {"messages": tool_msgs}


def should_continue(state: AgentState) -> Literal["tools", "END"]:
    last_msg = state["messages"][-1]
    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        return "tools"
    return "END"


graph = StateGraph(AgentState)
graph.add_node("llm_node", llm_node)
graph.add_node("tools_node", tools_node)
graph.add_edge(START, "llm_node")
graph.add_conditional_edges(
    source="llm_node",
    path=should_continue,
    path_map={"tools": "tools_node", "END": END},
)
graph.add_edge("tools_node", "llm_node")

# 只传 checkpointer，不要 recursion_limit
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    # recursion_limit写在这里！config顶层，不在configurable里面
    config_session1 = {"configurable": {"thread_id": "1"}, "recursion_limit": 10}

    print("==== 第一轮：我叫小明 ====")
    res1 = app.invoke({"messages": [("user", "我叫小明")]}, config=config_session1)
    print(res1["messages"][-1].content)

    print("\n==== 第二轮：我叫什么？同一个thread_id，带记忆 ====")
    res2 = app.invoke({"messages": [("user", "我叫什么？")]}, config=config_session1)
    print(res2["messages"][-1].content)

    print("\n==== thread_id=2 全新会话，无记忆 ====")
    config_session2 = {"configurable": {"thread_id": "2"}, "recursion_limit": 10}
    res3 = app.invoke({"messages": [("user", "我叫什么？")]}, config=config_session2)
    print(res3["messages"][-1].content)
