#### 题目 2：dataclass ⭐⭐⭐

from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    age: int
    score: list[float] = field(default_factory=list)

    @property  # 调用下列函数不加括号
    def average(self) -> float:
        if len(self.score) != 0:
            return sum(self.score) / len(self.score)
        else:
            return 0


s1 = Student("小明", 20, [85, 92, 78])
s2 = Student("小明", 20, [85, 92, 78])
print(s1)
print(s1 == s2)
print(s1.average)
