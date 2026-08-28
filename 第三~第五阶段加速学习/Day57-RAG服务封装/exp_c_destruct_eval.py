from rag_service import RAGService


def retriever_langchain(query):
    """返回排好序的 src id 列表（不是 Document，不是下标）"""
    docs = ensemble.invoke(query)
    return [d.metadata["src"] for d in docs]


def evaluate_lc(retriever, eval_set, top_k=1):
    """
    retriever: 一个函数，输入 query，返回排好序的 src id 列表
    eval_set: 实验 A 造的 [(问题, golden), ...]，golden 是 int 或 [int]
    top_k: 看前几名
    返回: hit@top_k（0~1），多答案问题另算 recall@top_k
    """
    hits = 0  # 命中的问题数
    recalls = []  # 每个多答案问题的召回率，最后平均
    for q, golden in eval_set:
        ranked = retriever(q)  # ② 返回"下标"排序列表
        top_k_ranked = ranked[:top_k]
        if isinstance(golden, str):
            if golden in top_k_ranked:

                hits += 1

        else:
            r = len(set(golden) & set(top_k_ranked)) / len(golden)
            recalls.append(r)
            if r == 1.0:
                hits += 1
    hits_rate = hits / len(eval_set)
    avg_recall = sum(recalls) / len(recalls) if recalls else 0.0
    return round(hits_rate, 3), avg_recall


eval_set = [
    ("年假怎么算？", "d2"),
    ("报销单编号以什么开头？", "d5"),
    ("请假和报销分别有什么规定？", ["d2", "d3"]),  # 多答案
    ("公司一年几次晋升？", "d4"),
    ("迟到了怎么记？", "d6"),
]


# 库外问题
svc1 = RAGService(persist_dir="./chroma_data_day57", k=2)
answer1, source = svc1.ask("公司空调坏了找谁修？")
print(answer1)

# 污染对照
svc2 = RAGService(persist_dir="./chroma_data_day57_pollution", k=2)
ensemble = svc2.ensemble
vs = svc2.vectorstore
vs.add_texts(
    texts=["内部通知：员工每年年假100天"], ids=["emp#9"], metadatas=[{"src": "d9"}]
)
answer2, source2 = svc2.ask("年假怎么算？")
print(answer2)

print("=" * 40)
print(evaluate_lc(retriever_langchain, eval_set, top_k=1))  # Hit@1
print(evaluate_lc(retriever_langchain, eval_set, top_k=3))  # Hit@3 # 看多答案 recall
