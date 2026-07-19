"""
Day 26 练习题：FastAPI 入门
==========================

⚠️ 前置准备：
    pip install fastapi uvicorn

今天的练习是"实验清单"模式。
你需要写代码 → 启动服务器 → 在 /docs 或浏览器中测试。

💡 每个实验都是独立的，可以写在同一个 main.py 里逐个测试。
"""


# ============================================================
# 【实验 1】Hello World — 你的第一个 API
# ============================================================
"""
目标：创建一个最基本的 FastAPI 应用

步骤：
1. 创建 main.py，写入以下代码：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, 第二阶段！"}
```

2. 启动：uvicorn main:app --reload
3. 浏览器访问 http://localhost:8000
4. 浏览器访问 http://localhost:8000/docs

问题 1.1：访问 /docs 时看到了什么？
你的答案：_____________

问题 1.2：在 /docs 中点击 GET /  → "Try it out" → "Execute"，响应体是什么？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# 1.1：看到了 Swagger UI 自动生成的交互式文档页面，列出了 GET / 接口
# 1.2：{"message": "Hello, 第二阶段！"}  状态码 200


# ============================================================
# 【实验 2】路径参数 — 动态 URL
# ============================================================
"""
目标：理解路径参数的类型验证

步骤：把以下代码加入 main.py（或替换），重启服务器。

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "type": type(user_id).__name__}
```

测试用例（在浏览器或 /docs 中测试）：

| URL | 期望结果 | 实际结果 |
|-----|---------|---------|
| /users/123 | 成功，type 为 int | _________ |
| /users/abc | 失败，422 错误 | _________ |
| /users/3.14 | 失败，422 错误 | _________ |
| /users/ | 失败，404 错误 | _________ |

问题 2.1：user_id 被自动转换成了什么类型？
你的答案：_____________

问题 2.2：传入 "abc" 时返回的状态码是多少？错误信息是什么？
你的答案：_____________

💡 破坏性实验：
  把 user_id: int 改成 user_id: str，再用 /users/123 测试。
  观察：type 变成了什么？
"""

# ==================== 参考答案 ====================
# /users/123 → 成功，type 为 "int"
# /users/abc → 422 错误（类型验证失败）
# /users/3.14 → 422 错误（不是整数）
# /users/ → 404 错误（路径不匹配）
# 2.1：int 类型
# 2.2：422，提示 value is not a valid integer
# 破坏性实验：改成 str 后，123 变成了字符串类型 "123"


# ============================================================
# 【实验 3】查询参数 — 过滤和分页
# ============================================================
"""
目标：理解查询参数的默认值、必填、可选

步骤：在 main.py 中添加：

```python
from typing import Optional

@app.get("/items")
def list_items(page: int = 1, size: int = 10, keyword: Optional[str] = None):
    result = {"page": page, "size": size}
    if keyword:
        result["keyword"] = keyword
    return result
```

测试用例：

| URL | 期望的返回值 |
|-----|-------------|
| /items | {"page": 1, "size": 10} |
| /items?page=2&size=20 | ___________________ |
| /items?keyword=python | ___________________ |
| /items?page=abc | ___________________ |
| /items?size=5&keyword=fastapi&page=3 | ___________________ |

问题 3.1：哪些参数是必填的？哪些是可选的？
你的答案：_____________

问题 3.2：keyword 不传时，返回值中有 keyword 字段吗？
你的答案：_____________

💡 破坏性实验：
  把 keyword: Optional[str] = None 改成 keyword: str（去掉默认值）
  再用 /items 测试（不传 keyword），会发生什么？
"""

# ==================== 参考答案 ====================
# /items?page=2&size=20 → {"page": 2, "size": 20}
# /items?keyword=python → {"page": 1, "size": 10, "keyword": "python"}
# /items?page=abc → 422 错误（page 不是整数）
# /items?size=5&keyword=fastapi&page=3 → {"page": 3, "size": 5, "keyword": "fastapi"}
# 3.1：都是可选的（都有默认值）。如果 keyword: str 没有默认值则 keyword 必填。
# 3.2：没有 keyword 字段（因为 if keyword: 条件不满足）
# 破坏性实验：改成 keyword: str 后，/items 返回 422（缺少必填参数）


# ============================================================
# 【实验 4】路径参数 + 查询参数混合
# ============================================================
"""
目标：区分路径参数和查询参数

步骤：添加以下代码：

```python
@app.get("/users/{user_id}/items")
def get_user_items(user_id: int, category: str = "all", limit: int = 10):
    return {
        "user_id": user_id,
        "category": category,
        "limit": limit
    }
