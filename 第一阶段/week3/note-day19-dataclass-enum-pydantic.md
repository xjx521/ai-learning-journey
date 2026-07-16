# Day 19 扩展笔记：dataclass、Enum、Pydantic 初识

> 本笔记面向 **AI 应用开发** 方向，基于你已学完的类型注解，把三个非常实用的工具串起来。
> 后面学 FastAPI、LangChain、配置管理时，你会反复见到它们。

---

## 1. dataclass：自动生成"样板代码"的类

### 1.1 为什么要学？

以前写一个"数据容器"类，需要写很多重复代码：

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age!r})"

    def __eq__(self, other):
        ...
```

`dataclass` 帮你自动生成 `__init__`、`__repr__`、`__eq__` 等方法。

### 1.2 最常用写法

```python
from dataclasses import dataclass

@dataclass#（order=Ture）比大小（unsafe_hash=True）哈希
class User:
    name: str
    age: int

u1 = User("Tom", 20)
print(u1)          # User(name='Tom', age=20)
print(u1 == User("Tom", 20))  # True，自动支持相等比较
```

### 1.3 默认值与默认值工厂

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str#dataclass中这些叫字段（filed）
    scores: list[int] = field(default_factory=list)  # 避免可变默认值的坑 default_factory表示不需要參數

s = Student("Jerry")
s.scores.append(90)
print(s)  # Student(name='Jerry', scores=[90])
```

> ⚠️ 不要把 `scores: list[int] = []` 当默认值，否则所有实例会共享同一个列表。

### 1.4 **post_init**：初始化后做额外处理

```python
from dataclasses import dataclass
#from typing import Classvar
@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self):#还可以用来修改类变量
        if self.price < 0:
            raise ValueError("价格不能为负数")
```

### 1.5 frozen：不可变对象

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1, 2)
# p.x = 3  # 会报错 FrozenInstanceError
```

### 1.6 AI 开发中常见的使用场景

- 封装配置：`class AppConfig:`
- 封装 LLM 返回的字段：`class ChatMessage:`
- 中间数据结构：RAG 里的 `Document`、`Chunk`

### 1.7 需要掌握到什么程度？

| 能力                                  | 要求     |
| ------------------------------------- | -------- |
| `@dataclass` 基本装饰器               | 必须熟练 |
| 默认值与 `field(default_factory=...)` | 必须熟练 |
| `frozen=True` 不可变                  | 了解     |
| `__post_init__`                       | 了解     |
| 继承 dataclass                        | 了解     |

---

## 2. Enum：让"常量"有名字、有归类

### 2.1 为什么要学？

直接用字符串表示状态容易写错：

```python
status = "running"  # 可能写成 "Runing"、"running "
```

用 `Enum` 可以把一组相关的常量统一管理。

### 2.2 基础写法

```python
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"

print(TaskStatus.PENDING)         # TaskStatus.PENDING
print(TaskStatus.PENDING.value)   # pending
print(TaskStatus("pending"))      # TaskStatus.PENDING
```

### 2.3 自动编号

```python
from enum import Enum, auto

class Priority(Enum):
    LOW = auto()
    MIDDLE = auto()
    HIGH = auto()

print(Priority.LOW.value)  # 1
```

### 2.4 使用场景

```python
def handle_status(status: TaskStatus):
    if status == TaskStatus.PENDING:
        print("任务等待中")
    elif status == TaskStatus.RUNNING:
        print("任务运行中")
    elif status == TaskStatus.DONE:
        print("任务完成")

