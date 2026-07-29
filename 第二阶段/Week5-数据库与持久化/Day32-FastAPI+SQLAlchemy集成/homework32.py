"""
Day 32 练习题：FastAPI + SQLAlchemy 集成 — 依赖注入与数据库会话管理
=====================================================================

⚠️ 前置准备：
    pip install fastapi uvicorn sqlalchemy

💡 建议：所有实验写在 main.py 中，逐个添加测试通过后再继续。
完成每一个「测试」和「问题」后再翻到文件末尾的参考答案。
"""

# ============================================================
# 【实验 1】创建 get_db 依赖（Depends）
# ============================================================
"""
目标：理解 Depends() 如何自动化 Session 管理

步骤：在 main.py 中写以下代码：

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import session,sessionmaker, DeclarativeBase
from pydantic import BaseModel
from typing import Optional

# ---------- 数据库配置 ----------
engine = create_engine(
    "sqlite:///./experiment1.db",
    connect_args={"check_same_thread": False}   # SQLite 特有参数
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# ---------- Todo 模型 ----------
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

# ---------- 依赖函数 ⭐ ----------
def get_db():
    """
依赖注入：自动创建 Session，请求结束后自动关闭
"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Pydantic 模型 ----------
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    class Config:
        from_attributes = True

# ---------- FastAPI 应用 ----------
app = FastAPI(title="Experiment 1")

@app.get("/todos")
def list_todos(db: Session = Depends(get_db)):          # ← 注意类型注解是 Session
    return db.query(Todo).all()

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/health")
def health_check():                                     # ← 这个不需要 db
    return {"status": "ok"}
```

📝 **测试 1.1**：启动服务 `uvicorn main:app --reload`，访问 http://localhost:8000/docs
      观察有什么接口？能正常使用吗？
有get("/todo") post("/todos") get("/heath") 都能正常使用
📝 **测试 1.2**：先 POST 创建一个待办 `{"title": "学习 FastAPI", "description": "Day32"}`
      返回了什么？状态码是多少？
返回了	
Response body
{
  "title": "学习 FastAPI",
  "description": "Day32",
  "completed": false,
  "id": 3
}状态码201
📝 **测试 1.3**：再 GET 查看列表，能看到刚才创建的条目吗？
可以看到
❓ **问题 1.1**：如果没有 yield，只是 return db，然后手动 db.close() 会有什么问题？
那么函数就会直接在return db终止会话无法记录任何东西
❓ **问题 1.2**：为什么 /health 不需要写 `db: Session = Depends(get_db)`？
因为这个函数只是用来检查健康运行状态
"""


# ============================================================
# 【实验 2】Todo CRUD 全部走 SQLAlchemy
# ============================================================
"""
目标：掌握完整的增删改查四个接口

步骤：在 main.py 的上面基础上追加以下代码：

```python
# ---------- PUT 全量更新 ----------
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="待办不存在")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo

# ---------- PATCH 部分更新 ----------
class TodoPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

@app.patch("/todos/{todo_id}")
def patch_todo(todo_id: int, patch: TodoPatch, db: Session = Depends(get_db)):
    db_todo = db.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="待办不存在")
    update_data = patch.model_dump(exclude_unset=True)   # ← 只取客户端真正传的字段
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# ---------- DELETE 删除 ----------
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="待办不存在")
    db.delete(db_todo)
    db.commit()
    # 不返回任何东西，HTTP 状态码 204
```

---
📝 **测试用例**（按顺序执行）：

Step A：POST /todos → `{"title": "买牛奶", "description": "早上的事"}`
预期：______（自己试完后填写）______

Step B：POST /todos → `{"title": "写周报", "description": null}`
预期：______（自己试完后填写）______

Step C：GET /todos
预期：______（自己试完后填写）______

Step D：GET /todos/999
预期：______（自己试完后填写）______

Step E：PUT /todos/1 → `{"title": "买全脂牛奶", "description": "早点去"}`
预期：______（自己试完后填写）______

Step F：PATCH /todos/2 → `{"completed": true}`
预期：______（自己试完后填写）______

Step G：DELETE /todos/2
预期：______（自己试完后填写）______

Step H：GET /todos
预期：______（自己试完后填写）______

---

❓ **问题 2.1**：PUT 和 PATCH 的区别是什么？各适合什么场景？

❓ **问题 2.2**：为什么 DELETE 返回 204 而不是 200？

❓ **问题 2.3**：patch_todo 里的 `exclude_unset=True` 有什么用？
"""


# ============================================================
# 【实验 3】搜索、分页 + 分类统计
# ============================================================
"""
目标：实现查询参数过滤、分页切片、聚合统计

步骤：在 main.py 中添加以下代码：

```python
from sqlalchemy import func

