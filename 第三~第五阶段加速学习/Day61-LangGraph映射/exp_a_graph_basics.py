from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ① State：整张图共享的数据（Agent 里就是 messages 对话历史)
class AgentState(TypedDict):
    count: int  # 示例先用一个计数器


# ② 节点：普通 Python 函数，输入 State，返回要更新的字段
def node_1(state: AgentState):
    print("node_1 执行")
    return {"count": state["count"] + 1}  # 返回的 dict 会写回 State


def node_2(state: AgentState):
    print("node_2 执行")
    return {"count": state["count"] + 1}


def node_3(state: AgentState):
    print("node_3 执行")
    return {"count": state["count"] + 1}


# ③ 建图：加节点 + 加边（START→node_1→node_2→END）
graph = StateGraph(AgentState)
graph.add_node("n1", node_1)
graph.add_node("n2", node_2)
graph.add_node("n3", node_3)
graph.add_edge(START, "n1")  # 入口
graph.add_edge("n1", "n2")
graph.add_edge("n2", "n3")
graph.add_edge("n3", END)

# ④ 编译 + 执行（compile 会做校验，invoke 传入初始 State）
app = graph.compile()
# result = app.invoke({"count": 0})
# print("结果 count =", result["count"])  # 期望 2
# 逐节点流式迭代执行
for chunk in app.stream({"count": 0}):
    print("===== 节点输出chunk =====")
    print(chunk)
