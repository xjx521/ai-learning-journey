# 🐍 Python 第一阶段学习笔记（Day 1 - Day 20）

> 📅 学习周期：2026.06.29 - 2026.07.17 | 共 20 天
> 📌 本笔记基于个人作业、报错记录整理，适合日常查阅和记忆

---

## 目录

- [Day 1-2：变量与数据类型](#day-1-2变量与数据类型)
- [Day 3：运算符、条件判断、输入输出](#day-3运算符条件判断输入输出)
- [Day 4：循环（for/while）、break/continue](#day-4循环forwhilebreakcontinue)
- [Day 5：列表、元组、字典、集合](#day-5列表元组字典集合)
- [Day 6：字符串、列表推导式](#day-6字符串列表推导式)
- [Day 7：综合复习](#day-7综合复习)
- [Day 8：函数定义、参数、返回值](#day-8函数定义参数返回值)
- [Day 9：作用域、lambda、map/filter](#day-9作用域lambdamapfilter)
- [Day 10：异常处理](#day-10异常处理)
- [Day 11：文件操作](#day-11文件操作)
- [Day 12：模块与包、pip、虚拟环境](#day-12模块与包pip虚拟环境)
- [Day 13：常用标准库](#day-13常用标准库)
- [Day 14：综合项目——命令行记账本](#day-14综合项目命令行记账本)
- [Day 15：面向对象基础](#day-15面向对象基础)
- [Day 16：继承、多态、装饰器](#day-16继承多态装饰器)
- [Day 17：魔法方法](#day-17魔法方法)
- [Day 18：迭代器、生成器、装饰器](#day-18迭代器生成器装饰器)
- [Day 19：类型注解、dataclass](#day-19类型注解dataclass)
- [Day 20：综合项目——OOP重构记账本](#day-20综合项目oop重构记账本)
- [📕 个人错题本](#-个人错题本)

---

## Day 1-2：变量与数据类型

### 🔴 必须掌握

#### 1. 变量赋值
> **核心**：变量 = 一个标签，指向内存中的某个值

```python
name = "小明"      # 字符串
age = 20           # 整数 int
height = 175.5     # 浮点数 float
is_student = True  # 布尔值 bool
nothing = None     # 空值

# 查看类型
type(name)   # <class 'str'>
type(age)    # <class 'int'>
```

💡 **速记**：Python 变量不需要声明类型，赋值即定义

#### 2. input 输入与类型转换
> **核心**：`input()` 返回的永远是字符串，需要手动转换

```python
age = int(input("年龄："))        # 字符串 → 整数
height = float(input("身高："))   # 字符串 → 浮点数
text = str(123)                   # 整数 → 字符串 "123"
```

🟡 **易错坑**：`bool()` 不是你想象的那样！
```python
# ❌ 错误用法
student = bool(input("是否学生（1/0）："))  # 输入任何东西都是 True！

# ✅ 正确用法
student = input("是否学生（1/0）：") == "1"  # 比较结果才是 bool
```

#### 3. f-string 格式化
> **核心**：`f"..."` 字符串前面必须加 `f`，花括号 `{}` 内放变量

```python
name = "小明"
age = 20
print(f"我叫{name}，今年{age}岁")  # ✅
print("我叫{name}，今年{age}岁")   # ❌ 忘加 f，原样输出
```

#### 4. 多行字符串
```python
print(f"""我叫{name}
今年{age}岁
身高{height}厘米""")
```

### 了解即可

#### 5. 变量交换
```python
# Python 特有写法（简洁）
a, b = b, a

# 传统写法
temp = a
a = b
b = temp
```

---

## Day 3：运算符、条件判断、输入输出

### 🔴 必须掌握

#### 1. 比较运算符与逻辑运算符

| 运算符            | 含义     | 示例                 |
| ----------------- | -------- | -------------------- |
| `==`              | 等于     | `a == b`             |
| `!=`              | 不等于   | `a != b`             |
| `>` `<` `>=` `<=` | 大小比较 | `a > b`              |
| `and`             | 并且     | `a > 0 and b > 0`    |
| `or`              | 或者     | `a > 0 or b > 0`     |
| `not`             | 取反     | `not True` → `False` |

💡 **速记**：Python 支持链式比较：`0 < score < 100`（其他语言不支持！）

#### 2. if/elif/else 条件判断
> **核心**：缩进决定代码块归属，冒号 `:` 不能忘

```python
score = int(input("分数："))

if 90 <= score <= 100:
    print("A")
elif 80 <= score < 90:
    print("B")
elif 70 <= score < 80:
    print("C")
elif 60 <= score < 70:
    print("D")
elif 0 <= score < 60:
    print("F")
else:
    print("请输入正确分数")  # 处理异常输入
```

🟡 **易错坑**：条件判断的顺序很重要！先判断最严格的条件

```python
# ❌ 错误：先判断宽松条件，后面的 elif 永远不会执行
if score >= 60:
    print("及格")
elif score >= 90:  # 永远不会到这里！
    print("优秀")

# ✅ 正确：从严格到宽松
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
```

#### 3. 三角形判断（经典练习）
```python
a, b, c = int(input("边1：")), int(input("边2：")), int(input("边3："))

if a + b <= c or a + c <= b or b + c <= a:
    print("不能组成三角形")
else:
    if a == b == c:
        print("等边三角形")
    elif a == b or a == c or b == c:
        print("等腰三角形")
    elif a**2 + b**2 == c**2 or a**2 + c**2 == b**2 or b**2 + c**2 == a**2:
        print("直角三角形")  # 三种情况都要检查！
    else:
        print("普通三角形")
```

---

## Day 4：循环（for/while）、break/continue

### 🔴 必须掌握

#### 1. for 循环
> **核心**：`range(start, stop, step)` 左闭右开 `[start, stop)`

```python
# 打印 1 到 100
for i in range(1, 101):   # 不包含 101
    print(i)

# 求 1+2+...+n
total = 0
for x in range(1, n + 1):
    total += x
```

#### 2. while 循环
```python
x = 1
while x <= 100:
    print(x)
    x += 1   # 别忘了更新条件，否则死循环！
```

#### 3. break 和 continue

| 关键字     | 作用                 | 类比       |
| ---------- | -------------------- | ---------- |
| `break`    | 跳出整个循环         | 直接离场   |
| `continue` | 跳过本次，继续下一次 | 跳过这一轮 |

#### 4. 九九乘法表（经典）
```python
for k in range(1, 10):          # 外层控制行数
    for j in range(1, k + 1):   # 内层控制每行打印几个
        print(f"{j}*{k}={j*k}", end="\t")
    print()                      # 换行
```

💡 **速记**：外层 `k` 从 1 到 9，内层 `j` 从 1 到 `k`（每行打印 k 个式子）

#### 5. 素数判断（for-else 语法）
> **核心**：`for-else` 的 `else` 在循环**正常结束**（没有 break）时执行

```python
for i in range(2, 101):
    for x in range(2, i):
        if i % x == 0:
            break           # 不是素数，跳出内层循环
    else:
        print(f"{i}是素数")  # 内层循环没被 break，说明是素数
```

🟡 **易错坑**：`else` 必须和**内层 for** 对齐，不能和 `if` 对齐！
```python
# ❌ 错误：else 和 if 对齐 → 只要 2 不整除就打印
for i in range(2, 101):
    for x in range(2, i):
        if i % x == 0:
            break
        else:              # ❌ 这个 else 属于 if
            print(f"{i}是素数")

# ✅ 正确：else 和 for 对齐
for i in range(2, 101):
    for x in range(2, i):
        if i % x == 0:
            break
    else:                  # ✅ 这个 else 属于 for 在外层遍历完所有i%x后才进行打印
        print(f"{i}是素数")
```

---

## Day 5：列表、元组、字典、集合

### 🔴 必须掌握

#### 1. 列表（list）
> **核心**：有序、可变、可重复，用 `[]` 创建

```python
fruits = ["苹果", "香蕉", "橘子"]

# 增
fruits.append("葡萄")         # 末尾添加
fruits.insert(1, "芒果")      # 指定位置插入

# 删
fruits.remove("香蕉")         # 按值删除（只删第一个）
fruits.pop(0)                 # 按索引删除，返回被删的值
fruits.clear()                # 清空

# 改
fruits[0] = "西瓜"            # 直接赋值

# 查
fruits[0]                     # 索引访问
fruits[1:3]                   # 切片 [start:stop:step]
fruits[-1]                    # 最后一个元素

# 常用方法
len(fruits)                   # 长度
fruits.sort()                 # 原地排序
fruits.sort(reverse=True)     # 降序
fruits.reverse()              # 反转
fruits.count("苹果")          # 计数
fruits.index("苹果")          # 找索引
"苹果" in fruits              # 判断是否存在
```

🟡 **易错坑**：空列表不能用索引赋值，必须用 `append()`
```python
# ❌ 错误
martix = []
martix[0] = 10  # IndexError: list assignment index out of range

# ✅ 正确
martix = []
martix.append(10)
```

🟡 **易错坑**：方括号 `[]` 和圆括号 `()` 别搞混
```python
rhyme = [1, 2, 3]
rhyme(0)       # ❌ TypeError: 'list' object is not callable
rhyme[0]       # ✅ 用方括号取元素
```

#### 2. 列表推导式
> **核心**：`[表达式 for 变量 in 可迭代对象 if 条件]`

```python
# 基本用法
evens = [i for i in range(21) if i % 2 == 0]        # [0, 2, 4, ..., 20]
squares = [x**2 for x in range(1, 11)]               # [1, 4, 9, ..., 100]
lower_words = [w.lower() for w in ["Hello", "WORLD"]]  # ['hello', 'world']

# 嵌套推导（矩阵展平）
matrix = [[1,2,3], [4,5,6], [7,8,9]]
flat = [col for row in matrix for col in row]  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

💡 **速记**：嵌套推导的阅读顺序 = 把 for 从上往下写成嵌套循环

```python
# 推导式                        等价于
[col for row in matrix          flat = []
       for col in row]          for row in matrix:
                                    for col in row:
                                        flat.append(col)
```

#### 3. 元组（tuple）
> **核心**：有序、**不可变**、可重复，用 `()` 创建

```python
t = (1, 2, 3)
t[0]         # 1
t[1:]        # (2, 3)
t[0] = 10    # ❌ TypeError: 'tuple' object does not support item assignment

# 单元素元组必须加逗号
x = (520,)   # ✅ tuple
x = (520)    # ❌ 只是 int，不是元组
```

💡 **速记**：元组 = 只读列表。适用于不需要修改的数据（坐标、配置等）

```python
# 元组解包
x, y, z = (1, "hello", 3.14)
```

#### 4. 字典（dict）
> **核心**：键值对存储，用 `{}` 创建，键必须唯一且不可变

```python
student = {"姓名": "小明", "年龄": 20, "成绩": 85}

# 增/改
student["性别"] = "男"          # 新增
student["年龄"] = 21            # 修改

# 删
del student["性别"]
student.pop("年龄")             # 删除并返回值
student.pop("不存在的键", "默认值")  # 键不存在时返回默认值

# 查
student["姓名"]                 # 键不存在会报错！
student.get("姓名")             # 安全访问，不存在返回 None
student.get("电话", "未填写")    # 带默认值

# 遍历
for key in student:             # 遍历键
    print(key, student[key])

for key, value in student.items():  # 遍历键值对
    print(key, value)

# 字典推导式
d = {x: ord(x) for x in "fishc"}  # {'f': 102, 'i': 105, ...}
```

🟡 **易错坑**：字典的键必须是不可变类型（字符串、数字、元组），列表和字典不能当键
```python
d = {[1,2]: "value"}           # ❌ TypeError: unhashable type: 'list'
d = {(1,2): "value"}           # ✅ 元组可以当键
```

#### 5. 集合（set）
> **核心**：无序、不重复，用于去重和集合运算

```python
s = {1, 2, 3, 3, 2}   # 自动去重 → {1, 2, 3}
s = set([1, 1, 2, 3])  # 列表去重

# 集合运算
s1 = {1, 2, 3, 4}
s2 = {3, 4, 5, 6}

s1 & s2    # 交集 {3, 4}
s1 | s2    # 并集 {1, 2, 3, 4, 5, 6}
s1 - s2    # 差集 {1, 2}（s1 有但 s2 没有的）
s1 ^ s2    # 对称差集 {1, 2, 5, 6}（两边各自独有的）
```

| 四大容器对比 | 有序？  | 可变？ | 可重复？ | 创建符号 |
| ------------ | ------- | ------ | -------- | -------- |
| list 列表    | ✅       | ✅      | ✅        | `[]`     |
| tuple 元组   | ✅       | ❌      | ✅        | `()`     |
| dict 字典    | ✅(3.7+) | ✅      | 键不重复 | `{}`     |
| set 集合     | ❌       | ✅      | ❌        | `{}`     |

---

## Day 6：字符串、列表推导式

### 🔴 必须掌握

#### 1. 字符串切片
> **核心**：`s[start:stop:step]`，左闭右开，step 为负数表示反向

```python
s = "Hello, Python World!"

s[0:5]      # "Hello"
s[-5:]      # "orld!"     最后5个字符
s[::2]      # "Hlo yhn ol!"  隔一个取
s[::-1]     # "!dlroW nohtyP ,olleH"  反转
```

💡 **速记**：`[::-1]` = 反转字符串（面试高频）

#### 2. 字符串常用方法

```python
s = "  Hello World  "

# 大小写
s.upper()          # "  HELLO WORLD  "
s.lower()          # "  hello world  "
s.title()          # "  Hello World  "
s.swapcase()       # "  hELLO wORLD  "

# 去空白
s.strip()          # "Hello World"
s.lstrip()         # "Hello World  "
s.rstrip()         # "  Hello World"

# 查找
s.find("World")    # 8（索引），找不到返回 -1
s.index("World")   # 8（索引），找不到抛异常
s.count("l")       # 3

# 替换
s.replace("World", "Python")

# 分割与拼接
"aaa,bbb,ccc".split(",")       # ['aaa', 'bbb', 'ccc']
",".join(['aaa', 'bbb', 'ccc']) # "aaa,bbb,ccc"

# 判断
"123".isdigit()     # True（是否纯数字）
"abc".isalpha()     # True（是否纯字母）
"abc123".isalnum()  # True（是否字母或数字）
"  ".isspace()      # True（是否空白）
s.startswith("He")  # True
s.endswith("ld")    # True
```

🟡 **易错坑**：`strip()` 去掉的是**字符**，不是字符串
```python
"www.91short.com".strip("w.com")   # '91short'（去掉所有 w/./c/o/m 字符）
"www.91short.com".removeprefix("www.")  # '91short.com'（去掉整个前缀字符串）
"www.91short.com".removesuffix(".com")  # 'www.91short'
```

#### 3. 字符串格式化对比

| 方式             | 语法              | 示例                     |
| ---------------- | ----------------- | ------------------------ |
| f-string（推荐） | `f"{变量}"`       | `f"年龄：{age}"`         |
| .format()        | `"{}".format(值)` | `"年龄：{}".format(age)` |
| % 格式化（旧）   | `"%s" % 值`       | `"年龄：%d" % age`       |

```python
# .format() 常用格式控制
"{:.2f}".format(3.1415)    # '3.14'    保留2位小数
"{:,}".format(1234567)     # '1,234,567' 千分位
"{:>10}".format("hi")      # '        hi' 右对齐，宽度10
"{:010}".format(-520)      # '-000000520' 零填充 |： ：后面开始写格式化规则 10 ：总宽度固定占 10 个字符位，整个结果字符串长度必须等于 10  0 ：空位用数字 0 来填充补齐（默认是空格填充） '-520'占据4个字符位 差6个 用0补齐 
"{:%}".format(0.98)        # '98.000000%' 百分比
```

---

## Day 7：综合复习

### 🟡 易错点总结

#### FizzBuzz 的判断顺序
```python
# ❌ 错误：先判断单一条件，"15" 会先匹配到 Fizz
for i in range(1, 101):
    if i % 3 == 0:         # 15 % 3 == 0 → 进了这里
        print("Fizz")
    elif i % 5 == 0:       # 永远到不了
        print("Buzz")

# ✅ 正确：先判断最严格的（同时满足的）
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:   # 先判断同时满足
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

#### 遍历字典：for 只遍历键
```python
student = {"id": "1", "name": "张三", "score": 90}

# ❌ 只打印键
for each in student:
    print(each)  # 输出: id, name, score

# ✅ 打印值
for each in student:
    print(student[each])  # 输出: 1, 张三, 90

# ✅ 更推荐
for key, value in student.items():
    print(key, value) #输出id 1
                    ## name 张三
                    ## score 90

```

---

## Day 8：函数定义、参数、返回值

### 🔴 必须掌握

#### 1. 函数定义与调用
> **核心**：`def` 定义函数，`return` 返回值，没 return 返回 None

```python
def greet(name):
    print(f"你好，{name}！")

def add(a, b):
    return a + b

result = add(3, 5)  # result = 8
```

🟡 **易错坑**：函数没有 `return` 就返回 `None`
```python
def say_hello():
    print("hello")

x = say_hello()  # 打印 "hello"
print(x)         # None！不是 "hello"
```

#### 2. 参数类型

| 参数类型       | 语法              | 示例          |
| -------------- | ----------------- | ------------- |
| 位置参数       | `def f(a, b)`     | `f(1, 2)`     |
| 关键字参数     | `def f(a, b)`     | `f(b=2, a=1)` |
| 默认参数       | `def f(a, b=10)`  | `f(1)` → b=10 |
| 可变位置参数   | `def f(*args)`    | args 是元组   |
| 可变关键字参数 | `def f(**kwargs)` | kwargs 是字典 |

```python
# 默认参数
def make_coffee(size="中杯", sugar=2, milk=True):
    print(f"{size}，加{sugar}份糖，{'加奶' if milk else '不加奶'}")

make_coffee()                   # 中杯，加2份糖，加奶
make_coffee("大杯")             # 大杯，加2份糖，加奶
make_coffee(sugar=0)            # 中杯，加0份糖，加奶
make_coffee("小杯", 1, False)   # 小杯，加1份糖，不加奶
```

💡 **速记**：位置参数必须在关键字参数之前；默认参数放在最后

#### 3. *args 和 **kwargs
```python
def sum_all(*args):         # *args 打包成元组
    return sum(args)

sum_all(1, 2, 3)            # 6

def print_info(**kwargs):   # **kwargs 打包成字典
    print(kwargs)

print_info(name="小明", age=20)  # {'name': '小明', 'age': 20}

# 解包
args = (1, 2, 3, 4)
def f(a, b, c, d):
    print(a, b, c, d)

f(*args)    # 解包元组 → 1 2 3 4
kwargs = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
f(**kwargs) # 解包字典 → 1 2 3 4
```

🟡 **易错坑**：f-string 中忘加 `{}`
```python
# ❌
print(f"第2个参数是：args[1]")   # 原样输出 "args[1]"

# ✅
print(f"第2个参数是：{args[1]}") # 输出实际值
```

---

## Day 9：作用域、lambda、map/filter

### 🔴 必须掌握

#### 1. 作用域（LEGB 规则）
> **核心**：变量查找顺序：局部(L) → 嵌套外层(E) → 全局(G) → 内置(B)

```python
x = 800          # 全局变量

def myfunc():
    x = 520      # 局部变量，覆盖全局
    print(x)     # 520

myfunc()
print(x)         # 800（全局没变）

# 用 global 修改全局变量
def myfunc():
    global x
    x = 520      # 修改的是全局 x

# 用 nonlocal 修改外层函数的变量（闭包中用）
def outer():
    x = 520
    def inner():
        nonlocal x
        x = 800
    inner()
    print(x)     # 800
```

#### 2. lambda 表达式
> **核心**：一行匿名函数，`lambda 参数: 表达式`

```python
square = lambda x: x * x
square(5)   # 25

# 常配合 sorted() / map() / filter() 使用
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
sorted(students, key=lambda x: x[1])  # 按成绩排序
# [('Charlie', 78), ('Alice', 85), ('Bob', 92)]
```

#### 3. map 和 filter
```python
# map(函数, 可迭代对象) → 对每个元素执行函数
list(map(lambda x: x * 3, [1, 2, 3]))    # [3, 6, 9]

# filter(函数, 可迭代对象) → 保留函数返回 True 的元素
list(filter(lambda x: x > 0, [1, -2, 3]))  # [1, 3]
```

---

## Day 10：异常处理

### 🔴 必须掌握

#### 1. try/except 基本结构
> **核心**：把可能出错的代码放在 `try` 里，用 `except` 捕获特定异常

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为0")
except TypeError:
    print("类型错误")
```

#### 2. 常见异常对照表

| 异常                | 触发场景                  |
| ------------------- | ------------------------- |
| `ValueError`        | 值不对（如 `int("abc")`） |
| `TypeError`         | 类型不对（如 `10 / "a"`） |
| `ZeroDivisionError` | 除以零                    |
| `IndexError`        | 索引越界                  |
| `KeyError`          | 字典键不存在              |
| `FileNotFoundError` | 文件不存在                |
| `AttributeError`    | 属性/方法不存在           |
| `NameError`         | 变量未定义                |
| `StopIteration`     | 迭代器耗尽                |

🟡 **易错坑**：异常类型要匹配！`10 / 'a'` 是 `TypeError`，不是 `ValueError`
```python
# ❌ 错误：except ValueError 接不住 TypeError
try:
    10 / 'a'
except ValueError:     # 接不住！程序崩溃
    print("类型错误")

# ✅ 正确
try:
    10 / 'a'
except TypeError:      # 正确匹配
    print("类型错误")
```

#### 3. try/except/else/finally 完整结构
```python
try:
    f = open("data.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("文件不存在")
else:
    print("读取成功")     # 没有异常时才执行
finally:
    if f:
        f.close()        # 无论有没有异常，都执行
```

#### 4. 自定义异常
```python
class AgeError(Exception):
    pass

try:
    age = int(input("年龄："))
    if age < 0 or age > 150:
        raise AgeError("年龄超出合理范围！")
except ValueError:
    print("请输入数字！")
except AgeError as e:
    print(f"错误：{e}")
else:
    print(f"你的年龄是 {age}")
```

💡 **速记**：finally 一定执行，但变量可能还没赋值 → 用 `f = None` + `if f:` 兜底

---

## Day 11：文件操作

### 🔴 必须掌握

#### 1. with 语句（推荐写法）
> **核心**：`with` 自动管理资源，退出时自动关闭文件，不用手动 close

```python
# 写文件
with open("diary.txt", "w", encoding="utf-8") as f:
    f.write("今天学了Python\n")

# 读文件
with open("diary.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 追加
with open("diary.txt", "a", encoding="utf-8") as f:
    f.write("明天继续加油！\n")
```

| 文件模式 | 含义         | 文件不存在时 |
| -------- | ------------ | ------------ |
| `"r"`    | 只读         | 报错         |
| `"w"`    | 写入（覆盖） | 创建新文件   |
| `"a"`    | 追加         | 创建新文件   |
| `"r+"`   | 读写         | 报错         |
| `"rb"`   | 二进制读     | 报错         |
| `"wb"`   | 二进制写     | 创建新文件   |

#### 2. CSV 文件操作
```python
import csv

# 写入
with open("student.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows([["姓名", "语文", "数学"], ["小明", "85", "92"]])

# 读取
with open("student.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)   # 跳过表头
    for row in reader:
        name = row[0]
        score = int(row[1])  # CSV 读出来都是字符串！
```

🟡 **易错坑**：CSV 读出来的数据都是字符串，需要手动转换类型

#### 3. JSON 文件操作
```python
import json

data = [{"name": "小明", "score": 92}]

# 写入
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

💡 **速记**：`dump/load` 操作文件，`dumps/loads` 操作字符串（多了个 s = string）

| 方法           | 操作对象 | 用途            |
| -------------- | -------- | --------------- |
| `json.dump()`  | 文件     | 写入文件        |
| `json.load()`  | 文件     | 从文件读取      |
| `json.dumps()` | 字符串   | 字典→JSON字符串 |
| `json.loads()` | 字符串   | JSON字符串→字典 |

### 了解即可

#### 4. pathlib 路径操作
```python
from pathlib import Path

p = Path(".")              # 当前目录
p.is_dir()                 # 是否目录
list(p.glob("*.py"))       # 查找所有 .py 文件
list(p.glob("**/*.py"))    # 递归查找
(p / "subdir").mkdir(parents=True, exist_ok=True)  # 创建目录
```

---

## Day 12：模块与包、pip、虚拟环境

### 🔴 必须掌握

#### 1. 模块导入
```python
import math                  # 导入整个模块
from math import sqrt        # 导入特定函数
from math import *           # 导入所有（不推荐）
import math as m             # 起别名

# 自定义模块：把函数放在 .py 文件里，import 即可
import my_math as m
m.add(3, 4)
```

#### 2. pip 安装第三方库
```bash
pip install requests         # 安装
pip install requests==2.28.0 # 指定版本
pip uninstall requests       # 卸载
pip list                     # 查看已安装
```

🟡 **易错坑**：SSL 证书过期导致 pip/requests 请求失败
```python
# 临时绕过 SSL 验证
import requests
response = requests.get("https://xxx.com", verify=False, timeout=10)
```

---

## Day 13：常用标准库

### 🔴 必须掌握

#### 1. datetime
```python
from datetime import datetime, timedelta

now = datetime.now()                          # 当前时间
now.strftime("%Y-%m-%d")                      # 格式化：'2026-07-17'
datetime.strptime("2026-01-01", "%Y-%m-%d")   # 字符串→datetime

# 时间加减
after_3_days = now + timedelta(days=3)
before_2_hours = now - timedelta(hours=2)

# 时间差
birthday = datetime(2027, 5, 22)
days_left = (birthday - now).days
```

🟡 **易错坑**：`import datetime` 和 `from datetime import datetime` 不一样！
```python
import datetime
datetime.datetime.now()     # ✅ 模块.类.方法

from datetime import datetime
datetime.now()              # ✅ 直接用类
```

#### 2. random
```python
from random import randint, choice, shuffle

randint(1, 100)             # 随机整数 [1, 100]
choice(["石头", "剪刀", "布"])  # 随机选一个
my_list = [1, 2, 3, 4, 5]
shuffle(my_list)            # 原地打乱（不返回新列表）
```

#### 3. collections
```python
from collections import Counter, defaultdict

# Counter：计数
c = Counter("abracadabra")
c.most_common(2)            # [('a', 5), ('b', 2)]

# defaultdict：键不存在时自动创建默认值
d = defaultdict(list)       # 默认值是空列表
d["数学"].append(85)        # 不会报 KeyError
```

#### 4. re 正则表达式
```python
import re

# 查找所有匹配
re.findall(r"\d+", "我25岁，有3个朋友")   # ['25', '3', '10000']

# 搜索第一个匹配
result = re.search(r"\w+@\w+\.\w+", "邮箱是 test@example.com")
result.group()    # 'test@example.com'

# 完全匹配（验证用）
re.fullmatch(r"1[3-9]\d{9}", "13812345678")  # Match 对象 or None

# 替换
re.sub(r"\d+", "***", "密码是123456")   # '密码是***'
```

| 正则符号 | 含义               |
| -------- | ------------------ |
| `\d`     | 数字 0-9           |
| `\w`     | 字母/数字/下划线   |
| `\s`     | 空白字符           |
| `.`      | 任意字符（除换行） |
| `*`      | 0 个或多个         |
| `+`      | 1 个或多个         |
| `?`      | 0 个或 1 个        |
| `{n,m}`  | n 到 m 个          |
| `^`      | 字符串开头         |
| `$`      | 字符串结尾         |
| `[abc]`  | a 或 b 或 c        |
| `( )`    | 分组捕获           |

---

## Day 14：综合项目——命令行记账本

### 项目要点
- **6 大功能**：记一笔 / 查看所有 / 按类别筛选 / 删除记录 / 统计汇总 / 退出保存
- **JSON 持久化**：启动时加载，退出时保存
- **异常处理**：所有用户输入都有 try/except 保护
- **自增 ID**：每次添加记录 ID +1

💡 **项目核心模式**：`while True` 主菜单 + `if/elif/else` 分支 + `continue` 跳过无效输入

---

## Day 15：面向对象基础

### 🔴 必须掌握

#### 1. 类与对象
> **核心**：类 = 模板/图纸，对象 = 根据模板创建的实例

```python
class Student:
    def __init__(self, name, age, score=None):
        self.name = name          # 实例属性
        self.age = age
        self.score = score if score is not None else []  # 避免可变默认值陷阱

    def add_score(self, new_score):     # 实例方法
        self.score.append(new_score)

    def average(self):
        try:
            return sum(self.score) / len(self.score)
        except ZeroDivisionError:
            return 0

    def introduce(self):
        print(f"我叫{self.name}，平均分{self.average()}")  # 调用方法要加 ()

s = Student("小明", 20)
s.add_score(85)
s.introduce()
```

🟡 **易错坑**：可变默认参数陷阱
```python
# ❌ 所有实例共享同一个列表！
def __init__(self, score=[]):
    self.score = score

# ✅ 用 None 作为默认值
def __init__(self, score=None):
    self.score = score if score is not None else []
```

#### 2. self 的含义
> **核心**：`self` 就是调用方法的那个实例对象本身

```python
class Cat:
    def __init__(self, name):
        self.name = name     # self.name 绑定到实例
    def say(self):
        print(f"{self.name}: 喵")

c = Cat("小花")
c.say()    # c.say() 中 self = c，所以 self.name = "小花"
```

#### 3. 封装（私有属性）
```python
class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self._balance = balance   # _ 开头表示私有（约定俗成）

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def get_balance(self):
        return self._balance
```

---

## Day 16：继承、多态、装饰器

### 🔴 必须掌握

#### 1. 继承与 super()
> **核心**：子类继承父类的属性和方法，用 `super()` 调用父类

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        pass

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)   # 调用父类 __init__
    def speak(self):
        print(f"{self.name}说：汪汪！")

class Cat(Animal):
    def speak(self):
        print(f"{self.name}说：喵喵！")
```

#### 2. 多态
> **核心**：同一方法，不同对象有不同行为

```python
def make_sound(animal):    # 不需要知道具体类型，只要有 speak() 方法
    animal.speak()

make_sound(Dog("旺财"))     # 汪汪！
make_sound(Cat("咪咪"))     # 喵喵！
```

#### 3. isinstance 和 issubclass
```python
isinstance(dog, Dog)      # True：dog 是 Dog 的实例
isinstance(dog, Animal)   # True：Dog 继承自 Animal
issubclass(Dog, Animal)   # True：Dog 是 Animal 的子类
```

#### 4. @property 装饰器
> **核心**：把方法伪装成属性，像访问字段一样调用方法

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance

    @property                    # 读：acc.balance（不加括号）
    def balance(self):
        return self._balance

    @balance.setter              # 写：acc.balance = 1000
    def balance(self, value):
        if value < 0:
            raise ValueError("余额不能为负")
        self._balance = value
```

### 了解即可

#### 5. @classmethod 和 @staticmethod
```python
class MyClass:
    count = 0

    @classmethod              # 类方法：第一个参数是 cls（类本身）
    def get_count(cls):
        return cls.count

    @staticmethod             # 静态方法：不需要 self 或 cls
    def helper():
        print("工具方法")
```

| 方法类型 | 装饰器        | 第一个参数 | 用途         |
| -------- | ------------- | ---------- | ------------ |
| 实例方法 | 无            | self       | 操作实例数据 |
| 类方法   | @classmethod  | cls        | 操作类属性   |
| 静态方法 | @staticmethod | 无         | 工具函数     |

#### 6. __slots__ 节省内存
```python
class Point:
    __slots__ = ['x', 'y']   # 限制只能有 x, y 属性
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 3   # ❌ AttributeError：不能动态添加属性
```

---

## Day 17：魔法方法

### 🔴 必须掌握

#### 1. __str__ 和 __repr__
> **核心**：`__str__` 给用户看，`__repr__` 给开发者看

```python
class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def __str__(self):       # print(obj) 时调用
        return f"Student({self.name}, 平均{sum(self.scores)/len(self.scores):.1f})"

    def __repr__(self):      # 在列表/字典中显示
        return f"Student(name={self.name}, scores={self.scores})"

s = Student("小明", [85, 90])
print(s)        # Student(小明, 平均87.5)
[s]             # [Student(name=小明, scores=[85, 90])]
```

💡 **速记**：`__repr__` 比 `__str__` 应用范围更广，但优先级低于 `__str__`

#### 2. __len__、__eq__、__lt__
```python
class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def __len__(self):                # len(obj) 时调用
        return len(self.scores)

    def __eq__(self, other):          # obj == other 时调用
        return sum(self.scores) == sum(other.scores)。q

    def __lt__(self, other):          # obj < other 时调用（排序用）
        return sum(self.scores) < sum(other.scores)
```

#### 3. __getitem__、__iter__、__enter__
```python
# __getitem__：让对象能 obj[i] 取值
class BookShelf:
    def __init__(self):
        self.books = ["Python入门", "FastAPI实战"]
    def __getitem__(self, i):
        return self.books[i]

shelf = BookShelf()
shelf[0]      # 'Python入门'
for b in shelf: print(b)   # 自动支持遍历

# __iter__ + __next__：让对象能 for 遍历
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current

# __enter__ / __exit__：让对象能用 with 语句
class MyFile:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.f = open(self.path, 'r')
        return self.f
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
```

| 魔法方法      | 作用               | 触发时机                |
| ------------- | ------------------ | ----------------------- |
| `__init__`    | 初始化             | `类()` 创建时           |
| `__str__`     | 用户友好的字符串   | `print(obj)`            |
| `__repr__`    | 开发者友好的字符串 | 交互式输出、列表中      |
| `__len__`     | 长度               | `len(obj)`     家450【  |
| `__eq__`      | 相等比较           | `obj1 == obj2`          |
| `__lt__`      | 小于比较           | `obj1 < obj2`（排序用） |
| `__getitem__` | 索引取值           | `obj[key]`              |
| `__iter__`    | 返回迭代器         | `for x in obj`          |
| `__next__`    | 下一个值           | 迭代器取下一个          |
| `__enter__`   | 进入 with          | `with obj as f:`        |
| `__exit__`    | 退出 with          | with 块结束时           |
| `__call__`    | 让对象可调用       | `obj()`                 |
| `__new__`     | 创建实例对象       | `类()` 时最先调用       |
| `__del__`     | 销毁实例对象       | 对象被垃圾回收时        |

---

## Day 18：迭代器、生成器、装饰器

### 🔴 必须掌握

#### 1. 闭包
> **核心**：内层函数记住了外层函数的变量，即使外层函数已执行完毕

```python
def outer():
    num = 10
    def inner():
        print(num)     # 记住了外层的 num
    return inner

f = outer()            # outer 执行完毕，num 本该回收
f()                    # 但闭包保留了 num → 输出 10
```

#### 2. 生成器（yield）
> **核心**：用 `yield` 替代 `return`，函数变成生成器，每次产出一个值并暂停

```python
def fibonacci(n):
    x, y = 0, 1
    for _ in range(n):
        yield x
        x, y = y, x + y

for num in fibonacci(10):
    print(num, end=" ")   # 0 1 1 2 3 5 8 13 21 34

# 手动调用
g = fibonacci(10)
next(g)    # 0
next(g)    # 1
next(g)    # 1
```

💡 **速记**：生成器 = 惰性列表。不会一次性占满内存，适合处理大数据

#### 3. 装饰器
> **核心**：不修改原函数，给它添加额外功能。本质是闭包

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):         # *args/**kwargs 万能转发
        print(f"{func.__name__}开始执行...")
        start = time.time()
        result = func(*args, **kwargs)     # 执行原函数（核心！）
        stop = time.time()
        print(f"耗时 {(stop-start):.4f}秒")
        return result                      # 返回原函数的返回值
    return wrapper

@timer              # 等价于 slow_function = timer(slow_function)
def slow_function():
    return sum(range(1000000))

slow_function()     # 自动打印耗时
```

🟡 **易错坑**：装饰器常见错误
```python
# ❌ 错误 1：忘调用原函数
def timer(func):
    def wrapper():
        start = time.time()
        timer()       # ❌ 调用了 timer 而不是 func
        stop = time.time()
    return wrapper

# ❌ 错误 2：忘返回原函数返回值
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)    # 执行了但没 return
        stop = time.time()
        # ❌ 没有 return result → 调用者拿到 None
    return wrapper

# ✅ 正确
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)   # 保存返回值
        stop = time.time()
        return result                    # 返回
    return wrapper
```

#### 4. 装饰器执行顺序（多层嵌套）
```python
@add        # 3. 最后执行
@cube       # 2. 中间执行
@square     # 1. 最先执行（从下往上）
def test():
    return 2

# 等价于：add(cube(square(test)))
```

---

## Day 19：类型注解、dataclass

### 🔴 必须掌握

#### 1. 类型注解
> **核心**：给函数参数和返回值标注类型，不强制但提高可读性

```python
def process(name: str, age: int, scores: list[float]) -> dict:
    return {"name": name, "age": age, "average": sum(scores)/len(scores)}

# 常用类型
x: int = 10
y: str = "hello"
z: list[int] = [1, 2, 3]
w: dict[str, int] = {"a": 1}
v: tuple[int, str] = (1, "hello")
```

💡 **速记**：类型注解只是注释，Python 不会阻止你传错类型。用 mypy 等工具可以做静态检查

#### 2. dataclass
> **核心**：自动生成 `__init__`、`__repr__`、`__eq__` 等，减少样板代码

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    age: int
    scores: list[float] = field(default_factory=list)  # 可变默认值用 field

    @property
    def average(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores else 0

s1 = Student("小明", 20, [85, 92, 78])
s2 = Student("小明", 20, [85, 92, 78])
print(s1)          # Student(name='小明', age=20, scores=[85, 92, 78])
print(s1 == s2)    # True（自动生成 __eq__）
print(s1.average)  # 85.0
```

### 了解即可

#### 3. Enum 枚举
```python
from enum import Enum

class Category(Enum):
    FOOD = "餐饮"
    TRAFFIC = "交通"
    SHOPPING = "购物"

Category.FOOD           # <Category.FOOD: '餐饮'>
Category.FOOD.value     # '餐饮'
```

---

## Day 20：综合项目——OOP重构记账本

### 项目要点
- **Record 类**：表示一条记录（id/type/category/amount/note/date + `__str__`）
- **AccountBook 类**：管理所有记录（add/delete/search/update/get_all/get_by_id/summary）
- **JSON 持久化**：`load()` 字典→Record对象，`save()` Record对象→字典
- **Category 枚举**：用 Enum 管理类别
- **命令行主菜单**：8 个功能（比 Day 14 多了按 ID 查找和更新记录）

### OOP 重构核心思路
```
Day 14（面向过程）：函数 + 全局变量 + 字典
Day 20（面向对象）：类 + 实例属性 + 方法封装

好处：
1. 数据和方法绑定，逻辑更清晰
2. 增删改查都在类里，外部只需调用方法
3. 方便扩展（比如以后加数据库支持）
```

---

## 📕 个人错题本

> 以下是你在学习过程中实际遇到的报错，按类型分类整理

### 1. 类型错误（TypeError）

| 错误代码                        | 报错                                       | 原因                                  |
| ------------------------------- | ------------------------------------------ | ------------------------------------- |
| `rhyme(0)`                      | `'list' object is not callable`            | 列表取值用 `[]` 不是 `()`             |
| `a[len(a)] = [3]`               | `list assignment index out of range`       | 空列表不能用索引赋值，要用 `append()` |
| `rhyme[0] = 10`（元组）         | `'tuple' does not support item assignment` | 元组不可变                            |
| `str='ilove'` 后再调 `str(520)` | `'str' object is not callable`             | 变量名覆盖了内置函数 str              |
| `10 / 'a'`                      | `unsupported operand type(s)`              | 除法要求数字                          |
| `hash([1])`                     | `unhashable type: 'list'`                  | 列表不可哈希，不能当字典键/集合元素   |
| `choice(dict_value)`            | `KeyError: 0`                              | choice 不支持字典                     |
| `choice(set_value)`             | `'set' object is not subscriptable`        | choice 不支持集合                     |

### 2. 逻辑错误（不报错但结果不对）

| 场景             | 错误代码                               | 问题                                      |
| ---------------- | -------------------------------------- | ----------------------------------------- |
| FizzBuzz         | 先判 `i%3==0` 再判 `i%3==0 and i%5==0` | 15 会被先判为 Fizz，永远不到 FizzBuzz     |
| 素数打印         | `else` 和 `if` 对齐                    | 只要 2 不整除就打印，应为 for-else        |
| 遍历字典         | `for each in d: print(each)`           | 只打印了键，应该 `print(d[each])`         |
| 装饰器           | `timer()` 而非 `func()`                | 调用了装饰器而非原函数                    |
| 装饰器返回值     | 忘 `return result`                     | 原函数有返回值但装饰器没返回              |
| 布尔转换         | `bool(input())`                        | 任何非空输入都是 True，应比较字符串       |
| f-string         | `print("我叫{name}")`                  | 忘加 f 前缀                               |
| 函数返回值       | 函数没 return                          | 返回 None                                 |
| 可变默认参数     | `def f(x=[])`                          | 所有实例共享同一个列表                    |
| finally 中变量   | `finally: f.close()`                   | open 前就报错时 f 未定义，应先 `f = None` |
| CSV 数据类型     | `int(row[1])`                          | CSV 读出来都是字符串，需手动转换          |
| 单元素元组       | `x = (520)`                            | 不是元组，应为 `(520,)`                   |
| 列表推导式       | `[i*2 for i in range(len(A))]`         | 用了 range(len()) 而非直接遍历 A          |
| `sorted` 参数    | `sorted(x, revese=True)`               | 拼写错误，应为 `reverse=True`             |
| `timedelta` 参数 | `timedelta(day=3)`                     | 应为 `days=3`（复数）                     |
| 字典嵌套         | 用字典当键 `{dict: value}`             | 字典不可哈希，不能当键                    |

### 7. 环境问题

| 场景       | 报错                 | 原因                                 |
| ---------- | -------------------- | ------------------------------------ |
| emoji 输出 | `UnicodeEncodeError` | GBK 控制台不支持 emoji，改用纯 ASCII |
| SSL 请求   | `SSL 证书验证失败`   | 网站证书过期，用 `verify=False`      |

---

## 📊 掌握程度速查表

| Day | 内容           | 掌握度 | 重点复习                     |
| --- | -------------- | ------ | ---------------------------- |
| 1-2 | 变量与数据类型 | ⭐⭐⭐    | bool() 陷阱、f-string        |
| 3   | 条件判断       | ⭐⭐⭐    | 判断顺序、链式比较           |
| 4   | 循环           | ⭐⭐⭐    | for-else、break 位置         |
| 5   | 四大容器       | ⭐⭐⭐    | append vs 索引赋值、字典遍历 |
| 6   | 字符串         | ⭐⭐⭐    | strip 是字符级、切片         |
| 7   | 综合复习       | ⭐⭐⭐    | FizzBuzz 顺序、字典遍历      |
| 8   | 函数           | ⭐⭐⭐    | *args/**kwargs、f-string {}  |
| 9   | 作用域/lambda  | ⭐⭐⭐    | LEGB、sorted+key             |
| 10  | 异常处理       | ⭐⭐⭐    | except 类型匹配、finally     |
| 11  | 文件操作       | ⭐⭐⭐    | with、CSV 字符串转换         |
| 12  | 模块与包       | ⭐⭐     | pip、SSL 问题                |
| 13  | 标准库         | ⭐⭐⭐    | datetime 导入、Counter       |
| 14  | 记账本项目     | ⭐⭐⭐    | JSON 持久化、异常保护        |
| 15  | OOP 基础       | ⭐⭐⭐    | self、可变默认参数           |
| 16  | 继承/多态      | ⭐⭐⭐    | super()、@property           |
| 17  | 魔法方法       | ⭐⭐⭐    | __str__ vs __repr__          |
| 18  | 生成器/装饰器  | ⭐⭐     | 装饰器返回值、yield          |
| 19  | 类型注解       | ⭐⭐     | dataclass、field             |
| 20  | OOP 重构       | ⭐⭐⭐    | 类设计、JSON↔对象            |
