from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import uvicorn

app = FastAPI(title="JWT 认证演示")

# 密钥 —— 生产环境应该从环境变量读取！
SECRET_KEY = "your-secret-key-change-in-production-abc123xyz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # token 有效期 30 分钟

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Bearer Token 方案（FastAPI 内置）
# tokenUrl 指向登录接口，让 /docs 自动弹出授权按钮
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


### Step 2：数据模型


# 注册请求体
class UserRegister(BaseModel):
    username: str
    email: str
    password: str  # 明文密码，会被哈希后存储


# 登录请求体（OAuth2 标准格式）
# OAuth2PasswordRequestForm 会自动解析 form-data 类型的登录请求
class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# 受保护接口的响应
class ProtectedResponse(BaseModel):
    message: str
    username: str


### Step 3：模拟数据库（先用内存字典，后面替换为 SQLAlchemy）

# 模拟数据库：key=用户名，value=数据库记录
fake_db: dict[str, dict] = {}


def get_user_from_db(username: str) -> dict | None:
    """根据用户名查用户"""
    return fake_db.get(username)


### Step 4：POST /register 注册接口


@app.post("/users/register", status_code=201)
def register(user: UserRegister):
    # 1. 检查用户名是否已存在
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="用户名已被注册")

    # 2. 哈希密码
    hashed = pwd_context.hash(user.password)

    # 3. 存入"数据库"（真实场景中用 SQLAlchemy 插入 users 表）
    fake_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed,
    }

    return {"message": f"用户 {user.username} 注册成功！"}


### Step 5：POST /auth/login 登录接口


@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. 查用户
    db_user = get_user_from_db(form_data.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="账号或密码错误")

    # 2. 验证密码（用 verify 对比，不能用 == 直接比较！）
    if not pwd_context.verify(form_data.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="账号或密码错误")

    # 3. 签发 JWT Token
    #    设置过期时间：当前时间 + 30 分钟
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #    payload 内容（只有这些会被存到 token 里）
    payload = {
        "sub": db_user["username"],  # 主题：用户名
        "exp": expire,  # 过期时间
        "iat": datetime.now(timezone.utc),  # 签发时间
    }

    #    生成 token（内部做了 header 编码 + payload 编码 + signature 签名）
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return TokenResponse(access_token=token, token_type="bearer")


### Step 6：Bearer Token 验证函数


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    从 Bearer Token 中提取用户信息

    这个函数会在每个需要认证的接口中被自动调用（Depends(get_current_user)）
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},  # 告诉客户端需要用 Bearer 格式
    )

    try:
        # 解码并验证 token
        #    - SECRET_KEY：必须是和签发时用的一样的密钥
        #    - algorithms：必须包含签发时用的算法
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        # token 签名不对、格式错误或过期都会到这里
        raise credentials_exception

    # 查"数据库"获取完整用户信息
    user = get_user_from_db(username)
    if user is None:
        raise credentials_exception

    return user


### Step 7：需要认证的接口


@app.get("/protected", response_model=ProtectedResponse)
def protected_route(current_user: dict = Depends(get_current_user)):
    return ProtectedResponse(
        message="恭喜你！你已经通过了 JWT 认证！",
        username=current_user["username"],
    )


@app.get("/")
def index():
    return {"message": "欢迎！这个接口不需要认证。"}


if __name__ == "__main__":
    uvicorn.run("day33-login:app", port=8080, reload=True)
