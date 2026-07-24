from fastapi import APIRouter
from typing import Union, Optional  # 类型注解

app02 = APIRouter()


@app02.get("/jobs/{kd}")
async def get_jobs(
    kd, xl: Union[str, None] = None, gj: Optional[str] = None
):  # 路径参数没有的自动识别为查询参数 这里kd就是路径参数其余就是查询参数
    # 基于kd,xl,gj数据库查询岗位信息
    # 有默认参数不必须填 引入Union后xl必须是str或者默认None Optional是Union的简写Optional[str]相当于Union[str,None]
    return {
        "kd": kd,
        "xl": xl,
        "gj": gj,
    }
