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

# knowledge = [
#     "薪酬发放：每月15号发放上个月的薪水，遇节假日提前到最近的工作日。",
#     "年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
#     "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
#     "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
#     "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
#     "团建聚餐：每月最后一周有团建活动，公司报销聚餐和场地费用。",
# ]

# col.add(
#     ids=["d7", "d8", "d9", "d10", "d11", "d12"],
#     documents=knowledge,
#     metadatas=[
#         {"dept": "finance"},
#         {"dept": "hr"},
#         {"dept": "finance"},
#         {"dept": "hr"},
#         {"dept": "hr"},
#         {"dept": "finance"},
#     ],
# )  # 添加标签
# res = col.query(query_texts=["工资"], n_results=2, where={"dept": "hr"})
# print(res["documents"][0])
# col.update(ids=["d1"], documents=["改后的内容"])
# col.delete(ids=["d2"])
# print("库里现存文档数:", col.count())
# for q in [
#     "我入职两年有几天年假？",
#     "工资什么时候发？",
#     "最近累，想出去放松两天",
#     "团建花钱公司报销吗？",
# ]:
#     res = col.query(query_texts=[q], n_results=2)  # query_text存提问
#     print(q, "→", res["documents"][0])
#     print("距离：", round(res["distances"][0][0], 3))

# C3
text = """员工考勤、年假及差旅报销管理规范：公司执行每日早晚两次打卡制度，员工迟到超过30分钟将记一次书面警告，月度累计多次警告会影响年度绩效评分。年假按司龄分级享受，员工入职满一年可享有5天带薪年假，入职满三年调整为10天，入职满五年及以上可享受15天年假，年假可分段申请，当年未休完年假部分按公司制度结转。员工因公出差可申请差旅报销，住宿标准上限为每晚500元，餐饮补贴为每日100元，超出标准产生的费用由员工个人自行承担，报销需要提供对应票据，走线上审批流程。所有考勤记录、年假剩余天数、报销单据统一由人事与财务部门联合审核，相关疑问可先咨询直属主管，再对接对应职能岗位。"""

chunk1 = text[:100]
chunk2 = text[100:200]
chunk3 = text[200:300]
col.add(ids=["d13"], documents=[text])

col.add(ids=["d14"], documents=chunk1)
col.add(ids=["d15"], documents=chunk2)
col.add(ids=["d16"], documents=chunk3)

# 查询：迟到多久记警告？
query_str = "迟到多久记警告？"
res = col.query(query_texts=[query_str], n_results=4)

print("提问：", query_str)
print("召回全部结果：")
for doc, dist in zip(res["documents"][0], res["distances"][0]):
    print(f"距离(L2): {round(dist,3)}  片段：{doc}")
