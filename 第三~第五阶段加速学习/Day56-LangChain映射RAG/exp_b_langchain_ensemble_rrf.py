# 新版本： BM25Retriever 在 community
# EnsembleRetriever(RRF) 在classic
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import jieba


# ⚠️ 中文坑：BM25Retriever 默认按空白分词，中文"一个词都不分" → 必须挂分词器
def jieba_tokenizer(text):
    return list(jieba.cut(text))


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
# 2. 字符串 → Document 对象（page_content=正文；metadata 存 src 编号）
docs = [
    Document(page_content=d, metadata={"src": f"d{i+1}"})
    for i, d in enumerate(code_docs)
]
# ① BM25 侧（映射 Day53 手写 BM25）
bm25 = BM25Retriever.from_documents(documents=docs, preprocess_func=jieba_tokenizer)
bm25.k = 2  # 默认返回全部文档，要限 top2

# ② 向量侧
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OllamaEmbeddings(model="bge-m3"),
    ids=[d.metadata["src"] for d in docs],
    persist_directory="./chroma_data_day56",
)
vec_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ③ 融合（映射 Day53 手写 rrf_score，内部就是 1/(60+rank)）
ensemble = EnsembleRetriever(retrievers=[bm25, vec_retriever], weights=[0.5, 0.5])

# ④ 跑 Day53 的 4 问
for q in [
    "入职两年有几天年假？",
    "工资什么时候发？",
    "最近压力大想请几天假，有政策吗？",
    "外勤报销单编号以什么开头？",
]:
    print(q, "->", [d.page_content for d in ensemble.invoke(q)])
