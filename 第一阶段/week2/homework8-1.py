### Day 8：函数定义、参数、返回值

#### 题目 1：基础函数 ⭐

def greet(name):#1. `greet(name)` —— 打印 "你好，xxx！欢迎学习 Python！"
    print(f'你好，{name}!欢迎学习 Python!')

def add(a,b):#2. `add(a, b)` —— 返回两数之和
    return a+b

def is_even(n):#3. `is_even(n)` —— 返回 True（偶数）或 False（奇数）
    if n%2==0:
        return True
    else:
        return False

def max_of_three(a,b,c):#4. `max_of_three(a, b, c)` —— 返回三个数中最大的
    return max(a,b,c)

greet('xjx')
print(add(1,2))
print(is_even(3))
print(is_even(10))
print(max_of_three(1,2,3))
