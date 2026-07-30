"""
Day 33 练习题：JWT 认证基础 — 密码哈希、Token 签发、Bearer 鉴权
=====================================================================

⚠️ 前置准备：
    pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic[email]

💡 建议：所有实验写在 main.py 中，逐个测试通过后再继续。

📖 先读学习笔记.md，理解 JWT 三段结构和 bcrypt 原理！
完成每一个「测试」和「问题」后再翻到文件末尾的参考答案。
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

📝 **测试 1.1**：两次 hash 同一个密码，结果一样吗？
答：______________不一样________________________________________________

📝 **测试 1.2**：用 verify() 验证正确密码，返回 True 还是 False？
答：__________________返回True____________________________________________

📝 **测试 1.3**：用 verify() 验证错误密码，返回 True 还是 False？
答：_______________________返回False_______________________________________

❓ **问题 1.1**：如果两个用户密码相同，哈希值会一样吗？有什么安全隐患？
不一样 bcrypt 自带 salt，所以同密码的不同哈希值看起来完全不同。安全优势就是防彩虹表。
      但如果攻击者破解了一个用户的哈希，可以用同样的明文去尝试其他账户的 verify()——所以弱密码还是要单独处理。
❓ **问题 1.2**：能把 bcrypt 哈希值存到前端代码里吗？为什么？
不能这样技术人员就可以盗取用户信息
"""

