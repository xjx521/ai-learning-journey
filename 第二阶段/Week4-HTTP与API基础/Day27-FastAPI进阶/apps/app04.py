from fastapi import APIRouter, Form
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

app04 = APIRouter()


@app04.post("/register")
async def reg(
    username: str = Form(), password: str = Form()
):  # username和password是请求体里的Form表单数据
    print(f"username={username},password={password}")
    return {"username": username}
