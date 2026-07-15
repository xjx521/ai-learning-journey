# Day 18 笔记：上下文管理器（Context Manager）与 with 语句

## 1. 你已经用过无数次了——只是没注意

```python
# Day 11 文件操作里写过的代码：
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
# 出了 with 块，文件自动关闭，不需要写 f.close()
```

**问题：不用 with 的写法有什么坑？**

```python
# 不用 with —— 容易忘记 close
f = open("test.txt", "r", encoding="utf-8")
content = f.read()
# 如果上面 read() 抛了异常，f.close() 就不会执行 → 文件句柄泄漏
f.close()

# 手动处理异常版（啰嗦）：
f = open("test.txt", "r", encoding="utf-8")
try:
    content = f.read()
finally:
    f.close()  # 不管有没有异常，finally 都会执行
```

**结论：`with` 语句 = `try...finally` 的语法糖，自动帮你"善后"。**

---

## 2. with 语句的执行流程

```python
with EXPR as VAR:
    BLOCK
```

**执行顺序（重点）：**

```
1. 计算 EXPR，得到一个对象
2. 调用该对象的 __enter__ 方法
3. __enter__ 的返回值绑定给 VAR（如果写了 as VAR）
4. 执行 BLOCK 里的代码
5. 不管 BLOCK 正常结束还是抛异常，都会调用 __exit__ 方法
6. __exit__ 负责清理资源（关闭文件、释放锁、回滚事务等）
```

---

## 3. 上下文管理器协议：两个魔法方法

你在 Day 17 学过了，这里正式串起来：

```python
class MyContextManager:
    def __enter__(self):
        """进入上下文时调用 —— 做"准备工作"（打开资源、获取锁等）"""
        print("进入上下文")
        return self  # 返回值就是 with ... as 拿到的对象

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时调用 —— 做"清理工作"（关闭资源、释放锁等）"""
        print("退出上下文")
        # exc_type, exc_val, exc_tb 是异常的三要素，没异常时都是 None

        # 返回值决定异常是否被"吞掉"：
        #   返回 True  → 异常被压制，程序继续执行
        #   返回 False/None → 异常正常抛出
        return False
```

**__exit__ 的三个参数（异常三要素）：**

| 参数 | 类型 | 含义 | 无异常时 |
|------|------|------|----------|
| `exc_type` | 异常类 | 如 `ValueError` | `None` |
| `exc_val` | 异常实例 | 如 `ValueError("消息")` | `None` |
| `exc_tb` | traceback 对象 | 堆栈跟踪信息 | `None` |

**示例：**

```python
class MyContextManager:
    def __enter__(self):
        print("  [enter] 准备工作完成")
        return "我是enter返回的值"

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"  [exit] 捕获到异常: {exc_type.__name__}: {exc_val}")
        else:
            print("  [exit] 正常退出，没有异常")
        return False  # 不吞异常

# 正常使用：
print("=== 正常情况 ===")
with MyContextManager() as val:
    print(f"  拿到: {val}")
    print("  正常执行")
# 输出：
#   [enter] 准备工作完成
#   拿到: 我是enter返回的值
#   正常执行
#   [exit] 正常退出，没有异常

# 异常情况：
print("\n=== 有异常 ===")
try:
    with MyContextManager() as val:
        print(f"  拿到: {val}")
        raise ValueError("出错了！")
except ValueError:
    print("  异常被外面接住了")
# 输出：
#   [enter] 准备工作完成
#   拿到: 我是enter返回的值
#   [exit] 捕获到异常: ValueError: 出错了！
#   异常被外面接住了
```

---

## 4. 实战一：自己写一个文件管理器

```python
class ManagedFile:
    """模仿内置 open() + with 的行为"""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None  # 先占个位

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file  # 注意：返回的是 file 对象，不是 self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"  文件 {self.filename} 已关闭")
        return False  # 不吞异常


# 使用：
with ManagedFile("test.txt", "w") as f:
    f.write("Hello, context manager!\n")
# 退出时自动关闭文件
```

**理解要点：`with ... as` 拿到的是 `__enter__` 的返回值，不是上下文管理器对象本身。**

---

## 5. 实战二：计时器（很实用的工具）

```python
import time

class Timer:
    """测量一段代码的执行时间"""

    def __init__(self, label="耗时"):
        self.label = label
        self.elapsed = None  # 执行时间存这里，外面可以访问

    def __enter__(self):
        self.start = time.perf_counter()  # 高精度计时器，比 time.time() 更准
        return self  # 返回 self，这样外面能拿到 self.elapsed

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"  [{self.label}] {self.elapsed:.4f} 秒")
        return False


# 使用：
with Timer("计算") as t:
    total = sum(i**2 for i in range(1_000_000))
print(f"  结果: {total}")
# 输出类似：
#   [计算] 0.0523 秒
#   结果: 333332833333500000
```

