from openai import OpenAI


def get_embedding(text: str) -> list:
    resp = client.embeddings.create(model="bge-m3", input=text)
    return resp.data[0].embedding


def cosine_similarity(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    len_a = sum(x * x for x in a) ** 0.5
    len_b = sum(y * y for y in b) ** 0.5
    return dot / (len_a * len_b)


def semantic_retrieve(query: str, docs: list, top_k: int = 1) -> list:
    q_vec = get_embedding(query)
    scored = []

    for doc in docs:
        d_vec = get_embedding(doc)
        score = cosine_similarity(q_vec, d_vec)
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    # 可选：打印每条分数方便填表
    for s, d in scored[:top_k]:
        print(f"相似度：{round(s,3)}  文档：{d}")
    return [item[1] for item in scored[:top_k]]


client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

knowledge = [
    "薪酬发放：每月15号发放上个月的薪水，遇节假日提前到最近的工作日。",
    "年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
    "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
    "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
    "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
    "团建聚餐：每月最后一周有团建活动，公司报销聚餐和场地费用。",
]

if __name__ == "__main__":
    print(semantic_retrieve(query="我们公司股票代码是多少？ ", docs=knowledge))
    print(semantic_retrieve(query="今天天气怎么样？ ", docs=knowledge))
    print(semantic_retrieve(query="每个月哪天发钱来着？ ", docs=knowledge))
