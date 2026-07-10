#### 题目 2：random ⭐⭐

from random import *
import string

my_list=[]
for i in range(10):
    a=randint(1,100)
    my_list.append(a)

print(my_list)

shuffle(my_list)# 直接调用，原地打乱，不赋值
print(my_list)

password=''
for x in range(3):
    words=choice(string.ascii_letters)
    digits=choice(string.digits)
    password+=words
    password+=digits



print(f'密码是：{password}')