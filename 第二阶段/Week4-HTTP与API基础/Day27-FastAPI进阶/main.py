from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()


# 【实验 1】第一个请求体
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
        "price": book.price,
    }


# 【实验 2】Field 验证规则
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0, le=99999)
    stock: int = Field(default=0, ge=0)
    category: str = Field(default="未分类")


@app.post("/products")
def create_products(products: ProductCreate):
    return {"name": products.name, "price": products.price}


# 【实验 3】响应模型 — 过滤敏感字段
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
    return {"username": user.username, "email": user.email, "password": user.password}


# 【实验 4】嵌套模型 + 列表
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
        "employee_count": len(company.employees),
    }


# 【实验 5】HTTPException 错误处理
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


# 【实验 6】综合练习：混合参数
class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, notify: bool = False):
    updates = item.model_dump(exclude_unset=True)  # 只获取实际传的字段
    return {"item_id": item_id, "updates": updates, "notify": notify}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
