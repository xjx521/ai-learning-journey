# 🗄️ 第二阶段学习笔记(三):数据库与 ORM(异步为主)

> 📅 学习周期:2026.07.27 - 2026.07.29 | 对应 Day29-32
> 📌 本笔记以**课堂异步代码 day30-create.py** 为基准(更贴近未来生产开发),同步写法放进对比表格
> 🎯 掌握后应能:用异步 SQLAlchemy 写 CRUD、管理迁移、在 FastAPI 里集成数据库

---

## 目录

- [第 7 章 SQL 基础 + SQLite(Day29)](#第-7-章-sql-基础--sqliteday29)
- [第 8 章 SQLAlchemy ORM 异步实战(Day30)【核心】](#第-8-章-sqlalchemy-orm-异步实战day30核心)
- [第 9 章 Alembic 迁移 + 数据库设计(Day31)](#第-9-章-alembic-迁移--数据库设计day31)
- [第 10 章 FastAPI + SQLAlchemy 集成(Day32)【异步版】](#第-10-章-fastapi--sqlalchemy-集成day32异步版)
- [📕 本册错题本](#-本册错题本)

---

# 第 7 章 SQL 基础 + SQLite(Day29)

## 7.1 关系型数据库概念

### 🔴 数据库 = 有结构的 Excel

> 📌 **知识点说明**:关系型数据库把数据存进**表格**,每张表有行(记录)和列(字段),表之间能通过**主键/外键**关联。最常用的轻量数据库是 **SQLite**(一个文件就是整个库,零配置,适合学习和开发)。

| 数据库术语 | 类比 Excel | 说明 |
|-----------|-----------|------|
| 表 Table | 工作表 | 一类数据的集合 |
| 行 Row / 记录 | 一行 | 一条具体数据 |
| 列 Column / 字段 | 一列 | 一个属性 |
| 主键 Primary Key | 序号 | 唯一标识一行(不能重复、不能空) |
| 外键 Foreign Key | 跨表引用 | 引用别的表的主键,建立关联 |

## 7.2 SQL CRUD 四件套

### 🔴 SELECT / INSERT / UPDATE / DELETE

> 📌 **知识点说明**:SQL 是操作数据库的语言。四个核心动词:**查(SELECT)、增(INSERT)、改(UPDATE)、删(DELETE)**。记住格式套路,写错顺序会语法报错。

**最简可运行示例** — 用 Python 的 sqlite3 模块操作(第一阶段基础 + SQLite 命令行):

```python
import sqlite3

# 连接(没有就自动创建)数据库文件
conn = sqlite3.connect("study.db")
cursor = conn.cursor()

# 1. 建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 主键自增
        title TEXT NOT NULL,                    -- 标题,不能为空
        completed INTEGER DEFAULT 0             -- 是否完成(0/1)
    )
""")

# 2. 插入(用 ? 占位符,防 SQL 注入!值永远不要拼进字符串)
cursor.execute("INSERT INTO todos (title) VALUES (?)", ("学习 FastAPI",))
cursor.execute("INSERT INTO todos (title) VALUES (?)", ("写作业",))

# 3. 查询
cursor.execute("SELECT * FROM todos")
rows = cursor.fetchall()          # 所有行:[(1, '学习 FastAPI', 0), ...]

# 4. 更新
cursor.execute("UPDATE todos SET completed = 1 WHERE id = ?", (1,))

# 5. 删除
cursor.execute("DELETE FROM todos WHERE id = ?", (2,))

# 重要:插入/更新/删除后必须 commit 才真正保存!
conn.commit()
conn.close()
```

⚠️ **易错点**:
```python
# ❌ 把用户输入直接拼进 SQL → SQL 注入漏洞
# title = input("标题:")
# cursor.execute(f"INSERT INTO todos (title) VALUES ('{title}')")  # 危险!

# ✅ 永远用 ? 占位符传参
cursor.execute("INSERT INTO todos (title) VALUES (?)", (title,))
```

## 7.3 WHERE 条件 + 运算符

### 🔴 条件过滤

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `=` | 等于 | `WHERE id = 1` |
| `!=` / `<>` | 不等于 | `WHERE completed != 1` |
| `>` `<` `>=` `<=` | 大小 | `WHERE price >= 50` |
| `AND` / `OR` | 并且/或者 | `WHERE a = 1 AND b = 2` |
| `LIKE` | 模糊匹配 | `WHERE title LIKE '%学习%'` |
| `IN` | 在列表里 | `WHERE id IN (1,3,5)` |
| `IS NULL` | 是空 | `WHERE description IS NULL` |

💡 **LIKE 通配符**:`%` = 任意多个字符(`'%学习%'` 包含"学习"),`_` = 单个字符(`'谢_'` 谢后面跟一个字)。

## 7.4 多表查询 JOIN

### 🟡 INNER JOIN vs LEFT JOIN

> 📌 **知识点说明**:多表查数据用 JOIN。**INNER JOIN = 只返回两边都能匹配上的行;LEFT JOIN = 返回左边表所有行,右边没有的用 NULL 补**。

**对比表(面试必考)**:

| 对比 | INNER JOIN(内连接) | LEFT JOIN(左连接) |
|------|-------------------|-------------------|
| 返回范围 | 两表都有匹配的行 | 左表全部 + 右表匹配(没有则 NULL) |
| 类比 | 两班都来的同学 | 一班全体 + 恰好也认识二班的 |
| 默认 | 不是默认 | 不写 JOIN 类型时 SQLite 默认 INNER |

```sql
-- 用户 + 待办:内连接(只显示有待办的用户)
SELECT users.username, todos.title
FROM users
INNER JOIN todos ON users.id = todos.user_id;

-- 左连接(显示所有用户,没待办的用户 title 是 NULL)
SELECT users.username, todos.title
FROM users
LEFT JOIN todos ON users.id = todos.user_id;
```

⚠️ **易错点**:用户曾把 INNER/LEFT 的解释**写反**。记住口诀:**LEFT 保左**(左边表的记录一条不少)。

## 7.5 聚合函数 + GROUP BY + HAVING

### 🟡 COUNT / SUM / AVG / MAX / MIN

> 📌 **知识点说明**:聚合函数把多行算成一个结果。**COUNT 计数、SUM 求和、AVG 平均、MAX 最大、MIN 最小**。配合 `GROUP BY`(按组统计)和 `HAVING`(对组做过滤,类似 WHERE 但用于分组后)。

```sql
-- 统计:总共有多少条 / 已完成几条
SELECT COUNT(*) FROM todos;
SELECT COUNT(*) FROM todos WHERE completed = 1;

-- 按分类统计每个分类的数量
SELECT category, COUNT(*)
FROM todos
GROUP BY category;

-- 分组后过滤:只显示记录数 > 3 的分类(HAVING,不能用 WHERE)
SELECT category, COUNT(*) as cnt
FROM todos
GROUP BY category
HAVING cnt > 3;
```

💡 **速记**:`WHERE` 过滤**行**(分组前),`HAVING` 过滤**组**(分组后)。

## 7.6 分页:LIMIT / OFFSET

### 🟡 分页公式

> 📌 **知识点说明**:SQL 分页用 `LIMIT`(取几条)+ `OFFSET`(跳过几条)。公式:**OFFSET = (page-1) * page_size**。

```sql
-- 第 2 页,每页 5 条:跳过前 5 条,取 5 条
SELECT * FROM todos LIMIT 5 OFFSET 5;
```

---

## 🎯 第 7 章 面试/开发高频考点

**必问**:
1. 什么是 SQL 注入?怎么防?(? 占位符,永远不要拼接用户输入)
2. INNER JOIN 和 LEFT JOIN 的区别?
3. WHERE 和 HAVING 的区别?(过滤行 vs 过滤组)
4. 分页 SQL 怎么写?(LIMIT OFFSET)

**加分项**:
- LIKE 的 % 和 _ 区别
- 主键和外键的作用

**冷门**:
- `COUNT(*)` vs `COUNT(字段)`(后者忽略 NULL)

---

# 第 8 章 SQLAlchemy ORM 异步实战(Day30)【核心】

> 📌 本章以**课堂代码 day30-create.py** 为基准(异步 + SQLAlchemy 2.0 新写法)。这是**未来开发的主力写法**,一定要吃透。同步写法(笔记/作业里的 `db.query(...)`)放在对比表格里。

## 8.1 什么是 ORM

### 🔴 用 Python 对象操作数据库

> 📌 **知识点说明**:ORM(Object Relational Mapping,对象关系映射)= 把数据库表映射成 Python 类,**用操作对象代替写 SQL**。`User` 类 = users 表,`user.name` = 查/改某行的 name 字段。
>
> 类比:数据库表是"仓库货架",ORM 是"仓库管理员" —— 你说"我要 3 号货架 5 号格子里的东西",管理员帮你取(帮你生成 SQL)。

| 数据库概念 | ORM 概念 | 例子 |
|-----------|---------|------|
| 表 table | Python 类 | `class Book(Base)` |
| 行 row | 类的实例对象 | `book = Book(...)` |
| 列 column | 类的属性 | `book.price` |
| 外键 | ForeignKey + relationship | `user_id = ForeignKey(...)` |

## 8.2 异步三件套:引擎 / 会话工厂 / 会话

### 🔴 异步数据库连接(第一块基石)

> 📌 **知识点说明**:异步 SQLAlchemy 用 `sqlalchemy.ext.asyncio` 下的三个组件。**关键标志:连接串里带 `+异步驱动` 后缀**(MySQL→`+aiomysql`,PostgreSQL→`+asyncpg`,SQLite→`+aiosqlite`),函数是 `create_async_engine`。

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 1. 异步引擎:负责和数据库建立连接池
#    连接串格式: mysql+aiomysql://用户:密码@主机:端口/库名?charset=utf8mb4
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_first?charset=utf8mb4"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,          # 打印生成的 SQL(调试神器,生产关掉)
    pool_size=10,       # 连接池保持的持久连接数
    max_overflow=20,    # 连接池满后还能额外创建的最多连接数
)

# 2. 异步会话工厂:生成"会话"的模板
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,          # 绑定引擎
    class_=AsyncSession,        # 必须显式指定异步会话类
    expire_on_commit=False,     # commit 后对象不过期(异步必配,见易错点)
)

# 3. 异步会话:一次操作数据库的"工作单元"
# 用法见 8.5 的 get_db 依赖
```

| 组件 | 类比 | 同步写法 | 异步写法 |
|------|------|---------|---------|
| 引擎 engine | 通往数据库的连接池 | `create_engine(...)` | `create_async_engine(...)` |
| 会话工厂 | 生成会话的工厂 | `sessionmaker(bind=engine)` | `async_sessionmaker(bind=engine, class_=AsyncSession, ...)` |
| 会话 session | 一次操作的工作单元 | `Session` | `AsyncSession` |

⚠️ **易错点**:
```python
# ❌ 用同步驱动连异步引擎(会报驱动不支持)
# "mysql://root:...@localhost/fastapi_first"   # 少了 +aiomysql

# ✅ 异步连接串三选一
# mysql+pymysql://...        → 同步(不配异步)
# mysql+aiomysql://...       → 异步 MySQL
# sqlite+aiosqlite:///a.db   → 异步 SQLite(本地学习最方便)
```

## 8.3 模型定义:SQLAlchemy 2.0 新写法

### 🔴 Mapped + mapped_column(第二块基石)

> 📌 **知识点说明**:SQLAlchemy 2.0 用类型注解声明字段:`Mapped[Python类型]` 写**Python 类型**,`mapped_column(列类型, ...)` 写**数据库列细节**。基类可以放所有表共用的字段(创建时间/更新时间)。

```python
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import INTEGER, DateTime, Float, String, func

# ---- 基类:所有表都继承,自动带上时间字段 ----
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),   # 数据库层默认值(INSERT 时生效)
        default=func.now,            # ORM 层默认值(Python 创建对象时生效)
        comment="创建时间",           # 注释(自动生成到表结构)
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), default=func.now, comment="更新时间"
    )

