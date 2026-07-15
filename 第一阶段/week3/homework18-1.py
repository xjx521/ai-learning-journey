### Day 18：迭代器、生成器、装饰器

#### 题目 1：生成器 ⭐⭐⭐


def fibonacci(n):
    i = 0
    x, y = 0, 1

    for i in range(10):
        yield x
        x, y = y, x + y


for num in fibonacci(10):
    print(num, end=" ")
