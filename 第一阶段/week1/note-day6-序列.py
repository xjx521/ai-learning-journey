Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
[1,2,3]+[4,5,6]
[1, 2, 3, 4, 5, 6]
(1,2,3)+(4,5,6)
(1, 2, 3, 4, 5, 6)
"123"+"456"
'123456'
[1,2,3]*3
[1, 2, 3, 1, 2, 3, 1, 2, 3]
(1,2,3)*3
(1, 2, 3, 1, 2, 3, 1, 2, 3)
"123"*3
'123123123'
S=[1,2,3]
id(S)
2585470064192
S=S*3
id(S)
2585470210944
S=[1,2,3]
id(S)
2585470064192
S*=3
id(S)
2585470064192
t=(1,2,3)
id(t)
2585470211072
t*=3
id(t)
2585468806960
del s,t
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    del s,t
NameError: name 's' is not defined. Did you mean: 'S'?
del S,t
S
Traceback (most recent call last):
  File "<pyshell#20>", line 1, in <module>
    S
NameError: name 'S' is not defined
t
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    t
NameError: name 't' is not defined
x=[1,2,3,4,5]
del x[1:4]
x
[1, 5]
x=[1,2,3,4,5]
x[1:4]=[]
x
[1, 5]
list("fishc")
['f', 'i', 's', 'h', 'c']
tuple("fishc")
('f', 'i', 's', 'h', 'c')
str([1,2,3])
'[1, 2, 3]'
str((1,2,3))
'(1, 2, 3)'
x=[1,2,3,4,5]
min(x,default="error")
1
del x
min(x,default="error")
Traceback (most recent call last):
  File "<pyshell#35>", line 1, in <module>
    min(x,default="error")
NameError: name 'x' is not defined
x=[1,2,3,4,5]
del x[:]
min(x,default="error")
'error'
max(1,5,2,5,6,7)
7
x=[1,2,3,4,5]
sum(x,start=100)#从一百开始加
115
x=[1,2,3,0,6]
sorted(x)
[0, 1, 2, 3, 6]
 x
 
SyntaxError: unexpected indent
x
[1, 2, 3, 0, 6]
x.sorted()
Traceback (most recent call last):
  File "<pyshell#46>", line 1, in <module>
    x.sorted()
AttributeError: 'list' object has no attribute 'sorted'. Did you mean: 'sort'?
x.sort()
x
[0, 1, 2, 3, 6]
sorted(x,revese=True)
Traceback (most recent call last):
  File "<pyshell#49>", line 1, in <module>
    sorted(x,revese=True)
TypeError: sort() got an unexpected keyword argument 'revese'. Did you mean 'reverse'?
sorted(x,reverse=True)
[6, 3, 2, 1, 0]
sorted(t,key=len)
Traceback (most recent call last):
  File "<pyshell#51>", line 1, in <module>
    sorted(t,key=len)
NameError: name 't' is not defined
t=["apple","FISH",'Banana',"book",'pen']
sorted(t)
['Banana', 'FISH', 'apple', 'book', 'pen']
sorted(t,key=len)#比较字符长度
['pen', 'FISH', 'book', 'apple', 'Banana']
X=[1,1,0]
Y=[1,1,9]
all(x)
False
any(x)#某个元素
True
all(y)
Traceback (most recent call last):
  File "<pyshell#59>", line 1, in <module>
    all(y)
NameError: name 'y' is not defined. Did you mean: 'Y'?
all(Y)
True
list(enumerate(x))
[(0, 0), (1, 1), (2, 2), (3, 3), (4, 6)]
x
[0, 1, 2, 3, 6]
X
[1, 1, 0]
a=zip(X,Y)
a
<zip object at 0x00000259FA097E80>
a=zip(X,Y)
a
<zip object at 0x00000259FA094240>
list(a)
[(1, 1), (1, 1), (0, 9)]
z="fishc"
a=zip(X,Y,z)
list(a)
[(1, 1, 'f'), (1, 1, 'i'), (0, 9, 's')]
import itertools
a=itertools.zip_longest(X,Y,z)
list(a)
[(1, 1, 'f'), (1, 1, 'i'), (0, 9, 's'), (None, None, 'h'), (None, None, 'c')]
>>> mapped=map(ord,"FishC")
>>> list(mapped)
[70, 105, 115, 104, 67]
>>> mapped=map(pow,[2,4,10],[5,2,4])#前面是计算方法，后面计算对象
>>> list(mapped)
[32, 16, 10000]
>>> list(filter(str.islower,"fishc"))#与map类似，只传真值
['f', 'i', 's', 'h', 'c']
>>> list(filter(str.islower,"fISHc"))#与map类似，只传真值
['f', 'c']
>>> x=[1,2,3,4,5]
>>> y=iter(x)#把可迭代对象变成迭代器
>>> type(y)
<class 'list_iterator'>
>>> next(y)
1
>>> next(y)
2
>>> next(y)
3
>>> next(y)
4
>>> next(y)
5
>>> c=iter(x)
>>> next(c,"没了")
1
>>> next(c,"没了")
2
>>> next(c,"没了")
3
>>> next(c,"没了")
4
>>> next(c,"没了")
5
>>> next(c,"没了")
'没了'
>>> next(c,"没了")
'没了'