# ---- 业务表:Book(书籍)----
class Book(Base):
    __tablename__ = "book"           # 表名(不加就默认类名小写)

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, comment="书籍ID")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")
```

**新写法 vs 旧写法对比表**:

| 对比 | 旧写法(笔记/作业) | 新写法(2.0,day30-create) |
|------|------------------|--------------------------|
| 列定义 | `id = Column(Integer, primary_key=True)` | `id: Mapped[int] = mapped_column(INTEGER, primary_key=True)` |
| 类型位置 | 全在 Column() 里 | Python 类型写 `Mapped[]`,列类型写 `mapped_column()` |
| 基类 | `Base(DeclarativeBase)` | 相同,可在基类放公共字段 |
| 推荐度 | 兼容旧项目 | **新项目默认用** |

## 8.4 建表 + 生命周期(lifespan)

### 🔴 异步建表必须 run_sync + lifespan 管理

> 📌 **知识点说明**:异步引擎**不能直接**执行同步的 `create_all`(会阻塞/报错),必须用 `await conn.run_sync(...)` 把同步建表包装进异步上下文。FastAPI 用 `@asynccontextmanager + lifespan` 管理**启动时建表、关闭时释放连接池**。

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# 异步建表函数:conn 是异步连接,run_sync 执行同步的 create_all
async def create_tables():
    async with async_engine.begin() as conn:        # 开启事务
        await conn.run_sync(Base.metadata.create_all)  # 桥接:把同步建表放进异步

# 生命周期:启动时 / 关闭时各跑一次
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()              # 🔼 服务启动:建表
    print("服务启动,数据表初始化完成")
    yield                              # ← 暂停在这里,等待请求进来
    print("服务器正在关闭,回收资源")
    await async_engine.dispose()       # 🔽 服务关闭:销毁连接池

app = FastAPI(lifespan=lifespan)
```

