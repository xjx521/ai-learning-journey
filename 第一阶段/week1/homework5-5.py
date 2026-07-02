#### 题目 5：集合——去重与交并集 ⭐⭐

s1=input("请输入第一组数字：")# → "1 2 3 4 5"
part1=s1.split()# → ["1", "2", "3", "4", "5"]

s2=input("请输入第二组数字：")
part2=s2.split()

# 方法A：循环
numbers=[]
for x in part1:
    numbers.append(int(x))
set1=set(numbers)

# 方法B：列表推导式
set2=set(int(y) for y in part2)

print("交集：",set1&set2)
print("并集：",set1|set2)
print("差集：",set1-set2)
