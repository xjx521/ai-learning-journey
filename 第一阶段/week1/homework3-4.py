#### 题目 4：三角形判断 ⭐⭐⭐

a=int(input("请输入第一条边："))
b=int(input("请输入第二条边："))
c=int(input("请输入第三条边："))

if a+b<=c or a+c<=b or b+c<=a :
    print("不能组成三角形")
else:
    print("能组成三角形！")
    if a==b==c:
        print("三角形类型：等边三角形")
    elif a==b or a==c or b==c:
        print("三角形类型：等腰三角形")
    elif pow(a,2)+pow(b,2)==pow(c,2) or pow(a,2)+pow(c,2)==pow(b,2) or pow(b,2)+pow(c,2)==pow(a,2):
        print("三角形类型：直角三角形")
    else:
        print("三角形类型：普通三角形")
