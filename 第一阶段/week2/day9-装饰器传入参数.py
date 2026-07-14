import time

def logger(msg):
    def time_master(func):
        def call_func():
            start=time.time()
            func()
            stop=time.time()
            print(f'[{msg}]一共耗费了{(stop-start):.2f}')
        return call_func#传函数time_master
    return time_master#传参数

@logger(msg='A')#== funA = logger(msg='A')(funA)
def funA():
    time.sleep(1)
    print('在调用funA ')

@logger(msg='B')
def funB():
    time.sleep(1)
    print('在调用funB ')

funA()
funB()