💡 **速记**:`run_sync` = 异步世界的"翻译官",把同步函数塞进异步上下文执行。

## 8.5 依赖注入 get_db

### 🔴 async 版 get_db(第三块基石)

> 📌 **知识点说明**:`get_db` 是连接"会话"和"路由"的桥梁。**async def + async with + yield** 三步:打开会话 → 交给路由用 → 用完自动关闭;出错 `await rollback()` 回滚保证数据一致。

```python
from fastapi import Depends

async def get_db():
    async with AsyncSessionLocal() as session:   # 创建会话(自动管理关闭)
        try:
            yield session                        # 把会话交给路由的 db 参数
        except Exception:
            await session.rollback()             # 有异常回滚,保证数据一致
            raise

# 路由里这样用:db 就是自动注入好的异步会话
# async def get_book_list(db: AsyncSession = Depends(get_db)):
```

**同步 vs 异步 get_db 对比**:

| 对比 | 同步 | 异步(day30-create) |
|------|------|--------------------|
| 函数定义 | `def get_db()` | `async def get_db()` |
| 打开方式 | `db = SessionLocal()` | `async with AsyncSessionLocal() as session:` |
| 异常处理 | `except: db.rollback()` | `except: await session.rollback()` |
| 收尾 | `finally: db.close()` | `async with` 自动关闭 |

