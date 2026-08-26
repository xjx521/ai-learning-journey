from openai import OpenAI
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from collections import Counter
from math import log
import re


class OllamaEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self):
        self._client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

    def __call__(self, input: Documents) -> Embeddings:
        resp = self._client.embeddings.create(model="bge-m3", input=list(input))
        return [r.embedding for r in resp.data]


def tokenize(text):
    return list(text)


def bm25_score(q, doc_tf, doc_len, avgdl, idf, k1=1.5, b=0.75):
    score = 0.0
    for token in tokenize(q):
        if token not in idf:
            continue
        tf = doc_tf.get(token, 0)
        if tf == 0:
            continue
        denom = tf + k1 * (1 - b + b * doc_len / avgdl)
        score += (idf[token] * (tf * (k1 + 1))) / denom
    return score


def bm25_retrieve(q, docs, doc_tfs, avgdl, idf, top_k=1):
    scored = []
    for index, doc in enumerate(docs):
        score = bm25_score(
            q=q, doc_tf=doc_tfs[index], doc_len=len(doc), avgdl=avgdl, idf=idf
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


def retrieve_top_k(q, k=2):
    """Day54 的 retriever_hybrid，返回前 k 个文档字符串"""
    # 第一步：BM25 侧，给每篇文档编号。 你已经写好了 bm25_retrieve，它返回的是按分降序排好的列表。用 enumerate把"第几名"抽出来存成字典：
    bm25_result = bm25_retrieve(
        q=q, docs=code_docs, doc_tfs=doc_tfs, avgdl=avgdl, idf=idf, top_k=8
    )
    rank_in_bm25 = {doc: i + 1 for i, (score, doc) in enumerate(bm25_result)}
    # 第二步：ChromaDB 侧，同样编一份号。
    vec_result = col.query(query_texts=[q], n_results=8)
    vec_doc = vec_result["documents"][0]
    rank_in_vec = {doc: i + 1 for i, doc in enumerate(vec_doc)}

    # 第三步：融合。对 8 篇文档循环，每篇算 rrf_score(rank_in_bm25[doc], rank_in_vector[doc])，存成 (融合分, doc)的列表，排序取第一名。
    hybrid = []
    for doc in code_docs:
        rrf = rrf_score(rank_in_bm25[doc], rank_in_vec[doc])
        hybrid.append((rrf, doc))
    hybrid.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in hybrid[:k]]


def build_prompt(query, docs):
    doc_line = []
    for idx, doc in enumerate(docs, start=1):
        doc_line.append(f"[{idx}] {doc}")
    doc_content = "资料：\n" + "\n".join(
        doc_line
    )  #  给每段编号 [1][2]，拼成"资料：\n[1] ...\n[2] ..."
    system = f"""{doc_content}你是公司HR助手，请回答员工的问题。只能依据上面提供的资料回答用户问题；资料没有相关信息就直接说不知道。回答每一处事实后面必须标注来源编号，格式[1][2]。"""  #  拼 system（防幻觉 + 引用要求）+ user（问题）
    messages = [{"role": "user", "content": query}]
    return system, messages


def extract_citations(answer):
    result = re.findall(r"\[(\d+)\]", answer)  #  提出所有编号
    raw = [int(num) for num in result]
    return raw


def call_llm(system, messages):
    """对接大模型，输入system、messages，返回模型字符串回答，自行替换成你的OpenAI/Ollama调用"""
    resp = llm_client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": system},
        ]
        + messages,
    )
    return resp.choices[0].message.content


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
doc_tfs = [Counter(tokenize(doc)) for doc in code_docs]
N = len(code_docs)
doc_freq = {}
for tf in doc_tfs:
    for token in tf:
        doc_freq[token] = doc_freq.get(token, 0) + 1
idf = {t: log(1 + (N - df + 0.5) / (df + 0.5)) for t, df in doc_freq.items()}
avgdl = sum(len(d) for d in code_docs) / N
llm_client = OpenAI(api_key="ollama", base_url="http://127.0.0.1:11434/v1")
client = chromadb.PersistentClient(path="./chroma_data")

col = client.get_or_create_collection(
    name="hr_hybrid", embedding_function=OllamaEmbeddingFunction()
)
col.upsert(ids=["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8"], documents=code_docs)
queries = [
    "入职两年有几天年假？",
    "出差报销住宿标准多少？",
    "晋升需要什么条件？",
    "团建费用公司报销吗？",
]
for query in queries:
    docs = retrieve_top_k(query, k=2)
    system, message = build_prompt(query, docs)
    answer = call_llm(system, message)
    print(f"问题：{query}\n答案：{answer}\n引用来源：")
    for c in extract_citations(answer):
        if 1 <= c <= len(docs):
            print(f"[{c}] {docs[int(c)-1]}")
    print("-" * 40)
