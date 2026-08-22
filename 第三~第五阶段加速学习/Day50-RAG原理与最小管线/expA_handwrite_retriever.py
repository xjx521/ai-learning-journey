def char_overlap_score(query: str, doc: str) -> int:
    """最朴素的'相似度'：问题和文档共用了多少个字。
    字重叠越多 = 越相关。
    先能跑，理解'检索=打分+排序'的本质；Day51 再换成真正的语义相似度。"""
    q_set = set(query)  # 把问题拆成字符集合（自动去重）
    d_set = set(doc)  # 把文档拆成字符集合
    return len(q_set & d_set)  # 两个集合的交集大小 = 重叠字符数


def retrieve(query: str, docs: list, top_k: int = 2) -> list:
    """返回和 query 最相关的 top_k 段文档内容（只返回文档，不要分数）"""
    scored = []
    for doc in docs:
        score = char_overlap_score(query, doc)  # 给每段打一个分
        scored.append((score, doc))  # 把 (score, doc) 这个元组加进 scored
        scored = sorted(scored, key=lambda x: x[0], reverse=True)  # 按分数从高到低排序

    return [
        i[1] for i in scored[0:top_k]
    ]  # 取前 top_k 个，只 return 文档内容（不要分数）


knowledge = [
    "我们公司的年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
    "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
    "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
    "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
]

if __name__ == "__main__":
    print(retrieve(query="我入职两年了，有几天年假？", docs=knowledge))
    print(retrieve(query="出差住酒店超标准了怎么办？", docs=knowledge))
    print(retrieve(query="怎么才能晋升？", docs=knowledge))
