Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
[1,2,3,4,5,"faf",True,1.1]
[1, 2, 3, 4, 5, 'faf', True, 1.1]
rhyme=[1,2,3,4,5,"faf",True,1.1]
print(rhyme)
[1, 2, 3, 4, 5, 'faf', True, 1.1]
for each in rhyme:
    print(each)

1
2
3
4
5
faf
True
1.1
rhyme[0]
1
rhyme[7]
1.1
rhyme[-1]
1.1
length =len(rhyme)
rhyme(length-1)
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    rhyme(length-1)
TypeError: 'list' object is not callable
rhyme[length-1]
1.1
rhyme[-3]
'faf'
rhyme[:3]
[1, 2, 3]
rhyme[1:3]
[2, 3]
rhyme[:]
[1, 2, 3, 4, 5, 'faf', True, 1.1]
rhyme[3:]
[4, 5, 'faf', True, 1.1]
rhyme[:4]
[1, 2, 3, 4]
rhyme[:4:2]
[1, 3]
rhyme[::-2]
[1.1, 'faf', 4, 2]
rhyme[::-1]
[1.1, True, 'faf', 5, 4, 3, 2, 1]
a=["b","c"]
a.append("d")
a
['b', 'c', 'd']
a.extend([1,2])
a
['b', 'c', 'd', 1, 2]
a[len(a)]=[3]
Traceback (most recent call last):
  File "<pyshell#26>", line 1, in <module>
    a[len(a)]=[3]
IndexError: list assignment index out of range
a[len(a):]=[3]
a
['b', 'c', 'd', 1, 2, 3]
a=[1,3,4]
a.insert(1,2)
a
[1, 2, 3, 4]
a.insert(3,5)
a
[1, 2, 3, 5, 4]
a,remove(1)
Traceback (most recent call last):
  File "<pyshell#34>", line 1, in <module>
    a,remove(1)
NameError: name 'remove' is not defined
a.remove(1)
a
[2, 3, 5, 4]
a,remove(6)
Traceback (most recent call last):
  File "<pyshell#37>", line 1, in <module>
    a,remove(6)
NameError: name 'remove' is not defined
a.remove(6)
Traceback (most recent call last):
  File "<pyshell#38>", line 1, in <module>
    a.remove(6)
ValueError: list.remove(x): x not in list
a.pop(0)
2
a
[3, 5, 4]
a.clear()
a
[]
a=[1,2,3,4,5]
a
[1, 2, 3, 4, 5]
a[0:3]
[1, 2, 3]
a[0:3]=[a,b,c]
Traceback (most recent call last):
  File "<pyshell#46>", line 1, in <module>
    a[0:3]=[a,b,c]
NameError: name 'b' is not defined
a[0:3]=["a","b","c"]
a
['a', 'b', 'c', 4, 5]
a=[12,46,3,4]
a.sort()
a
[3, 4, 12, 46]
a.reverse()
a
[46, 12, 4, 3]
a=[12,46,3,4]
a.sort(reverse=True)
a
[46, 12, 4, 3]
a=[12,4,6,3,4]
a.count(4)
2
a.index(4)
1
a[a.index(4)]=5
a
[12, 5, 6, 3, 4]
a=[1,2,4,6,3,4,4]
a.index(4,2)
2
a.index(4,4,6)
5
b=a.copy()
b
[1, 2, 4, 6, 3, 4, 4]
b=a[0:4]
b
[1, 2, 4, 6]
matrix=[[1,2,3],[4,5,6],[7,8,9]]
print(matrix)
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for i in matrix:
    print(i)

