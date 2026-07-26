from fastapi import APIRouter
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

app03 = APIRouter()


class Addr(BaseModel):
    province: str
    city: str


class User(BaseModel):
    # name: str = Field(pattern="^a")  # 正则只能以a开头
    name: str
    age: int = Field(default=0, gt=0, lt=100)
    birthday: Optional[date] = None
    friends: List[int] = []
    description: Optional[str] = None
    addr: Addr  # 类型嵌套

    @field_validator("name")
    def name_must_alpha(cls, value):
        assert value.isalpha(), "name must be alpha"  # 判断是否纯英文
        # assert断言
        # 条件为 True：代码正常往下走，无任何反应
        # 条件为 False：直接抛出 AssertionError 终止程序，展示你写的提示
        return value


class Data(BaseModel):
    data: List[User]  # 组合嵌套


@app03.post("/user")
async def user(user: User):
    print(user, type(user))
    print(user.name, user.age)
    # print(user.dict())
    return user


@app03.post("/data")
async def data(data: Data):
    return data
