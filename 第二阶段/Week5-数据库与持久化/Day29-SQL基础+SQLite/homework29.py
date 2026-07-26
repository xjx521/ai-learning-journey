"""
Day 29 练习题：SQL 基础 + SQLite
=================================

⚠️ 前置准备：
    Python 自带 sqlite3 模块，无需安装任何包。
    所有实验写在 main.py 中运行（不是直接跑 homework）。

💡 建议：创建 main.py，逐个添加实验代码并运行验证。
完成每一个「测试」和「问题」后再翻到文件末尾的参考答案。
"""

import sqlite3

# ============================================================
# 【实验 1】建表 + INSERT 插入数据
# ============================================================
"""
目标：用 Python sqlite3 模块创建数据库、建表、插入数据

步骤：创建 main.py，写以下代码：

```python
import sqlite3

# 连接数据库（文件不存在会自动创建）
conn = sqlite3.connect("study.db")
cursor = conn.cursor()

# 建表：用户表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT,
        created_at TEXT DEFAULT (date('now'))
    )
''')

# 建表：待办事项表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT DEFAULT '未分类',
        completed INTEGER DEFAULT 0,
        user_id INTEGER,
        created_at TEXT DEFAULT (date('now'))
    )
''')

# 插入测试数据
users = [
    ('zhangsan', 'zs@test.com'),
    ('lisi', 'ls@test.com'),
    ('wangwu', 'ww@test.com'),
]
cursor.executemany(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    users
)

todos = [
    ('学习 SQL', '完成Day29练习', '学习', 0, 1),
    ('买牛奶', None, '生活', 0, 1),
    ('写周报', '本周完成Web框架学习', '工作', 0, 2),
    ('背单词', '英语六级词汇', '学习', 1, 2),
    ('健身', '跑步5公里', '健康', 0, 3),
    ('交房租', '每月固定支出', '生活', 1, 3),
]
cursor.executemany(
    "INSERT INTO todos (title, description, category, completed, user_id) VALUES (?, ?, ?, ?, ?)",
    todos
)

# 保存并关闭
conn.commit()
print("数据插入成功！")

# 查看一下
cursor.execute("SELECT * FROM users")
print("=== 用户列表 ===")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM todos")
print("=== 待办列表 ===")
for row in cursor.fetchall():
    print(row)

conn.close()
```

📝 **测试 1.1**：运行上面的代码，观察输出结果。

📝 **测试 1.2**：再运行一次（重复插入相同的用户名会怎样？）
会报错 用户名定义了UNIQUE只能唯一不能重复
❓ **问题 1.1**：为什么 INSERT 用 `?` 占位符而不是 f-string？
防止SQL注入攻击
❓ **问题 1.2**：completed 字段为什么用 INTEGER（0/1）而不是 TEXT（'已完成'/'未完成'）？数字比字符串更快
"""


# ============================================================
# 【实验 2】SELECT 查询练习
# ============================================================
"""
目标：练习 WHERE / ORDER BY / LIMIT / OFFSET 等查询语法

步骤：在 main.py 中添加以下代码：

```python
import sqlite3

conn = sqlite3.connect("study.db")
conn.row_factory = sqlite3.Row  # 让每行可以用列名访问（不只是索引）
cursor = conn.cursor()

# --- 练习 2.1：查所有已完成的待办 ---
cursor.execute("SELECT * FROM todos WHERE completed = 1")
rows = cursor.fetchall()
for row in rows:
    print(f"{row['title']} — {row['category']}")

# --- 练习 2.2：按用户查待办（user_id=2 的）---
cursor.execute("SELECT * FROM todos WHERE user_id = ?", (2,))
rows = cursor.fetchall()
for row in rows:
    print(f"[用户{row['user_id']}] {row['title']} — {row['description']}")

# --- 练习 2.3：搜索类别包含"学"的待办，按ID倒序 ---
cursor.execute(
    "SELECT id, title, category FROM todos WHERE category LIKE '%学%' ORDER BY id DESC"
)
for row in cursor.fetchall():
    print(f"#{row['id']} {row['title']} [{row['category']}]")

# --- 练习 2.4：分页——第2页，每页2条 ---
page = 2
page_size = 2
offset = (page - 1) * page_size
cursor.execute(
    "SELECT * FROM todos ORDER BY id ASC LIMIT ? OFFSET ?",
    (page_size, offset)
)
print(f"\n=== 第{page}页（每页{page_size}条）===")
for row in cursor.fetchall():
    print(f"{row['title']}")

conn.close()
```

📝 **测试 2.1**：completed = 1 的有几条？分别是什么？
两条 背单词 — 学习
交房租 — 生活
📝 **测试 2.2**：user_id = 2（lisi）的待办有哪些？
[用户2] 写周报 — 本周完成Web框架学习
[用户2] 背单词 — 英语六级词汇
📝 **测试 2.3**：LIKE '%学%' 匹配了哪些待办？
#4 背单词 [学习]
#1 学习 SQL [学习]
📝 **测试 2.4**：第2页第2条是什么？
背单词
❓ **问题 2.1**：LIMIT 和 OFFSET 的顺序能调换吗？为什么？
SQL 标准执行顺序是 ORDER BY -> LIMIT -> OFFSET。SQLite 允许互换位置但不推荐。
         正确的语义：先排好序，取前 N 条，跳过 M 条。写成标准顺序不容易出错。
❓ **问题 2.2**：ORDER BY 不指定的话，结果的顺序是固定的吗？不是 ORDER BY指定id排序
"""