## 8.6 异步 CRUD 全流程(核心!)

### 🔴 查询 / 新增 / 更新 / 删除

> 📌 **知识点说明**:**异步 CRUD 的唯一口诀:凡是数据库 IO 都要 `await`** —— `db.execute` / `db.get` / `db.commit` / `db.refresh` / `db.delete` 全是协程。只有 `db.add()` 不需要 await(只放入内存)。

**① 查询(select 2.0 风格)**:

```python
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

# 查所有
result = await db.execute(select(Book))        # 构造查询语句
books = result.scalars().all()                 # 取所有行(每个是 Book 对象)

# 查单条(按主键,最快)
book = await db.get(Book, 1)                   # 直接拿主键=1 的

# 条件查询(where)
result = await db.execute(select(Book).where(Book.price >= 50))
books = result.scalars().all()

# 模糊查询(like):"谢%" = 以谢开头;"谢_" = 谢+一个字
result = await db.execute(select(Book).where(Book.author.like("谢%")))

# 复合条件:& 是 and,| 是 or,~ 是非(必须加括号)
result = await db.execute(
    select(Book).where((Book.author.like("谢%")) & (Book.price > 100))
)

# IN 查询
result = await db.execute(select(Book).where(Book.id.in_([1, 3, 5])))

# 聚合(avg/max/min/sum/count)
result = await db.execute(select(func.avg(Book.price)))
avg_price = result.scalar()                    # 取单个数字用 scalar()

# 分页(offset 跳过 + limit 取几条)
skip = (page - 1) * page_size
result = await db.execute(select(Book).offset(skip).limit(page_size))
```

**② 新增(add → commit → refresh)**:

```python
# Pydantic 请求体 → ORM 对象 → 入库
class BookBase(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str

@app.post("/book/add_book")
async def add_book(book: BookBase, db: AsyncSession = Depends(get_db)):
    book_obj = Book(**book.__dict__)   # 把 Pydantic 转成字典再展开成 ORM 对象
    db.add(book_obj)                   # 加入会话(不立即写库)
    await db.commit()                  # 提交事务(真正写库)
    await db.refresh(book_obj)         # 刷新对象(拿到数据库生成的 id 等)
    return book_obj
```

**③ 更新(先查再改再 commit)**:

```python
@app.put("/book/update_book/{book_id}")
async def update_book(book_id: int, bookupdate: BookUpdate, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)         # 1. 先查
    if not book:
        raise HTTPException(status_code=404, detail="查无此书")   # 2. 找不到就 404
    book.bookname = bookupdate.bookname        # 3. 改属性
    book.price = bookupdate.price
    await db.commit()                          # 4. 提交
    return book
```

**④ 删除(先查再删再 commit,返回 204)**:

```python
@app.delete("/book/delete_book/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="查无此书")
    await db.delete(book)      # 删除也要 await!
    await db.commit()
    return {"msg": "删除图书成功"}
```

### 🔴 同步 vs 异步完整对比表(背下来)

| 环节 | 同步写法 | 异步写法(day30-create) |
|------|---------|------------------------|
| 导入 | `from sqlalchemy import create_engine` | `from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker` |
| 连接串 | `mysql://...` / `sqlite:///a.db` | `mysql+aiomysql://...` / `sqlite+aiosqlite:///a.db` |
| 引擎 | `create_engine(...)` | `create_async_engine(...)` |
| 会话工厂 | `sessionmaker(bind=engine)` | `async_sessionmaker(bind=..., class_=AsyncSession, expire_on_commit=False)` |
| 建表 | 顶层 `Base.metadata.create_all(bind=engine)` | `await conn.run_sync(Base.metadata.create_all)` |
| 路由函数 | `def` | `async def` |
| 查询 | `db.query(Todo).filter(...).all()` | `await db.execute(select(Book).where(...))` |
| 提交/刷新 | `db.commit()` / `db.refresh()` | `await db.commit()` / `await db.refresh()` |
| 按主键取 | `db.get(Model, id)` | `await db.get(Model, id)` |
| 删除 | `db.delete(obj)` | `await db.delete(obj)` |
| get_db | `def` + try/finally | `async def` + `async with` + `await rollback()` |
| 取结果 | `.scalars().all()` 等 | 相同 |

