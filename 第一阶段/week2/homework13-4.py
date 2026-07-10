#### 题目 4：正则表达式基础 ⭐⭐⭐

import re

text="我的邮箱是 test@example.com，电话是 138-1234-5678"

email=re.search(r'\w+@\w+\.[a-zA-z]+',text)
number=re.search(r'\d{3}-\d{4}-\d{4}',text)

print('提取邮箱：',email.group())#要拿到真正的字符串，需要调用 .group()：
print('提取电话：',number.group())

user=input('请输入手机号：')
result=re.fullmatch(r'1[3-9]\d{9}',user)

if result:
    print('✅ 合法手机号')
else:
    print('❌手机号错误')

