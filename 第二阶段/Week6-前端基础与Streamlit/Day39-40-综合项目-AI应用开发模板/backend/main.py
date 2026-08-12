from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, async_engine, Base
from models import PromptCreate, PromptOut, Prompt, ChatRequest
import math
import uvicorn

# main.py FastAPI 应用 + 路由


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
def get_llm_answer(
    text: str,
) -> str:  # 把"回答逻辑"单独抽成一个函数，下周只要换这个函数内部
    # 关键词 → 回答 的映射表
    rules = {
        "你好": "你好！我是你的 AI 助手，有什么可以帮你？",
        "天气": "我现在还是模拟回答，暂时查不了天气。下周接上真 LLM 后就能查了！",
        "python": "Python 是个很适合 AI 开发的语言，你学得很对！",
    }
    # 遍历规则，如果问题里包含某个关键词，就返回对应回答
    for keywords, answer in rules.items():
        if keywords in text:  # 判断 text 里有没有这个关键词
            return answer
    # 兜底：都没命中
    return f"你问的是，【{text}】，我是模拟回答。下周我会换成真正的 LLM！"


@app.post(
    "/api/chat", status_code=201
)  # 此接口只回答不存入数据库 由前端打包 再存入后端
async def get_llm_chat(
    req: ChatRequest,
):
    answer = get_llm_answer(req.text)
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
