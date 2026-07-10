#### 题目：正则表达式 re 模块 笔记+练习 ⭐⭐⭐

import re

"""
========== 一、re 模块的三个常用方法 ==========

1. re.search(正则, 文本) —— 在文本中找一个位置匹配，返回 Match 对象或 None
2. re.match(正则, 文本) —— 必须从文本开头开始匹配
3. re.fullmatch(正则, 文本) —— 整个文本必须完全匹配（最严格）

拿到匹配结果后，用 .group() 取出字符串：
  result = re.search(r'\d+', "abc123def")
  print(result.group())  # 输出: 123

判断是否匹配成功：
  if result:  → 匹配到了（Match 对象为真）
  else:       → 没匹配到（None 为假）

========== 二、正则表达式基础符号 ==========

【字符匹配】
符号        含义                    例子
\d        任意一个数字 0-9          r'\d'      → "3"
\w        字母、数字、下划线         r'\w'      → "a"、"5"、"_"
\s        空白字符（空格、换行等）    r'\s'      → " "
.         任意一个字符（除换行外）   r'.'       → "x"、"3"、"@"
[...]     字符组，匹配其中一个       r'[abc]'   → "a" 或 "b" 或 "c"
[^...]    不在字符组中的字符        r'[^abc]'  → 除了 a/b/c 以外的
|         或                        r'a|b'     → "a" 或 "b"

【常用简写字符组】
r'[a-z]'      小写字母
r'[A-Z]'      大写字母
r'[0-9]' 或 r'\d    数字
r'[a-zA-Z]'   所有字母
r'[a-zA-Z0-9]'  字母+数字

【数量控制】
符号        含义                        例子
*         0 个或多个                    r'\d*'     → ""、"1"、"123"
+         1 个或多个（至少一个）         r'\d+'     → "1"、"123"（不能是空）
?         0 个或 1 个                   r'\d?'     → "" 或 "1"
{n}       正好 n 个                    r'\d{3}'   → "123"
{n,m}     n 到 m 个                    r'\d{2,4}' → "12"、"123"、"1234"
{n,}      至少 n 个                    r'\d{2,}'  → "12"、"123"、"1234"（更多也可以）

【位置锚点】
^         字符串开头                   r'^hello'  → 必须以 hello 开头
$         字符串结尾                   r'hello$'  → 必须以 hello 结尾

========== 三、常见正则模式 ==========

# 邮箱：用户名@域名.后缀
# 用户名可以有字母、数字、点、下划线、横杠
r'\w+@\w+\.\w+'
注意：. 在正则里有特殊含义（任意字符），要匹配真正的点要转义写成 \.

# 电话号码（带横杠）：138-1234-5678
r'\d{3}-\d{4}-\d{4}'

# 手机号（11位纯数字）：1开头，第二位3-9
r'^1[3-9]\d{9}$'
用 fullmatch 时不需要 ^ 和 $：
r'1[3-9]\d{9}'

# 纯数字
r'^\d+$' 或 fullmatch 用 r'\d+'

# 纯字母
r'^[a-zA-Z]+$' 或 fullmatch 用 r'[a-zA-Z]+'

========== 四、其他有用方法 ==========

# re.findall(正则, 文本) —— 找出所有匹配的内容，返回列表
text = "1号房间住3人，2号房间住5人"
nums = re.findall(r'\d+', text)
print(nums)  # ['1', '3', '2', '5']

# re.sub(正则, 替换内容, 文本) —— 把匹配的内容替换掉
text = "密码是 123456，别告诉别人"
result = re.sub(r'\d+', '***', text)
print(result)  # 密码是 ***，别告诉别人
"""

# ===== 练习题 =====

"""
练习 1：提取所有数字
从 "我今年25岁，有3个朋友，存了10000元" 中提取所有数字，返回 ['25', '3', '10000']
提示：re.findall(r'??', text)
"""


"""
练习 2：验证纯字母字符串
判断一个字符串是否只包含英文字母（可以大小写），不能有空格、数字、符号
提示：用 re.fullmatch(r'??', text)
"""


"""
练习 3：提取网址中的域名
从 "访问 https://www.baidu.com 搜索" 中提取域名（www.baidu.com）
提示：域名在 https:// 后面，/ 之前，可以用 r'https://??/??'
提示：[^/]+ 表示一个或多个非斜杠字符
"""


"""
练习 4：验证密码强度（可选，较难）
密码规则：6-16位，必须包含至少一个字母和一个数字，可以包含下划线
思路：先检查长度，再用 search 分别找字母和数字
"""


"""
练习 5：替换敏感信息
把 "张三的手机号是13812345678，李四的手机号是15987654321" 中的手机号替换为 '***'
提示：re.sub(r'??', '***', text)
"""


"""
练习 6：提取 URL 的协议和域名（可选，较难）
从 "https://github.com/xjxx" 中分别提取协议（https）和域名（github.com）
提示：用 search 匹配，再用 .group() 提取
"""


# 答案区（做完再看！）
"""
练习 1 答案：
  text = "我今年25岁，有3个朋友，存了10000元"
  nums = re.findall(r'\d+', text)
  print(nums)  # ['25', '3', '10000']

练习 2 答案：
  text = "helloWorld"
  result = re.fullmatch(r'[a-zA-Z]+', text)
  if result:
      print("✅ 纯字母")
  else:
      print("❌ 不是纯字母")

练习 3 答案：
  text = "访问 https://www.baidu.com 搜索"
  result = re.search(r'https://([^/]+)', text)
  # ([^/]+) 表示捕获一个或多个非斜杠字符
  if result:
      print(result.group(1))  # www.baidu.com

练习 4 答案：
  password = "abc123"
  if 6 <= len(password) <= 16 and re.search(r'[a-zA-Z]', password) and re.search(r'\d', password):
      print("✅ 密码合法")
  else:
      print("❌ 密码不合法")

练习 5 答案：
  text = "张三的手机号是13812345678，李四的手机号是15987654321"
  result = re.sub(r'1[3-9]\d{9}', '***', text)
  print(result)  # 张三的手机号是***，李四的手机号是***

练习 6 答案：
  text = "https://github.com/xjxx"
  result = re.search(r'(\w+)://([^/]+)', text)
  if result:
      print("协议:", result.group(1))   # https
      print("域名:", result.group(2))   # github.com
"""
