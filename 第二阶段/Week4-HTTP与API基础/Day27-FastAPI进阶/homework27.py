"""
Day 27 练习题：FastAPI 进阶 — 请求体、响应模型、数据验证
====================================================

⚠️ 前置准备：
    pip install fastapi uvicorn pydantic[email]

今天的练习是"实验清单"模式，你需要写 main.py 并测试。

💡 建议：所有实验写在同一个 main.py 中，逐个添加接口。
"""


# ============================================================
# 【实验 1】第一个请求体
# ============================================================
"""
目标：用 Pydantic Model 接收 POST 请求体

步骤：创建 main.py：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    isbn: str | None = None

@app.post("/books")
def create_book(book: BookCreate):
    return {
        "message": f"《{book.title}》创建成功",
        "author": book.author,
        "price": book.price
    }
```

测试（在 /docs 中或 curl）：

测试 1：正确数据
```json
{"title": "Python入门", "author": "张三", "price": 59.9, "isbn": "978-7-111"}
```
结果：_________

测试 2：缺少必填字段 title
```json
{"author": "张三", "price": 59.9}
```
结果：_________

测试 3：类型错误
```json
{"title": "Python入门", "author": "张三", "price": "五十九块九"}
```
结果：_________

测试 4：不传可选字段 isbn
```json
{"title": "Python入门", "author": "张三", "price": 59.9}
```
结果：_________

问题 1.1：Pydantic 是怎么知道哪些字段必填、哪些可选的？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# 测试 1：200 {"message": "《Python入门》创建成功", "author": "张三", "price": 59.9}
# 测试 2：422 field required (title)
# 测试 3：422 value is not a valid float
# 测试 4：200 正常创建，isbn 为 None
# 1.1：有默认值（= None, = [] 等）的字段是可选的，没有默认值的是必填的


# ============================================================
# 【实验 2】Field 验证规则
# ============================================================
"""
目标：用 Field() 添加验证约束

步骤：添加以下代码：

```python
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0, le=99999)
    stock: int = Field(default=0, ge=0)
    category: str = Field(default="未分类")
```

测试用例：

| 输入 | 期望结果 | 实际结果 |
|------|---------|---------|
| {"name": "A", "price": 10} | 422（name 太短） | _________ |
| {"name": "手机", "price": -5} | _________ | _________ |
| {"name": "手机", "price": 100000} | _________ | _________ |
| {"name": "手机", "price": 99} | 成功，stock=0 | _________ |

问题 2.1：gt=0 和 ge=0 有什么区别？
你的答案：_____________

💡 破坏性实验：
  把 price: float = Field(..., gt=0) 改成 price: float = Field(default=0, gt=0)
  然后发送 {"name": "测试"}（不传 price），会怎样？
"""

# ==================== 参考答案 ====================
# {"name": "A", "price": 10} → 422 (min_length=2)
# {"name": "手机", "price": -5} → 422 (gt=0)
# {"name": "手机", "price": 100000} → 422 (le=99999)
# {"name": "手机", "price": 99} → 成功，{"name": "手机", "price": 99, "stock": 0, "category": "未分类"}
# 2.1：gt=0 表示 > 0（不包含 0），ge=0 表示 >= 0（包含 0）
# 破坏性实验：不传 price 会使用默认值 0，但 0 不满足 gt=0 的验证，所以仍然报 422！
#            这告诉你：default 值也必须满足验证规则。


# ============================================================
# 【实验 3】响应模型 — 过滤敏感字段
# ============================================================
"""
目标：用 response_model 过滤不想暴露的字段

步骤：添加以下代码：

```python
class UserCreate(BaseModel):
    username: str
    password: str  # 密码只在创建时需要
    email: str

class UserResponse(BaseModel):
    username: str
    email: str
    # 注意：没有 password 字段

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    # 模拟存入数据库（实际中密码要哈希）
    return {
        "username": user.username,
        "email": user.email,
        "password": user.password  # 即使返回了，response_model 会过滤掉
    }
```

测试：
  POST /users {"username": "zhangsan", "password": "123456", "email": "z@test.com"}

问题 3.1：响应中包含 password 字段吗？
你的答案：_____________

问题 3.2：在 /docs 中查看 POST /users 的响应示例，看到了什么？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# 3.1：不包含，response_model=UserResponse 自动过滤了 password
# 3.2：响应示例只显示 username 和 email，不显示 password


