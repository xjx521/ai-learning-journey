from fastapi import APIRouter

shop = APIRouter()  # 创建子路由对象shop，用于统一管理商铺相关接口 接口路由对象


@shop.get("/food")
def shop_food():
    return {"message": "food"}


@shop.get("/phone")
def shop_phone():
    return {"message": "phone"}
