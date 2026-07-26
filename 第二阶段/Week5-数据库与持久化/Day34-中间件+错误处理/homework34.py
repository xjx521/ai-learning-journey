"""
Day 34 练习题：中间件（CORS/日志）、错误处理、环境变量管理
===========================================================

⚠️ 前置准备：
    pip install fastapi uvicorn python-dotenv

💡 建议：所有实验写在 main.py 中逐个测试，完成后访问 http://localhost:8000/docs 查看。
完成每一个「测试」和「问题」后再翻到文件末尾的参考答案。
"""

# ============================================================
# 【实验 1】CORS 中间件
# ============================================================
"""
目标：理解跨域问题及其解决方法

步骤：创建 main.py，添加以下代码：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CORS 实验", version="1.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # 只允许前端地址
    allow_credentials=True,                    # 允许携带 Cookie
    allow_methods=["*"],                       # 所有 HTTP 方法
    allow_headers=["*"],                       # 所有请求头
)

@app.get("/")
def root():
    return {"message": "Hello from API server :8000"}

@app.get("/data")
def get_data():
    return {"users": ["Alice", "Bob", "Charlie"]}
```

📝 **测试 1**：用浏览器或 curl 直接访问 localhost:8000/
      返回了什么？状态码是多少？
答：______________________________________________________________

📝 **测试 2**：从浏览器开发者工具发一个 `fetch("http://localhost:8000/data")`（模拟同域）
      需要 CORS 吗？为什么？
答：______________________________________________________________

📝 **测试 3**：写一个 HTML 文件在 localhost:3000 上调用 fetch("http://localhost:8000/data")
      不配 CORS 时浏览器的报错是什么？
答：______________________________________________________________

      加上 `allow_origins=["http://localhost:3000"]` 后再试，能拿到数据吗？响应头有什么变化？
答：______________________________________________________________

❓ **问题 1.1**：为什么不能同时用 `allow_origins=["*"]` 和 `allow_credentials=True`？

💡 **破坏性实验 1：**
把 `allow_origins=["http://localhost:3000"]` 改成 `allow_origins=["*"]`
然后保留 `allow_credentials=True` 不变，重启服务观察。

💡 **破坏性实验 2：**
把 `allow_origins=["http://localhost:3000"]` 改成 `allow_origins=["http://evil.com"]`
然后用 `http://localhost:3000` 的页面去请求。会发生什么？
思考：CORS 是浏览器给的最终安全保障吗？

❓ **问题 1.2**：生产环境应该用什么方式配置允许的域名？
"""


# ============================================================
# 【实验 2】自定义日志中间件 + 性能监控
# ============================================================
"""
目标：掌握 BaseHTTPMiddleware 自定义中间件的编写

步骤：在 main.py 中添加以下代码：

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        print(f"[{request.method:6s}] {request.url.path:<20s} "
              f"{response.status_code:3d} | {duration:.3f}s")

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
```

发送以下请求并记录控制台输出的日志：

| 请求 | 预期日志格式 | 实际日志 |
|------|-------------|---------|
| GET /todos | `[GET ] /todos              _XX_ _X.XXXs` | _________ |
| POST /todos (title=test) | `[POST] /todos             _XX_ _X.XXXs` | _________ |
| GET /todos/999 | `[GET ] /todos/999        _XX_ _X.XXXs` | _________ |
| DELETE /todos/1 | `[DEL ] /todos/1          _XX_ _X.XXXs` | _________ |
| DELETE /todos/999 | `[DEL ] /todos/999       _XX_ _X.XXXs` | _________ |

💡 **破坏性实验：**
把 `duration:.3f` 改成 `duration:.10f` 看看精度变化。
或者加一个 sleep 让某个接口变慢：
```python
import asyncio

@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(2)  # 模拟慢查询
    return {"message": "两秒后才回来"}
```
然后在日志中观察这个接口的耗时是否真的是 ~2s。

❓ **问题 2.1**：响应是正着经过中间件还是反着经过中间件？为什么 duration 算在 call_next 之后？

❓ **问题 2.2**：如果把 `call_next(request)` 注释掉，会发生什么？
"""


