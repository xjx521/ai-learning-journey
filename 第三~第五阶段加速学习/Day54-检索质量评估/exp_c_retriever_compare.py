# 实验 C：三路检索器打分，用数字证明混合 ≥ 单一
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import OpenAI
from math import log
from collections import Counter


class OllamaEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self):
        self._client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

    def __call__(self, input: Documents) -> Embeddings:
        resp = self._client.embeddings.create(model="bge-m3", input=list(input))
        return [r.embedding for r in resp.data]


def tokenize(text):
    return list(text)


def bm25_score(query, doc_tf, doc_len, avgdl, idf, k1=1.5, b=0.75):
    score = 0.0
    for token in tokenize(query):
        if token not in idf:
            continue
        tf = doc_tf.get(token, 0)
        if tf == 0:
            continue
        denom = tf + k1 * (1 - b + b * doc_len / avgdl)
        score += (idf[token] * (tf * (k1 + 1))) / denom
    return score


def bm25_retrieve(query, docs, doc_tfs, avgdl, idf, top_k=1):
    scored = []
    for index, doc in enumerate(docs):
        score = bm25_score(
            query=query, doc_tf=doc_tfs[index], doc_len=len(doc), avgdl=avgdl, idf=idf
        )
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def rrf_score(rank_in_bm25, rank_in_vector):
    """
    RRF倒数排名融合
    rank_in_bm25: 当前文档在BM25结果里的名次，从1开始（第1名=1，第2名=2）
    rank_in_vector: 当前文档在向量检索结果里的名次，从1开始
    """
    score = 1 / (60 + rank_in_bm25) + 1 / (60 + rank_in_vector)
    return score


def evaluate(retriever, eval_set, top_k=1):
    """
    retriever: 一个函数，输入 query，返回"排好序的文档下标列表"（不是文档字符串！）
    eval_set: 实验 A 造的 [(问题, golden), ...]，golden 是 int 或 [int]
    top_k: 看前几名
    返回: hit@top_k（0~1），多答案问题另算 recall@top_k
    """
    hits = 0  # 命中的问题数
    recalls = []  # 每个多答案问题的召回率，最后平均
    for query, golden in eval_set:
        ranked = retriever(query)  # ② 返回"下标"排序列表
        top_k_ranked = ranked[:top_k]  # 只要前top_k名
        if isinstance(golden, int):
            if golden in top_k_ranked:  # 如果在前K名里
                hits += 1
        else:
            r = len(set(golden) & set(top_k_ranked)) / len(golden)
            if r == 1.0:  # 全命中才算
                hits += 1
            recalls.append(r)
            # hits 计数、recall 存进 recalls
    hits_rate = hits / len(eval_set)  # 命中率 = hits / 题目总数
    avg_recall = (
        sum(recalls) / len(recalls) if recalls else 0.0
    )  # 平均 recall（没有多答案题时给 0）
    return round(hits_rate, 3), avg_recall


def retriever_bm25(query):
    """返回排好序的文档下标列表"""
    result = bm25_retrieve(
        query=query, docs=code_docs, doc_tfs=doc_tfs, avgdl=avgdl, idf=idf, top_k=8
    )
    return [code_docs.index(doc) for score, doc in result]


def retriever_vector(q):
    """返回按距离升序的文档下标"""
    result = col.query(query_texts=[q], n_results=8)
    return [code_docs.index(doc) for doc in result["documents"][0]]


def retriever_hybrid(q):
    """BM25 + 向量各排名次 → RRF 融合 → 返回下标"""
    # 第一步：BM25 侧，给每篇文档编号。 你已经写好了 bm25_retrieve，它返回的是按分降序排好的列表。用 enumerate把"第几名"抽出来存成字典：
    bm25_result = bm25_retrieve(
        query=q, docs=code_docs, doc_tfs=doc_tfs, avgdl=avgdl, idf=idf, top_k=8
    )
    rank_in_bm25 = {doc: i + 1 for i, (score, doc) in enumerate(bm25_result)}
    # 第二步：ChromaDB 侧，同样编一份号。
    vector_result = col.query(query_texts=[q], n_results=8)
    vec_doc = vector_result["documents"][0]  # 纯文档字符串list
    rank_in_vector = {doc: i + 1 for i, doc in enumerate(vec_doc)}

    # 第三步：融合。对 8 篇文档循环，每篇算 rrf_score(rank_in_bm25[doc], rank_in_vector[doc])，存成 (融合分, doc)的列表，排序取第一名。
    hybrid = []
    for doc in code_docs:
        rrf = rrf_score(rank_in_bm25[doc], rank_in_vector[doc])
        hybrid.append((rrf, doc))

    hybrid.sort(key=lambda x: x[0], reverse=True)
    return [code_docs.index(doc) for score, doc in hybrid]


