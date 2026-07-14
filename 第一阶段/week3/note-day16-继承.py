Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
class A:
    x=520
    def hello(self):
        print('hi 我是A')

class B(A):
    pass

b.B()
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    b.B()
NameError: name 'b' is not defined. Did you mean: 'B'?
b=B()
b.x
520
b.hello()#访问父类属性方法
hi 我是A
class B(A):
    x=888
    def hello(self):
        print('hi 我是B')

b=B()
b.x#覆盖
888
b.hello()
hi 我是B
b.isinstance(A)
Traceback (most recent call last):
  File "<pyshell#17>", line 1, in <module>
    b.isinstance(A)
AttributeError: 'B' object has no attribute 'isinstance'
b.isinstance(B)
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    b.isinstance(B)
AttributeError: 'B' object has no attribute 'isinstance'
isinstance(b,B)#判断对象是否属于某个类
True
isinstance(b,A)#判断对象是否属于某个类
True
issubclass(B,A)#判断类是否属于后面的类的子类
True
issubclass(A,B)#判断类是否属于后面的类的子类
False
class B(A):
    x=888
    y=250
    def hello(self):
        print('hi 我是B')

class B:
    x=888
    y=250
    def hello(self):
        print('hi 我是B')

class C(A,B)：
SyntaxError: invalid character '：' (U+FF1A)
class C(A,B):
    pass
#多类继承访问从左到右 在类中C找不到找A最后找B

c=C()
c.x
520
c.hello()
hi 我是A
c.y
250
#组合
class Turtle:
    def say(self):
        print('小甲鱼')

    
class Cat:
    def say(self):
        print('喵喵喵')

class Dog:
    def say(self):
        print('汪汪汪')

class Garden:
    t=Turtle()
    c=Cat()
    d=Dog()
    def say(self)
    
SyntaxError: expected ':'
class Garden:
    t=Turtle()
    c=Cat()
    d=Dog()
    def say(self):
        self.t.say()
        self.c.say()
        self.d.say()

g=Gaeden()#没有丛属关系用组合
Traceback (most recent call last):
  File "<pyshell#56>", line 1, in <module>
    g=Gaeden()#没有丛属关系用组合
NameError: name 'Gaeden' is not defined. Did you mean: 'Garden'?
g=Garden()#没有丛属关系用组合
g.say()
小甲鱼
喵喵喵
汪汪汪
#绑定：self 就是实例对象本身
c=C()
d=C()
d.x=250
d.x
250
c.x
520
d=A()
c=Cat()
d=Cat()
c.x=250
c.x
250
d.x
Traceback (most recent call last):
  File "<pyshell#70>", line 1, in <module>
    d.x
AttributeError: 'Cat' object has no attribute 'x'
d.x=520
d.x
520
c.__dict__#用__dict__访问私有属性
{'x': 250}
class C:
    def set_x(self,x)
    
SyntaxError: expected ':'
class C:
    def set_x(self,x):
        self.x=v

c=C()
c.__dict__
{}
>>> c.set_x(250)
Traceback (most recent call last):
  File "<pyshell#81>", line 1, in <module>
    c.set_x(250)
  File "<pyshell#78>", line 3, in set_x
    self.x=v
NameError: name 'v' is not defined
>>> class C:
...     def set_x(self,v):
...         self.x=v#self.x=v相当于c.x=v
... 
>>> c=C()
>>> c.__dict__
{}
>>> c.set_x(250)
>>> c.__dict__
{'x': 250}
>>> #想修改对象属性要用self进行绑定
>>> 
>>> #最小的类
>>> class C:
...     pass
... 
>>> c=C()#可用来当作字典使用
>>> c.x=203
>>> c.y='nb'
>>> c.z=[1,2,3]
>>> print(c,x)
Traceback (most recent call last):
  File "<pyshell#98>", line 1, in <module>
    print(c,x)
NameError: name 'x' is not defined
>>> print(c.x)
203
>>> print(c.y)
nb
>>> print(c.z)
[1, 2, 3]
