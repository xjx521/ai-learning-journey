from fastapi import APIRouter, Request

app06 = APIRouter()


@app06.post("/items")
async def items(request: Request):
    return {
        "URL": request.url,
        "IP地址": request.client.host,
        "user-agent": request.headers.get("user-agent"),
        "cookies": request.cookies,
    }
