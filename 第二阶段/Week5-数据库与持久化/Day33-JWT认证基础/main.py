import sys
import os
import uvicorn
from datetime import datetime, timedelta, timezone

# ============================================================
# 前置导入（每个实验都需要）
# ============================================================
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from jose import jwt, JWTError
from passlib.context import CryptContext

# ============================================================
# 【实验 1】bcrypt 密码哈希实验
# ============================================================

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed1 = pwd_context.hash("mypassword123")
print(f"第一次哈希：{hashed1}")

hashed2 = pwd_context.hash("mypassword123")
print(f"第二次哈希：{hashed2}")

if not pwd_context.verify("wrongpassword", hashed1):
    print("✗ 密码错误")

# ============================================================
# 【实验 2】PyJWT 生成和验证 Token
# ============================================================

SECRET_KEY = "my-secret-key-123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
# --- 签发 token ---
payload = {
    "sub": "user_001",  # 用户名/ID
    "role": "admin",  # 自定义字段
    "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    "iat": datetime.now(timezone.utc),
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(f"Token: {token}")
# token 由三段组成，用 . 分隔
parts = token.split(".")
print(f"段数：{len(parts)}        # 应该是 3")
print(f"Header Base64: {parts[0][:50]}...")
print(f"Payload Base64: {parts[1][:50]}...")
print(f"Signature: {parts[2][:50]}...")

# --- 解码 token ---
decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print(f"解码结果：{decoded}")

# ============================================================
# 【实验 3】POST /register — 用户注册
# ============================================================
app = FastAPI(title="Day33 练习")

fake_db: dict[str, dict] = {}

# OAuth2 Bearer Token 方案（FastAPI 内置）
# tokenUrl 指向登录接口，让 /docs 自动弹出授权按钮
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str
    password: str = Field(..., min_length=6)


def get_user_from_db(username: str) -> dict | None:
    return fake_db.get(username)


@app.post("/users/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if get_user_from_db(user.username):
        raise HTTPException(status_code=400, detail="用户名已被注册")

    fake_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": pwd_context.hash(user.password),
    }
    return {"message": f"用户 {user.username} 注册成功！"}


# ============================================================
# 【实验 4】POST /login — 用户登录
# ============================================================
class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = get_user_from_db(form_data.username)

    if not db_user or not pwd_context.verify(
        form_data.password, db_user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号或密码错误",
        )

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": db_user["username"],
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return TokenResponse(access_token=token, token_type="bearer")


# ============================================================
# 【实验 5】Bearer Token 鉴权中间件
# ============================================================
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "恭喜你！你已经通过了 JWT 认证！",
        "username": current_user["username"],
    }


if __name__ == "__main__":
    uvicorn.run("day33-login:app", port=8080, reload=True)
