Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
#作用域
def myfunc():
    x=520
    print(x)

myfunc()
520
print(x)#在函数内部定义的x是局部变量
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    print(x)#在函数内部定义的x是局部变量
NameError: name 'x' is not defined
x=800
def myfunc():
    print(x)##外部定义是全局变量

myfunc()
800
print(x)
800
def myfunc():
    x=520
    print(x)

myfunc()
520
print(x)
800
#函数内局部变量覆盖全局变量
x=800
def myfunc():
    global x#表明是全局变量
    x=520
    print(x)

myfunc()
520
print(x)
520
#函数嵌套
def fun1():
    x=520
    def fun2():#内部嵌套函数外部无法直接调用
        x=800
        print("in fun2 x=",x)
    fun2()#只能在函数内部进行调用
    print("in fun1 x=",x)

fun1()
in fun2 x= 800
in fun1 x= 520
def fun1():
    x=520
    def fun2():#内部嵌套函数外部无法直接调用
        nonlocal x#声明调用外部函数变量
        x=800
        print("in fun2 x=",x)
    fun2()#只能在函数内部进行调用
    print("in fun1 x=",x)

fun1()
in fun2 x= 800
in fun1 x= 800
str(520)
'520'
str='ilove'
str(520)
Traceback (most recent call last):
  File "<pyshell#36>", line 1, in <module>
    str(520)
TypeError: 'str' object is not callable
#LEGB L:是lobal局部作用域 E是嵌套函数外层作用域 G是全局作用域 B是最小的内置作用域 G>B str 被覆盖了 L,G冲突用global LE冲突用nonlocal
#lambda表达式
def squareX(x):
    return x*x

squareX(3)
9
#等同于
squareY=lambda y:y*y#y变量:返回值y*y
squareY(3)
9
squareY
<function <lambda> at 0x0000026104D9F560>
squareX
<function squareX at 0x0000026104D9F420>
y=[lambda x:x*x,2,3]#可嵌套进列表
y[0](y[1])#调用
4
y[0](y[2])#调用
9
mapped=map(lambda x:ord(x)+10,"fishc")#map(函数，对象)
mapped
<map object at 0x0000026104DAC7C0>
list(mapped)
[112, 115, 125, 114, 109]
list(filter(lambda x:x%2,range(10)))
[1, 3, 5, 7, 9]

#类型注释
def times(s:str,n:int) -> str：
SyntaxError: invalid character '：' (U+FF1A)
>>> def times(s:str,n:int) -> str:
...     return s*n
... 
>>> times('fishc',5)
'fishcfishcfishcfishcfishc'
>>> times(5,5)
25
>>> #只是注释不会阻止
>>> def times(s:list[int],n:int=3) -> list:#默认参数
...     return s*n
... 
>>> times([1,2,3])
[1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> def times(s:dict[str,int],n:int=3) -> list:#默认参数,字典
...     return list(s.keys())*n
... times({'a':1,'b':2,'c':3})
SyntaxError: invalid syntax
>>> def times(s:dict[str,int],n:int=3) -> list:#默认参数,字典
...     return list(s.keys())*n
... 
>>> times({'a':1,'b':2,'c':3})
['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']
>>> 
>>> times._name_
Traceback (most recent call last):
  File "<pyshell#73>", line 1, in <module>
    times._name_
AttributeError: 'function' object has no attribute '_name_'. Did you mean: '__name__'?
>>> times.__name__
'times'
>>> times.__annotations__
{'s': dict['ilove', int], 'n': <class 'int'>, 'return': <class 'list'>}
>>> import functools
>>> def add(x,y):
...     return x+y
... 
>>> functools.reduce(add,[1,2,3,4,5])
15
