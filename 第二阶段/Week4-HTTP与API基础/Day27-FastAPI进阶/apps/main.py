from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from app03 import app03
from app04 import app04
from app05 import app05
from app06 import app06
from app07 import app07

app = FastAPI()

app.mount("/static", StaticFiles(directory="statics"))

app.include_router(app03, prefix="/app03", tags=["03 请求体参数"])
app.include_router(app04, prefix="/app04", tags=["04 form表单数据"])
app.include_router(app05, prefix="/app05", tags=["05 文件上传"])
app.include_router(app06, prefix="/app06", tags=["06 Request对象"])
app.include_router(app07, prefix="/app07", tags=["07 响应模型参数"])
if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
