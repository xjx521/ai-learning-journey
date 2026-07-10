#### 题目 2：使用第三方库 ⭐⭐

import requests

# 获取一条随机名言
response=requests.get("https://api.quotable.io/random", verify=False, timeout=10)#目标网站 SSL 证书过期，Python 在 HTTPS 请求时会强制校验安全证书，校验不通过直接拦截请求。用verify=False跳过校验，用timeout=10设置请求最长等待 10 秒，如果 10 秒内网站没返回数据，直接强制终止请求并抛出超时异常，防止程序卡死一直转圈。
data=response.json()#返回的json字符串转化为字典

print(f"名言： {data['content']}")
print(f"作者：{data['author']}")

