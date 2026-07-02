Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
{"aaa","bbb",1}
{1, 'aaa', 'bbb'}
set("fish")
{'h', 'i', 'f', 's'}
s={s for s in "fish"}
s
{'h', 'i', 'f', 's'}
'c' not in 's'
True
'c' not in s
True
'f' in s
True
for each in s:
    print(each)

h
i
f
s
set([1,1,2,3,6])
{1, 2, 3, 6}
s=[1,1,2,3,4]##去重操作
len(s)==len(set(s))
False
s.isdisjoint(set("JAVA"))#是否毫不相关
Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    s.isdisjoint(set("JAVA"))#是否毫不相关
AttributeError: 'list' object has no attribute 'isdisjoint'
s
[1, 1, 2, 3, 4]
s.isdisjoint(set("JAVA"))#是否毫不相关
Traceback (most recent call last):
  File "<pyshell#15>", line 1, in <module>
    s.isdisjoint(set("JAVA"))#是否毫不相关
AttributeError: 'list' object has no attribute 'isdisjoint'
s=set("fish")
s.issubset("fishc")
True
s.isdisjoint(set("JAVA"))#是否毫不相关
True
s,issuperset("fsh")
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    s,issuperset("fsh")
NameError: name 'issuperset' is not defined
s.issuperset("fsh")##超集
True
s.issubset("fishc.com")#子集
True
s.union({1,2,3})#并集
{1, 2, 3, 'f', 'h', 'i', 's'}
s.intersection("fsshh")#并集
{'h', 'f', 's'}
s.intersection("fsshh")#交集
{'h', 'f', 's'}
s.difference("ish")#差集
{'f'}
s.symmetric_difference("python")#对称差集
{'t', 'n', 'f', 's', 'o', 'i', 'p', 'y'}
s<=set("fishc")#检测子集和真子集
True
s>set("fishc")#检测超集
False
s|{1,2,3}|set("python")#检测并集
{1, 2, 3, 'f', 't', 'n', 'h', 's', 'o', 'i', 'p', 'y'}
s&set("php")&set('python')检测交集
SyntaxError: invalid syntax
s&set("php")&set('python')#检测交集
{'h'}
s-set('php')-set("python")#检测差集
{'i', 'f', 's'}
s^set('fisa')
{'a', 'h'}
s^set('fisa')#对称差集
{'a', 'h'}
a=set("fishc")
s
{'h', 'i', 'f', 's'}
a
{'f', 'h', 's', 'c', 'i'}
>>> a.update([1,2,3],"11")
>>> a
{1, 2, 3, 'f', 'h', 's', '1', 'c', 'i'}
>>> t=frozenset("fishc")
>>> t
frozenset({'f', 'h', 's', 'c', 'i'})
>>> a.add("45")
>>> a
{1, 2, 3, 'f', '45', 'h', 's', '1', 'c', 'i'}
>>> #删除
>>> a.discard("666")
>>> a
{1, 2, 3, 'f', '45', 'h', 's', '1', 'c', 'i'}
>>> a.remove("666")
Traceback (most recent call last):
  File "<pyshell#47>", line 1, in <module>
    a.remove("666")
KeyError: '666'
>>> a.remove(1)
>>> a
{2, 3, 'f', '45', 'h', 's', '1', 'c', 'i'}
>>> a.clear()
>>> a
set()
>>> hash(1)
1
>>> hash(1.0)
1
>>> hash([1])
Traceback (most recent call last):
  File "<pyshell#54>", line 1, in <module>
    hash([1])
TypeError: unhashable type: 'list'
>>> #嵌套集合
>>> x=frozenset(x)
Traceback (most recent call last):
  File "<pyshell#56>", line 1, in <module>
    x=frozenset(x)
NameError: name 'x' is not defined
>>> x=frozenset(1,2,3)
Traceback (most recent call last):
  File "<pyshell#57>", line 1, in <module>
    x=frozenset(1,2,3)
TypeError: frozenset expected at most 1 argument, got 3
>>> x={1,2,3}
>>> x=frozenset(x)
>>> y={x,4,5}
>>> y
{frozenset({1, 2, 3}), 4, 5}
