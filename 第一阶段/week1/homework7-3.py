#### 题目 3：数字反转 ⭐⭐

x=int(input("请输入一个整数："))

if x<0:
    
    abs_x=abs(x)
    a=str(abs_x)
    b=a[::-1]
    c=int(b)
    print("反转后：",c*-1)
else:
 
    a=str(x)
    b=a[::-1]
    c=int(b)
    print("反转后：",c)