⚠️ **易错点**:
```python
# ❌ 忘了 await(最常见的异步错误)
# result = db.execute(select(Book))     # 得到一个协程对象,不是结果!

# ❌ expire_on_commit=False 没配 → commit 后访问对象属性报错
# greenlet_spawn has not been called / MissingGreenlet
# ✅ 异步会话工厂必须配 expire_on_commit=False
# async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
```

## 8.7 一对多关系:ForeignKey + relationship

### 🟡 关联两张表(User 有多个 Todo)

> 📌 **知识点说明**:一对多(一个用户多个待办)用 `ForeignKey` 加外键列 + `relationship` 声明关系 + `back_populates` 双向绑定。`cascade="all, delete-orphan"` = 删用户时级联删他的待办。

```python
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    # relationship:通过 back_populates 和 Todo.owner 互相绑定
    # cascade:删用户时一起删他的待办(delete-orphan = 孤儿待办也删)
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))   # 外键指向 users.id
    owner = relationship("User", back_populates="todos")  # 反向关系
```

| 关系 | 代码写法 | 说明 |
|------|---------|------|
| 外键列 | `user_id = Column(ForeignKey("users.id"))` | 数据库层关联 |
| 正向关系 | `owner = relationship("User")` | 从 Todo 访问 User |
| 反向关系 | `todos = relationship("Todo", back_populates="owner")` | 从 User 访问所有 Todo |
| 级联删除 | `cascade="all, delete-orphan"` | 删父删子 |

⚠️ **易错点**:
```python
# ❌ 外键表名写错(必须和 __tablename__ 一致)
# user_id = Column(Integer, ForeignKey("user.id"))   # 表名是 "users" 就写 "users.id"
# ✅ ForeignKey("users.id")
```

## 8.8 N+1 查询问题(了解即可)

### ⚪ N+1 = 查 1 次主表却发了 N 次子表查询

> 📌 **知识点说明**:查询 User 列表(1 次),再逐个访问 `user.todos`(N 次) = 性能灾难。同步用 `joinedload`(一次 JOIN 查出来),**异步下用 `selectinload`**。

```python
from sqlalchemy.orm import selectinload

# 异步:查 User 时把 todos 一起查出来,避免 N+1
result = await db.execute(
    select(User).options(selectinload(User.todos))
)
users = result.scalars().all()   # 访问 user.todos 不再发额外查询
```

🎯 **使用场景**:面试常问"什么是 N+1、怎么解决";开发中列表接口带关联数据时用。

---

## 第 8 章【错误原因 + 修复方案】模块

### ❌ 问题 1:异步 commit 后访问对象属性报 MissingGreenlet

**错误原因**:异步会话默认 `expire_on_commit=True`,commit 后对象属性过期,访问时会触发"懒加载重新查库",但异步下没有事件循环上下文 → 报错。

**修复方案**:异步会话工厂**必须**配 `expire_on_commit=False`:
```python
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,   # 提交后不过期,不会自动重新查库
)
```

### ❌ 问题 2:用 `book.__dict__` 转 Pydantic(课堂遗留)

**错误原因**:`book.__dict__` 是 Pydantic v1 风格,取出的字典可能带内部字段;Pydantic v2 推荐 `model_dump()`。

**修复方案**(Day39-40 生产版已改正):
```python
# ❌ 课堂写法(v1 风格)
# book_obj = Book(**book.__dict__)
# ✅ 生产推荐(v2 写法)
data = book.model_dump()          # Pydantic v2 用 model_dump
book_obj = Book(**data)
```

### ❌ 问题 3:get_db 忘了 await rollback / 用同步 Session

**错误原因**:把同步 `get_db` 直接照搬到异步项目,或异常分支漏了回滚。

**修复方案**:按 8.5 的 async 版 get_db 写(await rollback + raise 重新抛出)。

---

## 🎯 第 8 章 面试/开发高频考点

**必问(本章是最重要的一章)**:
1. 什么是 ORM?好处?(不写 SQL、防注入、跨数据库)
2. 异步三件套是什么?异步连接串和同步有什么区别?(`+aiomysql` 等驱动后缀)
3. `await conn.run_sync(Base.metadata.create_all)` 为什么必须 run_sync?
4. 异步 CRUD 的通用规律?(所有数据库 IO 都要 await)
5. `expire_on_commit=False` 是干嘛的?(异步必配)
6. 一对多怎么建?(ForeignKey + relationship + back_populates)

**加分项**:
- 会 select 2.0 风格的各种查询(where/like/in_/聚合/分页)
- 知道 Mapped/mapped_column 新写法 vs Column 旧写法
- 知道 N+1 问题,异步用 selectinload

**冷门**:
- `&` `|` `~` 是 SQLAlchemy 的 and/or/not(必须加括号)
- `scalar()` vs `scalars().all()` 的区别(单个值 vs 多行)

---

