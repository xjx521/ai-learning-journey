Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> rhyme=(1,2,3,4,5,"fafaf")
>>> rhyme
(1, 2, 3, 4, 5, 'fafaf')
>>> rhyme=1,2,3,4,5,"fafaf"
>>> rhyme
(1, 2, 3, 4, 5, 'fafaf')
>>> rhyme[-1]
'fafaf'
>>> rhyme[0]=10
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    rhyme[0]=10
TypeError: 'tuple' object does not support item assignment
>>> rhymr[:3]
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    rhymr[:3]
NameError: name 'rhymr' is not defined. Did you mean: 'rhyme'?
>>> rhyme[:3]
(1, 2, 3)
>>> rhyme[3:]
(4, 5, 'fafaf')
>>> rhyme[:]
(1, 2, 3, 4, 5, 'fafaf')
>>> rhyme[::3]
(1, 4)
>>> rhyme[::-1]
('fafaf', 5, 4, 3, 2, 1)
>>> nums =3,1,34,5,63,3,3,3,2,1,
>>> nums.count(3)
4
>>> nums.index(34)
2
>>> s=1,2,3
>>> t=3,4,5
>>> s+t
(1, 2, 3, 3, 4, 5)
s*3
(1, 2, 3, 1, 2, 3, 1, 2, 3)
w=s,t
w
((1, 2, 3), (3, 4, 5))
for each in s:
    print(each)

1
2
3
[each for each in s]
[1, 2, 3]
s=1,2,3,4,5
[each*2 for each in s]
[2, 4, 6, 8, 10]
(each*2 for each in s)
<generator object <genexpr> at 0x000002A5B353AF60>
x=520,
type(x)
<class 'tuple'>
t=(1,"aaa",3.1)
x,y,z=t
x
1
y
'aaa'
z
3.1
t=[1,"aaa",3.1]
x,y,z=t
x
1
y
'aaa'
z
3.1
x,y,z="aaa"
x
'a'
y
'a'
z
'a'
s=[1,2,3]
t=[4,5,6\]
   
SyntaxError: unexpected character after line continuation character
t=[4,5,6]
   
w=(s,t)
   
w
   
([1, 2, 3], [4, 5, 6])
w[0][0]=0
   
w
   
([0, 2, 3], [4, 5, 6])
