import sqlite3

conn = sqlite3.connect("study.db")
conn.row_factory = sqlite3.Row  # 让每行可以用列名访问（不只是索引）
cursor = conn.cursor()

# --- 统计总数 ---
cursor.execute("SELECT COUNT(*) FROM todos")
total = cursor.fetchone()[0]
print(f"总待办数：{total}")

# --- 按分类统计 ---
cursor.execute(
    "SELECT category, COUNT(*) as cnt FROM todos GROUP BY category ORDER BY cnt DESC"
)
print("\n=== 各分类待办数量 ===")
for row in cursor.fetchall():
    print(f"  {row[0]}：{row[1]}条")

# --- 按用户统计 ---
cursor.execute(
    "SELECT u.username, COUNT(t.id) as count FROM users u LEFT JOIN todos t ON u.id = t.user_id GROUP BY u.id"
)
print("\n=== 每人待办数 ===")
for row in cursor.fetchall():
    print(f"  {row[0]}：{row[1]}条")

# --- MAX 和 MIN ---
cursor.execute("SELECT MIN(id), MAX(id) FROM todos")
min_id, max_id = cursor.fetchone()
print(f"\nID范围：{min_id} ~ {max_id}")

conn.close()
