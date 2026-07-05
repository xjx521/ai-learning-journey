Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
def myfunc():
    for i in range(3):
        print("hello world!")

myfunc()
hello world!
hello world!
hello world!
myfunc(6)
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    myfunc(6)
TypeError: myfunc() takes 0 positional arguments but 1 was given
def myfunc(name)#指定参数
    for i in range(3):
        print(f"hello {name}!")
        
SyntaxError: expected ':'
def myfunc(name):  #指定参数
    for i in range(3):
        print(f"hello {name}!")

myfunc(xjx)
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    myfunc(xjx)
NameError: name 'xjx' is not defined
myfunc('xjx')
hello xjx!
hello xjx!
hello xjx!
def myfunc(name,times):  #指定参数,多个参数，指定次数
    for i in range(times):
        print(f"hello {name}!")

myfunc('xjx',6)
hello xjx!
hello xjx!
hello xjx!
hello xjx!
hello xjx!
hello xjx!
def div(x,y):#形参
    if y==0:
        return "除数不能为0" #强制执行返回后面的代码不会执行
    else:
        return x/y

div(4,2)#4，2是实际参数
2.0
div(4,0)
'除数不能为0'
def myfunc():
    pass

print(myfunc())
None
#默认返回None
#位置参数
def myfunc(s,vt,o):
    return "".join((o,vt,s))

myfunc("我","打了","小甲鱼")
'小甲鱼打了我'
myfunc("Python","爱",o="我")#关键字参数，位置参数必须在关键字参数之前
'我爱Python'
#默认参数
def myfunc(s,vt,o="python"): #不传第三个参数默认是python
    return "".join((o,vt,s))

myfunc("我","爱")
'python爱我'
myfunc("我","爱","world")
'world爱我'
#默认参数应该放在位置参数之后
sum([1,2,3],start=4)
10
def abc(a,/,b,c):
    print(a,b,c)

abc(1,2,3)
1 2 3
abc(a=1,2,3)#默认左边是位置参数
SyntaxError: positional argument follows keyword argument
def abc(a,*,b,c):#*可以使左侧为任意参数，但是右侧必须为关键字参数
    print(a,b,c)

abc(a=1,b=2,c=3)
1 2 3
#位置可变参数*args
def myfunc(*args):
    print("有{}个参数。".format(len(args)))
    print(f"第2个参数是：args[1]")#函数以元组形式打包
    print(type(args))

myfunc("我",1,2)
有3个参数。
第2个参数是：args[1]
<class 'tuple'>
def myfunc(*args):
    print("有{}个参数。".format(len(args)))
    print(f"第2个参数是：{args[1]}")#函数以元组形式打包
    print(type(args))

myfunc("我",1,2)
有3个参数。
第2个参数是：1
<class 'tuple'>
myfunc("我",1,2，4)#收集参数
SyntaxError: invalid character '，' (U+FF0C)
myfunc("我",1,2,4)#收集参数
有4个参数。
第2个参数是：1
<class 'tuple'>
def func(*args,a,b):
    print(*args,a,b)

myfunc(1,2,3,4,5)
有5个参数。
第2个参数是：2
<class 'tuple'>
func(1,2,3,4,5)
Traceback (most recent call last):
  File "<pyshell#66>", line 1, in <module>
    func(1,2,3,4,5)
TypeError: func() missing 2 required keyword-only arguments: 'a' and 'b'
>>> func(1,2,3,4,5,a=6,b=7)#收集参数后要用关键字参数传递
1 2 3 4 5 6 7
>>> #**关键字可变参数
>>> def myfunc(**kwargs):
...     print(kwargs)#**是将参数打包成字典形式
... 
>>> myfunc(a=1,b=2,c=3)
{'a': 1, 'b': 2, 'c': 3}
>>> def myfunc(a,*b,**c):
...     print(a,b,c)#*b将多个参数打包成元组
... 
>>> myfunc(1,2,3,4,5,x=6,y=7)
1 (2, 3, 4, 5) {'x': 6, 'y': 7}
>>> #解包参数：形参加*打包，实参加*解包
>>> def myfunc(a,b,c,d)
SyntaxError: expected ':'
>>> def myfunc(a,b,c,d):
...     print(a,b,c,d)
... 
>>> args=(1,2,3,4)
>>> myfunc(args)
Traceback (most recent call last):
  File "<pyshell#82>", line 1, in <module>
    myfunc(args)
TypeError: myfunc() missing 3 required positional arguments: 'b', 'c', and 'd'
>>> myfunc(*args)#*解包元组
1 2 3 4
>>> kwargs={'a':1,'b':2,'c':3,'d':4}
>>> myfunc(**kwargs)#**解包字典
1 2 3 4