---

## 6. 实战三：临时切换目录

```python
import os

class TempDir:
    """临时切换工作目录，退出时自动恢复"""

    def __init__(self, new_dir):
        self.new_dir = new_dir
        self.old_dir = None

    def __enter__(self):
        self.old_dir = os.getcwd()  # 记住当前目录
        os.chdir(self.new_dir)      # 切换过去
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_dir)      # 恢复原来的目录
        print(f"  已恢复到目录: {self.old_dir}")
        return False


# 使用：
print(f"  当前: {os.getcwd()}")
with TempDir("D:\\") as ctx:
    print(f"  临时: {os.getcwd()}")
# 出来以后自动恢复了
```

---

## 7. contextlib.contextmanager —— 用 yield 写上下文管理器（重点！）

**用类写上下文管理器有点重，Python 提供了更轻量的写法：**

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode):
    """用生成器（yield）写一个上下文管理器"""
    f = open(filename, mode, encoding="utf-8")  # 准备阶段
    try:
        yield f  # yield 的值就是 with ... as 拿到的值
    finally:
        f.close()  # 清理阶段


# 使用和内置 with open 一样：
with managed_file("test.txt", "w") as f:
    f.write("用 yield 写的上下文管理器！\n")
```

**关键记忆点：**

```
@contextmanager 装饰器的函数：
  yield 之前  = __enter__ 做的事（准备资源）
  yield 的值  = __enter__ 的返回值（as 拿到的东西）
  yield 之后 = __exit__ 做的事（清理资源）
  finally     = 保证不管有没有异常都会清理
```

**计时器的生成器版本（对比上面类的版本）：**

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label="耗时"):
    start = time.perf_counter()
    result = {"elapsed": None}  # 用字典让外面能访问
    try:
        yield result
    finally:
        result["elapsed"] = time.perf_counter() - start
        print(f"  [{label}] {result['elapsed']:.4f} 秒")

with timer("计算") as t:
    total = sum(i**2 for i in range(1_000_000))
print(f"  结果: {total}, 耗时: {t['elapsed']:.4f}s")
```

---

## 8. contextlib 其他常用工具

### 8.1 suppress —— 忽略特定异常

```python
from contextlib import suppress

# 等同于 try...except...pass
with suppress(FileNotFoundError):
    os.remove("不存在的文件.txt")  # 文件不存在也不会报错
```

### 8.2 nullcontext —— 什么都不做的上下文

```python
from contextlib import nullcontext

# 有时你需要一个"可选的"上下文管理器
use_log = True
ctx = open("log.txt", "w") if use_log else nullcontext()

with ctx as f:
    if use_log:
        f.write("记录日志")
```

---

## 9. 经典应用场景总结

| 场景 | with 帮你做什么 |
|------|----------------|
| 文件操作 `with open(...)` | 自动 close |
| 数据库连接 `with conn:` | 自动 commit / rollback + close |
| 线程锁 `with lock:` | 自动 acquire / release |
| 网络请求 `with requests.Session()` | 自动关闭连接池 |
| 临时切换 | 退出后自动恢复（目录、环境变量等） |
| 计时/性能分析 | 自动开始计时、结束时输出 |
| 事务管理 | 成功 commit，失败 rollback |

---

## 10. 一图总结

```
                    with 语句
                       │
          ┌────────────┴────────────┐
          │                         │
     用类实现                   用 @contextmanager 实现
          │                         │
    __enter__()              yield 之前的代码
    __exit__(type,val,tb)    yield 之后的代码（finally里）
          │                         │
          └────────────┬────────────┘
                       │
              共同目的：
         保证资源正确获取 + 自动清理
              不用手写 try...finally
```

---

## 11. 你需要掌握的程度

**必须会：**
- 理解 `with` = 自动 `try...finally`，知道执行顺序
- 能用 `@contextmanager + yield` 写简单的上下文管理器
- 知道 `__enter__` 返回值给 `as`，`__exit__` 负责清理

**了解即可（用到再查）：**
- `__exit__` 异常三要素的细节
- `contextlib.suppress`、`nullcontext` 等辅助工具
- 多线程锁的 with 用法（后面学到并发时自然会用）

**不需要深究：**
- `contextlib.AbstractContextManager` 基类
- 异步上下文管理器 `async with` / `__aenter__`（学到 asyncio 时再看）
- CPython 内部实现细节