# 第 9 章 Alembic 迁移 + 数据库设计(Day31)

## 9.1 为什么需要迁移

### 🔴 表结构变了,数据不能丢

> 📌 **知识点说明**:直接改表结构(加列/删列/改类型)会丢数据或报错。**迁移(migration)= 把"表结构变化"记录成一步步的脚本**,团队协作/上线时按顺序执行,保证"所有人、所有环境"的表结构一致。
>
> 类比:装修房子前先画好改造图纸(迁移脚本),工头按图纸一步步改,每一步都能回退。

## 9.2 Alembic 完整流程

### 🔴 init → autogenerate → upgrade head

> 📌 **知识点说明**:Alembic 是 SQLAlchemy 官方迁移工具。核心流程三条命令,每次改模型后重复 2-3 步。

```bash
# 1. 初始化(只需要做一次):生成 alembic/ 目录 + alembic.ini
alembic init alembic

# 2. 改完模型后,自动生成迁移脚本(对比模型和数据库差异)
alembic revision --autogenerate -m "add_user_table"

# 3. 执行迁移(把脚本应用到数据库)
alembic upgrade head

# 辅助命令
alembic current      # 当前数据库在哪个版本
alembic history      # 查看迁移历史链
```

**三个核心文件**:

| 文件 | 作用 |
|------|------|
| `alembic.ini` | 全局配置(如数据库地址) |
| `alembic/env.py` | 迁移环境(要配置 `target_metadata = Base.metadata`,否则 autogenerate 不知道你的模型) |
| `alembic/versions/*.py` | 生成的迁移脚本(upgrade 升、downgrade 降) |

⚠️ **易错点**:**env.py 没配置 target_metadata 是 autogenerate 最常见的坑** —— 生成的迁移脚本会显示"空操作",因为 Alembic 看不到你的模型。必须:
```python
# env.py 里
from database import Base        # 导入你的 Base
target_metadata = Base.metadata   # 告诉 Alembic 你的模型元数据
```

## 9.3 回滚

### 🟡 downgrade 回退

| 命令 | 作用 |
|------|------|
| `alembic downgrade -1` | 回退一步(上一个版本) |
| `alembic downgrade base` | 回退到底(全部撤销) |
| `alembic upgrade head` | 升到最新 |

> 📌 **知识点说明**:迁移脚本成"链":**base → 001 → 002 → head**。每次迁移有 `upgrade()`(怎么改)和 `downgrade()`(怎么还原),所以能来回走。

## 9.4 autogenerate 的能力边界

### 🟡 它能干嘛、不能干嘛

| 能力 | 说明 |
|------|------|
| ✅ 自动生成 | 新增表、新增/删除列、修改 nullable、新增索引 |
| ❌ 不能自动 | **改列名**(会被当成删旧列+加新列)、**改列类型**(有时无法判断) |
| ✅ 解决方案 | 手动编辑迁移脚本 `op.alter_column(...)` / `op.rename(...)` |

⚠️ **易错点**:改列名后 autogenerate 可能生成"删掉旧列、加新列"的脚本 → **数据丢失**。遇到改列名,手动在迁移脚本里写 `op.alter_column("users", "old_name", new_column_name="new_name")`。

## 9.5 数据库设计三大范式(了解即可)

### ⚪ 1NF / 2NF / 3NF

> 📌 **知识点说明**:范式是表结构设计规范,目标:**减少数据冗余、避免更新异常**。三个层次,每层解决一类问题。

| 范式 | 要求 | 解决什么 | 例子 |
|------|------|---------|------|
| 1NF | 字段不可再分(原子性) | 避免"一个字段存多个值" | 电话字段不能存 "138,010" |
| 2NF | 消除**部分依赖**(非主键字段完全依赖整个主键) | 复合主键时的冗余 | 主键(学号,课程),成绩依赖两者,但"教师"只依赖课程 → 违反 2NF |
| 3NF | 消除**传递依赖**(非主键字段不依赖其他非主键字段) | 数据更新异常 | 用户表里存 customer_name,它通过 customer_id 依赖主键 → 违反 3NF |

💡 **速记**:1NF 拆字段(原子)、2NF 拆依赖(完全依赖主键)、3NF 拆传递(非主键不能依赖非主键)。**真实项目为了性能常"反范式"(故意冗余,减少 JOIN),面试能说出取舍 = 加分。**

## 9.6 索引(了解即可)

### ⚪ 索引让查询变快

> 📌 **知识点说明**:索引 = 书的目录,让 `WHERE` 条件不用"整本书翻"(全表扫描 SCAN),而是直接翻目录(B+树 SEARCH)。用 `EXPLAIN QUERY PLAN` 看查询走没走索引。

```sql
-- 建索引(常用 WHERE 条件的列)
CREATE INDEX idx_todo_user ON todos (user_id);

-- 看执行计划:SCAN 全表扫描 → SEARCH 走索引
EXPLAIN QUERY PLAN SELECT * FROM todos WHERE user_id = 1;
```

