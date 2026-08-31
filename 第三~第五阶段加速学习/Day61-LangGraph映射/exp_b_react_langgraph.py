from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_ollama import ChatOllama


# ===================== 1. State定义 =====================
class AgentState(TypedDict):
    messages: list[BaseMessage]


# ===================== 2. 模型与工具模拟 =====================
llm = ChatOllama(model="qwen2.5:7b", base_url="http://localhost:11434")


def get_weather(city: str) -> str:
    """查询城市天气"""
    mock_data = {"北京": "晴 28℃", "上海": "小雨 24℃"}
    return mock_data.get(city, f"没有{city}的天气数据")


TOOLS = {"get_weather": get_weather}
llm_with_tools = llm.bind_tools(list(TOOLS.values()))


# ===================== 3. 节点定义 =====================
def llm_node(state: AgentState):
    """LLM节点：调用模型，输出AI消息（可能带tool_calls）"""
    resp = llm_with_tools.invoke(state["messages"])
    # 只返回新增消息，框架reducer自动append
    return {"messages": [resp]}


def tools_node(state: AgentState):
    """工具执行节点，遍历tool_calls执行工具，生成ToolMessage"""
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
    """条件路由：有tool_calls去tools，否则结束"""
    last_msg = state["messages"][-1]
    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        return "tools"
    return "END"


# ===================== 4. 构建图、编译 =====================
graph = StateGraph(AgentState)
graph.add_node("llm_node", llm_node)
graph.add_node("tools_node", tools_node)

graph.add_edge(START, "llm_node")
graph.add_conditional_edges(
    source="llm_node",
    path=should_continue,
    path_map={"tools": "tools_node", "END": END},
)
graph.add_edge("tools_node", "llm_node")  # 工具执行完回到LLM，形成循环

app = graph.compile()

# ===================== 5. 运行实验：提问+打印每一步messages长度 =====================
if __name__ == "__main__":
    initial_input = {"messages": [("user", "北京天气怎么样？")]}

    print("===== stream逐节点执行，观察messages长度 =====")
    for chunk in app.stream(initial_input):
        print("\n----------- chunk 节点输出 -----------")
        print(chunk)
        node_name = list(chunk.keys())[0]
        data = chunk[node_name]
        if "messages" in data:
            print(f"【{node_name}】messages当前长度 = {len(data['messages'])}")

    # 获取最终完整结果
    final = app.invoke(initial_input)
    print("\n===== 最终全部消息 =====")
    for m in final["messages"]:
        print(f"{type(m).__name__}: {m.content}")
