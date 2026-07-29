from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Boolean, func
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Session,
)
from pydantic import BaseModel
from typing import Optional
import uvicorn

engine = create_engine(
    "sqlite:///./experiment1.db", connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


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
def list_todos(db: Session = Depends(get_db)):  # ← 注意类型注解是 Session
    return db.query(Todo).all()


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/health")
def health_check():  # ← 这个不需要 db
    return {"status": "ok"}


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
    query = db.query(Todo)  # 基础查询
    if keyword:
        query = query.filter(Todo.title.like(f"%{keyword}%"))
    if category:
        query = query.filter(Todo.category == category)  # 按分类过滤
    if completed is not None:
        query = query.filter(Todo.completed == completed)  # 按完成状态过滤
    todos = query.offset(skip).limit(limit).all()
    total = query.count()
    return {"data": todos, "total": total}


# ---------- 分类统计 ----------
@app.get("/todos/stats/categories")
def todo_stats_categories(db: Session = Depends(get_db)):
    """统计每个分类有多少待办"""
    results = db.query(Todo.category, func.count(Todo.id)).group_by(Todo.category).all()
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


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
