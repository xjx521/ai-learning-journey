"""
Day 30 练习题：SQLAlchemy ORM 基础 — 模型定义、CRUD、关系映射
===========================================================

⚠️ 前置准备：
    pip install sqlalchemy
    （不需要安装数据库！SQLite 是 Python 内置的）

💡 建议：所有实验写在 main.py 中，逐个添加测试通过后再继续。
完成每一个「测试」和「问题」后再翻到文件末尾的参考答案。
"""

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

# ============================================================
# 【实验 1】定义 User + Todo 模型（一对多关系）
# ============================================================
"""
目标：理解 SQLAlchemy 如何建模两个表的关系

步骤：在 models.py 中定义两个类：

```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    # ⭐ 一对多关系
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, default="未分类")
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # ⭐ 外键

    owner = relationship("User", back_populates="todos")
```

📝 **测试 1.1**：检查两个模型是否正确定义了字段——分别列出 User 和 Todo 的属性名。
User:id,username,email,hashed_password Todo:id,title,description,category,completed,user_id
📝 **测试 1.2**：运行 `Base.metadata.create_all(bind=engine)` 后生成了什么？
      用 sqlite3 命令行打开生成的 .db 文件，输入 `.schema` 看看实际建了什么表。
实际建了todos和users表
❓ **问题 1.1**：`cascade="all, delete-orphan"` 的作用是什么？
级联操作——"all" 表示对 User 做的所有操作（增、删、改）都自动级联到他的 Todos；
"delete-orphan" 表示如果 User 被删了，他的所有 Todo 也一起被删（孤儿不允许存在）。
如果不加这个，只删 User 不会动 Todo。
❓ **问题 1.2**：`back_populates` 需要两边都写吗？如果只在一边写会怎样？
需要两边都写，才能建立双向关联。只在一边写的话：
只能从 User 访问 Todo（`user.todos` 能拿到待办列表），
但不能从 Todo 访问 User（`todo.owner` 会报错或返回 None）。
"""


# ============================================================
# 【实验 2】Session CRUD — 增删改查
# ============================================================
"""
目标：掌握最基本的数据库操作

步骤：创建 main.py：

```python
import sys
sys.path.insert(0, '.')          # 找到 models.py
from models import Base, User, Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///crud_test.db", echo=False)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# --- 新增 ---
user = User(username="zhangsan", email="zs@test.com", hashed_password="hashed_abc")
db.add(user)
db.commit()
db.refresh(user)                   # 刷新：从数据库重新读取（获取自增的 id）
print(f"新建用户：{user.username} (ID={user.id})")

todo1 = Todo(title="学习 SQL", category="学习", user_id=user.id)
todo2 = Todo(title="买牛奶", category="生活", completed=True, user_id=user.id)
db.add_all([todo1, todo2])
db.commit()

# --- 查询所有 ---
all_users = db.query(User).all()
for u in all_users:
    print(f"用户：{u.username}, {u.email}")

# --- 条件查询 ---
completed_todos = db.query(Todo).filter(Todo.completed == True).all()
print(f"\n已完成的待办：{len(completed_todos)} 条")

incomplete_todos = db.query(Todo).filter(Todo.completed == False).all()
print(f"未完成的待办：{len(incomplete_todos)} 条")

# --- 更新 ---
todo = db.get(Todo, todo1.id)
todo.title = "复习 SQL"            # 改标题
todo.completed = True              # 标记完成
db.commit()

# --- 删除 ---
todo_to_delete = db.get(Todo, todo2.id)
db.delete(todo_to_delete)
db.commit()

# --- 验证最终状态 ---
print(f"\n=== 最终状态 ===")
print(f"用户数：{db.query(User).count()}")
print(f"待办数：{db.query(Todo).count()}")
print(f"未完成数：{db.query(Todo).filter(Todo.completed==False).count()}")

db.close()
```

📝 **测试 2.1**：插入 1 个用户 + 2 个待办，查询结果对吗？分别打印出数量。
对 1个用户两个待办
📝 **测试 2.2**：更新 todo1 的标题和 completed 后，再查一次得到的结果是什么？
title变成复习 completed=ture
📝 **测试 2.3**：删除 todo2 后，剩余的待办数是几？
1条
💡 **破坏性实验**：把 `db.commit()` 注释掉，然后再查——数据还在吗？为什么？
不在 数据未提交到数据库只是保存到对话session里面
❓ **问题 2.1**：`db.refresh()` 什么时候必须用？
获取自增id的时候
❓ **问题 2.2**：`db.get(Model, id)` 和 `db.query(Model).filter(Model.id == id).first()` 有什么区别？
get() 直接用主键查，走缓存更快（类似 dict.get()）；
filter 是通用查询，慢一些但功能更多（可以组合多个条件）
"""


