#### 题目 5：打印素数 ⭐⭐⭐

##for i in range(2,101):
##    for x in range(2,i):
##        if i%x==0:
##            break
##    else:
##            print(f"{i}是素数") # 若else在第二个循环内❌ 只要2不能整除就打印，错了

n=2
count=0

while n<=100:
    is_prime=True
    m=2
    while m<n:
        if n%m==0:
            is_prime=False
            break
        m+=1
    if is_prime:
        print(f"{n}是素数")
        count+=1
    n+=1

print(f"共{count}个素数")
