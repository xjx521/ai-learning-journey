#### 题目 5：简易登录系统 ⭐⭐

name="admin"
password="123456"

a=input("请输入用户名：")
b=input("请输入密码：")

if a == name and b == password:
    print("✅ 登录成功！欢迎回来，admin")
else:
    if a==name and b != password:
        print("密码错误")
    elif a != name and b == password:
        print("用户不存在")
    else:
        print("用户不存在及密码错误")
