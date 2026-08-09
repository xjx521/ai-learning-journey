from datetime import datetime
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import INTEGER, DateTime, Float, String, func, select
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# 1.创建异步引擎
ASYNC_DATABASE_URL = (
    "mysql+aiomysql://root:123456@localhost:3306/fastapi_first?charset=utf8mb4"
)

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,  # 连接池中保持持久链接数
    max_overflow=20,  # 连接池中允许创建的额外连接数
)


# 2.定义模型类：基类+表对应模型类
# 基类：创建时间、更新时间；书籍表：id、书名、作者、价格、出版社
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), default=func.now, comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now,
        comment="更新时间",
    )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, comment="书籍ID")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(INTEGER, primary_key=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(255), comment="用户名")
    password: Mapped[int] = mapped_column(INTEGER, comment="密码")


# 3.建表：定义函数建表：FastAPI启动时候调用建表函数
async def create_tables():
    # 获取异步引擎：创建事务-建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Base 模型类的元数据创建


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()  # 🔼 服务器启动时先跑这里
    print("服务启动，数据表初始化完成")
    yield  # ← 程序暂停在这里，等待请求进来
    # 🔽 服务器关闭时跑这里
    print("服务器正在关闭，回收资源")
    await async_engine.dispose()  # 销毁连接池


app = FastAPI(lifespan=lifespan)

# 手动写数据库会话依赖函数
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定对话类
    expire_on_commit=False,  # 提交后会话不过期不会重新查询数据库
)


# 依赖项
async def get_db():
    async with AsyncSessionLocal() as session:  # 创建数据库会话seesion
        try:
            yield session  # 把会话交给接口的db 跑完关闭
        except Exception:
            await session.rollback()  # 有异常回滚 保证数据一致
            raise


# 4.查询数据
# 需求：查询功能接口 ->依赖注入：创建依赖项获取数据库会话+Depend注入路由函数
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_db)):
    # 查询
    result = await db.execute(select(Book))  # 查询 ->返回一个ORM对象
    book = result.scalars().all()  # scalars().all()获取所有符合条件的
    # book = result.scalars().first()  # 获取第一条
    # book = await db.get(Book, 1)  # 获取单条数据，不需要select直接（模型类，主键）
    return book


# 需求：路径参数 书籍id
@app.get("/book/get_book/{book_id}")
async def get_book_id(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))  # 条件查询
    book = result.scalar_one_or_none()  # 获取数据返回一个或None
    return book


# 需求：条件 价格大于等于50
@app.get("/book/get_bookprice")
async def get_bookprice(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.price >= 50))
    books = result.scalars().all()
    return books


# 需求：作者以 谢 开头
@app.get("/book/search_book")
async def get_search_book(db: AsyncSession = Depends(get_db)):
    # like()模糊搜索
    # result = await db.execute(select(Book).where(Book.author.like("谢%")))  # 谢%：谢后面零个，一个，多个字符
    # result = await db.execute(select(Book).where(Book.author.like("谢_")))  # 谢_：一个字符
    # &:and |:or ~：非
    # result = await db.execute(select(Book).where((Book.author.like("谢%")) & (Book.price > 100)))  # &:and |:or ~：非
    # 需求：书籍id列表 如果数据库里的id在书籍列表里面，就返回
    id_list = [1, 3, 5, 7, 9]
    # .in_()包含
    result = await db.execute(select(Book).where(Book.id.in_(id_list)))
    book = result.scalars().all()
    return book


@app.get("/book/get_count")
async def get_count(db: AsyncSession = Depends(get_db)):
    # 聚合查询 select(func.方法名(模型类.属性))
    # result = await db.execute(select(func.count(Book.id)))  # count统计有多少行
    # result = await db.execute(select(func.max(Book.price)))  # max最大值 min最小值
    # result = await db.execute(select(func.sum(Book.price)))  # sum求Book.price的和
    result = await db.execute(select(func.avg(Book.price)))  # avg求Book.price的平均值
    num = result.scalar()  # 提取一个数字->标量值
    return num


# 分页查询：select().offset().limit()


@app.get("/book/get_book_page")
async def get_book_page(
    page: int = 1,  # 页码
    page_size: int = 2,  # 一页多少数据
    db: AsyncSession = Depends(get_db),
):
    # (页码-1)*每页数量
    skip = (page - 1) * page_size
    # offset:跳过的记录数 offset=(当前页码-1)*limit；limit返回的记录数（一页多少记录）
    result = await db.execute(select(Book).offset(skip).limit(page_size))
    books = result.scalars().all()
    return books


# 5.新增数据
# 需求：用户输入图书信息(书名、作者、价格、出版社)
# 用户输入-> 参数->请求体参数
class BookBase(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str


@app.post("/book/add_book")
async def add_book(
    book: BookBase,
    db: AsyncSession = Depends(get_db),
    # AsyncSession 类型标注，代表这是SQLAlchemy 异步数据库会话。
    # Depends 作用FastAPI 自带依赖系统：执行接口函数前，自动运行 get_db 函数
):
    # ORM对象->add->commit
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    return book


# 6.更新数据
# 需求：修改图书信息先查再改
# 设计思路：路径参数查图书ID 先查找 ；请求体参数修改：作用是更新数据（书名、作者、价格、出版社）


class BookUpdate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str


@app.put("/book/update_book/{book_id}")
async def update_book(
    book_id: int, bookupdate: BookUpdate, db: AsyncSession = Depends(get_db)
):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="查无此书")

    book.bookname = bookupdate.bookname
    book.author = bookupdate.author
    book.price = bookupdate.price
    book.publisher = bookupdate.publisher

    await db.commit()
    return book


# 7.删除数据
@app.delete("/book/delete_book/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    # 先查再删 提交
    book = await db.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="查无此书")

    await db.delete(book)
    await db.commit()
    return {"msg": "删除图书成功"}


# 查询数据

if __name__ == "__main__":
    uvicorn.run("day30-create:app", port=8080, reload=True)
