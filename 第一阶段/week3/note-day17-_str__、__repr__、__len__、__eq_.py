Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> #__len__
>>> class D:
...     def __init__(self,data):#len(对象) 获取长度
...         self.data=data
...     def __len__(self):
...         print('len')
...         return len(self.data)
... 
>>> d=D('fishc')
>>> bool(d)
len
True
>>> d=D('')
>>> bool(d)
len
False
>>> #比较运算符
>>> class S(str):
...     def __lt__(self,other):#小于
...         return len(self)<len(other)
...     def __gt__(self,other):#大于
...         return len(self)>len(other)
...     def __eq__(self,other):
...         return len(self)==len(other)
... 
>>> s1=S('FISHC')
>>> s2=S('fishc')
>>> s1>s2
False
>>> s1<s2
False
>>> s1==s2
True
>>> s1!=s2#类中没定义走的字符串比较
True
>>> class S(str):
...     def __lt__(self,other):#小于
...         return len(self)<len(other)
...     def __gt__(self,other):#大于
...         return len(self)>len(other)
    def __eq__(self,other):
        return len(self)==len(other)
    __le__=None#赋值为None魔法方法不生效 #<=
    __ge__=None#>=
    __ne__=None#!=

s1=S('FISHC')
s2=S('fishc')
s1!=s2
Traceback (most recent call last):
  File "<pyshell#33>", line 1, in <module>
    s1!=s2
TypeError: 'NoneType' object is not callable
#__call__
class C:
    def __call__(self,*args,**kwargs):
        print(f'位置参数：{args}\n关键字参数：{kwargs}')

c=C()
c
<__main__.C object at 0x00000228D74BECF0>
c(1,2,3,x=22542,y=4242)
位置参数：(1, 2, 3)
关键字参数：{'x': 22542, 'y': 4242}
#实现工厂
class Power:
    def __init__(self,exp):
        self.exp=exp
    def __call__(self,base):
        return base**self.exp

square=Power(2)
square(2)
4
square(5)
25
cube=Power(5)
cube=Power(3)
cube(2)
8
cube(5)
125
#__str__和__repr__
eval('1+2')#参数去引号后执行
3
class C:
    def __repr__(self):#返回程序可执行的字符串
        return 'xjx'

c=C()
repr(c)
'xjx'
str(c)#找repr代偿
'xjx'
class C:
    def __str__(self):#返回字符串
        return 'xjx'

c=C()
str(c)
'xjx'
repr(c)
'<__main__.C object at 0x00000228D74BECF0>'
#__str__只能打印列表顶层
cs=[C(),C(),C()]
for each in cs:
    print(each)

xjx
xjx
xjx
print(cs)
[<__main__.C object at 0x00000228D7487ED0>, <__main__.C object at 0x00000228D75B4190>, <__main__.C object at 0x00000228D6FDF230>]
class C:
    def __repr__(self):#返回程序可执行的字符串
        return 'xjx'

cs=[C(),C(),C()]
print(cs)
[xjx, xjx, xjx]
for each in cs:
    print(each)

xjx
xjx
xjx
class C:
    def __init__(self,data):
        self.data=data
    def __str__(self):#重构print信息 
        return f'str:{self.data}'
    def __repr__(self):#重构打印信息和对象名输出
        return f'repr:{self.data}'
    def __add__(self,other):
        return self.data+=other
    
SyntaxError: invalid syntax
class C:
    def __init__(self,data):
        self.data=data
    def __str__(self):#重构print信息 
        return f'str:{self.data}'
    def __repr__(self):#重构打印信息和对象名输出
        return f'repr:{self.data}'
    def __add__(self,other):
        return self.data += other
    
SyntaxError: invalid syntax
class C:
    def __init__(self,data):
        self.data=data
    def __str__(self):#重构print信息 
        return f'str:{self.data}'
    def __repr__(self):#重构打印信息和对象名输出
        return f'repr:{self.data}'
    def __add__(self,other):
        self.data += other

c=C(250)
print(c)
str:250
c
repr:250
c+250
print(c)
str:500
c
repr:500
#__repr__比__str__应用范围更广但是优先级低于str