handle_status(TaskStatus.RUNNING)
```

### 2.5 需要掌握到什么程度？

| 能力                                | 要求 |
| ----------------------------------- | ---- |
| 定义 Enum 类、取值 `.value`         | 了解 |
| 用 `auto()` 自动编号                | 了解 |
| 与类型注解结合 `status: TaskStatus` | 了解 |

> 💡 在 AI 项目里，Enum 常用于定义模型名称、任务状态、角色类型（user / assistant / system）。

---

## 3. Pydantic：数据验证与序列化的利器

### 3.1 为什么要学？

在 AI 应用开发里，你会经常遇到：

- 调用 LLM API 返回 JSON，需要解析成结构化数据
- 写 FastAPI 接口时，定义请求体、响应体
- 读取环境变量、配置文件时做类型校验

Pydantic 就是专门做这件事的："声明式地定义数据结构，自动做类型检查和转换"。

### 3.2 安装

```bash
pip install pydantic
```

### 3.3 最基础用法：BaseModel

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str | None = None  # 可选字段

# 创建实例时会自动校验类型
u = User(name="Tom", age="20")  # 字符串 "20" 会被自动转成 int
print(u)
# name='Tom' age=20 email=None
```

### 3.4 常见字段类型

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    tags: list[str] = []  # 默认空列表
    is_active: bool = True
```

### 3.5 验证失败会怎样？

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    age: int

try:
    u = User(age="not_a_number")
except ValidationError as e:
    print(e)
```

输出类似：

```
1 validation error for User
age
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not_a_number', input_type=str]
```

### 3.6 导出数据

```python
u = User(name="Tom", age=20)
print(u.model_dump())       # {'name': 'Tom', 'age': 20}
print(u.model_dump_json())  # '{"name":"Tom","age":20}'
```

> 旧版 Pydantic v1 用 `.dict()` 和 `.json()`，v2 改成了 `model_dump()` 和 `model_dump_json()`。

### 3.7 嵌套模型

```python
class Address(BaseModel):
    city: str
    zipcode: str

class Person(BaseModel):
    name: str
    address: Address  # 嵌套另一个模型

p = Person(
    name="Tom",
    address={"city": "Beijing", "zipcode": "100000"}
)
print(p.address.city)  # Beijing
```

### 3.8 与 FastAPI / AI 项目的关系

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-4"

@app.post("/chat")
def chat(req: ChatRequest):
    # req 已经被自动校验为 ChatRequest 实例
    return {"reply": f"你发送了：{req.message}"}
```

### 3.9 需要掌握到什么程度？

| 能力                                 | 要求     |
| ------------------------------------ | -------- |
| 定义 `BaseModel` 子类                | 必须熟练 |
| 基本类型注解字段 + 可选字段          | 必须熟练 |
| 创建实例、自动类型转换               | 必须熟练 |
| `model_dump()` / `model_dump_json()` | 必须熟练 |
| 嵌套模型                             | 需要掌握 |
| `ValidationError` 处理               | 需要掌握 |
| 配置类 `Settings`（环境变量读取）    | 后续再学 |

---

## 4. dataclass vs Pydantic：怎么选？

| 特性                             | dataclass      | Pydantic BaseModel          |
| -------------------------------- | -------------- | --------------------------- |
| 自动生成 `__init__` / `__repr__` | ✅              | ✅                           |
| 类型检查                         | 仅注解，不强制 | 强制校验并转换              |
| 数据验证                         | ❌ 无           | ✅ 强                        |
| JSON 序列化                      | 需自己写       | ✅ 内置                      |
| 运行性能                         | 轻量、快       | 略重，但可接受              |
| 适用场景                         | 内部数据结构   | 接口请求/响应、外部数据解析 |

> 💡 简单内部对象用 `dataclass`；需要验证、转换、序列化时用 Pydantic。

---

## 5. 小练习（建议自己敲一遍）

1. 用 `dataclass` 定义一个 `Book` 类，包含 `title`、`author`、`price`，并创建两个实例比较是否相等。
2. 定义一个 `Color(Enum)`，包含 RED、GREEN、BLUE，打印其中一种颜色。
3. 用 Pydantic 定义一个 `Student` 模型，字段：`name: str`、`age: int`、`scores: list[int]`，尝试传入合法和非法数据，观察验证行为。
4. （进阶）让 `Student` 在创建后自动计算平均分，并作为字段 `average_score` 输出。

---

## 6. 今日学习建议

- 优先级：**Pydantic > dataclass > Enum**
- 重点理解 "为什么要做数据建模 / 类型约束"
- 后面的 FastAPI、LangChain 会大量用到这些概念，现在打好基础很重要
