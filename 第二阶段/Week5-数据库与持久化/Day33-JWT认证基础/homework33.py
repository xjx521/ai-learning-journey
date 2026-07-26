"""
Day 33 练习题：JWT 认证基础 — 密码哈希、Token 签发、Bearer 鉴权
=====================================================================

⚠️ 前置准备：
    pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic[email]

💡 建议：所有实验写在 main.py 中，逐个测试通过后再继续。

📖 先读学习笔记.md，理解 JWT 三段结构和 bcrypt 原理！
"""

import sys
import os
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
"""
目标：理解哈希不可逆的特性，观察 salt 的作用

步骤：

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 注册时：明文密码 → 哈希值
hashed1 = pwd_context.hash("mypassword123")
print(f"第一次哈希：{hashed1}")

hashed2 = pwd_context.hash("mypassword123")
print(f"第二次哈希：{hashed2}")

# 验证：输入正确的密码
if pwd_context.verify("mypassword123", hashed1):
    print("✓ 密码正确")

# 验证：输入错误的密码
if not pwd_context.verify("wrongpassword", hashed1):
    print("✗ 密码错误")
```

测试 1.1：两次 hash 同一个密码，结果一样吗？
结果：______不一样！因为 bcrypt 每次自动生成不同的 random salt___________

测试 1.2：用 verify() 验证正确密码，返回 True 还是 False？
结果：_____True________

测试 1.3：用 verify() 验证错误密码，返回 True 还是 False？
结果：_____False________

问题 1.1：如果两个用户密码相同，哈希值会一样吗？有什么安全隐患？
你的答案：__一开始生成的哈希值不会一样（因为salt不同），所以不存在彩虹表直接碰撞的问题；但如果攻击者破解了一个用户的哈希，就能用同样的明文去尝试其他账户的verify()——所以弱密码还是要单独处理_____________

问题 1.2：能把 bcrypt 哈希值存到前端代码里吗？为什么？
你的答案：__不能！前端代码任何用户都能看到，他们拿到哈希值后可以用它来伪造登录请求（如果服务器只比对哈希值的话）。哈希值只能存在后端数据库里，验证必须用verify()函数在服务器端做___________
"""

# ==================== 参考答案 ====================
# 测试 1.1：两次哈希结果不同（salt 随机生成），但都能用 verify() 正确匹配
# 测试 1.2：True
# 测试 1.3：False
# 1.1：bcrypt 自带 salt，同密码的不同哈希值看起来完全不同。安全优势就是防彩虹表
# 1.2：绝对不行！前端代码对所有人可见，应该只存在后端数据库，验证必须在服务端进行
#     （注意：如果黑客拿到了存储在服务器上的 bcrypt 哈希值，他确实可以用暴力破解慢慢试出密码。）

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- 破坏性实验 ----------
# 实验 A：把 pwd_context.hash() 改成 pwd_context.verify() 然后再赋值给 hashed
# hashed_wrong = pwd_context.verify("test", "some_hash")  ← 返回的是 bool，不是哈希字符串！
# 后面再验证就会报错或永远不匹配
#
# 实验 B：用 hashlib.sha256("mypassword").hexdigest() 代替 bcrypt
# sha_hash = hashlib.sha256("mypassword".encode()).hexdigest()
# 优点：快。缺点：相同密码永远得到相同哈希 → 彩虹表秒破！
# bcrypt 的 slow 特性让暴力破解成本提高了几十万倍

print("=" * 50)
print("实验 1：bcrypt 密码哈希")
print("=" * 50)
h1 = pwd_context.hash("test123")
h2 = pwd_context.hash("test123")
print(f"h1 == h2: {h1 == h2}          # {h1 == h2} (应该是 False)")
print(f"verify correct: {pwd_context.verify('test123', h1)}   # True")
print(f"verify wrong:   {pwd_context.verify('wrong', h1)}    # False")
print()


