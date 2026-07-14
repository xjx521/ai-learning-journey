Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
class CapStr(str):
    def __new_-(cls,string):
        
SyntaxError: expected '('
class CapStr(str):
    def __new__(cls,string):#创建实例对象的魔法方法__new__ → 生成空对象 → 传给 __init__ 的 self → 执行初始化
        string=string.upper()
        return super().__new__(cls,string)

cs=CapStr('FishC')
cs
'FISHC'
cs.lower()
'fishc'
cs.capitalize()
'Fishc'
class C:
    def __init__(self):
        print('我来了!')
    def __del__(self):#销毁实例对象 在实例对象未被引用时候触发
        print('我走了')

c=C()
我来了!
del c
我走了
c=C()
我来了!
d=c
del c
del d
我走了
#魔法方法实际上就是拦截
class S(str):
    def __add__(self,other):
        return len(self)+len(ohter)

s1=S('FishC')
s2=S('Python')
s1+s2#s1.__add__(s2)
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    s1+s2#s1.__add__(s2)
  File "<pyshell#26>", line 3, in __add__
    return len(self)+len(ohter)
NameError: name 'ohter' is not defined. Did you mean: 'other'?
class S(str):
    def __add__(self,other):
        return len(self)+len(other)

s1=S('FishC')
s2=S('Python')
s1+s2#s1.__add__(s2)
11
#__radd__()左侧对象没有__add__()方法或者__add__()返回NotImplemented,Python就会找右侧对象有无__radd__()方法
class S1(str):
    def __add__(self,other):
        return NotImplemented

class S2(str):
    def __radd__(self,other):
        return len(self)+len(other)

s1=S1('apple')
s2=S2('banana')
s1+s2
11
class S1(str):
    def __iadd__(self,other):#相当于s1+=s2
        return len(self)+len(other)

s1=S1('apple')
s1+=s2
s1
11
type(s1)#运算兼赋值
<class 'int'>
#属性访问
class C:
    def __init__(self,name,age):
        self.name=name
...         self.age=age
... 
>>> c=C('xjx',18)
>>> hasattr(c,'name')#  hasattr — 有没有这个属性
True
>>> class C:
...     def __init__(self,name,age):
...         self.name=name
...         self.__age=age
... 
>>> hasattr(c,'name')#  hasattr — 有没有这个属性
True
>>> getattr(c,'name')# getattr — 获取属性（可以设默认值）
'xjx'
>>> getattr(c,'_C__age')# getattr — 获取属性（可以设默认值）
Traceback (most recent call last):
  File "<pyshell#65>", line 1, in <module>
    getattr(c,'_C__age')# getattr — 获取属性（可以设默认值）
AttributeError: 'C' object has no attribute '_C__age'
>>>  getattr(c, 'nalance', 8000)         # 8000  ← 没有就返回默认值
...  
SyntaxError: unexpected indent
>>> getattr(c, 'nalance', 8000)         # 8000  ← 没有就返回默认值
8000
>>> c.nalance
Traceback (most recent call last):
  File "<pyshell#68>", line 1, in <module>
    c.nalance
AttributeError: 'C' object has no attribute 'nalance'
>>> dir(c)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', 'age', 'name']
>>> setattr(c,'age',19)# setattr — 动态设置属性
>>> delattr(c,'age')#删除属性
>>> getattr(c,'age')# getattr — 获取属性（可以设默认值）
Traceback (most recent call last):
  File "<pyshell#72>", line 1, in <module>
    getattr(c,'age')# getattr — 获取属性（可以设默认值）
AttributeError: 'C' object has no attribute 'age'