# ---------- 执行代码 ----------
print("=" * 50)
print("实验 1：bcrypt 密码哈希")
print("=" * 50)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
```

📝 **测试 2.1**：token 被 `.` 分成了几段？分别叫什么名字？
答：________________分成了三段 Header头部 Payload负载 Signature标签 ______________________________________________

📝 **测试 2.2**：解码后用 payload.get("sub") 能拿到什么？
答：_________________会拿到用户名/ID_____________________________________________

📝 **测试 2.3**：用一个完全不同的密钥去 decode，会发生什么？
答：________JWT校验会不通过______________________________________________________

❓ **问题 2.1**：如果把 exp（过期时间）设成过去的时间，decode 会成功吗？
不会成功，这时候token已过期
❓ **问题 2.2**：jwt.encode() 的 SECRET_KEY 泄露了会发生什么？
非常危险！SECRET_KEY 泄露意味着攻击者可以签发任意身份的 token——比如创建一个 role=admin 的 token，
      然后以管理员身份访问系统。所以 SECRET_KEY 必须放在环境变量或配置中心里，绝不硬编码。
"""

# ---------- 执行代码 ----------
print("=" * 50)
print("实验 2：PyJWT 签发和解码")
print("=" * 50)

SECRET_KEY = "my-secret-key-change-in-production-abc123xyz"
ALGORITHM = "HS256"

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

try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"解码成功：sub={decoded['sub']}, role={decoded['role']}")
except JWTError as e:
    print(f"解码失败：{e}")

try:
    bad_token = jwt.decode(token, "wrong-key", algorithms=[ALGORITHM])
    print("用错密钥也成功了？不应该！")
except JWTError as e:
    print(f"用错密钥解码失败（正确行为）：{type(e).__name__}")
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

📝 **测试 3.1**：注册新用户 ``
      返回了什么？状态码是多少？
答：___________返回{用户alice注册成功} 状态码201___________________________________________________

📝 **测试 3.2**：再次注册同样的用户名
预期：______返回400____{ "detail": "用户名已被注册"}__

📝 **测试 3.3**：密码少于 6 位会怎样？
预期：______注册成功返回201_代码对密码和用户名进行限制没有生效_____

📝 **测试 3.4**：用户名少于 3 个字符会怎样？
预期：______注册成功返回201_代码没有对密码和用户名进行限制没有生效________

❓ **问题 3.1**：为什么密码字段不在响应体里返回？
不安全 
❓ **问题 3.2**：如果注册接口不用 Field 做验证，用户传空字符串会发生什么？
会报错 空字符串也能注册，变成无效账号，浪费资源且可能被恶意利用。
      用 Field(...) 约束是防御性编程——在最外层挡住非法输入
"""

# ---------- 执行代码 ----------
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

📝 **测试 4.1**：先用实验 3 注册的用户登录
预期：______{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsImV4cCI6MTc4NTQyNzc4MCwiaWF0IjoxNzg1NDI1OTgwfQ.Dw3jit_I5-JcsUII0pjRqCTkixZ3VRliziOR71GzWHs",
  "token_type": "bearer"
}______

📝 **测试 4.2**：登录一个还没注册的用户
预期：_____{
  "detail": "账号或密码错误"
}______

📝 **测试 4.3**：用正确的用户名但错误的密码登录
预期：______"detail": "账号或密码错误"_____

📝 **测试 4.4**：把 ACCESS_TOKEN_EXPIRE_MINUTES 改成 1，等 2 分钟再 decode 拿到的 token
预期：______报错401_{
  "detail": "Not authenticated"
}_____

❓ **问题 4.1**：为什么要统一返回"账号或密码错误"而不是分别返回"用户名不存在"和"密码错误"？
为了防枚举攻击。如果分别提示"用户名不存在"和"密码错误"，
      黑客可以尝试常见用户名+常见密码组合，直到发现有效组合。
      统一错误信息让攻击者无法判断哪些用户名是有效的。
❓ **问题 4.2**：`token_url="/auth/login"` 对 Swagger UI (/docs) 有什么好处？
点击 "Authorize" 按钮后输入 token，之后所有需要认证的接口都会自动带上这个 token。
"""

# ---------- 执行代码 ----------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


ACCESS_TOKEN_EXPIRE_MINUTES = 30


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

📝 **测试 5.1**：不带 token 直接调 /protected
预期：______401错误detail": "Not authenticated"______

📝 **测试 5.2**：带了合法 token 调 /protected
预期：______200{
  "message": "恭喜你！你已经通过了 JWT 认证！",
  "username": "string"
}______

📝 **测试 5.3**：复制别人的 token 用自己的用户名调 /protected
预期：______也是可以的！Token 里带的是谁的信息就代表谁的身份。这是正常的——JWT 就是用来传递身份信息的。
      （当然实际项目中应该加权限控制限制不同用户的操作范围）______

📝 **测试 5.4**：篡改 token 字符串（改一个字符）后调 /protected
预期：______401错误detail": "Not authenticated"______

📝 **测试 5.5**：把一个过期的 token 调 /protected
预期：_____401错误detail": "Not authenticated"______

❓ **问题 5.1**：为什么要把 credentials_exception 提到函数外面定义？
      如果在 try/except 内部 new 一个 HTTPException，headers 可能不会被正确设置。
      提外面保证每次 raise 时用的是同一个对象实例。
❓ **问题 5.2**：current_user 是从哪里来的？是谁调用了 get_current_user？
depends调用了
"""


# ---------- 执行代码 ----------
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
# 💡 参考答案（完成所有练习后再看！）
# ============================================================
# 🔑 使用说明：先独立做完上面所有【测试】和【问题】，再打开这里对照。
# 如果你的答案思路接近就算对，不必文字完全一致。
# ------------------------------------------------------------

"""
== 实验 1 参考答案 ==

测试 1.1：两次哈希结果不同（因为 bcrypt 每次自动生成不同的 random salt），但都能用 verify() 正确匹配。
测试 1.2：True。verify() 会用相同的 salt 重新计算哈希然后比较。
测试 1.3：False。错误的密码经过盐值混合后的哈希值与原哈希不匹配。

问题 1.1：bcrypt 自带 salt，所以同密码的不同哈希值看起来完全不同。安全优势就是防彩虹表。
      但如果攻击者破解了一个用户的哈希，可以用同样的明文去尝试其他账户的 verify()——所以弱密码还是要单独处理。
问题 1.2：绝对不能！前端代码对所有人可见，应该只存在后端数据库，验证必须在服务端进行。


== 实验 2 参考答案 ==

测试 2.1：3 段 —— header.payload.signature
      header 告诉解码器用的什么算法；payload 是有效载荷（用户信息等）；signature 是签名用于防篡改。
测试 2.2："user_001"。sub 声明了主体的身份标识。
测试 2.3：抛出 JWTError 异常（invalid signature）。签名不匹配说明 token 被篡改了或密钥不对。

问题 2.1：不会成功。JWT 库在 decode 时会自动检查 exp 字段，过期就抛 JWTError。
      这就是为什么生产环境一定要设 exp！
问题 2.2：非常危险！SECRET_KEY 泄露意味着攻击者可以签发任意身份的 token——比如创建一个 role=admin 的 token，
      然后以管理员身份访问系统。所以 SECRET_KEY 必须放在环境变量或配置中心里，绝不硬编码。


== 实验 3 参考答案 ==

测试 3.1：201 Created，返回包含注册成功的消息。
测试 3.2：400 Bad Request，返回 {"detail": "用户名已被注册"}。
      这是因为 fake_db 中已经存在该用户名。
测试 3.3：422 Unprocessable Entity（Pydantic 字段验证失败，min_length 不足）。
测试 3.4：422 Unprocessable Entity（同上，username 的 min_length 约束）。

问题 3.1：密码已经哈希存入数据库，不需要也不应该在任何响应中暴露明文或哈希值。
      这是基本的安全原则。
问题 3.2： 空字符串也能注册，变成无效账号，浪费资源且可能被恶意利用。
      用 Field(...) 约束是防御性编程——在最外层挡住非法输入。


== 实验 4 参考答案 ==

测试 4.1：200 OK，返回包含 access_token 和 token_type 的 JSON。
      Token 是一段很长的 Base64 字符串，有效期 30 分钟。
测试 4.2：401 Unauthorized，返回 {"detail": "账号或密码错误"}。
      因为 fake_db 中没有这个用户。
测试 4.3：也是 401，返回同样的 "账号或密码错误"。
      不要透露到底是用户名错还是密码错！这是为了安全（防止枚举攻击）。
测试 4.4：401 Unauthorized，token expired。因为 token 已过期，jwt.decode 自动拒绝。

问题 4.1：为了防枚举攻击。如果分别提示"用户名不存在"和"密码错误"，
      黑客可以尝试常见用户名+常见密码组合，直到发现有效组合。
      统一错误信息让攻击者无法判断哪些用户名是有效的。
问题 4.2：OAuth2PasswordBearer 会自动在 /docs 界面添加授权入口。
      点击 "Authorize" 按钮后输入 token，之后所有需要认证的接口都会自动带上这个 token。


== 实验 5 参考答案 ==

测试 5.1：401 Unauthorized，"无法验证凭证"。没有 token 就无法证明身份。
测试 5.2：200 OK，返回包含 welcome 消息和当前用户名。
      前提是之前通过 /auth/login 拿到了合法的 token 并用 Bearer 方式发送。
测试 5.3：也是可以的！Token 里带的是谁的信息就代表谁的身份。这是正常的——JWT 就是用来传递身份信息的。
      （当然实际项目中应该加权限控制限制不同用户的操作范围）
测试 5.4：401 Unauthorized。签名不对，抛出 JWTError。
      这证明了签名的作用——任何篡改都会被检测出来。
测试 5.5：401 Unauthorized，token expired。
      过期的 token 等同于无效令牌。

问题 5.1：确保 WWW-Authenticate: Bearer header 始终被正确设置。
      如果在 try/except 内部 new 一个 HTTPException，headers 可能不会被正确设置。
      提外面保证每次 raise 时用的是同一个对象实例。
问题 5.2：FastAPI 的依赖注入系统自动调用！当你写 Depends(get_current_user) 时，
      FastAPI 在进接口前先执行这个函数，把返回值赋给 current_user 参数。
      你不需要自己调用它。


== LeetCode 思路 ==

LC 387：遍历字符串一次，用字典统计每个字符的频率。找到第一个计数为 1 的字符并返回其索引。
      O(n) 时间和 O(1) 空间（因为只有小写字母）。
      类比：从大量数据中找唯一的记录——数据库 UNIQUE + LIMIT 1。
"""
