from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 8 段知识库（复用 Day50 的 code_docs）
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

# 3. 向量化建库（映射 Day52 的 ChromaDB；用本地 bge-m3；落盘到新目录，别污染旧库）
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OllamaEmbeddings(model="bge-m3"),
    ids=[d.metadata["src"] for d in docs],  # 显式给 id，重跑不会无限加重复
    persist_directory="./chroma_data_day56",
)

# 4. 取检索器（= 输入问题返回前 k 个 Document，映射 Day50 手写 retrieve）
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5},
    search_type="mmr",  # 设置`search_type="mmr"` 最大边际相关性去重
)

# 5. 拼 prompt（映射 Day50 build_prompt + Day55 防幻觉）
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "只能根据下面的资料回答，资料里没有就说不知道。\n\n{context}"),
        ("user", "{question}"),
    ]
)

# 6. 模型（映射 call_llm；本地 qwen2.5:7b）
llm = ChatOllama(model="qwen2.5:7b")

# 7. LCEL 管道（映射"检索→拼 prompt→生成"整条链）
chain = prompt | llm | StrOutputParser()

# 8. 跑一遍：检索 → 原文拼 context → 进管道
query = [
    "入职两年有几天年假？",
    "请假和报销分别有什么规定？",
    "公司一年有几次晋升机会？",
    "每月什么时候举办公司团建聚餐？",
]
for q in query:
    top_docs = retriever.invoke(q)  # 检索
    answer = chain.invoke(
        {"context": "\n".join(d.page_content for d in top_docs), "question": q}
    )
    print("=" * 70)
    print(f"问题：{q}")
    print(f"AI回答：{answer}")
