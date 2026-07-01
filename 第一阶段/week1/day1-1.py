"""用pyhon设计第一个游戏"""
import random
a=random.randint(1,10)
counts=3
while counts>0:
    temp=input("猜猜我心里想的数字")
    guess=int(temp)

    if guess==a:
        print("猜对了")
        print("nigger")
        break
    else:
        if guess<a:
            print("小了")
        else:
            print("大了")
    counts=counts-1
print("不玩了")
