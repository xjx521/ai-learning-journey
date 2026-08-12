# ⚡ 第二阶段学习笔记(二):FastAPI 核心

> 📅 学习周期:2026.07.22 - 2026.07.26 | 对应 Day26-28
> 📌 本笔记基于学习笔记 + 课堂代码(Day27/apps)+ 综合项目(Day28)整理
> 🎯 掌握后应能:从零写一个带 CRUD、搜索分页、数据持久化的完整 RESTful API

---

## 目录

- [第 4 章 FastAPI 入门(Day26)](#第-4-章-fastapi-入门day26)
- [第 5 章 FastAPI 进阶(Day27)](#第-5-章-fastapi-进阶day27)
- [第 6 章 综合项目:待办 API(Day28)](#第-6-章-综合项目待办-apiday28)
- [📕 本册错题本](#-本册错题本)

---

# 第 4 章 FastAPI 入门(Day26)

## 4.1 路由:四种方法装饰器

### 🔴 路由 = 一个"地址 → 一个函数"的映射表

> 📌 **知识点说明**:FastAPI 用**装饰器**把"URL 路径 + HTTP 方法"绑定到函数。请求进来时,框架按路径和方法找到对应函数执行,把返回值转成 JSON 返回。`@app.get()` 就是"当有人 GET 这个路径时,调用下面这个函数"。

**最简可运行示例** — 五种方法的路由(Hello World 起步):

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="第一个 API", description="Day 26 学习", version="0.1.0")

@app.get("/")                       # 根路径:浏览器直接访问
def read_root():
    return {"message": "Hello World!"}

@app.get("/items")                  # GET:查询
def list_items():
    return {"items": []}

@app.post("/items")                 # POST:创建
def create_item(name: str):
    return {"name": name, "message": "创建成功"}

@app.put("/items/{item_id}")        # PUT:全量更新
def update_item(item_id: int):
    return {"item_id": item_id}

@app.delete("/items/{item_id}")     # DELETE:删除
def delete_item(item_id: int):
    return None                     # 配合 status_code=204

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)  # reload=True 改代码自动重启
```

💡 **速记**:`uvicorn 文件:app` = 启动哪个文件里的哪个 FastAPI 实例(`app = FastAPI()` 的名字)。

🎯 **使用场景**:一切 API 的开始。启动后访问 `http://localhost:8000/docs` 会看到**自动生成的 Swagger 文档**,可以直接在网页里测试接口 —— 这是 FastAPI 最大的卖点。

⚠️ **易错点**:
```python
# ❌ uvicorn 模块名写错
uvicorn.run("main:app", ...)   # 必须是"文件名:app变量名"
# ✅ 文件叫 main.py 就用 main:app

# ❌ 同路径同方法重复定义两个函数(后面的会覆盖前面)
# @app.post("/users")
# def create1(...): ...
# @app.post("/users")          # ← 与上面冲突,后面的生效
# def create2(...): ...
```

## 4.2 路径参数:动态 URL + 类型验证

### 🔴 用 `{参数}` 捕获 URL 里的值

> 📌 **知识点说明**:`/users/{user_id}` 里的 `{user_id}` 是**路径参数** —— 从 URL 中捕获一段值传给函数。给参数加类型注解 `int`,FastAPI 会自动做**类型转换 + 校验**:传了非数字返回 **422** 错误。

**最简可运行示例**:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):              # 类型注解 int = 自动校验必须是数字
    return {"user_id": user_id, "type": type(user_id).__name__}
```

访问效果:
- `GET /users/5` → `{"user_id": 5, "type": "int"}`(字符串 "5" 被自动转成 int)
- `GET /users/abc` → **422 Unprocessable Entity**(校验失败)

⚠️ **易错点**:
```python
# ❌ 路径参数忘了类型注解,拿到的是字符串
# @app.get("/users/{user_id}")
# def get_user(user_id):        # user_id 是 str,"5" + 1 会报错
#     return user_id + 1

# ✅ 加 int 类型注解,自动转成数字
def get_user(user_id: int):
    return user_id + 1
```

## 4.3 查询参数:过滤、分页、搜索

### 🔴 函数参数没有路径对应 = 查询参数

> 📌 **知识点说明**:函数里**不是路径参数**的参数,自动变成**查询参数**(URL 里 `?key=value`)。带默认值的参数可不传,`Optional[str]` 表示"可空"。

**最简可运行示例** — 列表接口的过滤 + 分页(项目里天天用):

```python
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def list_items(
    page: int = 1,              # 页码,默认第 1 页
    size: int = 10,             # 每页条数,默认 10
    keyword: Optional[str] = None,  # 搜索关键词,可不传
):
    result = {"page": page, "size": size}
    if keyword:
        result["keyword"] = keyword
    return result
```

访问效果:
- `GET /items` → `{"page": 1, "size": 10}`
- `GET /items?page=2&size=5&keyword=python` → 全部生效

⚠️ **易错点**:**bool 类型的查询参数会自动转换**:`?completed=true`(字符串)会被 FastAPI 自动转成 Python 的 `True`。但前端传 `"yes"`/`"1"` 不会被转换,只认 `true`/`false`/`True`/`False`。

## 4.4 枚举参数:限制可选值

### 🟡 Enum 限定只能传固定的几个值

> 📌 **知识点说明**:用 `str, Enum` 定义枚举类,参数用它做类型注解后,**传其他值直接 422**。适合"排序方向 asc/desc"这类固定选项。

**最简可运行示例**:

```python
from enum import Enum
from fastapi import FastAPI

class SortOrder(str, Enum):     # 继承 str,Enum:既是字符串又是枚举
    asc = "asc"                 # 允许的值
    desc = "desc"

app = FastAPI()

@app.get("/sort/{order}")
def sort_data(order: SortOrder):
    return {"order": order, "message": f"按 {order.value} 排序"}
```

访问效果:`GET /sort/asc` ✅;`GET /sort/abc` → 422。

## 4.5 自定义状态码

### 🔴 用 status_code 指定返回码

> 📌 **知识点说明**:默认 GET 返回 200。创建资源用 **201**,删除用 **204**(无响应体)。FastAPI 提供 `status` 常量,写起来不易错。

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/users", status_code=status.HTTP_201_CREATED)   # 创建成功 → 201
def create_user(name: str):
    return {"name": name}

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)  # 删除 → 204
def delete_user(user_id: int):
    return None   # 204 不能有响应体!
```

⚠️ **易错点**:204 时如果 return 了内容,Starlette 会忽略它但可能引发警告。**记住:204 = 什么都不返回。**

## 4.6 路由分发:APIRouter + include_router

### 🟡 把路由拆到多个文件(大型项目必备)

> 📌 **知识点说明**:项目变大后,不能所有路由写在一个文件。用 `APIRouter()` 建子路由,`include_router` 挂到主应用,**prefix 统一加前缀**,tags 给文档分组。这是课堂代码(Day27/apps)的核心结构。

**最简可运行示例** — 分模块组织:

```python
# ===== 文件1:user_router.py =====
from fastapi import APIRouter

user_router = APIRouter(prefix="/users", tags=["用户"])   # prefix 统一前缀

@user_router.get("")            # 实际路径 = /users
def list_users():
    return {"users": []}

# ===== 文件2:main.py =====
from fastapi import FastAPI
from user_router import user_router

app = FastAPI()
app.include_router(user_router)   # 挂载子路由

# 最终接口:GET /users
```

💡 **速记**:`APIRouter` = 一个"路由模块";`include_router` = 装进主应用;`prefix` = 给这个模块的所有路由加统一前缀(如 `/api`)。

## 4.7 原始 socket HTTP 服务器(了解即可)

### ⚪ 不用框架手写 HTTP 服务

> 📌 **知识点说明**:Day26 的 `day26-http.py` 用底层 `socket` 手写了一个迷你 HTTP 服务器,目的是理解"框架到底做了什么"。生产上绝不这么写,但**理解它 = 理解 HTTP 协议和框架的价值**。

```python
import socket

# 创建一个 TCP socket 服务器
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8080))      # 绑定地址和端口
server.listen(5)                      # 最多 5 个排队连接

while True:
    conn, addr = server.accept()      # 等待客户端连接
    request = conn.recv(1024)         # 接收请求数据(字节)
    # 手动拼一个 HTTP 响应:状态行 + 响应头 + 空行 + 响应体
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/html\r\n"
        b"\r\n"
        b"<h1>Hello, World!</h1>"
    )
    conn.send(response)               # 发回给浏览器
    conn.close()                      # 关闭连接
```

🎯 **使用场景**:纯概念理解 —— 面试问"HTTP 协议底层怎么工作"时能讲出"接收字节 → 解析请求 → 拼响应 → 发送"这条链路。

---

## 第 4 章【错误原因 + 修复方案】模块

### ❌ 问题 1:main.py 里 POST /users 路由重复

**错误原因**:实验 6 和实验 7 都定义了 `POST /users`,但参数不同(FastAPI 按"函数签名"自动识别 `name` 和 `name+email` 两种请求体)。两个同名路由并存,顺序靠后、参数更全的定义覆盖了前面的,导致 /docs 里出现混乱。

**修复方案**:给重复路由**合并或改名**,确保每个"路径+方法"组合只有一条:
```python
# ✅ 只保留一个 POST /users,参数齐全
@app.post("/users", summary="创建用户", tags=["用户管理"])
def create_user(name: str, email: str):
    return {"name": name, "email": email}
```

### ❌ 问题 2:破坏性实验后 user_id 类型没改回 int

**错误原因**:验证"路径参数如果是字符串会怎样"后,忘记把 `user_id` 的类型注解从 `str` 改回 `int`,导致后续查询用字符串拼接出错。

**修复方案**:养成习惯 —— **破坏性实验做完立刻还原**,并在笔记里用 `# ✅ 已修复` 标注。

---

## 🎯 第 4 章 面试/开发高频考点

**必问**:
1. 路径参数和查询参数的区别?(URL 路径中的值 vs `?key=value`)
2. 422 错误什么时候出现?(类型校验失败:路径参数非数字、枚举值非法、请求体字段不合法)
3. FastAPI 自动文档在哪?有什么好处?(/docs,Swagger UI,可直接测试接口)
4. uvicorn 启动命令各部分的含义?(`uvicorn main:app --reload`)

**加分项**:
- 会讲 APIRouter + include_router 的分模块结构
- 知道 `Optional[str]` vs `str | None` 等价(都用 None 表示"可空")

**冷门**:
- 枚举参数为什么继承 `str, Enum`(为了既能当字符串又能当枚举校验)
- `--reload` 只应在开发用(生产关闭)

---

# 第 5 章 FastAPI 进阶(Day27)

> 本章含课堂代码(Day27/apps 里的 app03-app07),是普通笔记之外补充的内容。

## 5.1 请求体:Pydantic BaseModel

### 🔴 用 Pydantic 模型接收 Body

> 📌 **知识点说明**:POST/PUT 的复杂数据放**请求体(Body)**。用 `class Xxx(BaseModel)` 定义数据结构,函数参数里写 `xxx: Xxx`,FastAPI 会自动**解析 JSON → Pydantic 对象 → 校验**。`str | None = None` 表示可选字段。

**最简可运行示例**:

```python
from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name: str                      # 必填
    age: int = 0                   # 可选(有默认值)
    email: str | None = None       # 可空(可传可不传)

app = FastAPI()

@app.post("/users")
def create_user(user: User):       # user 自动是解析好的 User 对象
    print(user.name, user.age)     # 用 .字段 访问
    return user
```

🎯 **使用场景**:一切需要接收结构化数据的接口 —— 注册、创建待办、提交提问。**Pydantic 模型 = 后端的数据"说明书",同时负责校验和文档。**

⚠️ **易错点**:
```python
# ❌ 请求体字段名和模型对不上 → 422
# {"Name": "xiao", "Age": 20}  ← 大小写不对,校验失败
# ✅ 必须完全一致:{"name": "xiao", "age": 20}

# ❌ 用 .dict()(Pydantic v1 写法)
# user.dict()
# ✅ Pydantic v2 用 .model_dump()
data = user.model_dump()
```

## 5.2 Field 字段验证规则

### 🔴 Field 给字段加约束(gt/ge/le/min_length…)

> 📌 **知识点说明**:`Field(...)` 给字段加验证规则。`...` 表示必填;`gt` = **g**reater **t**han(大于);`ge` = greater or equal(大于等于);`lt` = less than;`le` = less or equal;`min_length` 限制最小长度。违反规则 → **422**。

**最简可运行示例**:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)   # 必填,2-50 字符
    age: int = Field(default=0, gt=0, lt=100)             # 0 < age < 100
    score: float = Field(default=0, ge=0, le=100)         # 0 ≤ score ≤ 100

