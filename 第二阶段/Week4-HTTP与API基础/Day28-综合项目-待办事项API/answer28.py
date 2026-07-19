"""
Day 28 参考实现：待办事项 API（完整版）
====================================

⚠️ 这是参考答案！请先自己尝试再来看。

运行方式：
    pip install fastapi uvicorn
    uvicorn answer28:app --reload
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
import json
import os
import math

# ============================================================
# 数据模型
# ============================================================

class TodoCreate(BaseModel):
    """创建待办事项"""
    title: str = Field(..., min_length=1, max_length=100, description="标题，1-100字符")
    description: Optional[str] = Field(default=None, description="详细描述")
    category: str = Field(default="未分类", description="分类")

class TodoResponse(BaseModel):
    """待办事项响应"""
    id: int
    title: str
    description: Optional[str]
    category: str
    completed: bool
    created_at: str

class TodoUpdate(BaseModel):
    """全量更新"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: str = "未分类"
    completed: bool = False

class TodoPatch(BaseModel):
    """部分更新（所有字段可选）"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    completed: Optional[bool] = None

class PaginationResponse(BaseModel):
    """分页信息"""
    page: int
    size: int
    total: int
    total_pages: int

class TodoListResponse(BaseModel):
    """列表响应"""
    data: list[TodoResponse]
    pagination: PaginationResponse

class StatsResponse(BaseModel):
    """统计响应"""
    total: int
    completed: int
    pending: int
    categories: dict[str, int]


# ============================================================
# 数据持久化
# ============================================================

DATA_FILE = "todos.json"

def load_todos() -> list[dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_todos():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos_db, f, ensure_ascii=False, indent=2)

# 启动时加载
todos_db = load_todos()


# ============================================================
# FastAPI 应用
# ============================================================

app = FastAPI(
    title="待办事项 API",
    description="Day 28 综合项目 — 完整的 CRUD API",
    version="1.0.0"
)


# ============================================================
# 辅助函数
# ============================================================

def find_todo(todo_id: int) -> Optional[dict]:
    """按 ID 查找待办事项"""
    for todo in todos_db:
        if todo["id"] == todo_id:
            return todo
    return None

def generate_id() -> int:
    """生成新的自增 ID"""
    if not todos_db:
        return 1
    return max(t["id"] for t in todos_db) + 1


# ============================================================
# 路由
# ============================================================

@app.get("/", tags=["系统"])
def root():
    """健康检查"""
    return {"message": "待办事项 API 运行中", "version": "1.0.0"}


@app.post("/todos", response_model=TodoResponse, status_code=201, tags=["待办事项"])
def create_todo(todo: TodoCreate):
    """创建新的待办事项"""
    new_todo = {
        "id": generate_id(),
        "title": todo.title,
        "description": todo.description,
        "category": todo.category,
        "completed": False,
        "created_at": date.today().isoformat(),
    }
    todos_db.append(new_todo)
    save_todos()
    return new_todo


@app.get("/todos", response_model=TodoListResponse, tags=["待办事项"])
def list_todos(
    keyword: Optional[str] = Query(default=None, description="搜索关键词（匹配标题和描述）"),
    category: Optional[str] = Query(default=None, description="按分类过滤"),
    completed: Optional[bool] = Query(default=None, description="按完成状态过滤"),
    page: int = Query(default=1, ge=1, description="页码"),
    size: int = Query(default=10, ge=1, le=100, description="每页数量"),
):
    """获取待办事项列表（支持搜索和分页）"""
    # 1. 过滤
    result = todos_db.copy()

    if keyword:
        kw = keyword.lower()
        result = [
            t for t in result
            if kw in t["title"].lower() or (t.get("description") and kw in t["description"].lower())
        ]

    if category:
        result = [t for t in result if t["category"] == category]

    if completed is not None:
        result = [t for t in result if t["completed"] == completed]

    # 2. 分页
    total = len(result)
    start = (page - 1) * size
    end = start + size
    page_data = result[start:end]

    return {
        "data": page_data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        }
    }


@app.get("/todos/stats/summary", response_model=StatsResponse, tags=["统计"])
def get_stats():
    """获取待办事项统计信息"""
    total = len(todos_db)
    completed = sum(1 for t in todos_db if t["completed"])
    pending = total - completed

    categories = {}
    for t in todos_db:
        cat = t.get("category", "未分类")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "categories": categories,
    }


@app.get("/todos/{todo_id}", response_model=TodoResponse, tags=["待办事项"])
def get_todo(todo_id: int):
    """获取单个待办事项详情"""
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoResponse, tags=["待办事项"])
def update_todo(todo_id: int, todo_update: TodoUpdate):
    """全量更新待办事项"""
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")

    todo["title"] = todo_update.title
    todo["description"] = todo_update.description
    todo["category"] = todo_update.category
    todo["completed"] = todo_update.completed

    save_todos()
    return todo


@app.patch("/todos/{todo_id}", response_model=TodoResponse, tags=["待办事项"])
def patch_todo(todo_id: int, updates: TodoPatch):
    """部分更新待办事项（只传需要修改的字段）"""
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")

    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="请至少提供一个要更新的字段")

    todo.update(update_data)
    save_todos()
    return todo


@app.delete("/todos/{todo_id}", status_code=204, tags=["待办事项"])
def delete_todo(todo_id: int):
    """删除待办事项"""
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")

    todos_db.remove(todo)
    save_todos()
    return None
