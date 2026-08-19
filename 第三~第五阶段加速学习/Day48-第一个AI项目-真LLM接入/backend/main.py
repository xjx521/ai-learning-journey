from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, async_engine, Base
from models import PromptCreate, PromptOut, Prompt, ChatRequest, ChatMessage
from dotenv import load_dotenv
from openai import AsyncOpenAI  # 使用官方异步客户端 AsyncOpenAI避免多个请求输入堵塞
from typing import Dict, List
import math
import uvicorn
import os
import re
import time

# main.py FastAPI 应用 + 路由

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


# create_all 只建"尚未存在的表"：ai_app 数据库里已有 Alembic 建的表，这里实际是空操作，
# 只是容器启动时的一个兜底。数据库结构一律以 Alembic 迁移为准。
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AI 应用开发模板", lifespan=lifespan)
# ③ 在 app = FastAPI(...) 之后，挂 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # 允许哪些来源访问后端（从 .env 读）
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许所有HTTP方法（GET/POST/...）
    allow_headers=["*"],  # 允许所有请求头
)


# 1.健康检查 |GET /api/health` 返回服务状态
@app.get("/api/health", status_code=200)
async def check_health():
    return {"status": "ok"}


# 2.提交提问 | `POST /api/prompts` 保存一条提问
@app.post("/api/prompts", response_model=PromptOut, status_code=201)
async def save_prompts(prompt: PromptCreate, db: AsyncSession = Depends(get_db)):
    data = prompt.model_dump()  # Pydantic v2 用model_dump，不要用__dict__
    prompt_obj = Prompt(**data)
    db.add(prompt_obj)
    await db.commit()
    await db.refresh(prompt_obj)
    return prompt_obj


# 3.查询记录 | `GET /api/prompts` 返回所有提问记录
@app.get("/api/prompts", status_code=200)
async def get_prompts_list(
    db: AsyncSession = Depends(get_db),
    prompt_id: int | None = None,
    page: int = 1,
    size: int = 5,
):
    skip = (page - 1) * size  # 跳过的记录数
    # ── ① 列表查询：倒序 ──
    stmt = select(Prompt).order_by(Prompt.created_at.desc())  # 倒序
    # ── ② 计数查询：数总共有几条 ──
    count_stmt = select(func.count(Prompt.id)).select_from(Prompt)
    # ── ③ 如果有 id 过滤，两个查询都要加同样的条件 ──
    if prompt_id:
        stmt = stmt.where(prompt_id == Prompt.id)  # 列表只查这一条
        count_stmt = count_stmt.where(prompt_id == Prompt.id)  # 总数也只数这一条
    # ── ④ 分页：只取这一页的数据 ──
    result = await db.execute(stmt.offset(skip).limit(size))  # 分页
    prompt = result.scalars().all()
    # ── ⑤ 总数：执行计数查询，取那一个数字 ──
    total = (await db.execute(count_stmt)).scalar_one()
    return {
        "data": prompt,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        },
    }


# 4.mock LLM | `POST /api/chat` 接收提问，返回一段模拟回答
###给后端加"多轮记忆"


# 计算总token
async def count_tokens(message: List[dict]) -> float:
    text = "".join(m["content"] for m in message)
    count_chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    count_english = len(re.findall(r"[a-zA-Z]+", text))
    count_symbol = len(re.findall(r"[^a-zA-Z\u4e00-\u9fff\s]", text))

    total_token = count_chinese * 1.5 + count_english * 1.3 + count_symbol * 1
    return round(total_token, 1)


# 管理对话历史
async def manage_history(messages: List[dict], limit: int) -> List[dict]:
    while await count_tokens(messages) > limit:
        if len(messages) <= 5:
            break

        del messages[1:3]

    return messages


# LRU淘汰对话
MAX_SESSIONS = 10  # 同时最多保留几个会话
session_last_active: Dict[str, float] = {}  # session_id -> 最近活跃时间戳


async def remember_activity(session_id: str, db: AsyncSession):
    """登记会话活跃 + 超上限就淘汰最久没活跃的会话"""
    session_last_active[session_id] = (
        time.time()
    )  # TODO 1: 先刷新当前会话的活跃时间（自己变成"最新"） 避免删除自己

    # TODO 2: 如果登记的会话数 > MAX_SESSIONS，淘汰最久没活跃的：
    if len(session_last_active) > MAX_SESSIONS:
        #   a) 找出 session_last_active 里 时间戳最小 的那个 session_id
        oldest_session_id = min(
            session_last_active, key=session_last_active.get
        )  # 返回session_id本身
        #   b) 从数据库删掉它所有的 ChatMessage（select + delete，参考 187 行写法）
        stmt = select(ChatMessage).where(ChatMessage.session_id == oldest_session_id)
        result = (await db.execute(stmt)).scalars().all()  # 一个列表
        for row in result:
            await db.delete(row)  # 一条条删除
        #   c) del session_last_active[那个 session_id]
        del session_last_active[oldest_session_id]


async def get_llm_answer(
    session_id: str, text: str, db: AsyncSession  # 普通函数只写类型，不写 Depends
) -> str:  # 把"回答逻辑"单独抽成一个函数，下周只要换这个函数内部
    """真 LLM 回答。text 是用户输入，返回模型回复。"""
    await remember_activity(session_id=session_id, db=db)
    await db.commit()  # 删完行后立刻 commit 一次，让淘汰先落库
    # 把会话存入列表查询
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id)
    )
    result = await db.execute(stmt)
    message = result.scalars().all()
    history = [{"role": m.role, "content": m.content} for m in message]

    # 不存在system时添加 保证只在首轮添加一次不重复添加system
    if not history or history[0]["role"] != "system":
        system_prompt = (
            "你是一个AI智能问答助手，简短回答，内容不超过20字，不要使用Markdown语法。"
        )
        history.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )
        system_text = ChatMessage(
            session_id=session_id, role="system", content=system_prompt
        )
        db.add(system_text)
    # 添加本轮用户提问
    history.append({"role": "user", "content": text})
    history = await manage_history(history, 1000)  # 检查token超没超上限 超上限当场截断

    response = await client.chat.completions.create(
        model="deepseek-v4-flash", messages=history
    )

    history.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )

    # 5. 持久化 user 和 assistant 两条记录进数据库
    user_text = ChatMessage(session_id=session_id, role="user", content=text)
    ai_text = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=response.choices[0].message.content,
    )
    db.add(user_text)
    db.add(ai_text)
    await db.commit()

    return response.choices[0].message.content or ""


@app.post("/api/chat", status_code=201)  # 此接口回答加存入数据库 由前端打包 再存入后端
async def get_llm_chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    session_id = req.session_id
    text = req.text
    answer = await get_llm_answer(session_id=session_id, text=text, db=db)
    return {"answer": answer}


# `DELETE /api/prompts/{id}` 接口
@app.delete("/api/prompts/{prompt_id}", status_code=204)
async def delete_prompts(prompt_id: int, db: AsyncSession = Depends(get_db)):
    # 先查再删 提交
    prompt = await db.get(Prompt, prompt_id)

    if not prompt:
        raise HTTPException(status_code=404, detail="该提问不存在")

    await db.delete(prompt)
    await db.commit()
    return None


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
