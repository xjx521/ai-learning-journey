#### 题目 2：列表统计 ⭐⭐

print("请输入十个数字")
martix=[]
for i in range(10):
    num=int(input(f"请输入第{i+1}个数字："))
    martix.append(num)# 用 append() 添加到列表末尾，不能用 martix[i] = xxx

print("你输入的数字：",martix)
print("最大值：",max(martix))
print("最小值：",min(martix))
print("总和：",sum(martix))
print("平均值：",sum(martix)/len(martix))