| 概念 | 说明 |
|------|------|
| B+树 | 数据库索引底层数据结构 |
| 最左前缀原则 | 复合索引 `(a, b, c)` 查询 a、a+b、a+b+c 能走索引,a+c 走不了 |
| EXPLAIN QUERY PLAN | SQLite 查看执行计划 |
| 索引代价 | 写数据变慢(要维护索引)、占空间 → 别乱建 |

---

## 🎯 第 9 章 面试/开发高频考点

**必问**:
1. 什么是数据库迁移?为什么不用直接改表?(数据不丢、团队一致、可回滚)
2. Alembic 三步流程?(init → revision --autogenerate → upgrade head)
3. `upgrade head` 和 `downgrade -1` 的区别?
4. env.py 里 target_metadata 是干嘛的?(告诉 Alembic 你的模型)

**加分项**:
- autogenerate 不能自动改列名(会丢数据),需手动 op.alter_column
- 索引加快查询的原理(目录/B+树),最左前缀原则

**冷门**:
- 三大范式各自的"依赖"类型(部分依赖 vs 传递依赖)
- 反范式化取舍(性能 vs 规范)

---

# 第 10 章 FastAPI + SQLAlchemy 集成(Day32)【异步版】

> 📌 本章把 Day32 的同步教学**改写为异步写法**(与 day30-create / Day39-40 生产工程一致),概念完全通用。

## 10.1 依赖注入 Depends 原理

### 🔴 Depends + yield 是灵魂

> 📌 **知识点说明**:FastAPI 的依赖注入 = **在路由执行前,自动运行依赖函数,把结果传进路由**。`Depends(get_db)` 表示"路由要用数据库会话,先去跑 get_db 拿到它"。好处:**会话统一创建/关闭,代码不重复、易测试**。

```
执行流程:
请求进来
  ↓
运行依赖 get_db() → 创建会话 → yield 交给路由
  ↓
路由函数执行(用 db 查数据库)
  ↓
路由返回 → get_db 恢复执行 → async with 自动关闭会话
```

## 10.2 异步 CRUD 四接口(完整集成示例)

### 🔴 一个完整的异步 FastAPI + 数据库应用骨架

> 📌 **知识点说明**:把 8.2-8.6 的知识串起来,就是 Day39-40 项目 backend 的结构。这里是精简版,生产版见第 5 册第 17 章。

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import math, uvicorn

# ===== 数据库连接(生产拆到 database.py)=====
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./app.db"   # 本地学习用 SQLite 异步
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# ===== 模型(生产拆到 models.py)=====
class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, default="未分类")
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

# ===== 生命周期:启动建表 =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app = FastAPI(title="Todo API(异步版)", lifespan=lifespan)

# ===== 依赖 =====
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

# ===== Pydantic 模型 =====
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    category: str = "未分类"

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    completed: bool | None = None

# ===== 路由:CRUD(全部 async def + await)=====
@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    new_todo = Todo(**todo.model_dump())   # Pydantic v2 用 model_dump
    db.add(new_todo)
    await db.commit()                      # 提交
    await db.refresh(new_todo)             # 刷新拿 id
    return new_todo

