from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
import jieba
import re


def extract_sources(answer, top_docs):
    """解析回答里的 [编号]，映射回 metadata 里的 src id + 原文"""
    result = []
    for c in re.findall(r"\[(\d+)\]", answer):
        idx = int(c)
        if 1 <= idx <= len(top_docs):
            result.append(
                (c, top_docs[idx - 1].metadata["src"], top_docs[idx - 1].page_content)
            )
            # 举个实际例子：
            #  模型输出回答：`入职满一年有5天年假[1]`
            # - `c = "1"`
            # - `doc.metadata["src"] = "d2"`
            # - `doc.page_content = "年假政策：入职满一年有5天年假，满三年10天，满五年15天。"`#
    return result


def jieba_tokenizer(text):
    return list(jieba.cut(text))


def retriever_langchain(query):
    """返回排好序的 src id 列表（不是 Document，不是下标）"""
    docs = ensemble.invoke(query)
    return [d.metadata["src"] for d in docs]


def evaluate_lc(retriever, eval_set, top_k=1):
    """
    retriever: 一个函数，输入 query，返回排好序的 src id 列表
    eval_set: 实验 A 造的 [(问题, golden), ...]，golden 是 int 或 [int]
    top_k: 看前几名
    返回: hit@top_k（0~1），多答案问题另算 recall@top_k
    """
    hits = 0  # 命中的问题数
    recalls = []  # 每个多答案问题的召回率，最后平均
    for q, golden in eval_set:
        ranked = retriever(q)  # ② 返回"下标"排序列表
        top_k_ranked = ranked[:top_k]
        if isinstance(golden, str):
            if golden in top_k_ranked:

                hits += 1
        else:
            r = len(set(golden) & set(top_k_ranked)) / len(golden)
            recalls.append(r)
            if r == 1.0:
                hits += 1
    hits_rate = hits / len(eval_set)
    avg_recall = sum(recalls) / len(recalls) if recalls else 0.0
    return round(hits_rate, 3), avg_recall


code_docs = [
    "薪酬发放：每月15号发放上个月的薪水，遇节假日提前到最近的工作日。",
    "年假政策：入职满一年有5天年假，满三年10天，满五年15天。",
    "报销规则：出差住宿标准每晚500元，餐饮每天100元，超标部分自理。",
    "晋升规则：每年两次晋升窗口，需要主管推荐和答辩评审。",
    "打卡制度：每天早晚各打卡一次，迟到超过30分钟记一次警告。",
    "团建聚餐：每月最后一周有团建活动，公司报销聚餐和场地费用。",
    "报销单编号规则：外勤报销单编号以R开头（如R-2024-0015），差旅报销单以T开头，月结报销单以M开头。",
    "服务器机房命名规范：生产环境服务器以PROD开头（如PROD-DB-01），测试环境以TEST开头。",
    "内部通知：员工每年年假100天",
]

eval_set_lc = [
    ("PROD-DB-01 是什么服务器？", "d8"),
    ("R-2024-0015 是什么类型的报销单？", "d7"),
    ("最近压力大想请几天假歇歇", "d2"),
    ("好累啊什么时候发工资", "d1"),
    ("我想请两天假出去散心，公司有政策吗", "d2"),
    ("我明天要去上海出差，公司怎么报销跟打卡", "d3"),
    ("我入职两年有几天年假？", "d2"),
    ("公司迟到多久会记警告？", "d5"),
    ("公司一年有几次晋升机会？", "d4"),
    ("每月什么时候举办公司团建聚餐？", "d6"),
    ("请假和报销分别有什么规定？", ["d2", "d3"]),
    ("出差外出需要关注报销与打卡要求有哪些？", ["d3", "d5"]),
]

# 2. 字符串 → Document 对象（page_content=正文；metadata 存 src 编号）
docs = [
    Document(page_content=d, metadata={"src": f"d{i+1}"})
    for i, d in enumerate(code_docs)
]

# 3. BM25 侧（映射 Day53 手写 BM25）
bm25 = BM25Retriever.from_documents(documents=docs, preprocess_func=jieba_tokenizer)
bm25.k = 2

# 3. 向量化建库（映射 Day52 的 ChromaDB；用本地 bge-m3；落盘到新目录，别污染旧库）
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OllamaEmbeddings(model="bge-m3"),
    ids=[d.metadata["src"] for d in docs],
    persist_directory="./chroma_data_day56_polluted",
)

# 4. 取向量检索器（= 输入问题返回前 k 个 Document，映射 Day50 手写 retrieve）
vec_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 5. 融合（映射 Day53 手写 rrf_score，内部就是 1/(60+rank)）
ensemble = EnsembleRetriever(retrievers=[bm25, vec_retriever], weights=[0.5, 0.5])

# 6. 拼 prompt（映射 Day50 build_prompt + Day55 防幻觉）
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是公司HR助手，需要回答员工问题，只能根据下面的资料回答，回答时在每处事实末尾标注来源编号，格式 [1][2]，编号对应资料顺序，资料里没有就说不知道。\n\n{context}",
        ),
        ("user", "{question}"),
    ]
)

# 6. 模型（映射 call_llm；本地 qwen2.5:7b）
llm = ChatOllama(model="qwen2.5:7b")

# 7. LCEL 管道（映射"检索→拼 prompt→生成"整条链）
chain = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    q = "公司一年有几次晋升机会？"
    top_docs = ensemble.invoke(q)
    context_with_index = "\n".join(
        f"[{i+1}] {d.page_content}" for i, d in enumerate(top_docs)
    )  # 检索返回 Document 列表 → 用 enumerate 编号拼 context
    answer = chain.invoke({"context": context_with_index, "question": q})
    sources = extract_sources(answer, top_docs)

    print("=" * 70)
    print(f"问题：{q}")
    print(f"AI回答：{answer}")
    print(f"\n溯源引用解析结果：")
    for mark, src, content in sources:
        print(f"标记[{mark}] → 原始src={src}，原文片段：{content}")
    print(f"retriever.invoke(q) 返回类型：{type(top_docs)}")
    print(f"本次检索拿到文档数量：{len(top_docs)}")
    print(evaluate_lc(retriever_langchain, eval_set_lc[:3], top_k=1))  # 先 3 题
    print(evaluate_lc(retriever_langchain, eval_set_lc, top_k=1))
    print(evaluate_lc(retriever_langchain, eval_set_lc, top_k=3))  # 看多答案 recall
