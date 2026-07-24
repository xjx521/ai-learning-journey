from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get(
    "/get",
    tags=["这是 get测试接口"],
    summary="这是get测试总结",
    description="这是get测试详情",
    response_description="这是get测试响应详情",
    deprecated=False,  # 废弃接口
)
def get_test():
    return {"message": "get方法"}


@app.post(
    "/post",
    tags=["这是post测试接口"],
    summary="这是post测试总结",
    description="这是post测试详情",
    response_description="这是post测试响应详情",
)
def post_test():
    return {"message": "post方法"}


@app.put(
    "/put",
    tags=["这是 put测试接口"],
    summary="这是put测试总结",
    description="这是put测试详情",
    response_description="这是put测试响应详情",
)
def put_test():
    return {"message": "put方法"}


@app.delete(
    "/delete",
    tags=["这是 delete测试接口"],
    summary="这是delete测试总结",
    description="这是delete测试详情",
    response_description="这是delete测试响应详情",
)
def delete_test():
    return {"message": "delete方法"}


if __name__ == "__main__":
    uvicorn.run("day26-路径操作装饰器方法:app", port=8080, reload=True)