@app.get("/todos")
async def list_todos(
    keyword: str | None = None,
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    # 1. 构造查询(按创建时间倒序)
    stmt = select(Todo).order_by(Todo.id.desc())
    # 2. 计数查询
    count_stmt = select(func.count(Todo.id)).select_from(Todo)
    # 3. 关键词过滤(两个查询都要加)
    if keyword:
        stmt = stmt.where(Todo.title.contains(keyword))
        count_stmt = count_stmt.where(Todo.title.contains(keyword))
    # 4. 分页执行
    result = await db.execute(stmt.offset((page - 1) * size).limit(size))
    todos = result.scalars().all()
    # 5. 总数
    total = (await db.execute(count_stmt)).scalar_one()
    return {
        "data": todos,
        "pagination": {
            "page": page, "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        },
    }

@app.patch("/todos/{todo_id}")
async def patch_todo(todo_id: int, updates: TodoUpdate, db: AsyncSession = Depends(get_db)):
    todo = await db.get(Todo, todo_id)              # 先查
    if not todo:
        raise HTTPException(status_code=404, detail="待办不存在")
    update_data = updates.model_dump(exclude_unset=True)   # 只取传了的字段
    for key, value in update_data.items():
        setattr(todo, key, value)                   # 逐个赋值(替代 update)
    await db.commit()
    await db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="待办不存在")
    await db.delete(todo)
    await db.commit()
    return None

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

## 10.3 事务:commit / flush / rollback

### 🟡 三个动作的区别(面试易考)

| 动作 | 作用 | 是否写数据库 | 可撤销? |
|------|------|------------|---------|
| `db.add(obj)` | 把对象加入会话(内存) | ❌ 否 | ✅ |
| `db.flush()` | 把 SQL 发到数据库但**没提交** | ⚠️ 暂存,事务内 | ✅ rollback 可撤销 |
| `db.commit()` | **提交事务,真正持久化** | ✅ 是 | ❌ 不可撤销 |
| `db.rollback()` | 撤销本次事务所有未提交操作 | - | - |

> 📌 **知识点说明**:事务(Transaction)= 一组要么全成功、要么全失败的操作(ACID)。`commit` 前可以 `rollback` 撤销;一旦 commit 就定型了。**批量操作用一次 commit 比逐条 commit 快很多(用户实测快约 221 倍)。**

```python
# 批量插入:先 add_all,最后一次性 commit(性能最佳)
db.add_all([Todo(title=f"任务{i}") for i in range(100)])
await db.commit()      # 一次提交,不是 100 次

# 出错自动回滚(get_db 里已经处理,不用手动写)
# except Exception: await session.rollback(); raise
```

## 10.4 分类统计:func.count vs len

### 🟡 数据库聚合 vs 内存统计

| 方式 | 代码 | 适用 |
|------|------|------|
| 数据库聚合 | `select(func.count(Todo.id)).where(...)` | 数据量大,性能好 |
| 内存统计 | `len(result)` / `sum(...)` | 数据量小,直观 |

```python
# 数据库聚合:只返回一个数字,不把数据全拉回内存
total = (await db.execute(
    select(func.count(Todo.id)).where(Todo.completed == True)
)).scalar_one()

# 分组统计:按分类计数
rows = (await db.execute(
    select(Todo.category, func.count(Todo.id)).group_by(Todo.category)
)).all()
# rows 格式:[("学习", 3), ("生活", 2)]
count_by_category = dict(rows)
```

---

## 第 10 章【错误原因 + 修复方案】模块

### ❌ 问题 1:Day32 的 Todo 模型缺 category 字段

**错误原因**:模型只定义了 id/title/description/completed,但搜索过滤路由用了 `Todo.category`,运行时报 `AttributeError: type object 'Todo' has no attribute 'category'`。

**修复方案**:给模型补上字段,或换用已有字段测试:
```python
class Todo(Base):
    ...
    category: Mapped[str] = mapped_column(String, default="未分类")   # ✅ 补字段
```

### ❌ 问题 2:同步代码直接改成 async 忘了 await

**错误原因**:把同步 `db.execute(...)` / `db.commit()` 平移进 async 路由,没加 await → 拿到协程对象、操作不生效。

**修复方案**:所有数据库 IO 加 await(见 8.6 口诀);get_db 用 async 版。

---

## 🎯 第 10 章 面试/开发高频考点

**必问**:
1. FastAPI 依赖注入的原理?(Depends + yield,请求生命周期管理)
2. commit 和 flush 的区别?(提交事务 vs 暂存待提交)
3. 分页查询怎么用 SQLAlchemy 写?(offset + limit + func.count 总数)
4. PATCH 更新在数据库里怎么做?(先查 → model_dump(exclude_unset=True) → setattr → commit)

**加分项**:
- 批量插入用 add_all + 一次 commit(性能优化)
- func.count 数据库聚合 vs len 内存统计的选择

**冷门**:
- `scalar_one()` 和 `scalar_one_or_none()` 的区别(找不到时前者报错、后者返回 None)
- `.scalars()` 必须写在 `db.execute()` 之后,不能拼在 select 链末尾

---

# 📕 本册错题本

| # | 错误代码/场景 | 报错/现象 | 原因 | 修复 |
|---|--------------|----------|------|------|
| 1 | SQL 拼接用户输入 | SQL 注入漏洞 | 值直接拼进字符串 | 用 `?` 占位符 |
| 2 | INNER/LEFT JOIN 解释写反 | 面试答错 | 记反了 | 口诀:LEFT 保左 |
| 3 | 异步连接串少了 `+aiomysql` | 驱动不支持/同步 | 用同步驱动串 | `mysql+aiomysql://...` |
| 4 | 异步忘了 `await db.execute` | 拿到协程对象 | 数据库 IO 没 await | 口诀:凡数据库 IO 都 await |
| 5 | 异步会话没配 `expire_on_commit=False` | MissingGreenlet | commit 后懒加载失败 | 必配 expire_on_commit=False |
| 6 | `book.__dict__` 转 Pydantic | v2 兼容问题 | v1 风格 | 用 `model_dump()` |
| 7 | env.py 没配 target_metadata | autogenerate 空操作 | Alembic 看不到模型 | 导入 Base 并赋值 |
| 8 | 改列名用 autogenerate | 数据丢失 | 被当删旧列加新列 | 手动 op.alter_column |
| 9 | 模型缺 category 字段 | AttributeError | 字段没定义 | 补字段或换字段 |
| 10 | `db.query(...)` 旧写法混入异步 | 风格混乱 | 旧 API | 统一用 `select()` + await |
