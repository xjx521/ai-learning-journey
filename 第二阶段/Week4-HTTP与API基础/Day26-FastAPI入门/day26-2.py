from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"user_id": 1001}


@app.get("/shop")
def shop():
    return {"shop": "phone"}


if __name__ == "__main__":
    uvicorn.run(
        "day26-2:app", port=8000, reload=True
    )  # 无需命令行启动uvicorn (:app,port,reload)
