def add(func):
    def inner():
        x=func()
        return x+1
    return inner

def cube(func):
    def inner():
        x=func()
        return x*x*x
    return inner

def square(func):
    def inner():
        x=func()
        return x*x
    return inner

@add#3
@cube#2
@square#调用顺序：语法糖从下往上调用 1
def test():
    return 2

print(test())
