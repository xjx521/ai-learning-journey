#### 题目 3：九九乘法表 ⭐⭐

#for
for k in range(1,10):
    for j in range(1,k+1):
        print(f"{j}*{k}={j*k}",end="\t")
    print()

#while
n=1

while n<=9:
    m=1
    while m<=n:
        print(f"{m}*{n}={m*n}",end="\t")
        m+=1
    print()
    n+=1
