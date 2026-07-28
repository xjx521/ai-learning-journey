import sqlite3
import time

conn = sqlite3.connect("index_test.db")
c = conn.cursor()

# # 创建一张大表（模拟真实场景）
# c.execute("""
#     CREATE TABLE articles (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT NOT NULL,
#         category TEXT,
#         content TEXT,
#         created_at TEXT
#     )
# """)

# 批量插入 10000 条数据
categories = ["技术", "生活", "学习", "工作", "娱乐"]
for i in range(10000):
    c.execute(
        "INSERT INTO articles (title, category, content, created_at) VALUES (?, ?, ?, ?)",
        (f"文章第{i}篇", categories[i % 5], "这是一段示例内容" * 100, "2026-01-01"),
    )
conn.commit()
start = time.perf_counter()
for _ in range(10):
    c.execute("SELECT * FROM articles WHERE category = ?", ("技术",))
    c.fetchall()
elapsed_no_index = (time.perf_counter() - start) / 10
print(f"不加索引的平均查询时间: {elapsed_no_index*1000:.2f} ms")

conn.commit()

start = time.perf_counter()
for _ in range(10):
    c.execute("SELECT * FROM articles WHERE category = ?", ("技术",))
    c.fetchall()
elapsed_with_index = (time.perf_counter() - start) / 10
print(f"加索引后的平均查询时间: {elapsed_with_index*1000:.2f} ms")
speedup = (
    elapsed_no_index / elapsed_with_index if elapsed_with_index > 0 else float("inf")
)
print(f"加速比: {speedup:.2f}x")

conn.close()
