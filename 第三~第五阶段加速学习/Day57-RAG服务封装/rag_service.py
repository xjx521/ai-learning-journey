from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
import jieba
import re
import os


class RAGService:
    def __init__(
        self,
        *,
        persist_dir,
        llm_model="qwen2.5:7b",
        embed_model="bge-m3",
        k=2,
        retriever_type="ensemble",
    ):
        # 1. 建/加载向量库（用 persist_dir，幂等）
        docs = [
            Document(page_content=d, metadata={"src": f"d{i+1}"})
            for i, d in enumerate(code_docs)
        ]
        if os.path.exists(persist_dir) and os.listdir(persist_dir):
            # 已存在 → 直接加载，不重复写入
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=OllamaEmbeddings(model=embed_model),
                collection_name="hr_docs",
            )
        else:
            # 不存在建库
            self.vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=OllamaEmbeddings(model=embed_model),
                ids=[d.metadata["src"] for d in docs],
                persist_directory=persist_dir,
                collection_name="hr_docs",
            )
        # 2. 按 retriever_type 选检索器：
        self.vector = self.vectorstore.as_retriever(search_kwargs={"k": k})
        self.bm25 = BM25Retriever.from_documents(
            documents=docs, preprocess_func=jieba_tokenizer, k=k
        )
        self.ensemble = EnsembleRetriever(
            retrievers=[self.bm25, self.vector], weights=[0.5, 0.5]
        )

        # 条件判断检索器类型 (测试用)
        if retriever_type == "vector":
            self.retriever = self.vector
        elif retriever_type == "bm25":
            self.retriever = self.bm25
        elif retriever_type == "ensemble":
            self.retriever = self.ensemble
        else:
            raise ValueError(f"不支持的 retriever_type: {retriever_type}")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是公司HR助手，需要回答员工问题，只能根据下面的资料回答，回答时在每处事实末尾标注来源编号，格式 [1][2]，编号对应资料顺序，资料里没有就说不知道。\n\n{context}",
                ),
                ("user", "{question}"),
            ]
        )
        self.llm = ChatOllama(model=llm_model)
        # 4. llm = ChatOllama(...) + chain = prompt | llm | StrOutputParser()
        self.chain = self.prompt | self.llm | StrOutputParser()

    def ask(self, query):
        # 1. self.retriever.invoke(query) → top_docs
        top_docs = self.retriever.invoke(query)
        # 2. enumerate 编号拼 context_with_index
        context_with_index = "\n".join(
            f"[{i+1}] {d.page_content}" for i, d in enumerate(top_docs)
        )
        # 3. self.chain.invoke({"context":..., "question": query}) → answer
        answer = self.chain.invoke({"context": context_with_index, "question": query})
        # 4. [编号] → 过滤越界 → 映射 metadata["src"] + 原文
        sources = self.extract_sources(answer, top_docs)
        # 返回 (answer, [(src_id, 原文), ...])
        return answer, sources

    def extract_sources(self, answer, top_docs):
        """[编号] → 过滤越界 → 映射 metadata["src"] + 原文"""
        result = []
        for c in re.findall(r"\[(\d+)\]", answer):
            idx = int(c)
            if 1 <= idx <= len(top_docs):
                result.append(
                    (
                        top_docs[idx - 1].metadata["src"],
                        top_docs[idx - 1].page_content,
                    )
                )
        return result


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

if __name__ == "__main__":
    svc = RAGService(persist_dir="./chroma_data_day57", k=5, retriever_type="ensemble")
    queries = [
        "请假和报销分别有什么规定",
        "出差报销住宿标准多少？",
    ]
    for q in queries:
        answer, sources = svc.ask(q)  # ← 关键：传问题进来
        # print(type(answer), type(sources))
        print(f"问题：{q}\n答案：{answer}\n引用来源：")
        for src, text in sources:
            print(f"  [{src}] {text}")
        print("-" * 40)
