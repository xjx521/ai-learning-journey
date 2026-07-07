### Day 10：异常处理

#### 题目 1：基础 try/except ⭐⭐

def safe_divide(x,y):
    try:
        return x/y
    except ZeroDivisionError:
        return "错误：除数不能为0"

    except TypeError:
        return "错误：请输入数字"

print(safe_divide(10,3))
print(safe_divide(10,0))
print(safe_divide(10,'a'))
