### Day 9：作用域、lambda、map/filter

#### 题目 1：作用域理解 ⭐⭐

x=10

def foo():
    x=20#这是局部变量x
    print(f"函数内：x={x}")

foo()#函数内x=20
print(f"函数外：x={x}")#函数外x=10

x=10
def bar():
    global x#声明全局变量
    x=20#全局变量x
    print(f"函数内：x={x}")

bar()#函数内20
print(f"函数外：x={x}")#函数外20
