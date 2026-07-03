#### 题目 3：列表推导式练习 ⭐⭐

#1. 生成 1-20 中所有偶数的列表

a=[i for i in range(21) if i%2==0]
print("1-20的偶数：",a)

#2. 生成 1-10 每个数的平方的列表

b=[pow(p,2) for p in range(11)]
print("1-10的平方：",b)

#3. 从 `words = ["hello", "WORLD", "Python"]` 生成全小写的列表

words=["hello","WORLD","Python"]
c=[k.lower() for k in words]
print("转小写：",c)

#4. 从 `nums = [1, -2, 3, -4, 5, -6]` 生成只包含正数的列表

nums=[1,-2,3,-4,5,-6]
d=[j for j in nums if j>0]
#d=[abs(j) for j in nums] 看错了应该是是否为正数而不是转换，abs是内置函数用abs(j)
print("正数：",d)