# ============================================================
# 【实验 3】UPDATE + DELETE 实验
# ============================================================
"""
目标：练习更新和删除数据

步骤：在 main.py 中添加以下代码：

```python
import sqlite3

conn = sqlite3.connect("study.db")
cursor = conn.cursor()

# --- 练习 3.1：标记 "买牛奶" 为已完成 ---
cursor.execute(
    "UPDATE todos SET completed = 1 WHERE title = ?",
    ("买牛奶",)          # 注意逗号！元组必须有一个逗号
)
print(f"影响了 {cursor.rowcount} 行")

# --- 练习 3.2：同时更新多个字段 ---
cursor.execute(
    "UPDATE todos
       SET title = ?, created_at = date('now')
       WHERE id = ?",
    ("买全脂牛奶", 2)     # 给created_at加一个字段演示多字段更新
)
print(f"更新了 {cursor.rowcount} 行")

# --- 练习 3.3：删除一条待办 ---
cursor.execute("DELETE FROM todos WHERE title = ? AND user_id = ?",
               ("健身", 3))
print(f"删除了 {cursor.rowcount} 行")

# --- 验证修改 ---
cursor.execute("SELECT * FROM todos WHERE user_id = 1")
print("\n=== zhangsan 的待办 ===")
for row in cursor.fetchall():
    status = "✅" if row["completed"] else "❌"
    print(f"  {status} {row['title']} — {row['category']}")

conn.commit()
conn.close()
```

📝 **测试 3.1**：UPDATE 后 affected rows 是多少？
影响了1行
📝 **测试 3.2**：如果 WHERE 条件是 title = '学'（模糊匹配）呢？会发生什么？
会报错 数据库中没有完全等于学的行 模糊匹配要用LIKE
📝 **测试 3.3**：DELETE 后还能恢复吗？
不能
💡 **破坏性实验**（千万别在真实项目上试）：
把 UPDATE todos SET completed = 1 WHERE title = '买牛奶' 里的 WHERE 去掉：
```sql
UPDATE todos SET completed = 1;
```
会发生什么？想一想，然后再自己试试看。
会把所有completed设置为1
❓ **问题 3.1**：如何批量把所有"学习"分类的待办改为已完成？
UPDATE todos SET completed = 1 WHERE category = '学习';
"""