# ============================================================
# 【实验 3】过滤 + 排序 + 分页
# ============================================================
"""
目标：练习各种查询条件、排序和分页

步骤：在 main.py 中添加以下代码：

```python
import sys
sys.path.insert(0, '.')
from models import Base, User, Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///query_test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# --- 先插入测试数据 ---
u1 = User(username="zhangsan", hashed_password="pwd1")
u2 = User(username="lisi", hashed_password="pwd2")
db.add_all([u1, u2])
db.flush()                             # flush 但不 commit，先拿 ID

db.add_all([
    Todo(title="学习 Python", category="学习", completed=False, user_id=u1.id),
    Todo(title="学习 SQL", category="学习", completed=True, user_id=u1.id),
    Todo(title="学习 FastAPI", category="学习", completed=False, user_id=u1.id),
    Todo(title="买牛奶", category="生活", completed=True, user_id=u1.id),
    Todo(title="写周报", category="工作", completed=False, user_id=u2.id),
    Todo(title="背单词", category="学习", completed=False, user_id=u2.id),
])
db.commit()

# --- 查询练习 ---
# Q1: 查 zhangsan 的所有待办
zs_todos = db.query(Todo).filter(Todo.user_id == u1.id).all()
print(f"[张三] 共 {len(zs_todos)} 条：")
for t in zs_todos:
    print(f"  {'✅' if t.completed else '❌'} {t.title}")

# Q2: 按 completed 分组统计
done = len(db.query(Todo).filter(Todo.completed == True).all())
pending = len(db.query(Todo).filter(Todo.completed == False).all())
print(f"\n已完成：{done}，未完成：{pending}")

# Q3: 按类别分组
cats = db.query(Todo.category).distinct().all()
print(f"\n类别：{[c[0] for c in cats]}")

# Q4: 排序——未完成排前面
unsorted = db.query(Todo).order_by(Todo.completed.desc(), Todo.title.asc()).all()
print("\n=== 排序：已完成在前，同组内按标题字母序 ===")
for t in unsorted:
    print(f"  [{t.category}] {t.title} ({'已完成' if t.completed else '未完成'})")

# Q5: 分页——第1页，每页3条
page, size = 1, 3
offset = (page - 1) * size
page_data = db.query(Todo).order_by(Todo.id).limit(size).offset(offset).all()
print(f"\n=== 第{page}页（每页{size}条）===")
for t in page_data:
    print(f"  {t.title}")

# Q6: LIKE 模糊搜索
keyword = "学习"
results = db.query(Todo).filter(Todo.title.like(f"%{keyword}%")).all()
print(f"\n搜索关键词'{keyword}'：")
for r in results:
    print(f"  {r.title}")

db.close()
```

📝 **测试 Q1**：zhangsan 有几条待办？列出标题。
4条待办   ❌ 学习 Python
  ✅ 学习 SQL
  ❌ 学习 FastAPI
  ✅ 买牛奶
📝 **测试 Q4**：排序后的完整顺序是什么？
=== 排序：已完成在前，同组内按标题字母序 ===
  [生活] 买牛奶 (已完成)
  [学习] 学习 SQL (已完成)
  [工作] 写周报 (未完成)
  [学习] 学习 FastAPI (未完成)
  [学习] 学习 Python (未完成)
  [学习] 背单词 (未完成)
📝 **测试 Q5**：第1页第3条是什么？
  学习 FastAPI
📝 **测试 Q6**：LIKE '%学习%' 匹配了几条？分别是什么？
三条搜索关键词'学习'：
  学习 Python
  学习 SQL
  学习 FastAPI
❓ **问题 3.1**：`db.flush()` 和 `db.commit()` 的区别是什么？
flush 把数据同步到当前事务的数据库中（能在同一个 session 中被立即查到），
         但不真正提交到磁盘（其他数据库连接看不到）。
         commit 才是真正持久化保存（其他连接也能看到，且不可 rollback）。
❓ **问题 3.2**：`order_by(Todo.completed.desc(), Todo.title.asc())` 这个写法是什么意思？
先按 completed **倒序**(降序)排，True(已完成=1)排前面，False(未完成=0)排后面；
同一组内再按 title **正序**(升序)排，A-Z 字母顺序。
"""


