from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from collections import Counter
import uvicorn
import math
import json
import os

# ============================================================
# FastAPI 应用
# ============================================================
### Step 1 🔲 搭建基础 + 内存存储
app = FastAPI(title="待办事项API", description="Day 28 综合项目", version="1.0.0")

# ============================================================
# 数据持久化
# ============================================================

### Step 4 🔲 JSON 文件持久化
DATA_FILE = "todos.json"


def load_todos():
    """启动时从文件加载数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_todos():
    """每次修改后保存到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos_db, f, ensure_ascii=False, indent=2)


# 启动时加载
todos_db = load_todos()

# ============================================================
# 辅助函数
# ============================================================


def generate_id():
    """生成新的自增 ID"""
    if not todos_db:
        return 1
    return max([t["id"] for t in todos_db]) + 1


def find_todo(todo_id: int) -> Optional[dict]:
    """按 ID 查找待办事项"""
    for todo in todos_db:
        if todo["id"] == todo_id:
            return todo
    return None


# ============================================================
# 数据模型
# ============================================================


### Step 2 🔲 实现 CRUD 接口
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    category: str = "未分类"


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    category: str
    completed: bool
    created_at: str


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    completed: bool | None = None


# ============================================================
# 路由
# ============================================================


@app.get("/", tags=["系统"], summary="查看运行情况")
def root():
    """健康检查"""
    return {"message": "待办事项API运行中"}


#### 2.1 POST /todos（创建）
@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["待办事项"],
    summary="创建待办事项",
)
def CreateTodos(todoscreate: TodoCreate):
    """创建新的待办事项"""
    new_todo = {
        "id": generate_id(),
        "title": todoscreate.title,
        "description": todoscreate.description,
        "category": todoscreate.category,
        "completed": False,
        "created_at": date.today().isoformat(),  # .isoformat()，把日期时间转成标准 ISO 字符串
    }
    todos_db.append(new_todo)
    save_todos()
    return new_todo


#### 2.2 GET /todos（列表）
@app.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    tags=["待办事项"],
    summary="查看所有待办事项",
)  # 返回列表TodoResponse格式的数组
def GetTodos(
    keyword: str | None = None,  # 搜索标题或描述中包含关键词的
    category: str | None = None,  # 按分类过滤
    completed: bool | None = None,  # 按完成状态过滤
    page: int = 1,  # 页码（从 1 开始）
    size: int = 10,  # 每页10条数据
):
    """获取待办事项列表（支持搜索和分页）"""

    # 1.过滤
    result = todos_db.copy()
    if keyword:
        result = [t for t in result if keyword.lower() in t["title"].lower()]
    if category:
        result = [t for t in result if category.lower() in t["category"].lower()]
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]

    # 2.分页：列表切片
    total = len(result)  # 一共total条数据
    start = (page - 1) * size  # (page - 1)索引从0开始
    end = start + size
    page_data = result[start:end]
    # eg:一页10条数据 取第二页数据：result[10:20]
    # 第二页数据应该从索引10开始 计算方式(2-1)*10=10
    # 结束：10条数据 到索引20结束 计算方式：10+10=20

    return {
        "data": page_data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        },
    }


#### 5.1 GET /todos/stats/summary
@app.get("/todos/stats/summary", tags=["统计"], summary="统计待办事项信息")
def SummaryTodos():
    """获取待办事项统计信息"""
    total = len(todos_db)
    completed = sum(1 for t in todos_db if t["completed"])
    pending = total - completed
    categories = dict(Counter(t["category"] for t in todos_db))
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "categories": categories,
    }


#### 2.3 GET /todos/{todo_id}（详情）
@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    tags=["待办事项"],
    summary="详情",
)
def FindTodos(todo_id: int):
    """获取单个待办事项详情"""
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="待办事项不存在"
        )

    return todo


#### 2.4 PUT /todos/{todo_id}（全量更新）
@app.put(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    tags=["待办事项"],
    summary="全量更新",
)
def UpdateTodos(todo_id: int, todoupdate: TodoUpdate):
    """全量更新待办事项"""
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="待办事项不存在"
        )

    todo["title"] = todoupdate.title
    todo["description"] = todoupdate.description
    todo["category"] = todoupdate.category
    todo["completed"] = todoupdate.completed

    save_todos()
    return todo


#### 3.2 PATCH /todos/{todo_id}（部分更新）
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["待办事项"],
    summary="部分更新",
)
def PatchTodos(todo_id: int, todoupdate: TodoUpdate):
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="待办事项不存在"
        )

    update_data = todoupdate.model_dump(
        exclude_unset=True
    )  # model_dump（）把BaseModel 实例对象转为普通 Python 字典 exclude_unset=True获取实际传的字段
    todo.update(update_data)
    save_todos()
    return todo


#### 2.5 DELETE /todos/{todo_id}（删除）
@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["待办事项"],
    summary="删除",
)
def DeleteTodos(todo_id: int):
    """删除待办事项"""
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="待办事项不存在"
        )

    todos_db.remove(todo)
    save_todos()
    return None


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
