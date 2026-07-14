import time
def time_master(func):
    def call_func():
        print('开始....')
        start=time.time()
        func()
        stop=time.time()
        print('结束....')
        print(f'一共耗费了{(stop-start):.2f}秒')
    return call_func#闭包

@time_master#装饰器名 #==myfunc=time_master(myfunc)
def myfunc():
    time.sleep(2)
    print("it's myfunc")

myfunc()