# ============================================================
# 【实验 4】嵌套模型 + 列表
# ============================================================
"""
目标：处理复杂的嵌套 JSON 数据

步骤：添加以下代码：

```python
class Address(BaseModel):
    city: str
    street: str
    zipcode: str | None = None

class CompanyCreate(BaseModel):
    name: str
    employees: list[str] = []
    address: Address
    tags: list[str] = []

@app.post("/companies")
def create_company(company: CompanyCreate):
    return {
        "company": company.name,
        "city": company.address.city,
        "employee_count": len(company.employees)
    }
```

测试：构造一个合法的 JSON 请求体
你的 JSON：
```json
{

}
```

问题 4.1：address 字段在 JSON 中是什么结构？
你的答案：_____________

问题 4.2：如果 address 中缺少 city 字段会怎样？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# 测试 JSON 示例：
# {
#     "name": "Tech Corp",
#     "employees": ["张三", "李四"],
#     "address": {"city": "北京", "street": "中关村大街"},
#     "tags": ["科技", "互联网"]
# }
# 4.1：address 是嵌套对象 {"city": "北京", "street": "...", "zipcode": "..."}
# 4.2：422 错误，address.city field required


# ============================================================
# 【实验 5】HTTPException 错误处理
# ============================================================
"""
目标：用 HTTPException 返回标准错误

步骤：添加以下代码：

```python
from fastapi import HTTPException

fake_db = {
    1: {"title": "学习 Python", "completed": False},
    2: {"title": "学习 HTTP", "completed": True},
}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    return fake_db[todo_id]

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="待办事项不存在")
    del fake_db[todo_id]
    return None
```

测试：
  GET /todos/1 → _________
  GET /todos/999 → _________
  DELETE /todos/1 → _________
  DELETE /todos/999 → _________
  GET /todos/1 （删除后再查）→ _________

💡 破坏性实验：
  把 detail="待办事项不存在" 改成 detail={"error": "not_found", "id": todo_id}
  观察 /docs 中错误响应的格式变化。
"""

# ==================== 参考答案 ====================
# GET /todos/1 → 200 {"title": "学习 Python", "completed": False}
# GET /todos/999 → 404 {"detail": "待办事项不存在"}
# DELETE /todos/1 → 204（无内容）
# DELETE /todos/999 → 404
# GET /todos/1 (删除后) → 404
# 破坏性实验：detail 可以传字典，返回的 JSON 中 detail 字段会是一个对象


# ============================================================
# 【实验 6】综合练习：混合参数
# ============================================================
"""
目标：同时使用路径参数、查询参数和请求体

步骤：添加以下代码：

```python
class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

@app.put("/items/{item_id}")
def update_item(
    item_id: int,                   # 路径参数
    item: ItemUpdate,               # 请求体
    notify: bool = False            # 查询参数
):
    updates = item.model_dump(exclude_unset=True)  # 只获取实际传的字段
    return {
        "item_id": item_id,
        "updates": updates,
        "notify": notify
    }
```

测试：
  PUT /items/5?notify=true
  Body: {"price": 29.9}

问题 6.1：返回值中 updates 包含哪些字段？为什么 name 和 description 不在里面？
你的答案：_____________

问题 6.2：exclude_unset=True 的作用是什么？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# 6.1：updates 只有 {"price": 29.9}，因为 exclude_unset=True 只包含客户端实际传的字段
# 6.2：exclude_unset=True 表示排除没有显式设置的字段。
#     如果不加，updates 会是 {"name": None, "price": 29.9, "description": None}


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 88 - 合并两个有序数组（Easy）
#    链接：https://leetcode.cn/problems/merge-sorted-array/
#    思路提示：从后往前双指针，避免覆盖
#
# 2. LeetCode 125 - 验证回文串（Easy）
#    链接：https://leetcode.cn/problems/valid-palindrome/
#    思路提示：双指针从两端向中间移动，跳过非字母数字字符
#
# 💡 继续练习双指针技巧
# ============================================================


# ============================================================
# 学习记录
# ============================================================
"""
📝 Day 27 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：第一个请求体
[ ] 实验 2：Field 验证规则
[ ] 实验 3：响应模型过滤字段
[ ] 实验 4：嵌套模型 + 列表
[ ] 实验 5：HTTPException
[ ] 实验 6：混合参数

遇到的问题：
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