# ============================================================
# 【实验 4】joinedload 关联查询
# ============================================================
"""
目标：用 ORM 的方式做 JOIN 查询，一次拿回关联数据

步骤：在 main.py 中添加以下代码：

```python
import sys
sys.path.insert(0, '.')
from models import Base, User, Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.orm import DeclarativeBase as _Base

# ---------- 重新建库，干净环境 ----------
import os
if os.path.exists("join_test.db"):
    os.remove("join_test.db")

engine = create_engine("sqlite:///join_test.db")
_Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 插入用户和待办
u1 = User(username="zhangsan", hashed_password="h1")
u2 = User(username="lisi", hashed_password="h2")
db.add_all([u1, u2])
db.flush()

db.add_all([
    Todo(title="学习 SQL", user_id=u1.id, category="学习"),
    Todo(title="买牛奶", user_id=u1.id, category="生活"),
    Todo(title="写报告", user_id=u2.id, category="工作"),
])
db.commit()

# --- 方法1：不用 joinedload —— N+1 问题 ---
print("=== 方法1：N+1 查询 ===")
users = db.query(User).all()
for user in users:
    print(f"{user.username}:")
    for todo in user.todos:            # 🔴 每次循环都会单独发一条 SQL！
        print(f"  - {todo.title}")

# --- 方法2：用 joinedload —— 一条 SQL 搞定 ---
print("\n=== 方法2：joinedload 查询 ===")
users = db.query(User).options(joinedload(User.todos)).all()
for user in users:
    print(f"{user.username}:")
    for todo in user.todos:            # ✅ 已经预加载好了，不再查数据库
        print(f"  - {todo.title}")

db.close()
```

📝 **测试 4.1**：如果有 100 个用户，"方法1"总共执行几条 SQL？"方法2"呢？
 101条（1个查user100个查todo）
❓ **问题 4.1**：joinedload 生成的 SQL 和原生 JOIN 有什么关系？
问题 4.1：都是 INNER JOIN（LEFT OUTER JOIN）。SQLAlchemy 帮你自动拼接 SQL 字符串，
         你只需要告诉它"我要预加载哪些关系"。

❓ **问题 4.2**：relationship 默认是 lazy loading 还是 eager loading？
问题 4.2：lazy loading（懒加载）。访问 user.todos 时才去查数据库。
         joinedload 把它改成 eager loading（预加载），一次性取回所有关联数据
"""


# ============================================================
# 【实验 5】外键约束 + 级联删除破坏性实验
# ============================================================
"""
目标：理解外键和级联行为对数据的影响

步骤：观察以下行为：

```python
import sys
sys.path.insert(0, '.')
from models import Base, User, Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///cascade_test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 插入一个用户和他的待办
u = User(username="test_user", hashed_password="pw")
db.add(u)
db.flush()
db.add_all([
    Todo(title="待办A", user_id=u.id),
    Todo(title="待办B", user_id=u.id),
])
db.commit()
print(f"用户{u.username}有 {len(db.query(Todo).filter(Todo.user_id==u.id).all())} 条待办")

# 尝试删除用户
db.delete(u)
db.commit()                            # 会发生什么？

# 检查剩余数据
remaining = db.query(User).all()
todo_count = db.query(Todo).count()
print(f"剩余用户数：{len(remaining)}, 剩余待办数：{todo_count}")

db.close()
```

📝 **测试 5.1**：删除 test_user 后，待办还剩几条？你是怎么解释这个结果的？
0条 建立数据库是设置了cascade="all, delete-orphan删除用户的时候也会删除他的待办
💡 **破坏性实验 1**：
把 `cascade="all, delete-orphan"` 去掉（或改为空字符串），再试一次删除用户，观察区别。
这样的话就只删除了用户没有删除代办还剩余两条
💡 **破坏性实验 2**：
把外键 `ForeignKey("users.id")` 加上 `ondelete="RESTRICT"`（SQLite 不支持 ON DELETE，改用 Python 逻辑），删除用户时会发生什么？
会报错
❓ **问题 5.1**：如果不想级联删除（删除父记录时子记录保留），应该怎么设置？
把 `cascade="all, delete-orphan"` 去掉
❓ **问题 5.2**：`ondelete="SET NULL"` 有什么用？
删除父记录时把子记录的 FK 字段设为 NULL（软断开关系）。
         例如删除用户后，该用户的待办依然存在但 user_id 变为 NULL，归属不明。
         前提是 user_id 允许为 NULL（nullable=True）。
"""


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 1 - 两数之和（Easy）
#    链接：https://leetcode.cn/problems/two-sum/
#    思路提示：用哈希字典做 O(n) 查找，就像数据库的主键索引一样高效
#
# 2. LeetCode 268 - 缺失的数字（Easy）
#    链接：https://leetcode.cn/problems/missing-number/
#    思路提示：数组索引天然对应数字，类似于数据库的主键自增逻辑
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

