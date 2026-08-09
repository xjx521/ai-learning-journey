from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post("/api/chat")
def amswer():
    return {"answer": "你好！ 收到你的问题 这里是后端8000端口的固定回答"}


if __name__ == "__main__":
    uvicorn.run("service:app", port=8000, reload=True)