# ============================================================
# 【实验 2】PyJWT 生成和验证 Token
# ============================================================
"""
目标：手动调用 jwt.encode() 和 jwt.decode()，观察 JWT 的结构

步骤：

```python
from jose import jwt

SECRET_KEY = "my-secret-key-123"
ALGORITHM = "HS256"

# --- 签发 token ---
payload = {
    "sub": "user_001",        # 用户名/ID
    "role": "admin",          # 自定义字段
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
# {'sub': 'user_001', 'role': 'admin', 'exp': ..., 'iat': ...}
```

测试 2.1：token 被 `.` 分成了几段？
结果：_____3段（header.payload.signature）________

测试 2.2：解码后用 payload.get("sub") 能拿到什么？
结果：_____"user_001"_________

测试 2.3：用一个完全不同的密钥去 decode，会发生什么？
结果：_____抛出 JWTError 异常（签名不匹配）__________

问题 2.1：如果把 exp（过期时间）设成过去的时间，decode 会成功吗？
你的答案：__不会成功，会抛 JWTError（token expired）__________

问题 2.2：jwt.encode() 的 SECRET_KEY 泄露了会发生什么？
你的答案：__任何人都能用这个密钥伪造任意用户的 token——比如创建一个 role=admin 的 token，然后以管理员身份访问系统____
"""

# ==================== 参考答案 ====================
# 测试 2.1：3 段
# 测试 2.2："user_001"
# 测试 2.3：抛出 JWTError（invalid signature）
# 2.1：不会，JWT 库在 decode 时会自动检查 exp 字段
# 2.2：非常危险！SECRET_KEY 泄露意味着攻击者可以签发任意身份的 token

SECRET_KEY = "my-secret-key-change-in-production-abc123xyz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

print("=" * 50)
print("实验 2：PyJWT 签发和解码")
print("=" * 50)

# 签发一个正常的 token
expire_time = datetime.now(timezone.utc) + timedelta(minutes=30)
payload = {
    "sub": "zhangsan",
    "role": "user",
    "exp": expire_time,
    "iat": datetime.now(timezone.utc),
}
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(f"Token 长度：{len(token)} 字符")
parts = token.split(".")
print(f"分成 {len(parts)} 段")

# 正常解码
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"解码成功：sub={decoded['sub']}, role={decoded['role']}")
except JWTError as e:
    print(f"解码失败：{e}")

# 用错密钥解码
try:
    bad_token = jwt.decode(token, "wrong-key", algorithms=[ALGORITHM])
    print("用错密钥也成功了？不应该！")
except JWTError as e:
    print(f"用错密钥解码失败（正确行为）：{type(e).__name__}")

print()

# ---------- 破坏性实验 ----------
# 实验 A：修改 token 字符串中的任意一个字符，再 decode
# tampered_token = token[:-1] + ("A" if token[-1] != "A" else "B")
# jwt.decode(tampered_token, SECRET_KEY, algorithms=[ALGORITHM])
# → 签名不匹配，抛出 JWTError！这就是签名的作用。

# 实验 B：去掉 exp 字段再 encode
payload_no_exp = {"sub": "admin", "role": "super_admin"}
forever_token = jwt.encode(payload_no_exp, SECRET_KEY, algorithm=ALGORITHM)
try:
    result = jwt.decode(forever_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"没有 exp 的 token 也能 decode：{result}")
    # ⚠️ 永不过期！生产环境必须有 exp！
except JWTError as e:
    print(f"无 exp token 解码失败：{e}")

print()