```

问题 4.1：哪些是路径参数？哪些是查询参数？
你的答案：_____________

问题 4.2：访问 /users/5/items?category=books&limit=3 的返回值是什么？
你的答案：_____________

问题 4.3：访问 /users/items（没有 user_id）会怎样？
你的答案：_____________

💡 破坏性实验：
  把参数顺序调换：def get_user_items(category: str, user_id: int, limit: int = 10)
  user_id 还是路径参数吗？（提示：看它是否在路径 {user_id} 中）
"""

# ==================== 参考答案 ====================
# 4.1：路径参数 = user_id；查询参数 = category, limit
# 4.2：{"user_id": 5, "category": "books", "limit": 3}
# 4.3：404 错误（路径不匹配，因为 /users/items 不匹配 /users/{user_id}/items 的模式，
#      除非 "items" 能被解析为整数传给 user_id，但 "items" 不是 int → 422）
# 破坏性实验：是的，user_id 仍然是路径参数！因为 FastAPI 根据路径中的 {user_id} 判断，
#            不是根据函数参数的位置。但 category 变成了必填查询参数（没有默认值）。


# ============================================================
# 【实验 5】枚举参数 — 限制可选值
# ============================================================
"""
目标：用 Enum 限制参数只能是特定值

步骤：添加以下代码：

```python
from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/sort/{order}")
def sort_data(order: SortOrder):
    return {"order": order, "message": f"按 {order.value} 排序"}
```

测试：
  /sort/asc → _________
  /sort/desc → _________
  /sort/random → _________

问题 5.1：传入 "random" 时返回了什么错误信息？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# /sort/asc → {"order": "asc", "message": "按 asc 排序"}
# /sort/desc → {"order": "desc", "message": "按 desc 排序"}
# /sort/random → 422 错误，提示值不在枚举选项中
# 5.1：类似 "value is not a valid enumeration member"


# ============================================================
# 【实验 6】返回状态码
# ============================================================
"""
目标：自定义返回的 HTTP 状态码

步骤：添加以下代码：

```python
from fastapi import status

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(name: str):
    return {"name": name, "message": "创建成功"}

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    return None  # 204 不需要返回内容
```

测试：
  POST /users?name=张三 → 观察状态码
  DELETE /users/123 → 观察状态码

问题 6.1：POST 返回的状态码是多少？（不是默认的 200）
你的答案：_____________

问题 6.2：DELETE 返回 204 时，响应体有内容吗？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# 6.1：201 Created
# 6.2：没有内容（204 No Content）


# ============================================================
# 【实验 7】自动文档实战
# ============================================================
"""
目标：给你的 API 添加描述信息，让 /docs 更漂亮

步骤：替换 app 的定义，并给接口添加描述：

```python
app = FastAPI(
    title="用户管理系统 API",
    description="Day 26 学习项目，用于练习 FastAPI 基础",
    version="0.1.0"
)

@app.get("/users", summary="获取用户列表", tags=["用户管理"])
def list_users(page: int = 1, size: int = 10):
    '''
    获取分页的用户列表。

    - **page**: 页码，从 1 开始
    - **size**: 每页数量
    '''
    return {"page": page, "size": size, "users": []}

@app.post("/users", summary="创建用户", tags=["用户管理"])
def create_user(name: str, email: str):
    '''创建新用户并返回用户信息'''
    return {"name": name, "email": email}

@app.get("/health", summary="健康检查", tags=["系统"])
def health_check():
    '''检查服务是否正常运行'''
    return {"status": "ok"}
```

任务：
1. 重启服务器，访问 /docs
2. 观察接口的分组（tags）、描述（summary）、详细说明（docstring）
3. 在 /docs 中直接测试每个接口

问题 7.1：tags 的作用是什么？
你的答案：_____________

问题 7.2：docstring（三引号注释）在 /docs 中显示在哪里？
你的答案：_____________
"""

# ==================== 参考答案 ====================
# 7.1：tags 用于在 /docs 中将接口分组，方便查看
# 7.2：docstring 显示在接口的详细描述区域，展开后可以看到


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 26 - 删除有序数组中的重复项（Easy）
#    链接：https://leetcode.cn/problems/remove-duplicates-from-sorted-array/
#    思路提示：双指针，慢指针记录不重复的位置，快指针遍历
#
# 2. LeetCode 27 - 移除元素（Easy）
#    链接：https://leetcode.cn/problems/remove-element/
#    思路提示：和上题类似，双指针原地替换
#
# 💡 双指针是面试高频技巧，这两题是入门级
# ============================================================


# ============================================================
# 学习记录
# ============================================================
"""
📝 Day 26 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：Hello World
[ ] 实验 2：路径参数
[ ] 实验 3：查询参数
[ ] 实验 4：路径 + 查询参数混合
[ ] 实验 5：枚举参数
[ ] 实验 6：状态码
[ ] 实验 7：自动文档

遇到的问题：
_____________________________________________
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
