from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="allama")


def get_embedding(text: str) -> list:
    """把一段文字变成 1024 个数字的向量"""
    resp = client.embeddings.create(model="bge-m3", input=text)  # 调本地向量模型
    return resp.data[0].embedding  # 向量藏在 data[0].embedding 里


# 认识向量：打印维度 + 前几个数字
vec = get_embedding("我们公司的年假政策")
print("维度:", len(vec))
print("前8个数字:", vec[:8])


# 手写余弦相似度：两个向量方向的接近程度
def cosine_similarity(a: list, b: list) -> float:
    """余弦相似度：夹角越小越接近 1。1=同向，0=垂直无关，-1=完全相反"""
    dot = sum(x * y for x, y in zip(a, b))  # 点积：对应位置相乘再求和
    len_a = sum(x * x for x in a) ** 0.5  # 向量 a 的长度（勾股定理推广到 1024 维）
    len_b = sum(x * x for x in b) ** 0.5  # 向量 b 的长度
    return dot / (len_a * len_b)


# 验证"意思相近的挨得近"
s1 = get_embedding("我们公司入职满一年有5天年假")
s2 = get_embedding("转正满一年能休几天假")
s3 = get_embedding("今天天气不错")
s4 = get_embedding("今天天气不错")
print("年假 vs 年假相关:", round(cosine_similarity(s1, s2), 3))  # 应该偏大（0.6~0.9）
print("年假 vs 天气:   ", round(cosine_similarity(s1, s3), 3))  # 应该偏小（<0.5）
print("天气 vs 天气:（同一句）   ", round(cosine_similarity(s3, s4), 3))