app = FastAPI()

@app.post("/users")
def create_user(user: User):
    return user
```

访问效果:`POST /users` body 里 `age: 0` → 422(`gt=0` 要求严格大于 0);`age: 150` → 422。

💡 **速记**:`gt` = "**大**于"(g + t,greater than);`ge` = "**大于等于**"。**用户曾把 gt/ge 含义写反过,面试题易错点!**

⚠️ **易错点**:
```python
# ❌ gt=0 的字段给了默认值 0,破坏性实验后没改回
# class User(BaseModel):
#     age: int = Field(default=0, gt=0)   # default=0 不满足 gt=0,一传空就 422
# ✅ 必填就用 Field(...),或者把默认值改成合法值
```

## 5.3 响应模型 response_model

### 🔴 用 response_model 过滤返回字段

> 📌 **知识点说明**:`response_model=xxx` 规定**这个接口返回什么结构**。最常用场景:**返回时把敏感字段(如 password)过滤掉**。数据格式不对会自动校验转换。

**最简可运行示例**:

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):        # 前端提交:含密码
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):       # 返回给前端:不含密码!
    username: str
    email: EmailStr

app = FastAPI()

@app.post("/register", response_model=UserOut)   # 响应被裁剪成 UserOut 结构
def register(user: UserIn):
    # 真实项目:这里把密码哈希后存数据库,再返回不包含密码的对象
    return user                 # 即使 user 里有 password,响应也会过滤掉
```