# ============================================================
# 【实验 3】POST /register — 用户注册
# ============================================================
"""
目标：实现完整的注册接口，包括密码哈希和查重

步骤：创建 main.py

```python
app = FastAPI(title="Day33 练习")

fake_db: dict[str, dict] = {}

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
```

测试 3.1：注册新用户 {"username":"alice","email":"a@test.com","password":"123456"}
结果：_____201 Created, {"message": "用户 alice 注册成功！"}________

测试 3.2：再次注册同样的用户名
结果：__400 Bad Request, {"detail": "用户名已被注册"}__________

测试 3.3：密码少于 6 位会怎样？
结果：____422 Unprocessable Entity (Field validation error: min_length)__________

测试 3.4：用户名少于 3 个字符会怎样？
结果：__422 Unprocessable Entity (Field validation error: min_length)____

问题 3.1：为什么密码字段不在响应体里返回？
你的答案：__密码应该只在注册时传入，存储时用哈希值，不应该在任何响应中暴露明文或哈希值__________

问题 3.2：如果注册接口不用 Field 做验证，用户传空字符串会发生什么？
你的答案：__空字符串也能注册，后续登录可能出问题，甚至成为垃圾账号。用 Field(...) 约束是防御性编程_______
"""

# ==================== 参考答案 ====================
# 3.1：密码已经哈希存入 fake_db["username"]["hashed_password"]，不需要也不应该返回
# 3.2：空字符串也能注册，变成无效账号，浪费资源且可能被恶意利用

app = FastAPI(title="Day33 练习")

fake_db: dict[str, dict] = {}


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


# ---------- 破坏性实验 ----------
# 实验：把 Field(min_length=6) 里的 6 改成 1，或者干脆删掉验证规则
# 然后注册 {"username":"a","email":"b@c.com","password":"1"}
# → 能注册成功！但是密码太短很危险，容易被暴力破解。
# → 所以密码应该有最低长度要求（至少 8 位更合理）

print("=" * 50)
print("实验 3：POST /register 注册接口")
print("=" * 50)
print("打开 http://localhost:8000/docs 测试以下接口：")
print("  POST /users/register → 注册")
print("  GET  /healthcheck → 健康检查")


# ============================================================
# 【实验 4】POST /login — 用户登录
# ============================================================
"""
目标：实现登录接口，验证密码后签发 JWT Token

步骤：添加以下代码

```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = get_user_from_db(form_data.username)

    if not db_user or not pwd_context.verify(form_data.password, db_user["hashed_password"]):
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
```

测试 4.1：先用实验 3 注册的用户登录，{"username":"alice","password":"123456"}
结果：__200 OK, 返回包含 access_token 和 token_type 的 JSON________

测试 4.2：登录一个还没注册的用户
结果：_401 Unauthorized, {"detail": "账号或密码错误"}________

测试 4.3：用正确的用户名但错误的密码登录
结果：___401 Unauthorized, {"detail": "账号或密码错误"}（不要透露到底是用户名错还是密码错！）____

测试 4.4：把 ACCESS_TOKEN_EXPIRE_MINUTES 改成 1，等 2 分钟再 decode 拿到的 token
结果：____抛 JWTError (token expired)__________

问题 4.1：为什么要统一返回"账号或密码错误"而不是分别返回"用户名不存在"和"密码错误"？
你的答案：__安全考虑——防止攻击者通过返回信息枚举哪些用户名是已注册的（User Enumeration 攻击）_______

问题 4.2：token_url="/auth/login" 对 Swagger UI (/docs) 有什么好处？
你的答案：__Swagger UI 会在每个需要认证的接口上方显示"Authorize"按钮，点击后输入 token 就可以带着 token 发请求，免去了手动加请求头的麻烦______
"""

# ==================== 参考答案 ====================
# 4.1：为了防枚举攻击。如果分别提示，黑客可以尝试常见用户名+常见密码组合，直到发现有效组合
# 4.2：OAuth2PasswordBearer 会自动在 /docs 界面添加授权入口

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = get_user_from_db(form_data.username)

    if not db_user or not pwd_context.verify(form_data.password, db_user["hashed_password"]):
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


print()
print("  POST /auth/login → 登录获取 token")
print()