# ============================================================
# 【实验 3】环境变量加载 + 配置文件
# ============================================================
"""
目标：掌握 python-dotenv 的用法和多环境配置

步骤 1：在项目根目录创建 .env 文件：

```bash
# .env — 开发环境配置
APP_NAME=Todo API
APP_VERSION=1.0.0
DEBUG=true
DATABASE_URL=sqlite:///./dev_todos.db
SECRET_KEY=my_local_dev_key_do_not_use_in_prod
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
LOG_LEVEL=debug
```

步骤 2：在 main.py 中加载并打印：

```python
from dotenv import load_dotenv
import os

# 加载 .env（默认加载当前目录下的 .env 文件）
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
```

📝 **测试 3.1**：运行 main.py，观察输出结果是否正确加载了 .env 中的值。
答：______________________________________________________________

📝 **测试 3.2**：把 .env 中的 DEBUG=true 改成 DEBUG=false，再运行。
答：______________________________________________________________

📝 **测试 3.3**：删除 .env 文件（或重命名），再运行。os.getenv 返回什么？
答：______________________________________________________________

📝 **测试 3.4**：在 .env 中加入一行空格值 `SPACES_TEST="hello world"`，读取它。
答：______________________________________________________________

❓ **问题 3.1**：load_dotenv() 为什么要放在代码最前面？

❓ **问题 3.2**：为什么 .env 文件要加到 .gitignore？如果被别人看到了会有什么后果？

💡 **破坏性实验 1：**
在 .env 中设置 DATABASE_URL=sqlite:///../../etc/passwd
观察会不会真的读取这个路径的文件？

💡 **破坏性实验 2：**
把 `load_dotenv()` 的参数改成 `load_dotenv(".env.nonexistent")`（一个不存在的文件）。
程序会报错吗？
"""


# ============================================================
# 【实验 4】统一错误响应格式
# ============================================================
"""
目标：实现全局异常处理器，返回统一的 JSON 错误格式

步骤：在 main.py 中注册异常处理器：

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="错误处理实验", version="1.0")

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
        }
    }

# --- 异常处理器 1：HTTPException（4xx）---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code=exc.status_code,
            message=exc.detail,
            path=str(request.url.path),
        )
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
            }
        }
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
        )
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
```

📝 **测试用例**（按顺序执行）：

| 请求 | 期望的状态码 | 期望的 body | 实际结果 |
|------|------------|------------|---------|
| GET /items | 200 | `{"success":true,"data":[...]}` | _________ |
| GET /items/999 | 404 | `{"success":false,"error":{"code":404,...}}` | _________ |
| DELETE /items/999 | 404 | `{"success":false,"error":{"code":404,...}}` | _________ |
| POST /items `{}` | 422 | `{"success":false,"error":{"code":422,...,"details":[...]}}` | _________ |
| POST /items `{"name":"","price":-1}` | 422 | `{"success":false,"error":{"code":422,...},"details":[{"field":"name","msg":"..."},{"field":"price","msg":"..."}]}` | _________ |
| POST /items `{"name":"香蕉","price":3.5}` | 201 | `{"success":true,"data":{"id":2,"name":"香蕉","price":3.5},...}` | _________ |

❓ **问题 4.1**：三个异常处理器谁的优先级最高？谁兜底？

❓ **问题 4.2**：error_response 里为什么要带上 path 字段？

💡 **破坏性实验 1：**
故意触发一个未被捕获的异常（比如除以零）：
```python
@app.get("/crash")
def crash():
    x = 1 / 0  # ZeroDivisionError
    return {"result": x}
```
收到了什么？符合你预期的统一格式吗？

💡 **破坏性实验 2：**
在异常处理器中故意制造错误（引用未定义的变量）：
```python
@app.exception_handler(Exception)
async def broken_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=undefined_variable_here)
```
会发生什么？FastAPI 是怎么处理的？

思考：这种统一格式对前端团队有什么好处？
答：______________________________________________________________
"""


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 20 - 有效的括号（Easy）
#    链接：https://leetcode.cn/problems/valid-parentheses/
#    思路提示：栈的经典应用——中间件的执行顺序类似括号的嵌套
#    请求进入时从左到右压栈，响应返回时从右到左弹栈
#
# 2. LeetCode 155 - 最小栈（Medium）
#    链接：https://leetcode.cn/problems/min-stack/
#    思路提示：设计一个支持 getMin() 的栈
#    类比：异常处理器栈——最近的（最后注册的）先执行
#
# 💡 中间件的执行顺序类似括号的嵌套：先进后出（Last In First Out）
# ============================================================


# ============================================================
# 💡 参考答案（完成所有练习后再看！）
# ============================================================
# 🔑 使用说明：先独立做完上面所有【测试】和【问题】，再打开这里对照。
# 如果你的答案思路接近就算对，不必文字完全一致。
# ------------------------------------------------------------

