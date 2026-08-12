from datetime import datetime
from database import Base
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text

# SQLAlchemy Prompt 模型


class Prompt(Base):  # 一条提问记录
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="提问记录id")
    text: Mapped[str] = mapped_column(String(255), comment="用户提问的内容")
    response: Mapped[str] = mapped_column(Text, comment="回答")


# 创建
class PromptCreate(BaseModel):
    text: str
    response: str = ""  # 可选，默认空字符串


# 返回
class PromptOut(BaseModel):
    id: int
    text: str
    response: str
    created_at: datetime
    updated_at: datetime


# AIchat
class ChatRequest(BaseModel):
    text: str
