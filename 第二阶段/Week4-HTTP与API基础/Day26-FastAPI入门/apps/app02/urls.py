from fastapi import APIRouter

user = APIRouter()  # 创建子路由对象user，用于统一管理商铺相关接口 接口路由对象


@user.post("/login")
def user_login():
    return {"message": "login"}


@user.post("/register")
def user_register():
    return {"message": "register"}
