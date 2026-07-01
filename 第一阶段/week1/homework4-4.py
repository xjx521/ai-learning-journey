#### 题目 4：猜数字游戏（完整版）⭐⭐⭐

secret=42
i=7

#while
while 0<i<=7:
    guess=int(input(f"我心里想了一个 1-100 的数字，你有 {i} 次机会!"))
    if guess==secret:
        print(f"恭喜，你猜对了！用了 {7-i+1} 次！")
        break
    else:
        if guess>secret:
            print("太大了")
            i-=1
        else:
            print("太小了")
            i-=1
print("游戏结束！答案是42")
##for
##for m in range(7,0,-1):
##        a=int(input(f"我心里想了一个 1-100 的数字，你有 {m} 次机会!"))
##        if a==secret:
##            print(f"恭喜，你猜对了！用了 {7-m+1} 次！")
##            break
##        else:
##            if a>secret:
##                print("太大了")
##
##            else:
##                print("太小了")
##print("游戏结束！答案是42")      

