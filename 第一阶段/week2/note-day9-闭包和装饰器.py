Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
#闭包：内层函数，记住并使用了外层函数里的变量，就算外层函数执行结束销毁，内层函数依旧能访问外层变量，这个内层函数 + 它绑定的环境，合起来就叫闭包。
def outer():
    # 外层变量
    num = 10
    # 内层函数
    def inner():
        # 内层使用外层的num
        print(num)
    # 把内层函数返回出去
    return inner

# 调用outer，拿到inner函数对象
f = outer()
# 此时outer函数已经运行完毕，按理说局部变量num应该被回收
# 但闭包会保留环境，依然可以打印num
f()#输出10
10
#装饰器：闭包+调用原本函数
def myfunc():
    print("正在调用myfunc...")

def report(func):
    print("主人，我要开始调用函数了...")
    func()
    print("主人，我调用完函数啦，快夸夸我^o^")

report(myfunc)
主人，我要开始调用函数了...
正在调用myfunc...
主人，我调用完函数啦，快夸夸我^o^
import time

def time_master(func):
    print("开始运行程序...")
    start = time.time()
...     func()
...     stop = time.time()
...     print("结束程序运行...")
...     print(f"一共耗费了 {(stop-start):.2f} 秒。")
...     
SyntaxError: multiple statements found while compiling a single statement
>>> import time
>>> def time_master(func):
...     print("开始运行程序...")
...     start = time.time()
...     func()
...     stop = time.time()
...     print("结束程序运行...")
...     print(f"一共耗费了 {(stop-start):.2f} 秒。")
... 
>>> def myfunc():
...     time.sleep(2)
...     print("Hello FishC.")
... 
>>> time_master(myfunc)
开始运行程序...
Hello FishC.
结束程序运行...
一共耗费了 2.05 秒。
>>> @time_master
... def myfunc():
...     time.sleep(2)
...     print("Hello FishC.")
... #语法糖标准装饰器写法
... 
开始运行程序...
Hello FishC.
结束程序运行...
一共耗费了 2.01 秒。
>>> myfunc()
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    myfunc()
TypeError: 'NoneType' object is not callable