⚠️ **易错点**:
```python
# ❌ 响应的字段类型和 response_model 不匹配 → 500 错误
# 比如 response_model 要求 int,返回了字符串
# ✅ response_model 字段类型必须能转换成功
```

### 🟡 response_model 的三个过滤参数(课堂代码 app07)

> 📌 **知识点说明**:除了定义模型,还可以用参数控制"哪些字段返回、哪些省略"。课堂代码 `app07.py` 演示了四种玩法。

| 参数 | 作用 | 示例 |
|------|------|------|
| `response_model_exclude_unset=True` | 没被设置的字段不返回(默认值省略) | 适合"只返回用户传过的" |
| `response_model_exclude_none=True` | 值是 None 的字段不返回 | 精简响应 |
| `response_model_include={"name","price"}` | 只返回指定字段 | 白名单 |
| `response_model_exclude={...}` | 排除指定字段 | 黑名单 |

```python
# 课堂代码示例:只返回 name 和 price
@app.post("/items/{items_id}", response_model=Item, response_model_include={"name", "price"})
def get_item(items_id: str):
    return items[items_id]
```

## 5.4 嵌套模型

### 🟡 模型里套模型(组合)

> 📌 **知识点说明**:Pydantic 模型可以作为另一个模型的字段类型(类型嵌套),也可以组合成列表(组合嵌套)。这对应数据库的一对一/一对多关系。课堂代码 `app03.py` 的 `User` 里嵌了 `Addr`。

