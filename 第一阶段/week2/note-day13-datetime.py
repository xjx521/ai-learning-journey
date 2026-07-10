Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import datetime
today=datetime.now()
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    today=datetime.now()
AttributeError: module 'datetime' has no attribute 'now'
today=datetime.datetime.now()#获取当前时间
print(today)
2026-07-10 17:14:43.137531
print(today.day)
10
print(today.year)
2026
print(today.hour)
17
date=datetime.datetime(2020.9.1)#创建一个datetime object年月日必需
SyntaxError: invalid syntax. Perhaps you forgot a comma?
date=datetime.datetime(2020,9,1)#创建一个datetime object年月日必需
print(date)
2020-09-01 00:00:00
date=datetime.datetime(2020,9,1,12,34,57,1313)#创建一个datetime object年月日必需
print(date)
2020-09-01 12:34:57.001313
print(date.strftime('%a'))
Tue
print(date.strftime('%A'))
Tuesday
print(date.strftime('%Y %m %d'))
2020 09 01
#strftime()把一个datetime object 转换成一个可读的字符串
print(date.strftime('%Y-%m-%d'))
2020-09-01
print(date.strftime('%Y/%m/%d'))
2020/09/01
t = datetime.strptime("2026-01-01", "%Y-%m-%d")# 3. 字符串转时间（strptime)
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    t = datetime.strptime("2026-01-01", "%Y-%m-%d")# 3. 字符串转时间（strptime)
AttributeError: module 'datetime' has no attribute 'strptime'
after3=date+timedelta(day=3)# 4. 时间加减 timedelta
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    after3=date+timedelta(day=3)# 4. 时间加减 timedelta
NameError: name 'timedelta' is not defined
after3 = now + timedelta(days=3)
Traceback (most recent call last):
  File "<pyshell#20>", line 1, in <module>
    after3 = now + timedelta(days=3)
NameError: name 'now' is not defined. Did you mean: 'pow'?
after3 = date + timedelta(days=3)
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    after3 = date + timedelta(days=3)
NameError: name 'timedelta' is not defined
import datetime
after3=date+timedelta(day=3)# 4. 时间加减 timedelta
Traceback (most recent call last):
  File "<pyshell#23>", line 1, in <module>
    after3=date+timedelta(day=3)# 4. 时间加减 timedelta
NameError: name 'timedelta' is not defined
t = datetime.strptime("2026-01-01", "%Y-%m-%d")# 3. 字符串转时间（strptime)
Traceback (most recent call last):
  File "<pyshell#24>", line 1, in <module>
    t = datetime.strptime("2026-01-01", "%Y-%m-%d")# 3. 字符串转时间（strptime)
AttributeError: module 'datetime' has no attribute 'strptime'
>>> from datetime import datetime
... 
>>> 
>>> t = datetime.strptime("2026-01-01", "%Y-%m-%d")# 3. 字符串转时间（strptime)
>>> t
datetime.datetime(2026, 1, 1, 0, 0)
>>> after3=date+timedelta(day=3)# 4. 时间加减 timedelta
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    after3=date+timedelta(day=3)# 4. 时间加减 timedelta
NameError: name 'timedelta' is not defined
>>> from datetime import datetime, date, timedelta
>>> after3=date+timedelta(day=3)# 4. 时间加减 timedelta
Traceback (most recent call last):
  File "<pyshell#31>", line 1, in <module>
    after3=date+timedelta(day=3)# 4. 时间加减 timedelta
TypeError: __new__() got an unexpected keyword argument 'day'. Did you mean 'days'?
>>> after3=date+timedelta(days=3)# 4. 时间加减 timedelta
Traceback (most recent call last):
  File "<pyshell#32>", line 1, in <module>
    after3=date+timedelta(days=3)# 4. 时间加减 timedelta
TypeError: unsupported operand type(s) for +: 'type' and 'datetime.timedelta'
>>> now=datetime.now()
>>> after3=now+timedelta(days=3)# 4. 时间加减 timedelta
>>> after3
datetime.datetime(2026, 7, 13, 17, 35, 39, 985048)
>>> after3=now-timedelta(hours=2)# 4. 时间加减 timedelta
>>> after3
datetime.datetime(2026, 7, 10, 15, 35, 39, 985048)
>>> ts=now.timestamp() # 时间戳浮点数
>>> ts
1783676139.985048
>>> dt = datetime.fromtimestamp(ts)# 5. 时间戳互转
>>> dt
datetime.datetime(2026, 7, 10, 17, 35, 39, 985048)
