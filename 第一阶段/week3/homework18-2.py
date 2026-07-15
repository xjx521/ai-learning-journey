#### 题目 2：装饰器 ⭐⭐⭐

import time


def timer(func):
    def wrapper(*args, **kwargs):
        # (*args, **kwargs) 是一个"万能转发"写法——不管被装饰的函数有没有参数、有几个参数，都能正确传递
        print(f"{func.__name__}开始执行...")  # func.__name__ 拿到函数名
        start = time.time()
        func(*args, **kwargs)  # 执行原函数（这才是核心！）
        stop = time.time()
        print(f"{func.__name__} 执行完毕，耗时 {(stop-start):.4f}秒")
        return f"返回值：{func(*args, **kwargs)}"

    return wrapper


@timer
def slow_function():
    # 模拟耗时操作
    total = sum(range(1000000))
    return total


slow_function()
