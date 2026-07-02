Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
y={"吕布":"}
   
SyntaxError: unterminated string literal (detected at line 1)
y={"吕布":"口口布","关羽":"关喜喜"}
   
y
   
{'吕布': '口口布', '关羽': '关喜喜'}
y["吕布"]
   
'口口布'
y["刘备"]="刘baby"
   
y
   
{'吕布': '口口布', '关羽': '关喜喜', '刘备': '刘baby'}
a={"吕布":"口口布","关羽":"关喜喜"}
   
b=dict(吕布="口口布",关羽="关喜喜")
   
c=dict([("吕布","口口布"),("关羽","关喜喜")])
   
d=dict({"吕布":"口口布","关羽":"关喜喜"})
   
e=dict({"吕布":"口口布"},关羽="关喜喜"})
SyntaxError: closing parenthesis '}' does not match opening parenthesis '('
e=dict({"吕布":"口口布"},关羽="关喜喜")
f=dict(zip(["吕布","关羽"],["口口布","关喜喜"]))

a==b==c==d==e==f
True
d=dict.fromkeys("FISHC",250)
d
{'F': 250, 'I': 250, 'S': 250, 'H': 250, 'C': 250}
d['c']=67
d
{'F': 250, 'I': 250, 'S': 250, 'H': 250, 'C': 250, 'c': 67}
d.pop("c")
67
d
{'F': 250, 'I': 250, 'S': 250, 'H': 250, 'C': 250}
d.pop("a")
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    d.pop("a")
KeyError: 'a'
d.pop("a","1")
'1'
d.popitem()
('C', 250)
del d["I"]
d
{'F': 250, 'S': 250, 'H': 250}
del d
d
Traceback (most recent call last):
  File "<pyshell#27>", line 1, in <module>
    d
NameError: name 'd' is not defined. Did you mean: 'id'?
d=dict.fromkeys("FISHC",250)
d
{'F': 250, 'I': 250, 'S': 250, 'H': 250, 'C': 250}
d.clear
<built-in method clear of dict object at 0x000002E2E0F7A300>
d.clear()
d
{}
d=dict.fromkeys("FISHC")
d["s"]=115
d
{'F': None, 'I': None, 'S': None, 'H': None, 'C': None, 's': 115}
d["S"]=115
D
Traceback (most recent call last):
  File "<pyshell#37>", line 1, in <module>
    D
NameError: name 'D' is not defined. Did you mean: 'd'?
d
{'F': None, 'I': None, 'S': 115, 'H': None, 'C': None, 's': 115}
d.update('F':313,"H":213)
SyntaxError: invalid syntax
d.update('F'=313,"H"=213)
SyntaxError: expression cannot contain assignment, perhaps you meant "=="?
d.update(F="313",H="13")
d
{'F': '313', 'I': None, 'S': 115, 'H': '13', 'C': None, 's': 115}
d.update({'I':11,"C":22})
d
{'F': '313', 'I': 11, 'S': 115, 'H': '13', 'C': 22, 's': 115}
d['C']
22
d.get('c','error')
'error'
d.setdefault('C','code')
22
d.setdefault('c','code')
'code'
d
{'F': '313', 'I': 11, 'S': 115, 'H': '13', 'C': 22, 's': 115, 'c': 'code'}
key=d.keys()
items=d.items()
values=d.values()
key
dict_keys(['F', 'I', 'S', 'H', 'C', 's', 'c'])
items
dict_items([('F', '313'), ('I', 11), ('S', 115), ('H', '13'), ('C', 22), ('s', 115), ('c', 'code')])
values
dict_values(['313', 11, 115, '13', 22, 115, 'code'])
d['F']=111
values
dict_values([111, 11, 115, '13', 22, 115, 'code'])
a=copy(d)
Traceback (most recent call last):
  File "<pyshell#58>", line 1, in <module>
    a=copy(d)
NameError: name 'copy' is not defined. Did you forget to import 'copy'?
a=d.copy()
a
{'F': 111, 'I': 11, 'S': 115, 'H': '13', 'C': 22, 's': 115, 'c': 'code'}
'C'ind
SyntaxError: invalid syntax
'C'in d
True
'G'in d
False
list(d)
['F', 'I', 'S', 'H', 'C', 's', 'c']
list(d.values())
[111, 11, 115, '13', 22, 115, 'code']
e=iter(d)#迭代
next(e)
'F'
next(e)
'I'
next(e)
'S'
>>> next(e)
'H'
>>> next(e)
'C'
next(e)
>>> next(e)
's'
>>> next(e)
'c'
>>> next(e)
Traceback (most recent call last):
  File "<pyshell#74>", line 1, in <module>
    next(e)
StopIteration
>>> list(d.items())
[('F', 111), ('I', 11), ('S', 115), ('H', '13'), ('C', 22), ('s', 115), ('c', 'code')]
>>> list(reversed(d.items()))
[('c', 'code'), ('s', 115), ('C', 22), ('H', '13'), ('S', 115), ('I', 11), ('F', 111)]
>>> d={"吕布":{"语文"：100,"数学":70},"关羽":{"语文"：20,"数学":10}}
SyntaxError: invalid character '：' (U+FF1A)
>>> d={"吕布":{"语文":100,"数学":70},"关羽":{"语文":20,"数学":10}}
>>> d["吕布"]["数学"]
70
>>> d={"吕布":{"语文":100,"数学":70},{"语文":20,"数学":10}:{"语文":20,"数学":10}}
Traceback (most recent call last):
  File "<pyshell#80>", line 1, in <module>
    d={"吕布":{"语文":100,"数学":70},{"语文":20,"数学":10}:{"语文":20,"数学":10}}
TypeError: unhashable type: 'dict'
>>> d={"吕布":{"语文":100,"数学":70},{"语文":20,"数学":10}:1}
Traceback (most recent call last):
  File "<pyshell#81>", line 1, in <module>
    d={"吕布":{"语文":100,"数学":70},{"语文":20,"数学":10}:1}
TypeError: unhashable type: 'dict'
>>> d={"吕布":[100,70],"关羽":[20,10]}
>>> d["关羽"][0]
20
>>> d=dict.fromkeys("FISHC",250)
>>> d["C"]=80
d
{'F': 250, 'I': 250, 'S': 250, 'H': 250, 'C': 80}
b={v:k for k,v in d.items()}
b
{250: 'H', 80: 'C'}
c={v:k for k,v in d.items() if v<100}
c
{80: 'C'}
d={x:ord(x) for x in "fishc"}
d
{'f': 102, 'i': 105, 's': 115, 'h': 104, 'c': 99}
d={x:y for x in[1,3,5] for y in [2,4,6]}
d
{1: 6, 3: 6, 5: 6}