[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
for i in matrix:
    for each in i:
        print(each)

1
2
3
4
5
6
7
8
9
for i in matrix:
    for each in i:
        print(each,end=" ")
    print()

1 2 3 
4 5 6 
7 8 9 
matrix[0]
[1, 2, 3]
matrix[0][0]
1
matrix[0][1]
2
matrix[1][0]
4
for i in range(3):
    A[i]=[0]*3

Traceback (most recent call last):
  File "<pyshell#86>", line 2, in <module>
    A[i]=[0]*3
NameError: name 'A' is not defined. Did you mean: 'a'?
a=[0]*3
A=[0]*3
a
[0, 0, 0]
A
[0, 0, 0]
for i in range(3):
    A[i]=[0]*3

A
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
import copy
A
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
A.copy.deepcopy()
Traceback (most recent call last):
  File "<pyshell#96>", line 1, in <module>
    A.copy.deepcopy()
AttributeError: 'builtin_function_or_method' object has no attribute 'deepcopy'
B=A.copy.deepcopy()
Traceback (most recent call last):
  File "<pyshell#97>", line 1, in <module>
    B=A.copy.deepcopy()
AttributeError: 'builtin_function_or_method' object has no attribute 'deepcopy'
\
B=copy.deepcopy(A)
B
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
B[1][2]=3
B
[[0, 0, 0], [0, 0, 3], [0, 0, 0]]
A
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
A=[1,2,3,4,5]
A
[1, 2, 3, 4, 5]
for i in range(len(A)):
    A[i]=A[i]*2

A
[2, 4, 6, 8, 10]
A=[1,2,3,4,5]
A=[i*2 for i in range(len(A))]
A
[0, 2, 4, 6, 8]
A=[1,2,3,4,5]
A=[i*2 for i in A]
A
[2, 4, 6, 8, 10]
matrix=[[1,2,3],
        [4,5,6]
        [7,8,9]]
Traceback (most recent call last):
  File "<pyshell#115>", line 2, in <module>
    [4,5,6]
TypeError: list indices must be integers or slices, not tuple
>>> matrix=[[1,2,3],
...         [4,5,6],
...         [7,8,9]]
>>> matrix
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> a=[i[1] for i in matrix]
>>> a
[2, 5, 8]
>>> a=[i[0] for i in matrix]
>>> a
[1, 4, 7]
>>> a=[i[2] for i in matrix]
>>> a
[3, 6, 9]
>>> b=[matrix[i][i] for i in range(len(matrix))]
>>> b
[1, 5, 9]
>>> b=[matrix[i][len(matrix)-1-i] for i in range(len(matrix))]
>>> b
[3, 5, 7]
>>> A=[0]*3
>>> for i in range(3:)
SyntaxError: invalid syntax
>>> for i in range(3)
SyntaxError: expected ':'
>>> for i in range(3):
...     A[i]=[0]*3
... A
SyntaxError: invalid syntax
>>> A
[0, 0, 0]
>>> for i in range(3):
...     A[i]=[0]*3
... 
...     
>>> 
>>> A
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
S=[[0]*3 for i in range(3)]
S
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
A=[i for i in range(10)if i%2 ==0]
A
[0, 2, 4, 6, 8]
words=["great","Fishc","afaervv","afafagvzbg","zviuzbnz"]
b=[f for f in words if f=="f"]
b
[]
b=[f for f in words if f[0]=="f"]
b
[]
b=[f for f in words if f[0]=="a"]
b
['afaervv', 'afafagvzbg']
matrix=[[1,2,3],
        [4,5,6],
        [7,8,9]]
flatten=[col for row in matrix for col in row]
flaten
Traceback (most recent call last):
  File "<pyshell#152>", line 1, in <module>
    flaten
NameError: name 'flaten' is not defined. Did you mean: 'flatten'?
flatten
[1, 2, 3, 4, 5, 6, 7, 8, 9]
[x+y for x in "fishc" for y in "FISHC"]
['fF', 'fI', 'fS', 'fH', 'fC', 'iF', 'iI', 'iS', 'iH', 'iC', 'sF', 'sI', 'sS', 'sH', 'sC', 'hF', 'hI', 'hS', 'hH', 'hC', 'cF', 'cI', 'cS', 'cH', 'cC']
[[x,y] for x in range(10) if x%2==0 for y in range(10) if y%3==0]
[[0, 0], [0, 3], [0, 6], [0, 9], [2, 0], [2, 3], [2, 6], [2, 9], [4, 0], [4, 3], [4, 6], [4, 9], [6, 0], [6, 3], [6, 6], [6, 9], [8, 0], [8, 3], [8, 6], [8, 9]]
_=[]
for x in range(10):
    if x%2==0:
        for y in range(10):
            if y%3==0:
                _.append([x,y])

_
[[0, 0], [0, 3], [0, 6], [0, 9], [2, 0], [2, 3], [2, 6], [2, 9], [4, 0], [4, 3], [4, 6], [4, 9], [6, 0], [6, 3], [6, 6], [6, 9], [8, 0], [8, 3], [8, 6], [8, 9]]