# ---------- 带过滤的列表查询 ----------
@app.get("/todos/search")
def search_todos(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Todo)                   # 基础查询
    if keyword:
        query = query.filter(Todo.title.like(f"%{keyword}%"))   # 模糊搜索
    if category:
        query = query.filter(Todo.category == category)         # 按分类过滤
    if completed is not None:
        query = query.filter(Todo.completed == completed)       # 按完成状态过滤
    todos = query.offset(skip).limit(limit).all()               # 分页
    total = query.count()                                        # 总数
    return {"data": todos, "total": total}

# ---------- 分类统计 ----------
@app.get("/todos/stats/categories")
def todo_stats_categories(db: Session = Depends(get_db)):
    """统计每个分类有多少待办"""
    results = (
        db.query(Todo.category, func.count(Todo.id))
        .group_by(Todo.category)
        .all()
    )
    # results 格式：[('学习', 3), ('生活', 2), ...]
    return {cat: cnt for cat, cnt in results}

# ---------- 完成度统计 ----------
@app.get("/todos/stats/summary")
def todo_stats_summary(db: Session = Depends(get_db)):
    """统计总览"""
    total = db.query(func.count(Todo.id)).scalar()
    done = db.query(func.count(Todo.id)).filter(Todo.completed == True).scalar()
    pending = total - done
    return {"total": total, "done": done, "pending": pending}
```

---
📝 **测试用例**：

Step A：先插入 5 条数据：
  - POST: `{"title": "学习 Python", "category": "学习"}`
  - POST: `{"title": "学习 SQL", "category": "学习"}`
  - POST: `{"title": "买牛奶", "category": "生活"}`
  - POST: `{"title": "写周报", "category": "工作", "completed": true}`
  - POST: `{"title": "健身", "category": "健康"}`

Step B：GET /todos/search?keyword=学习
预期：_{
  "data": [
    {
      "description": "Day32",
      "id": 3,
      "title": "学习 FastAPI",
      "completed": false
    },
    {
      "description": null,
      "id": 4,
      "title": "学习 Python",
      "completed": false
    },
    {
      "description": null,
      "id": 5,
      "title": "学习 Python",
      "completed": false
    },
    {
      "description": null,
      "id": 6,
      "title": "学习 SQL",
      "completed": false
    }
  ],
  "total": 4
}_____

Step C：GET /todos/search?completed=true
预期：_____
  {"data": [],
  "total": 0
}_____

Step D：GET /todos/search?skip=1&limit=2
预期：______{
  "data": [
    {
      "description": "好累",
      "id": 2,
      "title": "111",
      "completed": false
    },
    {
      "description": "Day32",
      "id": 3,
      "title": "学习 FastAPI",
      "completed": false
    }
  ],
  "total": 9
}______

Step E：GET /todos/stats/categories
预期：_____我在别的表试过了 这个作业表 一开始没定义category字段 导致查询不了 返回的按category查询______

Step F：GET /todos/stats/summary
预期：______{
  "total": 9,
  "done": 0,
  "pending": 9
}______

---

❓ **问题 3.1**：search_todos 里为什么要先用 `query = db.query(Todo)` 再链式加 filter？
先查询Todo表 再用filter加条件

❓ **问题 3.2**：`func.count(Todo.id)` 和 `len(todos)` 有什么区别？
一个是统计Todo.id有多少行 一个是统计todo表的长度
❓ **问题 3.3**：offset 和 limit 的顺序能换吗？
不能换固定顺序先告诉跳过多少数据再限制一页多少数据
"""


# ============================================================
# 【实验 4】事务回滚破坏性实验
# ============================================================
"""
目标：理解 commit 和 rollback 的关系，学会处理异常情况

步骤：新建 test_rollback.py（不要混在 main.py 里）：

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("sqlite:///rollback_test.db", echo=True)
Base.metadata.drop_all(bind=engine)            # 清理旧表
Base.metadata.create_all(bind=engine)           # 重新建表
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===== 场景 1：正常 commit =====
print("=" * 50)
print("场景 1：正常提交")
db = SessionLocal()
item = Item(name="苹果")
db.add(item)
db.commit()                                    # ← 成功提交
db.refresh(item)
print(f"添加了：{item.name} (ID={item.id})")
db.close()

# ===== 场景 2：出错后 rollback =====
print("=" * 50)
print("场景 2：异常后回滚")
db = SessionLocal()
item1 = Item(name="香蕉")
db.add(item1)

item2 = Item(name=None)                       # name 不允许为 NULL（模拟错误）
db.add(item2)

try:
    db.commit()                               # ← 这里会报错
except Exception as e:
    print(f"出错了：{e}")
    db.rollback()                              # ← 关键！回滚撤销刚才的操作
    print("已回滚，item1 和 item2 都没保存")

# 验证——看看数据库里有没有刚才的东西
db2 = SessionLocal()
remaining = db2.query(Item).all()
print(f"数据库剩余记录数：{len(remaining)}")
db2.close()

# ===== 场景 3：flush 但不 commit =====
print("=" * 50)
print("场景 3：flush 之后 rollback")
db = SessionLocal()
item3 = Item(name="橘子")
db.add(item3)
db.flush()                                     # ← 写入当前事务但不持久化
can_see = db.query(Item).count()
print(f"flush 后可见记录数：{can_see}")
db.rollback()                                  # ← 撤销
after_rollback = db.query(Item).count()
print(f"rollback 后可见记录数：{after_rollback}")
db.close()
```