# ============================================================
# 【实验 5】Bearer Token 鉴权中间件
# ============================================================
"""
目标：实现 get_current_user 依赖注入函数，保护接口

步骤：添加以下代码

```python
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
```

测试 5.1：不带 token 直接调 /protected
结果：____401 Unauthorized（"无法验证凭证"）__________

测试 5.2：带了合法 token 调 /protected
结果：__200 OK, {"message": "恭喜你！...", "username": "alice"}__________

测试 5.3：复制别人的 token 用自己的用户名调 /protected
结果：__也是可以的！Token 里带的是谁的信息就代表谁的身份。这是正常的——JWT 就是用来传递身份信息的_____

测试 5.4：篡改 token 字符串（改一个字符）后调 /protected
结果：__401 Unauthorized（签名不对，抛出 JWTError）__________

测试 5.5：把一个过期的 token 调 /protected
结果：__401 Unauthorized（token expired）______________

问题 5.1：为什么要把 credentials_exception 提到函数外面定义？
你的答案：__如果在 try/except 内部 new 一个 HTTPException，HTTP 响应的 headers 字段可能不会被正确设置。提外面保证每次 raise 时用的是同一个对象实例，headers 格式一致_____

问题 5.2：current_user 是从哪里来的？是谁调用了 get_current_user？
你的答案：__FastAPI 自动调用！当你写 Depends(get_current_user) 时，FastAPI 在进接口前先执行这个函数，把返回值赋给 current_user 参数。你不需要自己调用它__________
"""

# ==================== 参考答案 ====================
# 5.1：确保 WWW-Authenticate: Bearer header 始终被正确设置
# 5.2：FastAPI 的依赖注入系统自动调用，你只需要声明 Depends()
#
# ---------- 破坏性实验 ----------
# 实验 A：把 jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#       改成 jwt.decode(token, "wrong-key", algorithms=[ALGORITHM])
#       所有请求都会 401 —— 包括你自己签发的 token 也不行
#
# 实验 B：把 payload.get("sub") 改成 payload.get("not_exist")
#       永远是 None → 永远抛 credentials_exception → 所有接口都打不开
#
# 实验 C：故意不改 get_current_user，但把 /auth/login 返回的 token_type 从 "bearer" 改成 "basic"
#       前端如果严格按照 token_type 处理可能会出错，所以保持一致很重要
#
# ---------- 完整测试流程 ----------
# 1. uvicorn main:app --reload
# 2. curl -X POST http://localhost:8000/users/register \
#      -H "Content-Type: application/json" \
#      -d '{"username":"testuser","email":"t@test.com","password":"secret123"}'
# 3. curl -X POST http://localhost:8000/auth/login \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "username=testuser&password=secret123"
#    → 拿到 access_token
# 4. TOKEN=<上面的token>
#    curl http://localhost:8000/protected -H "Authorization: Bearer $TOKEN"
#    → 应该返回 {"message":"恭喜你！...","username":"testuser"}

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """从 Bearer Token 中提取并验证用户信息"""
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


@app.get("/")
def index():
    return {"message": "欢迎！这个接口不需要认证。"}


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 387 - 字符串中的第一个唯一字符（Easy）
#    链接：https://leetcode.cn/problems/first-unique-character-in-a-string/
#    思路提示：用字典统计频率，类似于从大量数据中找唯一的记录
#
# 💡 Token 中包含的用户 ID 就是那个"唯一的标识符"
# ============================================================


# ============================================================
# 学习记录
# ============================================================
"""
📝 Day 33 学习打卡

完成时间：____年____月____日

我完成了以下实验：
[ ] 实验 1：bcrypt 密码哈希
[ ] 实验 2：PyJWT 签发和解码
[ ] 实验 3：POST /register 注册接口
[ ] 实验 4：POST /login 登录接口
[ ] 实验 5：Bearer Token 鉴权

遇到的问题：
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
