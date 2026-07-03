#### 题目 2：字符串常用方法 ⭐⭐

word=input("请输入一句话：")

upper_count=0
lower_count=0
digit_count=0
space_count=0

for char in word:
    if char.isupper():
        upper_count+=1
    elif char.islower():
        lower_count+=1
    elif char.isdigit():
        digit_count+=1
    elif char.isspace():
        space_count+=1
        
print(f"大写字母：{upper_count}个")
print(f"小写字母：{lower_count}个")
print(f"数字：{digit_count}个")
print(f"空格：{space_count}个")
