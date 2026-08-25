# 实验 C：重排序——LLM 当重排器（P24/25 两阶段管道第二段）

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import OpenAI
from math import log
from collections import Counter
import re


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

# 步骤2：把 query + 5 段带编号的候选塞给 qwen，要求只输出排序
RERANK_PROMPT = """你是检索重排器。下面是查询和 5 段候选资料。
只输出按"相关性从高到低"排序的编号，格式如 [2,1,4,3,5]，不要解释。

查询：{query}
候选：
[1] {doc1}
[2] {doc2}
[3] {doc3}
[4] {doc4}
[5] {doc5}"""
llm_client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

for q in [
    "我入职两年有几天年假？",
    "工资什么时候发？ ",
    "最近累，想出去放松两天 ",
    "团建花钱公司报销吗？ ",
    "R-2024-0015 是什么类型的报销单？",
]:
    print(f"测试问题：{q}")

    # 第一步：BM25 侧，给每篇文档编号。 你已经写好了 bm25_retrieve，它返回的是按分降序排好的列表。用 enumerate把"第几名"抽出来存成字典：
    bm25_result = bm25_retrieve(
        query=q, docs=code_docs, doc_tfs=doc_tfs, avgdl=avgdl, idf=idf, top_k=8
    )
    rank_in_bm25 = {
        doc: i + 1 for i, (score, doc) in enumerate(bm25_result)
    }  # （这里 i+1 就是名次，第一名 = 1。因为 top_k=8 = 全部 8 篇，所以 8 篇文档全在字典里。）

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
    # 输出对比
    print(f"纯BM25 top1：{bm25_result[0][1]}")
    print(f"纯向量top1：{vec_doc[0]}")
    print(f"RRF混合top1：{hybrid[0][1]}")

    # ===== 实验 C：重排（以下全在循环里）=====
    # 步骤1：取混合 top-5 当候选（只要文档，不要分数）
    top_5 = [doc for score, doc in hybrid[:5]]

    # 步骤2：填进 prompt
    prompt_text = RERANK_PROMPT.format(
        query=q,
        doc1=top_5[0],
        doc2=top_5[1],
        doc3=top_5[2],
        doc4=top_5[3],
        doc5=top_5[4],
    )

    # 步骤3：调 LLM

    resp = llm_client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt_text}],
    )
    rerank_text = resp.choices[0].message.content

    # 步骤4：解析 [2,1,4,3,5] → 按编号重排 → 取 top2（避免小模型输出多余文字）
    nums = re.findall(r"\d+", rerank_text)  # 取出所有数字
    order = [int(n) for n in nums if 1 <= int(n) <= 5]  # 只要1-5
    # 解析模型输出的 [..]，取前 2 名，作为"重排后的 top-2"
    reranked_top2 = [
        top_5[i - 1] for i in order[:2]
    ]  # 为什么是 i-1 LLM 看到的是编号 [1]..[5]，Python 列表下标从 0 开始

    # 步骤5：对照组（不重排，直接取 hybrid top2）
    no_rerank_top2 = [doc for score, doc in hybrid[:2]]

    print(f"不重排 top2：{no_rerank_top2}")
    print(f"重排后 top2：{reranked_top2}")
    print("-" * 40)
