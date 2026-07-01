#### 题目 3：BMI 计算器 ⭐⭐

tall=float(input("请输入身高："))
fat=float(input("请输入体重："))

BMI=fat/(tall**2)
print(f"你的BMI是：{BMI}")
if 0<BMI < 18.5:
    print("偏瘦")
elif 18.5 <= BMI < 24:
    print("正常")
elif 24 <= BMI < 28:
    print("偏胖")
elif BMI >= 28:
    print("肥胖")
else:
    print("请输入正确数值")
