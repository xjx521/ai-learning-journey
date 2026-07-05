#### 题目 4：石头剪刀布 ⭐⭐⭐

import random
print("=== 石头剪刀布 ===")

user=input("请输入（石头/剪刀/布）：")
computer=random.choice(["石头","剪刀","布"])

print("你出了：",user)
print("电脑出了：",computer)

if user=="石头" and computer=="剪刀":
    print("✊ 你赢了！")
elif user=="石头" and computer=="石头":
    print("平局")
elif user=="石头" and computer=="布":
    print("很遗憾，你输了！")

elif user=="剪刀" and computer=="布":
    print("✊ 你赢了！")
elif user=="剪刀" and computer=="剪刀":
    print("平局")
elif user=="剪刀" and computer=="石头":
    print("很遗憾，你输了！")

elif user=="布" and computer=="石头":
    print("✊ 你赢了！")
elif user=="布" and computer=="布":
    print("平局")
elif user=="布" and computer=="剪刀":
    print("很遗憾，你输了！")

else:
    print("游戏错误，你输入的值不符合规范")
#可采用更简洁的判断方式（比如先算谁赢的差值，或者简化为 3 种情况：赢、输、平）
