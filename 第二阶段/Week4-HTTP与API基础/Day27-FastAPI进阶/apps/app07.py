from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from typing import Union, List

app07 = APIRouter()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.3},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app07.post("/reg", response_model=UserOut)
def create_user(user: UserIn):
    # 存到数据库
    return user


@app07.post("/items/{items_id}", response_model=Item, response_model_exclude_unset=True)
def create_user(items_id: str):
    # 存到数据库
    return items[items_id]


@app07.post(
    "/items_none/{items_id}", response_model=Item, response_model_exclude_none=True
)  # response_model_exclude_none/default默认值是None不返回
def create_user_none(items_id: str):
    return items[items_id]


@app07.post(
    "/items_include/{items_id}",
    response_model=Item,
    response_model_include={"name", "price"},
)  # include返回包含include内的字段 exclude排除exclude内的字段
def create_user_include(items_id: str):
    return items[items_id]
