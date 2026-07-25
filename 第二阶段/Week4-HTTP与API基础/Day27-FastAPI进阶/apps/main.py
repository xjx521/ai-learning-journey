from fastapi import FastAPI
import uvicorn
from app03 import app03
from app04 import app04

app = FastAPI()

app.include_router(app03, prefix="/app03", tags=["03 请求体参数"])
app.include_router(app04, prefix="/app04", tags=["04 请求体参数"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
