from datetime import datetime
from database import Base
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from typing import Dict, List

# SQLAlchemy Prompt 模型


class Prompt(Base):  # 一条提问记录
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="提问记录id")
    text: Mapped[str] = mapped_column(String(255), comment="用户提问的内容")
    response: Mapped[str] = mapped_column(Text, comment="回答")


class ChatMessage(Base):
    __tablename__ = "chatmessages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="消息id")
    session_id: Mapped[str] = mapped_column(
        String(255), index=True, comment="会话id，标记消息属于哪个对话"
    )
    role: Mapped[str] = mapped_column(
        String(255), comment="消息角色：system/user/assistant/tool"
    )
    content: Mapped[str] = mapped_column(Text, comment="消息内容")


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
    session_id: str = "default"
