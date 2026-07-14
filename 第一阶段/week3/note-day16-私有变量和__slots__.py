Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
class C:
    def __init__(self,x):
        self.__x=x
    def set_x(self,x)
    
SyntaxError: expected ':'
class C:
    def __init__(self,x):
        self.__x=x
    def set_x(self,x):
        self.__x=x
    def get_x(self):
        print(self.__x)

c=C(250)
c.__x
Traceback (most recent call last):
  File "<pyshell#12>", line 1, in <module>
    c.__x
AttributeError: 'C' object has no attribute '__x'
#私有变量
c.get_x()
250
c.__dict__
{'_C__x': 250}
>>> c._C__x
250
>>> c.set_x(520)
>>> c.get_x()
520
>>> c.__y=250
>>> c.__dict__
{'_C__x': 520, '__y': 250}
>>> class D:
...     def __myfunc():
...         print('SSSS')
... 
>>> d=D()
>>> d.__myfunc()
Traceback (most recent call last):
  File "<pyshell#26>", line 1, in <module>
    d.__myfunc()
AttributeError: 'D' object has no attribute '__myfunc'. Did you mean: '_D__myfunc'?
>>> d._D__myfunc()
Traceback (most recent call last):
  File "<pyshell#27>", line 1, in <module>
    d._D__myfunc()
TypeError: D.__myfunc() takes 0 positional arguments but 1 was given
>>> d._D__myfunc()
Traceback (most recent call last):
  File "<pyshell#28>", line 1, in <module>
    d._D__myfunc()
TypeError: D.__myfunc() takes 0 positional arguments but 1 was given
>>> class D:
...     def __myfunc(self):
...         print('SSSS')
... 
>>> d._D__myfunc()
Traceback (most recent call last):
  File "<pyshell#31>", line 1, in <module>
    d._D__myfunc()
TypeError: D.__myfunc() takes 0 positional arguments but 1 was given
>>> #__slots__ 节省字典存入空间 不能额外动态添加属性
class C:
    __slots__=['x','y']
    def __init__(self,x):
        self.x=x

c=C(250)
c.x
250
c.y=520
c.y
520
c.z=66
Traceback (most recent call last):
  File "<pyshell#42>", line 1, in <module>
    c.z=66
AttributeError: 'C' object has no attribute 'z' and no __dict__ for setting new attributes
class D:
    __slots__=['x','y']
    def __init__(self,x,y,z):
        self.x=x
        self.x=y
        self.x=z#内部添加也不行

d=D(3,4,5)
class D:
    __slots__=['x','y']
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z#内部添加也不行

d=D(3,4,5)
Traceback (most recent call last):
  File "<pyshell#50>", line 1, in <module>
    d=D(3,4,5)
  File "<pyshell#49>", line 6, in __init__
    self.z=z#内部添加也不行
AttributeError: 'D' object has no attribute 'z' and no __dict__ for setting new attributes
class E(C):
    pass

e=E(230)
e.x
230
e,y=520
Traceback (most recent call last):
  File "<pyshell#56>", line 1, in <module>
    e,y=520
TypeError: cannot unpack non-iterable int object
e.y=520
e.z=6666#继承父类的slots属性不会在之类生效
e.z
6666
e.__slots__
['x', 'y']
e.__dict__
{'z': 6666}