**最简可运行示例**:

```python
from pydantic import BaseModel

class Addr(BaseModel):          # 地址模型
    province: str
    city: str

class User(BaseModel):
    name: str
    addr: Addr                  # 类型嵌套:一个用户有一个地址(一对一)
    friends: list[int] = []     # 列表字段

class Data(BaseModel):
    data: list[User]            # 组合嵌套:一个 Data 里有多个 User(一对多)

# 前端提交示例:
# {"name": "小明", "addr": {"province": "广东", "city": "深圳"}, "friends": [1, 2]}
```

🎯 **使用场景**:订单含商品列表、用户含地址、文章含评论 —— 都是嵌套模型。**写多表关联 API 时用它定义请求/响应结构。**

## 5.5 错误处理:HTTPException

### 🔴 主动抛出 HTTP 错误

> 📌 **知识点说明**:`raise HTTPException(status_code=..., detail="提示信息")` 让接口返回指定的错误状态码和消息。**这是"找不到资源返回 404"的标准写法**,配合前端判断成功/失败。

**最简可运行示例**:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_db = {1: {"id": 1, "title": "学习 FastAPI"}}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = fake_db.get(todo_id)
    if not todo:                                    # 查不到
        raise HTTPException(                        # 立刻中断,返回错误
            status_code=404,
            detail="待办事项不存在",
        )
    return todo
