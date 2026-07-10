Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import random
print(random.random())#生成0-1的浮点数
0.7743280685194226
print(random.random())#生成0-1的浮点数
0.5355278485117797
from random import random
print(random())#生成0-1的浮点数
0.21329079994992495
from random import random，randint
SyntaxError: invalid character '，' (U+FF0C)
from random import random,randint
print(randint(1,3))#包含左右侧的值
2
from random import random,randint,randrange,choice
print(randrange(1,10,2))#randrange(start,stop,step)不包含右侧值
1
>>> print(randrange(1,10,2))#randrange(start,stop,step)不包含右侧值
7
>>> #choice
>>> string='hello world'
>>> tuple_value=(1,2,3,4,5)
>>> list_value=[1,2,3,4,5]
>>> dict_value={'name':'xjx','age':18}
>>> set_value={1,2,3,4,5}
>>> print(choice(string))#从字符串，列表，元组中随机选择一个元素
r
>>> print(choice(tuple_value))#从字符串，列表，元组中随机选择一个元素
1
>>> print(choice(list_value))#从字符串，列表，元组中随机选择一个元素
4
>>> print(choice(list_value))#从字符串，列表，元组中随机选择一个元素
3
>>> print(choice(dict_value))#从字符串，列表，元组中随机选择一个元素
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    print(choice(dict_value))#从字符串，列表，元组中随机选择一个元素
  File "C:\Users\xjxx\AppData\Local\Python\pythoncore-3.13-64\Lib\random.py", line 352, in choice
    return seq[self._randbelow(len(seq))]
KeyError: 0
>>> print(choice(set_value))#从字符串，列表，元组中随机选择一个元素
Traceback (most recent call last):
  File "<pyshell#22>", line 1, in <module>
    print(choice(set_value))#从字符串，列表，元组中随机选择一个元素
  File "C:\Users\xjxx\AppData\Local\Python\pythoncore-3.13-64\Lib\random.py", line 352, in choice
    return seq[self._randbelow(len(seq))]
TypeError: 'set' object is not subscriptable
>>> 
>>> from random import random,randint,randrange,choice,shuffle
>>> list_value=[1,2,3,4,5]#shuffle只能是list ,str和tuple不可变，set和dict是无序的
>>> shuffle(list_value)
>>> print(list_value)
[5, 1, 4, 2, 3]