测试 1.1：
  User 属性：id, username, email, hashed_password, todos (relationship)
  Todo 属性：id, title, description, category, completed, user_id, owner (relationship)
测试 1.2：orm_test.db 文件里自动创建了 users 表和 todos 两张表。
         用 .schema 可以看到完整的 CREATE TABLE 语句。

问题 1.1：级联删除——删除 User 对象时，他的所有 Todo 也一起被删除。
         "all" 表示所有操作都级联，"delete-orphan" 表示孤儿 Todo（没有父用户的）不允许存在。
问题 1.2：两边都要写。单向声明只能从一方访问另一方：
         只有 User.todos → 可以用 user.todos 拿到待办，但不能用 todo.owner 拿到所属用户。

== 实验 2 参考答案 ==

测试 2.1：1 个用户（zhangsan），2 条待办（学习 SQL、买牛奶）。
测试 2.2：title 变成"复习 SQL"，completed 变成 True。
测试 2.3：剩余 1 条待办（"复习 SQL"）。

破坏性实验：不在！commit 之前修改只在 Session 缓冲区，没写入硬盘。
           这就是为什么有时需要 rollback() 来撤销未提交的修改。

问题 2.1：插入后立即需要知道自增 ID 的时候必须用 refresh()。
         否则新对象的 id 还是 None（因为 INSERT 还没真正执行到数据库）。
问题 2.2：get() 直接用主键查，走缓存更快（类似 dict.get()）；
         filter 是通用查询，慢一些但功能更多（可以组合多个条件）。

== 实验 3 参考答案 ==

测试 Q1：zhangsan 有 4 条待办：学习 Python ❌、学习 SQL ✅、学习 FastAPI ❌、买牛奶 ✅。
测试 Q4：排序后的顺序：
  [学习] 学习SQL (已完成)、[生活] 买牛奶 (已完成)、
  [学习] 学习FastAPI (未完成)、[学习] 学习Python (未完成)、[学习] 背单词 (未完成)、[工作] 写周报 (未完成)
测试 Q5：学习 FastAPI（按 ID 排序的第 3 条）。
测试 Q6：3 条——学习 Python、学习 SQL、学习 FastAPI。

问题 3.1：flush 把数据同步到当前事务的数据库中（能在同一个 session 中被立即查到），
         但不真正提交到磁盘（其他数据库连接看不到）。
         commit 才是真正持久化保存（其他连接也能看到，且不可 rollback）。
问题 3.2：先按 completed 倒序排（True 在前 = 已完成的先出现），
         completed 相同的再按 title 正序排（A-Z）。

== 实验 4 参考答案 ==

测试 4.1：方法1执行 101 条 SQL（1条查users + 100条每个用户的todos）。
         方法2只执行 1 条 SQL（带 JOIN 的一次查询）。
         差距随用户数量线性增长！

问题 4.1：都是 INNER JOIN（LEFT OUTER JOIN）。SQLAlchemy 帮你自动拼接 SQL 字符串，
         你只需要告诉它"我要预加载哪些关系"。
问题 4.2：lazy loading（懒加载）。访问 user.todos 时才去查数据库。
         joinedload 把它改成 eager loading（预加载），一次性取回所有关联数据。

== 实验 5 参考答案 ==

测试 5.1：剩余 0 条待办。因为 cascade="all, delete-orphan" 让删除用户连带删除他的所有待办。

问题 5.1：去掉 cascade 参数，保留默认的 RESTRICT 行为。
         SQLite 实际上不支持 ON DELETE，需要在 Python 层面处理。
问题 5.2：删除父记录时把子记录的 FK 字段设为 NULL（软断开关系）。
         例如删除用户后，该用户的待办依然存在但 user_id 变为 NULL，归属不明。
         前提是 user_id 允许为 NULL（nullable=True）。

== LeetCode 思路 ==

LC 1：用字典记录 {target - num: index}，遍历一次即可找到配对。类似数据库主键索引 O(1) 查找。
LC 268：排序后比较索引和值，或者用集合差集。
         range(len(nums)) 应该包含 0~n，缺的就是缺失的数字。
"""


# ============================================================
# 📝 今日学习记录
# ============================================================
"""
📝 Day 30 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：定义 User + Todo 模型
[ ] 实验 2：Session CRUD
[ ] 实验 3：过滤 + 排序 + 分页
[ ] 实验 4：joinedload 关联查询
[ ] 实验 5：外键约束 + 级联删除

遇到的问题：
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
