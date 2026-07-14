### Day 16：继承、多态、装饰器

#### 题目 1：继承 ⭐⭐

class Animal:
    def __init__(self,name):
        self.name=name

    def speak(self):# 父类的 speak 不需要 name 参数，name 应该是实例属性 self.name
        pass

class Dog(Animal):
    def __init__(self,name):
        super().__init__(name)

    def speak(self):
        print(f'{self.name}说：汪汪！')

class Cat(Animal):
    def __init__(self,name):
        super().__init__(name)

    def speak(self):
        print(f'{self.name}说：喵喵！')

def make_sound(animal):  # 核心函数：接受任何对象，调用它的 speak() 方法#自定义函数实现多态接口
    animal.speak()

make_sound(Dog("旺财"))
make_sound(Cat("咪咪"))