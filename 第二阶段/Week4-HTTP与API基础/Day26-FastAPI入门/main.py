from fastapi import FastAPI, status
from typing import Optional
from enum import Enum
import uvicorn

app = FastAPI(
    title="用户管理系统 API",
    description="Day 26 学习项目，用于练习 FastAPI 基础",
    version="0.1.0",
)


# 【实验 1】Hello World — 你的第一个 API
@app.get("/")
def read_root():
    return {"message": "Hello World!"}


# 【实验 2】路径参数 — 动态 URL
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id, "type": type(user_id).__name__}


# 【实验 3】查询参数 — 过滤和分页
@app.get("/items")
def list_items(page: int = 1, size: int = 10, keyword: Optional[str] = None):
    result = {"page": page, "size": size}
    if keyword:
        result["keyword"] = keyword
    return result


# 【实验 4】路径参数 + 查询参数混合
@app.get("/users/{user_id}/items")
def get_user_items(user_id: int, category: str = "all", limit: int = 10):
    return {"user_id": user_id, "category": category, "limit": limit}


# 【实验 5】枚举参数 — 限制可选值
class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@app.get("/sort/{order}")
def sort_data(order: SortOrder):
    return {"order": order, "message": f"按 {order.value} 排序"}


# 【实验 6】返回状态码
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(name: str):
    return {"name": name, "message": "创建成功"}


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    return None  # 204 不需要返回内容


# 【实验 7】自动文档实战
@app.get("/users", summary="获取用户列表", tags=["用户管理"])
def list_users(page: int = 1, size: int = 10):
    """
    获取分页的用户列表。

    - **page**: 页码，从 1 开始
    - **size**: 每页数量
    """
    return {"page": page, "size": size, "users": []}


@app.post("/users", summary="创建用户", tags=["用户管理"])
def create_user(name: str, email: str):
    """创建新用户并返回用户信息"""
    return {"name": name, "email": email}


@app.get("/health", summary="健康检查", tags=["系统"])
def health_check():
    """检查服务是否正常运行"""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
