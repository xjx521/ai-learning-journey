### Day 1-2：变量与数据类型（int, float, str, bool）

#### 题目 1：自我介绍 ⭐

name=str(input("请输入你的名字："))
age=int(input("请输入你的年龄："))
tall=float(input("请输入你的身高："))
student=input("是否为在校学生（输入1表示是，0表示否）：")#bool() 不是你想象的那样工作的 😅。不管你输入"是"还是"否"，只要输入了任何内容（哪怕是一个空格），bool() 都会返回True。只有输入完全为空（直接回车），才会返回 False。
student = student == "1"  # 如果输入的是"1"，student就是True，否则是False
print(f"""我叫 {name}
今年 {age}岁
我的身高是{tall}厘米
我是在校学生：{student}""")#记得加f格式化
