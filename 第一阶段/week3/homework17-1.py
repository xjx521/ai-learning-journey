### Day 17：魔术方法

#### 题目 1：实现常用魔术方法 ⭐⭐⭐


class Student:

    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def __str__(self):
        # 打印对象时的输出
        return f"Student(名字：{self.name}，平均分：{self.average():.1f})"

    def __repr__(self):
        # 开发者友好的表示
        return f"Student(name={self.name},scores={self.scores})"

    def __len__(self):
        # 返回科目数量
        return len(self.scores)

    def average(self):
        if not self.scores:
            return 0
        else:
            return sum(self.scores) / len(self.scores)

    def __eq__(self, other):
        # 比较两个学生的平均分是否相同
        return self.average() == other.average()

    def __lt__(self, other):
        # 按平均分排序用
        return self.average() < other.average()


# 测试：
s1 = Student("小明", [85, 90, 78])
s2 = Student("小红", [92, 88, 95])
print(s1)  # __str__
print(len(s1))  # __len__
print(s1 == s2)  # __eq__
students = [s2, s1]
students.sort()  # 用 __lt__ 排序
print(students)