# ============================================================
# 【实验 4】INNER JOIN + LEFT JOIN 多表查询
# ============================================================
"""
目标：理解 JOIN 的实际用法，这是 SQL 中最重要也最容易混淆的部分

步骤：在 main.py 中添加以下代码：

```python
import sqlite3

conn = sqlite3.connect("study.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# --- INNER JOIN ---
print("=== INNER JOIN：有匹配的才显示 ===")
cursor.execute("
    SELECT u.username, t.title, t.completed, t.category
    FROM users u
    INNER JOIN todos t ON u.id = t.user_id
    ORDER BY u.id, t.id
")
for row in cursor.fetchall():
    done = "✅已完成" if row["completed"] else "❌未完成"
    print(f"  [{row['username']}] {row['title']} [{row['category']}] {done}")

# --- LEFT JOIN ---
print("\n=== LEFT JOIN：左表全部保留 ===")
cursor.execute("
    SELECT u.username, t.title, t.completed
    FROM users u
    LEFT JOIN todos t ON u.id = t.user_id
    ORDER BY u.id
")
for row in cursor.fetchall():
    title = row["title"] if row["title"] else "(暂无待办)"
    print(f"  {row['username']} → {title}")

# --- 分组统计 ---
print("\n=== 按用户统计待办数量 ===")
cursor.execute("
    SELECT u.username,
           COUNT(t.id) as total,
           SUM(CASE WHEN t.completed = 1 THEN 1 ELSE 0 END) as done_count
    FROM users u
    LEFT JOIN todos t ON u.id = t.user_id
    GROUP BY u.id
    HAVING total > 0
")
for row in cursor.fetchall():
    print(f"  {row['username']}：{row['total']}条待办，完成{row['done_count']}条")

conn.close()
```

📝 **测试 4.1**：INNER JOIN 结果中 wangwu 出现了吗？为什么？
没有 todos表没有对应id
📝 **测试 4.2**：LEFT JOIN 结果中 wangwu 出现了吗？右边填了什么？
出现了 填了null
❓ **问题 4.1**：什么时候该用 INNER JOIN，什么时候该用 LEFT JOIN？
需要查看所有用户名单用INNER JOIN 查看所有待办事项用LEFT JOIN
❓ **问题 4.2**：`SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END)` 这个写法什么意思？试着用 Python 代码翻译一遍。
sum(1 if completed else 0 for todo in todos)"""


# ============================================================
# 【实验 5】聚合函数统计
# ============================================================
"""
目标：掌握 COUNT/SUM/AVG/MAX/MIN + GROUP BY

步骤：在 main.py 中添加以下代码：

```python
import sqlite3

conn = sqlite3.connect("study.db")
cursor = conn.cursor()

# --- 统计总数 ---
cursor.execute("SELECT COUNT(*) FROM todos")
total = cursor.fetchone()[0]
print(f"总待办数：{total}")

# --- 按分类统计 ---
cursor.execute("
    SELECT category, COUNT(*) as cnt
    FROM todos
    GROUP BY category
    ORDER BY cnt DESC
")
print("\n=== 各分类待办数量 ===")
for row in cursor.fetchall():
    print(f"  {row[0]}：{row[1]}条")

# --- 按用户统计 ---
cursor.execute("
    SELECT u.username, COUNT(t.id) as count
    FROM users u
    LEFT JOIN todos t ON u.id = t.user_id
    GROUP BY u.id
")
print("\n=== 每人待办数 ===")
for row in cursor.fetchall():
    print(f"  {row[0]}：{row[1]}条")

# --- MAX 和 MIN ---
cursor.execute("SELECT MIN(id), MAX(id) FROM todos")
min_id, max_id = cursor.fetchone()
print(f"\nID范围：{min_id} ~ {max_id}")

conn.close()
```

❓ **问题 5.1**：GROUP BY 后面能不能跟一个非聚合列？比如 `SELECT category, title FROM todos GROUP BY category`？为什么？
不能
❓ **问题 5.2**：HAVING 和 WHERE 有什么区别？
where过滤分组前结果 HAVING过滤分组后结果
"""


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 58 - 最后一个单词的长度（Easy）
#    链接：https://leetcode.cn/problems/length-of-last-word/
#    思路提示：SQL的LIKE和字符串处理类似，这道题锻炼你对字符串边界和空格的处理能力
#
# 2. LeetCode 196 - 删除重复的电子邮箱（简单SQL思维题）
#    链接：https://leetcode.cn/problems/delete-duplicate-emails/
#    思路提示：自连接（self-join）+ DELETE，对应今天学的 DELETE + JOIN 概念
# ============================================================


# ============================================================
# 💡 参考答案（完成所有练习后再看！）
# ============================================================
#
# 使用说明：先独立做完上面所有【测试】和【问题】，再打开这里对照。
# 如果你的答案思路接近就算对，不必文字完全一致。
# ------------------------------------------------------------

