### Day 13：常用标准库

#### 题目 1：datetime ⭐⭐

import datetime as d

today=d.datetime.now()
print(f"今天是：{today.strftime('%Y-%m-%d')}")

birthday=d.datetime(2027,5,22)
to_birthday=birthday-today
print(f'距离下次生日还有：{to_birthday.days}天')

born_day=d.datetime(2005,5,22)
to_born=today-born_day
print(f'我已出生：{to_born.days}天')