运行 `python test_rollback.py`，观察输出并回答：

📝 **测试结果**：

场景 1 后有几条记录？场景 2 rollback 后呢？
答：_________场景1有1条数据_添加了：苹果 (ID=1)_______回滚之后有数据库剩余记录数：3_____________________________________________

实验 2 的关键发现（rollback 到底撤销了什么）：
答：_________________撤销了错误数据_____________________________________________

❓ **问题 4.1**：如果不在 except 里写 rollback，会发生什么？
Session 会一直处于错误状态，后续任何操作都会报错。必须 rollback 才能恢复 Session 的正常使用。
❓ **问题 4.2**：什么时候用 flush，什么时候用 commit？
flush是拿到自增 ID 还没持久化的场景需要 持久化需要提交到数据库用commit
❓ **问题 4.3**：`echo=True` 的作用是什么？调试时有什么用？
echo=True是自动打印程序执行的全部原生的SQL语句到控制台Seesion
"""


# ============================================================
# 【实验 5】批量插入性能对比
# ============================================================
"""
目标：体会批量操作和普通循环的性能差异

步骤：在 main.py 旁边的 perf_test.py 中运行：

```python
import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer, default=0)

engine = create_engine("sqlite:///perf_test.db", echo=False)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===== 方法 1：逐条插入（慢）=====
db1 = SessionLocal()
start = time.perf_counter()
for i in range(1000):
    product = Product(name=f"商品{i}", price=i * 10)
    db1.add(product)                     # 每次 add 只放入缓冲区
    db1.commit()                         # 每次都提交！！！太慢了
elapsed1 = time.perf_counter() - start
print(f"方法1（逐条commit）：{elapsed1:.3f}秒")

# ===== 方法 2：批量加入 + 一次提交（快）=====
db2 = SessionLocal()
start = time.perf_counter()
products = [Product(name=f"商品{i}", price=i * 10) for i in range(1000)]
db2.add_all(products)                    # 一次性加入所有对象
db2.commit()                             # 一次提交搞定
elapsed2 = time.perf_counter() - start
print(f"方法2（add_all + 一次commit）：{elapsed2:.3f}秒")

# ===== 方法 3：flush + 一次 commit（最快）=====
db3 = SessionLocal()
start = time.perf_counter()
products = [Product(name=f"商品{i}", price=i * 10) for i in range(1000)]
db3.add_all(products)
db3.flush()                              # 先 flush 到数据库
db3.commit()                             # 再 commit 持久化
elapsed3 = time.perf_counter() - start
print(f"方法3（add_all + flush + commit）：{elapsed3:.3f}秒")

print(f"\\n最慢的是方法1，快了约 {elapsed1/elapsed2:.1f} 倍")
db1.close()
db2.close()
db3.close()
```

典型输出（不同电脑可能不同）：
  方法1（逐条commit）：0.850秒
  方法2（add_all + 一次commit）：0.012秒
  方法3（add_all + flush + commit）：0.010秒

📝 **测试结果**：

你的电脑上三种方法的耗时分别是多少？最慢的是哪种？
答：_________方法1（逐条commit）：7.310秒
方法2（add_all + 一次commit）：0.033秒
方法3（add_all + flush + commit）：0.030秒
最慢的是方法1，快了约 221.2 倍_____________________________________________________

❓ **问题 5.1**：为什么逐条 commit 这么慢？
因为他是插入一次就提交一次插入1000条就要提交1000次数据
❓ **问题 5.2**：在实际 API 中，如果客户端要批量创建 100 个待办，你会怎么写？
我应该会使用方法3 先创建100个待办然后一次添加所有对象 然后flush到数据库 然后commit持久化 失败时候rollback
❓ **问题 5.3**：add_all 和多次 add 有什么本质区别？
add_all是只提交一次 一次提交所有 add是一条待办就提交一次
"""


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
# 1. LeetCode 26 - 从排序数组中删除重复项（Easy）
#    链接：https://leetcode.cn/problems/remove-duplicates-from-sorted-array/
#    思路提示：双指针原地操作，类似于 SQL UPDATE 的思想
#
# 💡 数据库操作的本质是在已有数据集上做增删改查——LeetCode 的数组操作就是内存中的数据库
# ============================================================


# ============================================================
# 💡 参考答案（完成所有练习后再看！）
# ============================================================
# 🔑 使用说明：先独立做完上面所有【测试】和【问题】，再打开这里对照。
# 如果你的答案思路接近就算对，不必文字完全一致。
# ------------------------------------------------------------

"""
== 实验 1 参考答案 ==

