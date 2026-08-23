import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import OpenAI


class OllamaEmbeddingFunction(EmbeddingFunction[Documents]):
    # 用实验A的类（__init__存客户端）
    def __init__(self):
        self._client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

    def __call__(self, input: Documents) -> Embeddings:
        resp = self._client.embeddings.create(model="bge-m3", input=list(input))
        return [r.embedding for r in resp.data]


# TODO 2: 建持久化库，path 用 "./chroma_data_b"（换个文件夹，和实验A的数据不混）
client = chromadb.PersistentClient(path="./chroma_data_b")

# TODO 3: 建 collection
col = client.get_or_create_collection(
    name="hr_kb", embedding_function=OllamaEmbeddingFunction()
)

knowledge = [
    "薪酬发放：每月15号发放上个月的薪水，遇节假日提前到最近的工作日。",
    "年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
    "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
    "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
    "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
    "团建聚餐：每月最后一周有团建活动，公司报销聚餐和场地费用。",
]

col.add(ids=["d1", "d2", "d3", "d4", "d5", "d6"], documents=knowledge)

for q in [
    "我入职两年有几天年假？",
    "工资什么时候发？",
    "最近累，想出去放松两天",
    "团建花钱公司报销吗？",
]:
    res = col.query(query_texts=[q], n_results=2)  # query_text存提问
    print(q, "→", res["documents"][0])
    print("距离：", round(res["distances"][0][0], 3))
