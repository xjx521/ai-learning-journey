from passlib.context import CryptContext

# 创建密码上下文对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===== 注册时：哈希密码 =====
plain_password = "my_secret_password"
hashed_password = pwd_context.hash(plain_password)
print(f"哈希结果：{hashed_password}")
# 输出类似：$2b$12$xK9pLmN3oQrStUvWxYzABCDEFghijklmnopqrstuv

# ===== 登录时：验证密码 =====
input_password = "my_secret_password"
if pwd_context.verify(input_password, hashed_password):
    print("✓ 密码正确，允许登录")
else:
    print("✗ 密码错误")

# 试一个错误的密码
if pwd_context.verify("wrong_password", hashed_password):
    print("密码正确")
else:
    print("✗ 密码错误")  # ← 会走到这里
