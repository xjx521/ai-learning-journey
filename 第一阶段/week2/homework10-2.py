#### 题目 2：多个 except ⭐⭐

class AgeError(Exception):
        pass
try:
    age=int(input("请输入你的年龄："))

    if age<0 or age>150:# 2. 自己检查范围，不合法就主动 raise 自定义异常
        raise AgeError("年龄超出合理范围！")
except ValueError:
    print("❌ 错误：请输入有效的数字！")
except AgeError as e:
    print("❌ 错误：请输入有效的年龄！")
else:
    print(f"✅ 你的年龄是 {age} 岁")