实验 1 验证要点：
1. get_db() 用 yield 而不是 return —— yield 前创建 Session 交给路由用，yield 后 finally 里 close()
2. 路由函数中 `db: Session = Depends(get_db)` 是语法糖——FastAPI 自动调用 get_db()，把 yield 出来的 db 传进来
3. 不需要 db 的路由（如健康检查）可以不加 Depends，保持干净
4. visit http://localhost:8000/docs 可交互式调试 API

问题 1.1：如果路由中间报错了，db.close() 永远不会被执行，连接泄漏。yield + finally 保证无论正常还是异常都会执行清理。
问题 1.2：因为它不操作数据库，不需要 Session。Depends() 按需使用，不用的时候不加。


== 实验 2 参考答案 ==

问题 2.1：PUT 是全量替换——要传完整对象（即使很多字段没变）。PATCH 是部分更新——只传要改的字段（exclude_unset=True 排除没传的）。
      PUT 适合客户端有完整数据的场景；PATCH 适合表单编辑等只需改几个字段的场景。
问题 2.2：RESTful 规范中 DELETE 成功返回 204 且无 body，语义更清晰。
      204 No Content 表示操作成功但没有响应体。
问题 2.3：model_dump(exclude_unset=True) 过滤掉客户端没传的字段，避免把这些字段更新为 None 覆盖原有数据。
      Pydantic 默认所有 Optional 字段都有值（None），不加 exclude_unset 会把没传的字段也更新掉。


== 实验 3 参考答案 ==

问题 3.1：动态构建查询——用一个 Query 对象逐步叠加 filter，最后一次执行 .all()。
      哪个条件有值就加哪个 filter，没有就不加，比写一堆 if-else 分别调不同的查询清爽。
问题 3.2：func.count 是在数据库层面做的 COUNT(*)，只返回一个数字（快）；
      len(todos) 是先查出所有数据到内存再数个数（慢，还浪费带宽）。
      大数据量时性能差距巨大。
问题 3.3：SQLAlchemy 内部会正确排序生成 LIMIT/OFFSET，但推荐 offset().limit() 写法更直观。


== 实验 4 参考答案 ==

测试结果：
场景 1：添加了 1 条记录（苹果），然后 close() 了连接。
场景 2：新开启了一个 Session，插入香蕉和空名 Item。commit 失败 → rollback → 这个 Session 里没有任何数据。
两个场景互相不影响（因为用了不同的 Session，场景 1 已经 commit + close）。

问题 4.1：Session 会一直处于错误状态，后续任何操作都会报错。必须 rollback 才能恢复 Session 的正常使用。
问题 4.2：flush 用于需要拿到自增 ID 但还没准备好持久化的场景（比如插完父记录立刻要拿 ID 插子记录）。
      commit 是真正的持久化操作，一般在业务逻辑完成后统一 commit。
问题 4.3：打印每条执行的 SQL 语句。调试时可以看清楚 SQLAlchemy 实际生成了什么 SQL，方便排查问题。


== 实验 5 参考答案 ==

核心结论：
1. 永远不要在循环里 commit！把所有操作攒到一起，最后一次 commit。
2. 批量插入性能提升通常是几十倍甚至上百倍。
3. 生产环境大批量导入可以用 session.bulk_save_objects() 更快（但失去了一些 ORM 功能）。
4. API 设计：POST /todos/batch 接受数组，服务端做 add_all + 一次 commit。

问题 5.1：每次 commit 都要和数据库进行网络往返（即使是本地也要写磁盘），1000次 = 1000次 I/O 开销。
      改成一次 commit 就把 1000 次 I/O 减少到 1 次。
问题 5.2：接收 List[TodoCreate] 列表，然后用 db.add_all(items)，最后一次 commit。可以在 Service 层做事务包装，失败时整体 rollback。
问题 5.3：从 ORM 角度看效果一样——都是把对象放入 Session 缓冲区。关键区别在于 commit 的次数！
      add_all 后跟一次 commit 就是批量插入的优势所在。
"""


# ============================================================
# 学习记录
# ============================================================
"""
📝 Day 32 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：创建 get_db 依赖（Depends）
[ ] 实验 2：Todo CRUD 全部走 SQLAlchemy
[ ] 实验 3：搜索、分页 + 分类统计
[ ] 实验 4：事务回滚破坏性实验
[ ] 实验 5：批量插入性能对比

遇到的问题：
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
