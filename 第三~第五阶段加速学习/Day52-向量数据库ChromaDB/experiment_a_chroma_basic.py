# 实验 A：认识 ChromaDB
# 搞清 4 个动作：**建库 → 建 collection → add 存文档 → query 查**。
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import OpenAI


# 把 Day51 的 get_embedding 包成 ChromaDB 的接口：
# __init__ 里存好客户端（只建一次），__call__ 一次性把一批文字批量变向量
class OllamaEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self):
        self._client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

    def __call__(self, input: Documents) -> Embeddings:
        resp = self._client.embeddings.create(
            model="bge-m3", input=list(input)
        )  # 一批文字一次调用
        return [r.embedding for r in resp.data]


# ---- 2. 建库（PersistentClient = 持久化，数据落盘到文件夹）----
client = chromadb.PersistentClient(path="./chroma_data")  # 数据会存到这个文件夹

# ---- 3. 建 collection（相当于"一张表"，embedding_function 告诉它怎么把文字变向量）----
col = client.get_or_create_collection(
    name="hr_policies",  # collection 名字，随便起
    embedding_function=OllamaEmbeddingFunction(),  # 用本地 bge-m3，不额外下载模型
)

# ---- 4. 存文档（add：ids 唯一编号 + documents 内容）----
col.add(
    ids=["doc1", "doc2"],
    documents=[
        "年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
        "薪酬发放：每月15号发放上个月的薪水，遇节假日提前到最近的工作日。",
    ],
)
print("库里现有文档数：", col.count())

# ---- 5. 查（query：只传 query_texts，数据库自动 embedding 问题向量，再 ANN 搜最近的）----
res = col.query(query_texts=["我入职两年有几天年假？"], n_results=1)
print("命中：", res["documents"][0])
print("距离：", res["distances"][0])  # 越小越近（ChromaDB 默认 L2 距离，不是余弦！）
