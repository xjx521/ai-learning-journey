Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
from collections import namedtuple
Person=namedtuple("Person",['name','age'])#类名，[字段名]
man=Person(name='xjx',age='18')
print(man.name)
xjx
print(man.age)
18
man=Person._make(['小甲鱼',18])#将可迭代对象变为命名元组
#_make()
print(man.age)
18
print(man.name)
小甲鱼
print(man._asdict())#将命名元组返回成字典，元组字段名就是字典的键
{'name': '小甲鱼', 'age': 18}
man=man._replace(age=28)#返回一个替换好相应字段的新元组
print(man)
Person(name='小甲鱼', age=28)
#.fields命名元组所有字段的名称,fields_defaults命名元组所有字段名称及其对应默认值字典
#命名元组^

#Counter
from collections import Counter
text="In a world where technology is rapidly advancing, it is essential for individuals to stay updated and keep learning. I always look out for new learning resources that can help me hone my skills and expand my knowledge."
Counter(text).most_common(5)#单词计数
[(' ', 37), ('e', 19), ('n', 17), ('a', 17), ('l', 13)]
c=Counter("i love fishc.com")
c#计数统计（统计列表 / 字符串元素出现次数）
Counter({'i': 2, ' ': 2, 'o': 2, 'c': 2, 'l': 1, 'v': 1, 'e': 1, 'f': 1, 's': 1, 'h': 1, '.': 1, 'm': 1})
c=Counter(cat=6,dog=5)
c#返回的字典
Counter({'cat': 6, 'dog': 5})
c=Counter({'cat':3,'bird':2})
c
Counter({'cat': 3, 'bird': 2})
c['fish']
0
c=Counter([a=4,b=1,c=0,d=-2])
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
c=Counter(a=4,b=1,c=0,d=-2)
c
Counter({'a': 4, 'b': 1, 'c': 0, 'd': -2})
list.[c.elements()]#elements()返回迭代器
SyntaxError: invalid syntax
list.(c.elements())#elements()返回迭代器
SyntaxError: invalid syntax
list(c.elements())#elements()返回迭代器
['a', 'a', 'a', 'a', 'b']
c=Counter('fiiiishhhh')
c.most_common()#返回最多出现次数的列表
[('i', 4), ('h', 4), ('f', 1), ('s', 1)]
c=Counter('fiiiishhhh')
d=Counter('fffffish')
c.subtract(d)#两个计数值相减
c
Counter({'i': 3, 'h': 3, 's': 0, 'f': -4})
c=Counter()
c.update(['fisha','fishb','fishc','fishc'])#统计可迭代对象的次数
c
Counter({'fishc': 2, 'fisha': 1, 'fishb': 1})
c.update({'fishc':2,'fishb':2})#两者相加
c
Counter({'fishc': 4, 'fishb': 3, 'fisha': 1})
x=Counter(a=3,b=2,c=1)
y=Counter(a=1,b=2,c=3)
x+y
Counter({'a': 4, 'b': 4, 'c': 4})
x-y#小于/等于0抹去
Counter({'a': 2})
x&y#返回相应元素最小值
Counter({'b': 2, 'a': 1, 'c': 1})
x|y#并集：返回相应元素最大值
Counter({'a': 3, 'c': 3, 'b': 2})
x=Counter(a=3,b=-2,c=0)
+x
Counter({'a': 3})
-x
Counter({'b': 2})

#deque
d=deque('ish')
Traceback (most recent call last):
  File "<pyshell#54>", line 1, in <module>
    d=deque('ish')
NameError: name 'deque' is not defined
from collections import deque
d=deque('ish')
d.append('C')
d.appendleft('C')#双端队列左侧添加
d
deque(['C', 'i', 's', 'h', 'C'])
d.pop()
'C'
d
deque(['C', 'i', 's', 'h'])
d.popleft()
'C'
d
deque(['i', 's', 'h'])
d[0]
'i'
>>> d[-1]
'h'
>>> 'h'in d
True
>>> 'c'not in d
True
>>> d.extend('jkl')#添加多个
>>> d
deque(['i', 's', 'h', 'j', 'k', 'l'])
>>> d.extendleft('abc')#添加多个
>>> d
deque(['c', 'b', 'a', 'i', 's', 'h', 'j', 'k', 'l'])
>>> d.rotatr(1)#正数向右负数向左，参数代表旋转几个元素
Traceback (most recent call last):
  File "<pyshell#72>", line 1, in <module>
    d.rotatr(1)#正数向右负数向左，参数代表旋转几个元素
AttributeError: 'collections.deque' object has no attribute 'rotatr'. Did you mean: 'rotate'?
>>> d.rotate(1)#正数向右负数向左，参数代表旋转几个元素
>>> d
deque(['l', 'c', 'b', 'a', 'i', 's', 'h', 'j', 'k'])
>>> d.rotate(-1)#正数向右负数向左，参数代表旋转几个元素
>>> d
deque(['c', 'b', 'a', 'i', 's', 'h', 'j', 'k', 'l'])
>>> d.rotate(2)#正数向右负数向左，参数代表旋转几个元素
>>> d
deque(['k', 'l', 'c', 'b', 'a', 'i', 's', 'h', 'j'])
>>> #defaultdict
>>> from collections import defaultdict
>>> #defaultdict 带默认值字典，解决普通字典 key 不存在报错
>>> d=defaultdict(list)#默认值是空列表
>>> d['b1'].append('xjx')
>>> print(d['b2'])
[]
>>> #默认值为0
>>> d2=defaultdict(int)
>>> d2['苹果']+=1
>>> d2
defaultdict(<class 'int'>, {'苹果': 1})