"""
== 实验 1 参考答案 ==

测试 1.1：输出了 3 个用户记录 + 6 条待办记录。
测试 1.2：报错 —— SQLite: UNIQUE constraint failed: users.username（因为 UNIQUE 约束阻止重复插入）。

问题 1.1：防止 SQL 注入攻击。如果用 f-string，恶意用户可以输入 '"'; DROP TABLE users;--' 来删库。
         用 ? 占位符让 sqlite3 自动处理转义，SQL 注入语句只会当作普通字符串存入，不会执行。
问题 1.2：①节省空间，数字比较比字符串比较快；②JOIN/聚合时用数字更方便；
         ③SQLite 中 BOOLEAN 本身就是存为 0/1。

== 实验 2 参考答案 ==

测试 2.1：2 条 —— 背单词、交房租。
测试 2.2：写周报、背单词。
测试 2.3：学习SQL（category=学习）、背单词（category=学习）。
测试 2.4：写周报（排序后第3条，即第2页第2条）。

问题 2.1：SQL 标准执行顺序是 ORDER BY -> LIMIT -> OFFSET。SQLite 允许互换位置但不推荐。
         正确的语义：先排好序，取前 N 条，跳过 M 条。写成标准顺序不容易出错。
问题 2.2：不一定。ORDER BY 不指定时，结果是引擎决定的物理顺序（通常是 insert 顺序），但不保证稳定。
         生产环境一定要显式指定 ORDER BY。

== 实验 3 参考答案 ==

测试 3.1：1 行（只有"买牛奶"这一条被更新）。
测试 3.2：WHERE title = '学' 只会精确匹配 title 完全等于"学"的行。但如果改成 LIKE '%学%' 就会匹配所有含"学"的行——太危险！
         这说明了 WHERE 条件要写精确的重要性。
测试 3.3：不能直接恢复。SQLite 没有撤销命令。所以 DELETE 前先用 SELECT 看看要删哪些！！！

问题 3.1：UPDATE todos SET completed = 1 WHERE category = '学习';

== 实验 4 参考答案 ==

测试 4.1：没有出现。wangwu 没有任何待办数据，INNER JOIN 只保留两张表都有匹配的行。
测试 4.2：出现了。用户名正常显示，右边填了 "(暂无待办)"（即 title = NULL 时被替代了）。

问题 4.1：想只看有关联数据的用 INNER JOIN；想看完整名单（包括没数据的）用 LEFT JOIN。
         例如："查出所有有待办的用户"用 INNER JOIN；"查每个用户的待办情况（含零待办用户）"用 LEFT JOIN。
问题 4.2：这是 SQL 的条件求和。相当于 Python 的：
         sum(1 if todo.completed else 0 for todo in todos)
         CASE WHEN completed=1 THEN 1 ELSE 0 END → 每条记录判断
         SUM(...) → 加起来就是完成的数量

== 实验 5 参考答案 ==

问题 5.1：不行。这会报 SQL 错误。每个分组里选哪个 title？数据库不确定。
         SELECT 只能放 GROUP BY 的列或聚合函数。
问题 5.2：WHERE 过滤的是原始行（分组前），HAVING 过滤的是分组后的结果（分组后）。
         WHERE 不能用聚合函数，HAVING 可以。
         例如：WHERE completed=0 筛选出未完成的行；HAVING COUNT(*)>1 筛选出待办多于1条的用户。

== LeetCode 思路 ==

LC 58：用 rstrip().split() 或正则 \b\w+$ 找到最后一个单词然后算长度。
LC 196：用自连接 DELETE，选出 id 较大的那条删除：
   DELETE p1 FROM Persons p1, Persons p2 WHERE p1.email = p2.email AND p1.id > p2.id
"""


# ============================================================
# 📝 今日学习记录
# ============================================================
"""
📝 Day 29 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：建表 + INSERT
[ ] 实验 2：SELECT 查询
[ ] 实验 3：UPDATE + DELETE
[ ] 实验 4：JOIN 多表查询
[ ] 实验 5：聚合函数统计

遇到的问题：
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
