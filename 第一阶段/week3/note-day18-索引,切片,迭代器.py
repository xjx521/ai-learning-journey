Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
class C:
    def __getitem(self,index):#让普通实例像列表、字符串一样能用下标 / 切片拿数据
        print(index)

c=C()
c[2]
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    c[2]
TypeError: 'C' object is not subscriptable
class C:
    def __getitem__(self,index):#让普通实例像列表、字符串一样能用下标 / 切片拿数据
        print(index)

c=C()
c[2]
2
c[2:8]
slice(2, 8, None)
s='i love xjx'
s[2:6]
'love'
s[slice(2,6)]
'love'
 s[::4]
 
SyntaxError: unexpected indent
s[::4]
'ivj'
s[slice(None,None,4)]
'ivj'
class D:
    def __init__(self,data):
        self.data=data
    def __getitem__(self,index): # 取值
        return self.data[index]
    def __setitem__(self,index,value): # 赋值
        self.data[index]=value
    def __delitem__(self,index): # 删除
        del self.data[index]

d=D([1,2,3,4,5])
d[1]
2
d[0:1]=[7,8]
d
<__main__.D object at 0x000001FF738BECF0>
d[:]
[7, 8, 2, 3, 4, 5]
del d[0]
d[:]
[8, 2, 3, 4, 5]
#for  循环内部原理
x=[1,2,3,4,5]
dir(x)
['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
for i in x:
    print(i,end=' ')

1 2 3 4 5 
_=iter(x)
while True:
    try:
        i=_.__next__()
    except StopIteration:
        break
    print(i,end=' ')

1 2 3 4 5 
#迭代器
class Double:
    def __init__(self,start,stop):
        self.value=start-1#从索引下标0开始
        slef.stop=stop
...     def __iter__(self):
...         return self
...     def __next__(self):
...         if self.value==self.stop
...         
SyntaxError: expected ':'
>>> class Double:
...     def __init__(self,start,stop):
...         self.value=start-1#从索引下标0开始
...         slef.stop=stop
...     def __iter__(self):#把对象变成可迭代对象，返回迭代器本身
...         return self
...     def __next__(self):#每次迭代取下一个元素；没有元素就抛出 StopIteration 终止循环
...         if self.value==self.stop:
...             raise StopIteration
...         self.value+=1#加1结束
...         return self.value*2
... 
>>> d=Double(1,5)
Traceback (most recent call last):
  File "<pyshell#63>", line 1, in <module>
    d=Double(1,5)
  File "<pyshell#62>", line 4, in __init__
    slef.stop=stop
NameError: name 'slef' is not defined
>>> class Double:
...     def __init__(self,start,stop):
...         self.value=start-1#从索引下标0开始
...         slef.stop=stop
...     def __iter__(self):#把对象变成可迭代对象，返回迭代器本身
...         return self
...     def __next__(self):#每次迭代取下一个元素；没有元素就抛出 StopIteration 终止循环
...         if self.value==self.stop:
...             raise StopIteration
...         self.value+=1#加1结束
...         return self.value*2
... 
>>> d=Double(1,5)
Traceback (most recent call last):
  File "<pyshell#66>", line 1, in <module>
    d=Double(1,5)
  File "<pyshell#65>", line 4, in __init__
    slef.stop=stop
NameError: name 'slef' is not defined
class Double:
    def __init__(self,start,stop):
        self.value=start-1#从索引下标0开始
        self.stop=stop
    def __iter__(self):#把对象变成可迭代对象，返回迭代器本身
        return self
    def __next__(self):#每次迭代取下一个元素；没有元素就抛出 StopIteration 终止循环
        if self.value==self.stop:
            raise StopIteration
        self.value+=1#加1结束
        return self.value*2

d=Double(1,5)
for i in d：
SyntaxError: invalid character '：' (U+FF1A)
for i in d:
    print(i,end=' ')

2 4 6 8 10 
