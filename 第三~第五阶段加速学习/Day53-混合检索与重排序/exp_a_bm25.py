# 实验 A：手写 BM25 关键词打分（P13）
# BM25 是正规军：**稀有字撞上更值钱（IDF）+ 同字重复价值递减（TF 归一化）+ 长文档被惩罚**
from math import log  # `log`：计算 IDF 逆文档频率用到对数
from collections import (
    Counter,
)  # `Counter`：快速统计每个字符在文档里出现多少次（统计词频 TF）


# ---- 0. 中文分词：没有空格，先用"每个字一个 token"（字符级）----
def tokenize(text):
    return list(text)  # "报销规则" -> ['报','销','规','则']


# ---- 1. 每篇文档的词频 TF（token 在文档里出现几次）----
docs = [
    "薪酬发放：每月15号发放上个月的薪水，遇节假日提前到最近的工作日。",
    "年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
    "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
    "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
    "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
    "团建聚餐：每月最后一周有团建活动，公司报销聚餐和场地费用。",
]
doc_tfs = [
    Counter(tokenize(doc)) for doc in docs
]  # 每段文档一个 Counter 统计每个字符出现几次(TF词频)

# ---- 2. 逆文档频率 IDF（这个 token 在几篇文档里出现过？越少越值钱）----
N = len(docs)  # 总文档数量
doc_freq = (
    {}
)  # `doc_freq[token]`：记录**这个字符一共出现在多少篇文档**（不是总出现次数！是出现过该字的文档篇数）。
# 举例：“的” 几乎 6 篇文档都出现，doc_freq 很高；“薪” 只出现在少数文档，doc_freq 很小。
for tf in doc_tfs:
    for token in tf:
        doc_freq[token] = doc_freq.get(token, 0) + 1
idf = {t: log(1 + (N - df + 0.5) / (df + 0.5)) for t, df in doc_freq.items()}
# **IDF 逆文档频率**
# - df：该 token 出现在多少篇文档
# - 一个词出现在越少文档 (df 越小)，IDF 计算出来数值越大，代表这个词更珍贵，命中之后加分更高。
# > 加 0.5 是平滑，防止分母为 0（查询出现完全没见过的字符）

avgdl = (
    sum(len(d) for d in docs) / N
)  # 所有文档的平均字符长度，BM25 用来做**长文档惩罚**


# ---- 3. BM25 打分公式（k1=1.5, b=0.75 经典默认值）----
#   score(d,q) = Σ_{query里的每个字}  IDF * tf*(k1+1) / (tf + k1*(1-b + b*len(d)/avgdl))
#   直觉：tf 越大分越高但"递增变慢"；len(d) 越长分被拉低（惩罚又长又重复的文档）
def bm25_score(query, doc_tf, doc_len, avgdl, idf, k1=1.5, b=0.75):
    """
    1. `query` 用户提问
    2. `doc_tf`：当前文档的 Counter 词频对象
    3. `doc_len`：当前文档字符长度
    4. `avgdl`：全部文档平均长度
    5. `idf`：全局 idf 字典
    6. `k1=1.5`：控制**TF 词频饱和**。同一个词反复出现，分数不会无限上涨。k1 越大，词重复还能继续涨分；k1 越小很快饱和。
    7. `b=0.75`：**长文档惩罚系数**。文档比平均文档长就会被扣分
    """
    score = 0.0
    for token in tokenize(query):
        if token not in idf:
            continue  # query 的字全库没见过，跳过
        tf = doc_tf.get(token, 0)
        if tf == 0:
            continue
        denom = tf + k1 * (1 - b + b * doc_len / avgdl)
        score += (
            idf[token] * (tf * (k1 + 1)) / denom
        )  # 套用 BM25 完整公式，累加分数 返回该文档对于这条 query 的 BM25 总分。
    return score


# def char_overlap_score(query: str, doc: str) -> int:
#     q_set = set(query)
#     d_set = set(doc)
#     return len(q_set & d_set)


def bm25_retrieve(
    query: str, docs: list, doc_tfs: list, avgdl: int, idf: dict, top_k: int = 1
) -> list:
    scored = []
    for index, doc in enumerate(docs):
        # score = char_overlap_score(query, doc)
        score = bm25_score(
            query=query, doc_tf=doc_tfs[index], doc_len=len(doc), avgdl=avgdl, idf=idf
        )  # 把打分函数替换成正规军bm25
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    for q in [
        "我入职两年有几天年假？",
        "工资什么时候发？ ",
        "最近累，想出去放松两天 ",
        "团建花钱公司报销吗？ ",
    ]:
        result = bm25_retrieve(
            query=q, docs=docs, doc_tfs=doc_tfs, avgdl=avgdl, idf=idf
        )
        print("==== BM25检索结果 ====")
        for score, doc in result:
            print(f"分数:{round(score,3)} 文档：{doc}")
