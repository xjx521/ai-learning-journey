"""
Day 30 练习题：SQLAlchemy ORM 基础 — 模型定义、CRUD、关系映射
===========================================================

⚠️ 前置准备：
    pip install sqlalchemy
    （不需要安装数据库！SQLite 是 Python 内置的）

💡 建议：所有实验写在 main.py 中，逐个添加测试通过后再继续。
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

# ============================================================
# 共享配置（每个实验开头都要写）
# ============================================================
class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///orm_test.db", echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """每次实验创建新的 Session"""
    return SessionLocal()


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

测试 1：检查两个模型是否正确定义了字段
结果：_____user有id/username/email/hashed_password；todo有id/title/description/category/completed/user_id_________

测试 2：运行 Base.metadata.create_all(bind=engine) 后生成了什么？
结果：___orm_test.db 文件里自动创建了 users 表和 todos 表，可以用 sqlite3 orm_test.db → .schema 查看______

问题 1.1：cascade="all, delete-orphan" 的作用是什么？
你的答案：___级联删除——删除 User 时，他的所有 Todo 也一起被删了__________

问题 1.2：back_populates 需要两边都写吗？如果只在一边写会怎样？
你的答案：___两边都要写。单向写只能从一方访问另一方（比如只有 User.todos），但不能从 todo.owner 拿到所属用户_________
"""

# ==================== 参考答案 ====================
# 导入刚才定义的模型后：
# from models import Base, User, Todo
# engine = create_engine("sqlite:///orm_test.db")
# Base.metadata.create_all(bind=engine)
# 成功生成两张表！


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

测试 2.1：插入 1 个用户 + 2 个待办，查询结果对吗？
结果：___用户1人，待办2条_________

测试 2.2：更新 todo1 的标题和 completed 后，再查一次得到什么？
结果：___title变成"复习SQL"且completed为True__________

测试 2.3：删除 todo2 后，剩余的待办数是几？
结果：____1条_________

💡 **破坏性实验：**
把 `db.commit()` 注释掉，然后再查数据库——数据还在吗？
不在！因为 commit 之前修改只在 Session 缓冲区，没写入硬盘。

问题 2.1：db.refresh() 什么时候必须用？
你的答案：___插入后立即需要知道自增 ID 的时候必须用 refresh()，否则新对象的 id 还是 None______

问题 2.2：db.get(Model, id) 和 db.query(Model).filter(Model.id == id).first() 有什么区别？
你的答案：___get 直接用主键查，走缓存更快（O(1)）；filter 是通用查询，慢一些但功能更多______
"""

# ==================== 参考答案 ====================
# CRUD 流程总结：
# 新增：db.add(obj); db.commit()
# 查询：db.query(Model).filter(...).all() / db.get(Model, id)
# 更新：obj.attr = value; db.commit()
# 删除：db.delete(obj); db.commit()
# 2.1：insert 后立刻需要获取 autoincrement 的 id 时，必须调用 refresh()
# 2.2：get() 比 query().filter() 快，因为它直接命中主键索引（类似 dict.get()）


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
    print(f"  ✅ {r.title}")

db.close()
```

测试 Q1：zhangsan 有几条待办？
结果：____4条_______

测试 Q4：排序后的顺序是什么？
结果：___已完成的（学习SQL、买牛奶）排在前面，未完成的学习Python、学习FastAPI、背单词、写周报按标题排序_____

测试 Q5：第1页第3条是什么？
结果：__学习FastAPI（按ID排序的第3条）_______

测试 Q6：LIKE '%学习%' 匹配了几条？
结果：___3条（学习Python、学习SQL、学习FastAPI）__________

问题 3.1：`db.flush()` 和 `db.commit()` 的区别是什么？
你的答案：___flush 把数据同步到当前事务的数据库中（能在同一个session中被查到），但不真正提交到磁盘。commit 才是真正持久化保存_____________________

问题 3.2：order_by(Todo.completed.desc(), Todo.title.asc()) 这个写法是什么意思？
你的答案：___先按 completed 倒序排（True在前），相同completed的再按title正序排（A-Z）______
"""

# ==================== 参考答案 ====================
# flush vs commit：flush 只是在事务内部生效（可以在同一 session 中立即查到刚插入的数据），commit 才持久化到磁盘
# order_by 多个参数 = 多级排序，逗号前是第一排序键，逗号后是并列时的第二排序键


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
# 这里用上面 models 里的 Base 来建表——注意如果 models.py 里的 Base 不同
# 实际使用时请确保用的是同一个 Base

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
# 执行了 1 + N 条 SQL：1条查users + N条查每个用户的todos

# --- 方法2：用 joinedload —— 一条 SQL 搞定 ---
print("\n=== 方法2：joinedload 查询 ===")
users = db.query(User).options(joinedload(User.todos)).all()
for user in users:
    print(f"{user.username}:")
    for todo in user.todos:            # ✅ 已经预加载好了，不再查数据库
        print(f"  - {todo.title}")
# 只执行了 1 条 SQL（带 INNER JOIN），性能大幅优化！

db.close()
```

测试 N+1 方法：如果有 100 个用户，总共执行几条 SQL？
结果：__101条（1条查users + 100条查各自的todos）_________

测试 joinedload 方法：100 个用户执行几条 SQL？
结果：____1条（一条JOIN语句就查完了）___________

问题 4.1：joinedload 生成的 SQL 和原生 JOIN 有什么关系？
你的答案：___都是INNER JOIN，只是SQLAlchemy帮你自动拼接SQL字符串，你不需要手动写JOIN语法______

问题 4.2：relationship 默认是 lazy loading 还是 eager loading？
你的答案：___lazy loading（懒加载）。访问 user.todos 时才去查数据库。joinedload 把它改成 earger loading（预加载）_________
"""

# ==================== 参考答案 ====================
# joinedload 等价于 SQL 中的 SELECT ... LEFT OUTER JOIN ...，一条查询把关联数据全部取回来
# 对于大量数据的场景，性能差距可能是几十倍甚至上百倍


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

测试：删除 test_user 后，待办还剩几条？
结果：____0条，cascade="all, delete-orphan" 让删除用户连带删除他的所有待办_________

💡 **破坏性实验 1：**
把 cascade=""（空字符串）去掉或改为 cascade="all"：
- cascade="all" → 删除用户时 Todo 也被物理删除
- cascade="all, delete-orphan" → 同上，额外禁止孤儿 Todo

💡 **破坏性实验 2：**
把外键 ForeignKey("users.id") 改为没有 ondelete="CASCADE"：
删除用户时报错：FOREIGN KEY constraint failed
因为还有待办引用着这个用户，不允许删除。

问题 5.1：如果不想级联删除，应该怎么设置？
你的答案：___去掉 cascade 或者设为 cascade=""，同时在外键上加 ondelete="RESTRICT"（默认就是RESTRICT）__________

问题 5.2：ondelete="SET NULL" 有什么用？
你的答案：___删除父记录时，子记录的 user_id 自动设为 NULL（前提是 user_id 允许为 NULL）__________
"""

# ==================== 参考答案 ====================
# 5.1：去掉 cascade 参数，保留默认的 RESTRICT 行为
# 5.2：删除父记录时把子记录的 FK 字段设成 NULL（软断开关系）


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
#
# 💡 哈希表的思维在数据库查询中无处不在——索引的本质就是哈希表
# ============================================================


# ============================================================
# 学习记录
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