```

⚠️ **易错点**:
```python
# ❌ 返回 None 代替抛异常(前端拿到 null,不知道是对是错)
# if not todo:
#     return None

# ✅ 主动抛 HTTPException,前端能拿到 404 + 错误消息
# raise HTTPException(status_code=404, detail="待办事项不存在")
```

## 5.6 混合参数 + exclude_unset=True(PATCH 思想)

### 🟡 路径参数 + 查询参数 + 请求体混用

> 📌 **知识点说明**:一个接口可以同时用三种参数。`exclude_unset=True` 是 PATCH 部分更新的核心:`.model_dump(exclude_unset=True)` **只取前端实际传了的字段**,没传的不更新。这是 Day28/35 项目的核心机制。

**最简可运行示例**:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

app = FastAPI()
fake_db = {1: {"id": 1, "title": "旧标题", "completed": False}}

@app.patch("/todos/{todo_id}")          # 路径参数 todo_id
def patch_todo(
    todo_id: int,                       # 路径参数
    updates: TodoUpdate,                # 请求体
):
    todo = fake_db[todo_id]
    update_data = updates.model_dump(exclude_unset=True)   # 只取传了的字段
    todo.update(update_data)            # 只更新这些字段
    return todo
```

访问效果:传 `{"completed": true}` → 只改 completed,**title 保持"旧标题"不动**。

⚠️ **易错点**:
```python
# ❌ 不用 exclude_unset=True,传了空模型会把字段覆盖成 None
# update_data = updates.model_dump()          # 没传的字段也是 None!
# todo.update(update_data)                    # title 被覆盖成 None!
# ✅ 用 exclude_unset=True,只有真正传了的字段才在 dict 里
```

## 5.7 课堂补充:Form 表单 / 文件上传 / Request 对象

### 🟡 Form 表单数据(app04)

> 📌 **知识点说明**:`Form()` 让接口接收**表单格式**(不是 JSON)的字段,常用于登录表单。前端用 `data=` 提交表单而不是 `json=`。

```python
from fastapi import APIRouter, Form

app = APIRouter()

@app.post("/register")
async def reg(
    username: str = Form(),    # 从表单里取 username
    password: str = Form(),    # 从表单里取 password
):
    print(f"username={username}, password={password}")
    return {"username": username}
```

### 🟡 文件上传(app05)

> 📌 **知识点说明**:文件用 `UploadFile` 接收(比 `bytes` 更适合大文件,支持流式读取)。`bytes = File()` 适合小文件,直接把内容读进内存。

```python
from fastapi import APIRouter, File, UploadFile
import os

app = APIRouter()

@app.post("/upload")
async def upload(file: UploadFile):        # UploadFile = 带文件名的文件对象
    # 保存到本地 imgs 目录
    path = os.path.join("imgs", file.filename)   # 拼接保存路径
    with open(path, "wb") as f:
        for line in file.file:                  # 一行行读,避免大文件爆内存
            f.write(line)
    return {"file": file.filename}

# 小文件版:直接拿字节
@app.post("/small")
async def small(file: bytes = File()):
    return {"size": len(file)}
```

### 🟡 Request 对象(app06)

> 📌 **知识点说明**:把函数参数声明为 `request: Request`,可以拿到这次请求的所有"原始信息" —— URL、客户端 IP、请求头、Cookie。用于日志、限流、统计。

```python
from fastapi import APIRouter, Request

app = APIRouter()

@app.post("/items")
async def items(request: Request):
    return {
        "URL": str(request.url),                    # 请求的完整 URL
        "IP地址": request.client.host,              # 客户端 IP
        "user-agent": request.headers.get("user-agent"),  # 请求头
        "cookies": request.cookies,                 # Cookie
    }
```

### 🟡 field_validator 自定义验证(app03)

> 📌 **知识点说明**:内置验证不够时,用 `@field_validator("字段名")` 写自定义校验函数。函数里用 `assert` 或抛异常拦截非法值。

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str

    @field_validator("name")                # 校验 name 字段
    @classmethod
    def name_must_alpha(cls, value):
        assert value.isalpha(), "name must be alpha"   # 必须是纯英文字母
        return value                        # 校验通过,返回(可改)值
