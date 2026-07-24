from fastapi import APIRouter

app01 = APIRouter()


# 路由匹配顺序 优先级 结果跟路由顺序有关
# root用户
@app01.get("/user/1")  # 路径参数
def get_user():
    return {"user_id": "root user"}


@app01.get("/user/{id}")  # 路径参数
def get_user(id: int):  # 内置pydantic转换类型
    print("id:", id, type(id))
    return {"user_id": {id}}
