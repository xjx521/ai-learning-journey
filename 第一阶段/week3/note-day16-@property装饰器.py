Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
class C:
    def __init__(self,x):
        self._x=x
    def getx(self):
        return self._x
    def setx(self,value):
        self._x=value
    def delx(self):
        del self._x

c=C(250)
c.x
Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    c.x
AttributeError: 'C' object has no attribute 'x'
c.x=250
c.x
250
c.x=520
c.x
520
c.__dict__
{'_x': 250, 'x': 520}
class C:
    def __init__(self,x):
        self._x=250
    def getx(self):
        return self._x
    def setx(self,value):
        self._x=value
    def delx(self):
        del self._x
    x=property(getx,setx,delx)#把类中的方法伪装成属性，像访问字段一样调用方法；可以管控属性的「查、改、删」，实现数据校验、只读、逻辑封装。property (fget, fset, fdel, doc)

c=C()
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    c=C()
TypeError: C.__init__() missing 1 required positional argument: 'x'
class C:
    def __init__(self):
        self._x=250
    def getx(self):
        return self._x
    def setx(self,value):
        self._x=value
    def delx(self):
        del self._x
    x=property(getx,setx,delx)#把类中的方法伪装成属性，像访问字段一样调用方法；可以管控属性的「查、改、删」，实现数据校验、只读、逻辑封装。property (fget, fset, fdel, doc)
... 
>>> c=C()
>>> c.x
250
>>> c.x=520
>>> c.__dict__
{'_x': 520}
>>> del c.x
>>> c.__dict__
{}
>>> c._x=100
>>> c._x
100
>>> #装饰器
>>> class E:
...     def __init__(self):
...         self._x=250
...     @property#实现了查getx
...     def x(self):
...         return self._x
...     @x.setter#改setx
...     def x(self,value):
...         self._x=value
...     @x.deleter#删delx
...     def x(self):
...         del self._x
... 
>>> #==x=property(getx,setx,delx)
...         
>>> e=E()
>>> e.x
250
>>> e.x=520
>>> e.__dict__
{'_x': 520}
>>> del e.x
>>> e.__dict__
{}