code_docs = [
    "薪酬发放：每月15号发放上个月的薪水，遇节假日提前到最近的工作日。",
    "年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
    "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
    "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
    "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
    "团建聚餐：每月最后一周有团建活动，公司报销聚餐和场地费用。",
    "报销单编号规则：外勤报销单编号以R开头（如R-2024-0015），差旅报销单以T开头，月结报销单以M开头。",
    "服务器机房命名规范：生产环境服务器以PROD开头（如PROD-DB-01），测试环境以TEST开头。",
]

# ---- 1. 每篇文档的词频 TF（token 在文档里出现几次）----
doc_tfs = [Counter(tokenize(doc)) for doc in code_docs]
#  doc_tfs 是一个 list，里面有 8 个元素，每个元素是一个 Counter 对象（不是数字）。Counter 就是"字典"的亲戚，长得一样：
# doc_tfs[0] = {'薪': 2, '酬': 1, '发': 2, '放': 2, '月': 2, '的': 2, ...}

# ---- 2. 逆文档频率 IDF（这个 token 在几篇文档里出现过？越少越值钱）----
N = len(code_docs)
doc_freq = {}
for tf in doc_tfs:  # 第1层：先拿出第1篇的Counter，再第2篇的Counter……
    for token in tf:  # 第2层：在这个Counter里遍历它有哪些"字"
        doc_freq[token] = doc_freq.get(token, 0) + 1
idf = {
    t: log(1 + (N - df + 0.5) / (df + 0.5)) for t, df in doc_freq.items()
}  ## 每个字"记一笔"，跨文档累加
# **IDF 逆文档频率**
# 关键点：for token in tf 遍历的是 Counter 的键（字）
# - df：该 token 出现在多少篇文档
# - 一个词出现在越少文档 (df 越小)，IDF 计算出来数值越大，代表这个词更珍贵，命中之后加分更高。
# > 加 0.5 是平滑，防止分母为 0（查询出现完全没见过的字符）

avgdl = (
    sum(len(d) for d in code_docs) / N
)  # 所有文档的平均字符长度，BM25 用来做**长文档惩罚**

client = chromadb.PersistentClient(path="./chroma_data")

col = client.get_or_create_collection(
    name="hr_hybrid", embedding_function=OllamaEmbeddingFunction()
)
col.upsert(
    ids=["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8"], documents=code_docs
)  # upsert保证幂等判断不存在才添加

eval_set = [
    # ========== 2道【只有关键词能答‑编号题】BM25强，向量容易错 ==========
    ("PROD-DB-01 是什么服务器？", 7),  # 单答案，编号
    ("R-2024-0015 是什么类型的报销单？", 6),  # 单答案，编号
    # ========== 2道【只有语义能答‑大白话题】向量强，BM25容易漏 ==========
    ("最近压力大想请几天假歇歇", 1),  # 单答案，语义
    ("好累啊什么时候发工资", 0),  # 单答案，语义
    # ========== 2道【语义撞车题】语义容易召回相似无关文档 ==========
    ("我想请两天假出去散心，公司有政策吗", 1),  # 单答案；容易混淆团建5
    ("我明天要去上海出差，公司怎么报销跟打卡", 2),  # 单答案；容易混淆打卡4
    # ========== 4道普通单答案题 ==========
    ("我入职两年有几天年假？", 1),
    ("公司迟到多久会记警告？", 4),
    ("公司一年有几次晋升机会？", 3),
    ("每月什么时候举办公司团建聚餐？", 5),
    # ========== 2道【多答案问题】golden为列表 ==========
    ("请假和报销分别有什么规定？", [1, 2]),
    ("出差外出需要关注报销与打卡要求有哪些？", [2, 4]),
]


for top_k in [1, 3]:
    print(f"===== top_k={top_k} =====")
    print("纯BM25 :", evaluate(retriever_bm25, eval_set, top_k=top_k))
    print("纯向量 :", evaluate(retriever_vector, eval_set, top_k=top_k))
    print("RRF混合:", evaluate(retriever_hybrid, eval_set, top_k=top_k))
