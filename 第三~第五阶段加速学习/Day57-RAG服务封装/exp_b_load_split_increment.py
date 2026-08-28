from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_service import RAGService

# 1.加载txt文档
text = TextLoader(file_path="docs/员工手册.txt", encoding="utf-8")
docs = text.load()
doc = docs[0]
print("原始大文档page_content长度：", len(doc.page_content))  # 打印长度
print("Loader自带metadata：", doc.metadata)  # 打印 metadata（含 source 字段）


# 2.递归字符分块
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
split_chunks = splitter.split_documents(docs)
for idx, chunk in enumerate(split_chunks):
    chunk.metadata["src"] = f"{chunk.metadata["source"]}#{idx}"

print(f"分块之后总块数：{len(split_chunks)}")

# 3.入库校验
svc = RAGService(persist_dir="./chroma_data_day57_text", k=5)  # 复用 A 的库（8段已在）
vs = svc.vectorstore
chunk_ids = {f"emp#{i}" for i in range(len(split_chunks))}
vs.add_documents(split_chunks, ids=chunk_ids)
print("验证数量：", vs._collection.count())

# 4. 增量更新（全部走 langchain 层，用 bge-m3，不碰底层 MiniLM污染向量库）
# 4a. 演示"幂等更新 = count 不涨"：改一段 → 同 id 先删再加
modified = "（修订）迟到超过30分钟记一次警告，累计三次约谈。"
vs.delete(ids=["emp#0"])  # 删旧 emp#0
vs.add_texts(
    texts=[modified], ids=["emp#0"], metadatas=[{"src": "员工手册.txt#0"}]  # 同 id 加回
)
print("更新 emp#0 后数量（应不变）：", vs._collection.count())

# 4b. 演示"新增 + 删除"
vs.add_texts(texts=["你好"], ids=["emp#17"])  # 新增
print("增量新增验证数量：", vs._collection.count())
vs.delete(ids=["emp#17"])  # 删除
print("删一段验证数量：", vs._collection.count())
