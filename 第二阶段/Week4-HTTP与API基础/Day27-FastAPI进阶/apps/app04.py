from fastapi import APIRouter, Form

app04 = APIRouter()


@app04.post("/register")
async def reg(
    username: str = Form(), password: str = Form()
):  # username和password是请求体里的Form表单数据
    print(f"username={username},password={password}")
    return {"username": username}
