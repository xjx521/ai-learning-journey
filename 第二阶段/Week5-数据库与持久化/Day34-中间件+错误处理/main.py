from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import asyncio

from dotenv import load_dotenv
import os

app = FastAPI(title="CORS 实验", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://evil.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello from API server :8000"}


@app.get("/data")
def get_data():
    return {"users": ["Alice", "Bob", "Charlie"]}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)


# ============================================================
# 【实验 2】自定义日志中间件 + 性能监控
# ============================================================
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)
        duration = time.time() - start_time
        print(
            f"[{request.method:6s}] {request.url.path:<20s} "
            f"{response.status_code:3d} | {duration:.3f}s"
        )
        return response


app.add_middleware(LoggingMiddleware)

# 加几个测试路由
fake_todos = [
    {"id": 1, "title": "学习 Python"},
    {"id": 2, "title": "学习 HTTP"},
    {"id": 3, "title": "学习 FastAPI"},
]


@app.get("/todos")
def list_todos():
    return {"success": True, "data": fake_todos}


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = next((t for t in fake_todos if t["id"] == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    return {"success": True, "data": todo}


@app.post("/todos", status_code=201)
def create_todo(title: str):
    new_id = max(t["id"] for t in fake_todos) + 1
    fake_todos.append({"id": new_id, "title": title})
    return {"success": True, "data": fake_todos[-1]}


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if not any(t["id"] == todo_id for t in fake_todos):
        raise HTTPException(status_code=404, detail="待办事项不存在")
    fake_todos[:] = [t for t in fake_todos if t["id"] != todo_id]
    return None


@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(2)  # 模拟慢查询
    return {"message": "两秒后才回来"}


# 步骤 2：在 main.py 中加载并打印：
load_dotenv()
print(f"应用名称：{os.getenv('APP_NAME')}")
print(f"调试模式：{os.getenv('DEBUG')}")
print(f"数据库：{os.getenv('DATABASE_URL')}")
print(f"端口号：{os.getenv('PORT', '8000')}")
print(f"CORS来源：{os.getenv('ALLOWED_ORIGINS')}")

# 类型转换示例
DEBUG_BOOL = os.getenv("DEBUG", "false").lower() == "true"
print(f"DEBUG转为布尔值：{DEBUG_BOOL}")

PORT_INT = int(os.getenv("PORT", "8000"))
print(f"PORT转为整数：{PORT_INT}，类型：{type(PORT_INT)}")

print(f"新增空格值：{os.getenv("SPACES_TEST")}")


# ============================================================
# 【实验 4】统一错误响应格式
# ============================================================
# --- 统一成功响应辅助函数 ---
def success_response(data=None, message="ok"):
    return {"success": True, "data": data, "message": message}


# --- 统一错误响应辅助函数 ---
def error_response(code: int, message: str, path: str = ""):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "path": path,
        },
    }


# --- 异常处理器 1：HTTPException（4xx）---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code=exc.status_code, message=exc.detail, path=str(request.url.path)
        ),
    )


# --- 异常处理器 2：参数验证错误（422）---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"])
        errors.append({"field": field, "message": err["msg"]})
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": 422,
                    "message": "请求数据格式不正确",
                    "details": errors,
                    "path": str(request.url.path),
                },
            },
        )


# --- 异常处理器 3：兜底（500）---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=error_response(
            code=500,
            message="服务器内部错误",
            path=str(request.url.path),
        ),
    )


# --- 测试路由 ---
items = [{"id": 1, "name": "苹果", "price": 5.5}]


@app.get("/items")
def list_items():
    return success_response(data=items)


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="商品不存在")
    return success_response(data=item)


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if not any(i["id"] == item_id for i in items):
        raise HTTPException(status_code=404, detail="商品不存在")
    items[:] = [i for i in items if i["id"] != item_id]
    return None


from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)


@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
    new_id = max(i["id"] for i in items) + 1
    new_item = {"id": new_id, **item.model_dump()}
    items.append(new_item)
    return success_response(data=new_item, message="创建成功")


@app.get("/crash")
def crash():
    x = 1 / 0  # ZeroDivisionError
    return {"result": x}


# 💡 **破坏性实验 2：**
# 在异常处理器中故意制造错误（引用未定义的变量）：
# @app.exception_handler(Exception)
# async def broken_handler(request: Request, exc: Exception):
#     return JSONResponse(status_code=500, content=undefined_variable_here)