"""
== 实验 1 参考答案 ==

测试 1：直接访问 localhost:8000/ 正常返回 JSON，状态码 200。因为这是同源请求，不涉及跨域。
测试 2：同源（协议+域名+端口都一样）不需要 CORS，浏览器不会拦截。
测试 3：
  不配 CORS 时报错："Blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource."
  加上 allow_origins=["http://localhost:3000"] 后能正常拿到数据，响应头多了 Access-Control-Allow-Origin: http://localhost:3000。

问题 1.1：allow_origins=["*"] 表示任何网站都能访问，allow_credentials=True 允许带 Cookie/Token。
      两者结合等于允许全世界冒充用户身份操作，严重安全问题。FastAPI 检测到这个冲突会直接抛 ValueError。
问题 1.2：不应该用 "*" 或写死单个域名。最好从环境变量读取（如 os.getenv("ALLOWED_ORIGINS").split(",")），
      这样开发和生产可以用不同的 .env 文件配置不同域名。

破坏性实验 1：启动就会报错 ValueError! Cannot allow all origins ("*") with credentials.
破坏性实验 2：curl/Wget 等工具不受 CORS 限制！CORS 只是浏览器的保护机制。真正的安全要靠后端接口本身做鉴权验证。


== 实验 2 参考答案 ==

测试结果应类似：
[GET  ] /todos                 200 | 0.00Xs
[POST ] /todos                 201 | 0.00Xs
[GET  ] /todos/999             404 | 0.00Xs
[DEL  ] /todos/1               204 | 0.00Xs
[DEL  ] /todos/999             404 | 0.00Xs
/slow 应该是：[GET  ] /slow                  200 | 2.0XXs

问题 2.1：响应反着经过中间件（像穿脱外套一样）。duration 在 call_next 之后算，
      因为这段时间包含了后续所有中间件 + 路由函数的总耗时。call_next 之前只有计时开始的准备工作。
问题 2.2：不调用 call_next 则请求不会到达路由层，没有响应返回给客户端，连接挂起或超时。
      必须调用 call_next 才能把请求往下传并拿到响应。


== 实验 3 参考答案 ==

测试 3.1：正确加载了所有键值对——应用名称、调试模式、数据库 URL 等都显示了。
测试 3.2：DEBUG_BOOL 变为 False。比较表达式 "false".lower() == "true" 为 False。
测试 3.3：有默认值的键返回默认值（如 PORT 返回 "8000"），无默认值的键返回 None。
测试 3.4：os.getenv("SPACES_TEST") 返回 "hello world"（dotenv 会自动去除引号）。

问题 3.1：必须放在最前面。因为其他模块可能在导入时就读取环境变量（比如 DB 连接字符串），
      如果还没 load_dotenv 就读到的是 None 或默认值。
问题 3.2：防止密钥、密码泄露。SECRET_KEY 泄露 = 攻击者可伪造 JWT Token。
      数据库密码泄露可直接连接数据库删库。所以绝对不要提交 .env 到 Git。

破坏性实验 1：SQLite 会在指定路径创建文件，验证了路径注入风险——生产环境必须校验路径。
破坏性实验 2：不会报错。load_dotenv 找不到文件就静默跳过，依赖默认值兜底。


== 实验 4 参考答案 ==

测试用例应依次通过：
  GET /items → 200, 包含 success:true 和数据数组
  GET /items/999 → 404, 包含统一错误格式（code: 404）
  DELETE /items/999 → 404, 同上
  POST /items {} → 422, 包含 details 数组，列出每个字段的验证失败原因
  POST /items {"name":"","price":-1} → 422, name 的 msg 说至少 1 字符, price 的 msg 说要大于 0
  POST /items {"name":"香蕉","price":3.5} → 201, 新 ID=2 的完整对象

问题 4.1：RequestValidationError 最先匹配（最具体），然后是 HTTPException，
      最后是 Exception 兜底所有未处理的异常。越具体的 handler 优先级越高。
问题 4.2：path 帮助定位具体出错的接口，便于排查和前端提示。
      当多个接口共用同一个错误处理逻辑时，path 能帮助区分是 /items/999 还是 /users/1 报的错。

破坏性实验 1：收到 500 统一格式响应 {"success":false,"error":{"code":500,"message":"服务器内部错误","path":"/crash"}}。
      说明 Exception 兜底确实生效了。
破坏性实验 2：抛出 NameError，但没有被其他 handler 捕获的话，FastAPI 会检测并重试一次，
      最终返回一个简单的 500 页面。说明异常处理器自身也要健壮。

前端好处：只需要写一套错误处理逻辑——检查 res.success === false 就能知道出错了，
      然后通过 error.code/error.message 展示给用户。不用分别处理 404/422/500 等不同框架的错误格式。


== LeetCode 思路 ==

LC 20：用栈模拟括号的嵌套。遇到 '(' '[' '{' 入栈，遇到 ')' '}' ']' 检查栈顶是否配对。
      栈为空时仍有元素 → 多写了；遍历完栈不为空 → 少写了。
      O(n) 时间，O(n) 空间。
LC 155：用一个列表存最小值，每次 push 时同时存当前的最小值。
      getMin() 就是读栈顶的最小值——O(1)。
      类比：异常处理器栈——最近注册的先执行。
"""


# ============================================================
# 学习记录
# ============================================================
"""
📝 Day 34 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：CORS 中间件（含破坏性实验）
[ ] 实验 2：自定义日志中间件（含性能监控）
[ ] 实验 3：环境变量加载与 .env 配置
[ ] 实验 4：统一错误响应格式（含破坏性实验）

遇到的问题：
_____________________________________________
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
