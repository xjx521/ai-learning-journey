# __getitem__ — 让对象能 obj[i] / obj[key] 取值
class BookShelf:
    def __init__(self):
        self.books = ["Python入门", "FastAPI实战", "RAG指南"]

    def __getitem__(self, i):  # shelf[i] 时自动调用
        return self.books[i]

shelf = BookShelf()
shelf[0]     # 'Python入门'
shelf[1]     # 'FastAPI实战'
shelf[-1]    # 'RAG指南'  ← 负数索引也自动支持

# 实现了 __getitem__，Python 自动让你的对象支持：
for book in shelf:  # ✅ 能遍历（代偿：用__getitem__挨个试）
    print(book)

"FastAPI" in shelf  # ✅ 能用 in（代偿：遍历挨个比）

# ─────────────────────────────────────────────

# __iter__ + __next__ — 让对象能 for x in obj 遍历
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):       # for循环开始时会调用
        return self           # 返回迭代器自己

    def __next__(self):       # 每次循环取下一个值时调用
        if self.current >= self.limit:
            raise StopIteration  # 告诉for循环"没数据了，停"
        self.current += 1
        return self.current

c = Counter(3)
for x in c:  # 1, 2, 3
    print(x)

# 工作流程：
# for x in c:
#     → 调用 c.__iter__()   拿到迭代器
#     → 反复调用 c.__next__()  取下一个值
#     → __next__ 抛 StopIteration → 循环结束

# ⚠️ 手写 __iter__ + __next__ 太麻烦，日常用 yield 生成器替代
def counter(limit):  # 用生成器，效果一样，代码少一半
    current = 0
    while current < limit:
        current += 1
        yield current

for x in counter(3):  # 1, 2, 3
    print(x)

# ─────────────────────────────────────────────

# __enter__ / __exit__ — 让对象能用 with 语句
class MyFile:
    def __init__(self, path):
        self.path = path
        self.f = None

    def __enter__(self):              # 进入 with 时调用
        self.f = open(self.path, 'r')
        return self.f                 # 返回给 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):  # 退出 with 时调用
        self.f.close()                # 无论有没有异常，都会执行
        print("文件已关闭")

# with MyFile("test.txt") as f:
#     content = f.read()
#                                     # 退出时 __exit__ 自动关闭

# 对比旧写法：
# ❌ f = open("test.txt")
# ❌ try: content = f.read()
# ❌ finally: f.close()
#
# ✅ with open("test.txt") as f:
# ✅     content = f.read()            # 自动关闭，不用操心

# ─────────────────────────────────────────────

# 总结
# ┌──────────────────────┬───────────────────┬──────────────┐
# │ 魔法方法             │ 作用              │ 你该怎么写   │
# ├──────────────────────┼───────────────────┼──────────────┤
# │ __getitem__          │ 让对象能 obj[i]   │ 封装集合时用 │
# │ __iter__ + __next__  │ 让对象能 for 遍历 │ 别手写，用yield│
# │ __enter__ / __exit__ │ 让对象能用 with   │ 资源管理时用  │
# └──────────────────────┴───────────────────┴──────────────┘
