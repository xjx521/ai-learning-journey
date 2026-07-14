Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
class C:
    def funA(self):
        print(self)
    @classmethod#类方法 用于绑定类
    def funB(cls):
        print(cls)

c=C()
c.funA()
<__main__.C object at 0x000001C44293ECF0>
c.funB()
<class '__main__.C'>
Class C:
    
SyntaxError: invalid syntax
class C:
    count=0
    def __init__(self):
        C.count+=1
    @classmethod
    def get_count(cls):
        print(f'一共实例化了{cls.count}个对象')

c1=C()
c2=C()
c3=C()
c3.get_count()
一共实例化了3个对象
c3.count=1
c3.count
1
c3.get_count()
一共实例化了3个对象
class C:
    @staticmethod
    def funC():
        print('ccc')

#@staticmethod 静态方法不需要绑定任何参数
        
c.C()
Traceback (most recent call last):
  File "<pyshell#33>", line 1, in <module>
    c.C()
AttributeError: 'C' object has no attribute 'C'
>>> c=C()
>>> c.func()
Traceback (most recent call last):
  File "<pyshell#35>", line 1, in <module>
    c.func()
AttributeError: 'C' object has no attribute 'func'. Did you mean: 'funC'?
>>> c.funC()
ccc
>>> C.funC()
ccc
>>> class C:
...     count=0
...     @classmethod
...     def add(cls):
...         cls.count+=1
...     def __init__(self):
...         self.add()
...     @classmethod
...     def get_count(cls):
...         print(f'一共实例化了{cls.count}个对象')
... 
>>> class D(C);
SyntaxError: invalid syntax
>>> class D(C):
...     count=0
... 
>>> class E(C):
...     count=0
... 
>>> c1=C()
>>> d1,d2,=D(),D()
>>> e1,e2,e3=E(),E(),E()
>>> c1.get_count()
一共实例化了1个对象
>>> d1.get_count()
一共实例化了2个对象
>>> e1.get_count()
一共实例化了3个对象
