#### 题目 2：使用第三方库 ⭐⭐

import requests

# 获取一条随机名言
response=requests.get("https://api.quotable.io/random", verify=False, timeout=10)#目标网站 SSL 证书过期，Python 在 HTTPS 请求时会强制校验安全证书，校验不通过直接拦截请求。
data=response.json()#返回的json字符串转化为字典

print(f"名言： {data['content']}")
print(f"作者：{data['author']}")

