Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
#多态：不同情况下作用不同
class Shaqe:
    def __init__(self,name):
        self.name=name
    def area(self):
        pass

class Square(Shape):
    def __init__(self,length):
        super().__init__('正方形')
        self.length=length
    def area(self):
        return self.length*self.length

Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    class Square(Shape):
NameError: name 'Shape' is not defined. Did you mean: 'Shaqe'?
class Square(Shaqe):
    def __init__(self,length):
        super().__init__('正方形')
        self.length=length
    def area(self):
        return self.length*self.length

class Circle(Shaqe):
    def __init__(self,radius):
        super().__init__('圆形')
        self.radius=radius
    def area(self):
        return self.radius*self.radius*3.14

class Triangle(Shaqe):
    def __init__(self,base,height):
        super().__init__('三角形')
        self.base=base
        self.height=height
    def area(self):
        return self.base*self.height/2

s=Square(5)
c=Circle(6)
t=Triangle(3,4)
s.name
'正方形'
c.name
'圆形'
t.name
'三角形'
s.area()
25
c.area()
113.04
t.area()
6.0
#自定义函数实现多态接口
class Cat:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def intro(self):
        print('我是喵')
    def say(self):
        print('喵喵喵')

    
>>> class Dog:
...     def __init__(self,name,age):
...         self.name=name
...         self.age=age
...     def intro(self):
...         print('我是狗')
...     def say(self):
...         print('汪汪汪')
... 
>>> class Pig:
...     def __init__(self,name,age):
...         self.name=name
...         self.age=age
...     def intro(self):
...         print(f'我是猪，我叫{self.name},今年{self.age}')
...     def say(self):
...         print('屁股屁股')
... 
>>> def animal(x):
...     x.intro()
...     x.say()
... 
>>> c=Cat('哈基米',4)
>>> d=Dog('旺财',5)
>>> p=Pig('大餐',1)
>>> c.animal()
Traceback (most recent call last):
  File "<pyshell#51>", line 1, in <module>
    c.animal()
AttributeError: 'Cat' object has no attribute 'animal'
>>> animal(c)
我是喵
喵喵喵
>>> animal(d)
我是狗
汪汪汪
>>> animal(p)
我是猪，我叫大餐,今年1
屁股屁股