```

---

## 第 5 章【错误原因 + 修复方案】模块

### ❌ 问题 1:homework27 里 gt/ge 含义写反

**错误原因**:记反了 `gt`(greater than = **大于**)和 `ge`(greater or equal = **大于等于**),导致验证规则描述错误。

**修复方案**:
```python
# gt = greater than  = 大于      → Field(gt=0) 要求 > 0
# ge = greater or equal = 大于等于 → Field(ge=0) 要求 >= 0
# lt = less than    = 小于
# le = less or equal = 小于等于
```

### ❌ 问题 2:Pydantic 版本差异导致 .dict() 报错

**错误原因**:Pydantic v2 移除了 `BaseModel.dict()`,课堂代码 app03 里还留着 v1 的 `user.dict()` 注释。

**修复方案**:
```python
# ❌ Pydantic v1
# data = user.dict()
# ✅ Pydantic v2(现代版本都用这个)
data = user.model_dump()
```

---

## 🎯 第 5 章 面试/开发高频考点

**必问**:
1. 请求体用 Pydantic 模型的好处?(校验 + 文档 + 类型转换)
2. `Field(gt=0)` 和 `Field(ge=0)` 的区别?
3. response_model 有什么用?(过滤敏感字段、规定响应结构)
4. `exclude_unset=True` 是干嘛的?(PATCH 只更新传了的字段,是部分更新的核心)
5. HTTPException 怎么用?为什么返回 404 而不是 200?

**加分项**:
- 会嵌套模型(用户含地址)、列表字段
- 知道 Form、UploadFile、Request 三个特殊参数
- 会 field_validator 自定义校验

**冷门**:
- `response_model_exclude_unset` / `exclude_none` / `include` / `exclude` 四个过滤参数
- Pydantic v1 的 `.dict()` vs v2 的 `.model_dump()`

---

# 第 6 章 综合项目:待办 API(Day28)

## 6.1 项目架构:五步走

### 🔴 一个完整 API 项目的成长路径

> 📌 **知识点说明**:Day28 用"闯关模式"把待办 API 从零搭到完整,五步是每个 API 项目的通用成长路径:**内存 → CRUD → 搜索分页+PATCH → JSON 持久化 → 统计**。

| Step | 做了什么 | 对应知识点 |
|------|---------|-----------|
| 1 | FastAPI 初始化 + 内存列表 `todos_db = []` | 基础骨架 |
| 2 | CRUD 五接口(POST 201 / GET / GET{id} / PUT / DELETE 204) | 请求体 + 路径参数 + 状态码 |
| 3 | 搜索(过滤)+ 分页 + PATCH 部分更新 | 查询参数 + exclude_unset |
| 4 | JSON 文件持久化(load_todos / save_todos) | 文件读写 |
| 5 | 统计接口 + 完善文档(summary/tags) | 聚合统计 |

## 6.2 Pydantic 模型设计:三层结构

### 🔴 Create / Response / Update 三个模型

> 📌 **知识点说明**:同一个资源往往需要**三个 Pydantic 模型**:`Create`(创建时接收)、`Response`(返回给前端)、`Update`(更新时接收,全字段可选)。这是项目里的标准做法。

```python
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):              # 创建:只收用户要填的
    title: str = Field(..., min_length=1, max_length=100)  # 必填 + 长度限制
    description: str | None = None
    category: str = "未分类"               # 默认值

class TodoResponse(BaseModel):            # 返回:给前端看全部信息
    id: int
    title: str
    description: str | None
    category: str
    completed: bool
    created_at: str

class TodoUpdate(BaseModel):              # 更新:所有字段都可选(部分更新)
    title: str | None = None
    description: str | None = None
    category: str | None = None
    completed: bool | None = None
```

## 6.3 搜索 + 分页实现

### 🔴 过滤 → 统计 → 切片

> 📌 **知识点说明**:列表接口的搜索分页三步走:**①先过滤(条件筛选)②算 total ③用切片 `result[start:end]` 取当前页**。分页公式 `start = (page - 1) * size`(因为 page 从 1 开始,索引从 0 开始)。

```python
import math

