#### 题目 2：成绩等级 ⭐⭐


score=int(input("输入一个0-100的分数："))

if 90<=score<=100:
    print("A")
elif 80<=score<90:
    print("B")
elif 70<=score<80:
    print("C")
elif 60<=score<70:
    print("D")
elif 0<=score<60:
    print("F")
else:
    print("请输入正确的分数")
