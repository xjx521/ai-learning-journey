### Day 15：面向对象基础

#### 题目 1：定义一个类 ⭐⭐

class Student:


    def __init__(self,name,age,score=None):
        if score is None:
            score=[]
        self.name=name
        self.age=age
        self.score=score

    def add_score(self,new_score):
        self.score.append(new_score)

    def average(self):
        total=0
        for i in self.score:
            total+=i

        try:
            return total/len(self.score)
        except ZeroDivisionError:
            print('暂无成绩')
    
    def introduce(self):
        print(f'我叫{self.name},今年{self.age},平均分{self.average()}')#self.average()调用方法加()

s=Student('小明',20)
s.add_score(85)
s.add_score(92)
s.add_score(78)
s.introduce()