@app.get("/todos")
def list_todos(
    keyword: str | None = None,        # 搜索关键词
    category: str | None = None,       # 按分类过滤
    completed: bool | None = None,     # 按完成状态过滤
    page: int = 1,                     # 页码(从 1 开始)
    size: int = 10,                    # 每页条数
):
    # 1. 过滤(在副本上操作,不改原数据)
    result = todos_db.copy()
    if keyword:
        result = [t for t in result if keyword.lower() in t["title"].lower()]
    if category:
        result = [t for t in result if category.lower() in t["category"].lower()]
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]

    # 2. 分页切片
    total = len(result)                          # 过滤后的总条数
    start = (page - 1) * size                    # 起始索引
    end = start + size                           # 结束索引
    page_data = result[start:end]                # 切出这一页

    # 3. 返回数据 + 分页信息(前端要显示"共几页")
    return {
        "data": page_data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        },
    }
```

💡 **速记**:`math.ceil(total / size)` = 总页数(向上取整,3.2 页 → 4 页)。

## 6.4 JSON 文件持久化

### 🟡 重启不丢数据

> 📌 **知识点说明**:内存列表重启就没了。把数据写成 JSON 文件,**启动时 load,每次修改后 save**,实现简单持久化。真实项目用数据库(SQLite/MySQL,见 Day29-32),但这个思想(读写分离)是通用的。

```python
import json, os

DATA_FILE = "todos.json"          # 数据文件名

def load_todos():
    """启动时从文件加载数据"""
    if os.path.exists(DATA_FILE):              # 文件存在才读
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []                                  # 文件不存在返回空列表

