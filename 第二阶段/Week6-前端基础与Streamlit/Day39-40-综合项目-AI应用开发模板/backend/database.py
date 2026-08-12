from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, DateTime
from config import ASYNC_DATABASE_URL

# 引擎 + 会话 + Base

# 异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL, echo=True, pool_size=10, max_overflow=20
)

# 会话
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定对话类
    expire_on_commit=False,  # 提交后会话不过期不会重新查询数据库
)


# 依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()  # 异常回滚
            raise


# Base
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), default=func.now, comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), default=func.now, comment="更新时间"
    )