def save_todos():
    """每次修改后保存到文件(ensure_ascii=False 保留中文)"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos_db, f, ensure_ascii=False, indent=2)

todos_db = load_todos()          # 启动时加载
```

## 6.5 路由顺序坑

### 🟡 动态路由会拦截静态路由!

> 📌 **知识点说明**:`/todos/{todo_id}` 会匹配 `/todos/stats/summary`(把 `stats` 当 todo_id)。**所以 `/todos/stats/summary` 必须定义在 `/todos/{todo_id}` 之前**,否则永远匹配不到统计接口,还会因为 `int` 校验失败返回 422。

```python
# ❌ 错误顺序:先定义动态路由 {todo_id},后面统计接口被拦截
# @app.get("/todos/{todo_id}")
# def find_todo(todo_id: int): ...

# @app.get("/todos/stats/summary")   # ← 永远访问不到!被当成 {todo_id}="stats"

# ✅ 正确顺序:静态路由(无参数)在前,动态路由在后
@app.get("/todos/stats/summary")
def summary():
    return {"total": 3, "completed": 1, "pending": 2}

@app.get("/todos/{todo_id}")
def find_todo(todo_id: int):
    ...
```

## 6.6 完整 CRUD 接口一览(Day28 最终版)

### 🔴 五接口总览 + 统一细节

| 接口 | 方法 | 作用 | 关键点 |
|------|------|------|--------|
| `/todos` | POST | 创建 | 201 + `date.today().isoformat()` 存日期 |
| `/todos` | GET | 列表(搜索+分页) | 过滤→total→切片 |
| `/todos/{id}` | GET | 详情 | 查不到 → 404 |
| `/todos/{id}` | PUT | 全量更新 | 全部字段替换 |
| `/todos/{id}` | PATCH | 部分更新 | `model_dump(exclude_unset=True)` |
| `/todos/{id}` | DELETE | 删除 | 204 无响应体 |
| `/todos/stats/summary` | GET | 统计 | `Counter` 统计分类 |

```python
# 创建时把日期转成 ISO 字符串(重点:date 对象不能直接存 JSON)
from datetime import date
new_todo = {
    "id": generate_id(),
    "title": todoscreate.title,
    "completed": False,
    "created_at": date.today().isoformat(),   # .isoformat() 转成 "2026-07-26"
}
```

---

## 第 6 章【错误原因 + 修复方案】模块

> 来源:Day28 项目实战中修复的 6 个真实 Bug,每个都是面试/开发的常见坑。

### ❌ Bug 1:`date.today()` 不能直接 JSON 序列化

**错误原因**:`date.today()` 返回 `datetime.date` 对象,`json.dump` 不认识,报 `TypeError: Object of type date is not JSON serializable`。

**修复方案**:
```python
# ❌ 直接存 date 对象
# "created_at": date.today()        # 报错!
# ✅ 转成 ISO 字符串
"created_at": date.today().isoformat()   # "2026-07-26"
```

### ❌ Bug 2:completed 过滤用了 `.lower()`

**错误原因**:`completed` 是布尔值,`t["completed"].lower()` 在布尔值上调用 `.lower()` 直接报 `AttributeError`(只有字符串有 .lower())。这是把字符串处理习惯套到布尔值上了。

**修复方案**:
```python
# ❌ 错误
# result = [t for t in result if t["completed"].lower() == "true"]
# ✅ 正确:布尔值直接比较
result = [t for t in result if t["completed"] == completed]
```

### ❌ Bug 3:`total.size` 写法错误

**错误原因**:`total` 是数字,int 类型没有 `.size` 属性。分页计算里误写成 `total.size / size`。

**修复方案**:
```python
# ❌ total.size → AttributeError
# "total_pages": math.ceil(total.size / size)
# ✅ 直接用 total
"total_pages": math.ceil(total / size) if size > 0 else 0
```

### ❌ Bug 4:`/todos/stats/summary` 被 `{todo_id}` 拦截

**错误原因**:见 6.5 路由顺序坑,动态路由把 `stats` 当成 `todo_id`,且 int 校验失败返回 422。

**修复方案**:把 `/todos/stats/summary` 路由定义在 `/todos/{todo_id}` **之前**。

### ❌ Bug 5:`load_todos()` 返回 None 导致首次运行崩溃

**错误原因**:`load_todos()` 函数里 `return []` 的缩进错误,导致条件分支外没有 return,函数返回 `None`,`todos_db = None` 后 `.append()` 报错。

**修复方案**:保证函数**所有路径都有返回值**:
```python
def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []        # ← 缩进必须在 if 外面,文件不存在时也返回
```

### ❌ Bug 6:response_model 与分页字典冲突

**错误原因**:列表接口声明了 `response_model=List[TodoResponse]`,但实际返回的是 `{"data": [...], "pagination": {...}}` 字典,类型不匹配。

**修复方案**:返回分页字典的接口**不声明 List 类型的 response_model**,或单独定义分页响应模型。

---

## 🎯 第 6 章 面试/开发高频考点

**必问**:
1. 分页的公式是什么?为什么 `start = (page-1) * size`?
2. PATCH 部分更新怎么实现?(`model_dump(exclude_unset=True)`)
3. `math.ceil(total / size)` 求的是什么?(总页数,向上取整)
4. 路由顺序为什么影响功能?(动态路由拦截静态路由)
5. 内存存储和文件持久化的区别?

**加分项**:
- 能完整讲出"过滤 → total → 切片"的分页三步
- 知道 `date.today().isoformat()` 解决 JSON 序列化
- 用 Counter 统计分类数量

**冷门**:
- `generate_id()` 用 `max(id列表)+1` 而非 `len+1`(删过数据 id 不连续,用 len 会撞 id)
- `todos_db.copy()` 过滤时保护原数据(列表浅拷贝)

---

# 📕 本册错题本

| # | 错误代码/场景 | 报错/现象 | 原因 | 修复 |
|---|--------------|----------|------|------|
| 1 | `POST /users` 重复定义 | 文档混乱、后者覆盖前者 | 同路径同方法多条路由 | 合并/改名,一组合并一条 |
| 2 | 路径参数 user_id 类型忘写/写错 | 拿到字符串、运算报错 | 类型注解没加/破坏性实验没还原 | 加 `int`,实验后还原 |
| 3 | `Field(gt=0)` 配 `default=0` | 一提交就 422 | 默认值不满足校验 | 必填用 `Field(...)` 或改默认值 |
| 4 | gt/ge 含义记反 | 面试答错 | 记反了 greater than | 背:gt=大于,ge=大于等于 |
| 5 | `user.dict()` | Pydantic v2 报错 | v1 写法 | 改 `model_dump()` |
| 6 | 布尔值用 `.lower()` | AttributeError | completed 是 bool 不是 str | 直接比较 `==` |
| 7 | `total.size` | AttributeError | int 没有 .size | 直接用 `total` |
| 8 | stats 路由放 {id} 后面 | 访问统计接口 422 | 动态路由拦截 | 静态路由放前面 |
| 9 | load_todos 缩进错 | 首次运行 None 崩溃 | return [] 缩进在 if 里 | 所有路径都 return |
| 10 | 列表接口声明 List 响应模型但返回分页字典 | 类型冲突 | response_model 和返回结构不符 | 分页接口不声明 List 模型 |
