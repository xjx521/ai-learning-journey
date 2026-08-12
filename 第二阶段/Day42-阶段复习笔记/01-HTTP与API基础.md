# 🌐 第二阶段学习笔记(一):HTTP 与 API 基础

> 📅 学习周期:2026.07.19 - 2026.07.21 | 对应 Day22-25
> 📌 本笔记基于个人学习笔记、实验代码、报错记录整理,供日常查阅与面试复习
> 🎯 掌握后应能:看懂一个 URL、说清 GET/POST 区别、设计 RESTful 接口、写出异步并发代码

---

## 目录

- [第 1 章 HTTP 协议基础(Day22-23)](#第-1-章-http-协议基础day22-23)
- [第 2 章 RESTful API 设计(Day24)](#第-2-章-restful-api-设计day24)
- [第 3 章 异步编程基础(Day25)](#第-3-章-异步编程基础day25)
- [📕 本册错题本](#-本册错题本)

---

# 第 1 章 HTTP 协议基础(Day22-23)

## 1.1 HTTP 是什么

### 🔴 HTTP 请求-响应模型

> 📌 **知识点说明**:HTTP(HyperText Transfer Protocol,超文本传输协议)是浏览器和服务器之间"对话"的语言。**客户端发请求,服务器回响应**,一问一答,每次都是独立的两步。
>
> 类比:你去餐厅点餐 —— 你(客户端)报菜名(请求),厨师(服务器)做好端上来(响应)。**HTTP 无状态** = 厨师不记得你上一顿吃了什么,每桌菜都是"从零开始"。

**最简可运行示例** — 用 Python 发一个 HTTP 请求(第一阶段学过的 requests):

```python
import requests

# 发 GET 请求:向服务器要东西(浏览器地址栏输入网址就是发 GET)
resp = requests.get("https://httpbin.org/get")
print(resp.status_code)   # 200 = 成功
print(resp.json())        # 服务器返回的 JSON 数据
```

🎯 **使用场景**:Web 开发的一切都建立在 HTTP 之上 —— 前端调后端 API、爬虫抓网页、API 调试。理解它才能看懂浏览器 F12 里那些请求和报错。

⚠️ **易错点**:
```python
# ❌ 请求超时/连接不上时直接崩溃
resp = requests.get("https://不存在的域名.com")

# ✅ 加超时 + 捕获异常,避免程序卡死
try:
    resp = requests.get("https://httpbin.org/get", timeout=3)
except requests.exceptions.ConnectionError:
    print("网络不通,检查地址或代理")
```

### 🔴 HTTP 三大特性

> 📌 **知识点说明**:HTTP 的三个核心特性必须记牢:①**无状态**(服务器不记得上次的请求);②**明文**基于 TCP(HTTPS 才加密);③**请求-响应模式**(客户端主动发起)。

| 特性 | 含义 | 引发的痛点 | 解决方案 |
|------|------|-----------|---------|
| 无状态 | 服务器不记得你是谁 | 每次请求都要重新认证 | Cookie / Session / Token |
| 明文传输 | 内容可被截获 | 密码泄露风险 | HTTPS(TLS 加密) |
| 请求-响应 | 只有客户端能发起 | 服务器不能主动推送 | WebSocket / 轮询 |

## 1.2 URL 结构

### 🔴 URL 的组成

> 📌 **知识点说明**:URL(统一资源定位符)= 网上的"门牌号"。拆开来看有 6 个部分,每个部分都告诉浏览器"去哪里、怎么去、拿什么"。

以 `https://www.example.com:8080/path/to/page?name=xiao&age=20#section` 为例:

| 部分 | 例子 | 作用 | 是否必填 |
|------|------|------|---------|
| 协议 | `https://` | 用什么方式访问(http/https) | ✅ |
| 域名 | `www.example.com` | 哪台服务器(DNS 解析成 IP) | ✅ |
| 端口 | `:8080` | 服务器的哪个"门" | ❌ 默认 80/443 |
| 路径 | `/path/to/page` | 服务器上的哪个资源 | ✅ |
| 查询参数 | `?name=xiao&age=20` | 给服务器的附加条件 | ❌ |
| 锚点 | `#section` | 页面内部定位(不发给服务器) | ❌ |

**最简可运行示例** — 用 requests 的 `params` 传查询参数(重点记这个):

```python
import requests

# 方式一:直接把参数拼在 URL 里
resp = requests.get("https://httpbin.org/get?name=xiao&age=20")

# 方式二(推荐):用 params 字典,requests 会自动帮你拼好 ? 和 &
params = {"name": "xiao", "age": 20}
resp = requests.get("https://httpbin.org/get", params=params)
print(resp.url)  # https://httpbin.org/get?name=xiao&age=20
```

🎯 **使用场景**:设计 API 时,查询参数用来做"过滤、分页、搜索"(如 `?page=1&size=10&keyword=学习`)。

⚠️ **易错点**:
```python
# ❌ 中文/特殊字符直接拼 URL 会乱码或报错
requests.get("https://httpbin.org/get?name=小明")

# ✅ 让 requests 用 params 自动编码(它会处理 URL 编码)
params = {"name": "小明"}
requests.get("https://httpbin.org/get", params=params)  # 自动转成 %E5%B0%8F%E6%98%8E
```

## 1.3 HTTP 请求方法

### 🔴 四大方法(GET / POST / PUT / DELETE)+ PATCH

> 📌 **知识点说明**:HTTP 方法 = 你想对资源"做什么"。**URL 是名词(资源),方法是动词(动作)**。RESTful 设计的核心就是把"动作"放到方法里,而不是塞进 URL。
>
> 类比:图书馆里 —— GET=查看书架上的书,POST=新买一本书放进去,PUT=整本替换, PATCH=只改书的一页, DELETE=把书下架。

| 方法 | 含义 | 参数位置 | 幂等? | 典型场景 |
|------|------|---------|-------|---------|
| GET | 获取数据 | 查询参数(URL) | ✅ 是 | 查列表、看详情、搜索 |
| POST | 创建数据 | 请求体(Body) | ❌ 否 | 注册、发帖、提交订单 |
| PUT | 全量更新 | 请求体 | ✅ 是 | 整条替换(必须传全部字段) |
| PATCH | 部分更新 | 请求体 | ❌ 否 | 只改一个字段(如 completed) |
| DELETE | 删除数据 | 路径参数 | ✅ 是 | 删除一条记录 |

💡 **速记**:GET 拿、POST 建、PUT 换、PATCH 改、DELETE 删。
**幂等** = 同一个请求发 100 次和发 1 次,结果一样(GET 查 100 次不会改变数据;POST 发 100 次会创建 100 条 → 不幂等)。

**最简可运行示例** — 五种方法 + 对应参数位置:

```python
import requests

base = "https://httpbin.org"

# GET:参数在 URL(查询参数)
requests.get(f"{base}/get", params={"page": 1})

# POST:参数在 Body(JSON 请求体)
requests.post(f"{base}/post", json={"title": "买牛奶"})

# PUT:全量更新,Body 传完整数据
requests.put(f"{base}/put", json={"title": "买牛奶", "completed": True})

# PATCH:部分更新,只传要改的字段
requests.patch(f"{base}/patch", json={"completed": True})

# DELETE:删除,一般只用路径参数
requests.delete(f"{base}/delete/1")
```

⚠️ **易错点**:
```python
# ❌ 把删除/创建动作写进 URL(这是错误的 URL 设计)
requests.get("https://api.com/deleteUser?id=1")

# ✅ 用正确的 HTTP 方法表达动作
requests.delete("https://api.com/users/1")

# ❌ POST 用 params 传数据(应该用 json)
requests.post("https://api.com/users", params={"name": "xiao"})

# ✅ POST 数据放请求体
requests.post("https://api.com/users", json={"name": "xiao"})
```

## 1.4 HTTP 状态码

### 🔴 状态码速查(2xx-5xx)

> 📌 **知识点说明**:服务器处理完请求后,用**三位数字**告诉客户端结果。**第一位数字代表大类**:2 成功、3 重定向、4 客户端(你)错了、5 服务器(我)错了。
>
> 记忆技巧:**401 = "我不知道你是谁";403 = "我知道你是谁但不让你进"**。这是面试必考的对比!

| 状态码 | 含义 | 典型场景 | 记忆锚点 |
|--------|------|---------|---------|
| 200 | 成功 | GET 查询成功 | ✅ 一切正常 |
| 201 | 创建成功 | POST 新建资源 | Created |
| 204 | 无内容 | DELETE 删除成功 | No Content |
| 301 | 永久重定向 | 网址搬家 | Moved Permanently |
| 304 | 未修改(用缓存) | 资源没变,用本地缓存 | Not Modified |
| 400 | 请求错误 | 参数格式不对 | Bad Request |
| 401 | 未认证 | 没登录/没带 token | Unauthorized(你谁?) |
| 403 | 无权限 | 登录了但没权限 | Forbidden(不让进) |
| 404 | 资源不存在 | 路径写错 | Not Found |
| 405 | 方法不允许 | GET 的路径用 POST 访问 | Method Not Allowed |
| 413 | 请求体过大 | 上传超大文件 | Payload Too Large |
| 422 | 参数校验失败 | Pydantic 验证不通过(FastAPI 常见) | Unprocessable Entity |
| 429 | 请求过多 | 接口限流 | Too Many Requests |
| 500 | 服务器内部错误 | 代码 bug | Internal Server Error |
| 503 | 服务不可用 | 服务器过载/维护 | Service Unavailable |

**最简可运行示例** — 判断请求是否成功:

```python
import requests

resp = requests.get("https://httpbin.org/status/404")
print(resp.status_code)              # 404
print(resp.status_code == 200)       # False
print(resp.ok)                       # False(200-299 之间才为 True)
```

🎯 **使用场景**:写代码判断请求结果;设计 API 时选对状态码;调试时看报错定位是"你的错(4xx)"还是"服务器的错(5xx)"。

⚠️ **易错点**:很多人写 API 时**不管成功失败都返回 200**,这是典型坏习惯。正确做法是"**状态码表达结果,Body 表达细节**":
```python
# ❌ 错误:找不到用户却返回 200,前端只能靠解析 body 判断
# {"code": 404, "message": "用户不存在"}  ← 但 HTTP 状态码是 200!

# ✅ 正确:用 HTTPException 让 HTTP 状态码真的是 404
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="用户不存在")
```

## 1.5 请求头与响应头

### 🟡 常用请求头/响应头

> 📌 **知识点说明**:HTTP 消息分"**头(Headers)**"和"**体(Body)**"。头 = 元数据(快递单上的信息),体 = 实际内容(快递盒里的东西)。头用 `键: 值` 形式,每行一个。

| 请求头 | 作用 | 示例 |
|--------|------|------|
| `User-Agent` | 告诉服务器"我是谁"(浏览器/爬虫) | `Mozilla/5.0 ... Chrome/126.0` |
| `Accept` | 我能接受什么格式 | `application/json` |
| `Content-Type` | 我发送的 Body 是什么格式 | `application/json` |
| `Authorization` | 认证凭证(常放 JWT) | `Bearer eyJhbGciOi...` |
| `Cookie` | 携带会话信息 | `sessionid=abc123` |
| `Referer` | 我从哪个页面来的 | `https://www.baidu.com` |

| 响应头 | 作用 |
|--------|------|
| `Content-Type` | 返回内容的格式 |
| `Set-Cookie` | 服务器下发 Cookie |
| `Cache-Control` | 缓存策略 |
| `Access-Control-Allow-Origin` | CORS 允许的来源(见 Day34) |

**最简可运行示例** — 伪造 User-Agent 伪装成浏览器(爬虫/调试必备):

```python
import requests

# 不加 headers,很多网站会识别出是程序并拒绝(反爬)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0",
}
resp = requests.get("https://httpbin.org/headers", headers=headers)
print(resp.json()["headers"]["User-Agent"])  # 回显我们伪造的 UA
```

⚠️ **易错点**:**有些接口的 `Content-Type` 必须和请求体格式对应**。POST JSON 要用 `json=`,POST 表单要用 `data=`,混用会 422:
```python
# ❌ json= 传了,但服务器想要表单
requests.post(url, json={"username": "xiao"})

# ✅ 表单用 data=
requests.post(url, data={"username": "xiao"})
# ✅ JSON 用 json=
requests.post(url, json={"username": "xiao"})
```

## 1.6 无状态与 Cookie / Session / Token

### 🟡 三种"记住你"的方案

> 📌 **知识点说明**:HTTP 无状态 → 服务器每次都不知道你是谁。于是有三种"身份凭证"方案。**这是 Web 认证的基础,Day33 的 JWT 就是 Token 方案的具体实现。**

| 方案 | 凭证存在哪 | 流程 | 优点 | 缺点 |
|------|-----------|------|------|------|
| Cookie | 浏览器 | 服务器下发 Cookie,浏览器每次自动带上 | 简单 | 明文、可伪造 |
| Session | 服务器 | 服务器存会话数据,只给浏览器一个 session_id | 安全可控 | 服务器要存状态、扩展难 |
| Token(JWT) | 客户端 | 服务器签一个"带签名"的令牌,客户端保存 | 无状态、可扩展 | 泄露难撤销 |

💡 **速记**:Cookie 是"认脸",Session 是"对暗号(对的是服务器的账本)",Token 是"发盖章通行证(服务器不记账也能验证)"。

## 1.7 HTTPS vs HTTP

### ⚪ HTTPS 原理(了解即可)

> 📌 **知识点说明**:HTTPS = HTTP + **TLS 加密**。核心解决三件事:①**加密**(内容别人看不懂);②**防篡改**(内容没被改过);③**身份验证**(确认是真实服务器,防钓鱼)。
>
> 类比:HTTP 是"明信片"(路上谁都能看),HTTPS 是"上了锁的保险箱"(只有收发双方有钥匙)。

```bash
# 用 curl 查看一个网站的证书信息(了解 HTTPS 在干嘛)
curl -v https://www.baidu.com 2>&1 | grep -i "subject"
```

🎯 **使用场景**:面试聊安全必提 HTTPS;本地开发用 HTTP 即可,上线必须 HTTPS。

## 1.8 抓包与调试工具(F12 / curl / Postman)

### 🟡 三件调试工具

> 📌 **知识点说明**:写 Web 后端的日常 = 发请求、看响应、查报错。三个工具分工不同:**F12 看浏览器发的真实请求;curl 在命令行快速测试;Postman/Apifox 做接口调试和文档**。

**F12 → Network 面板关键操作**:
1. 打开浏览器按 `F12` → `Network` 标签
2. **勾选 "Preserve log"**(保留日志)—— 否则页面跳转后请求记录就没了
3. 刷新页面,点击任意请求 → 看 `Headers`(请求头/响应头)、`Payload`(请求体)、`Response`(响应体)
4. 用 `Filter`(过滤器)按类型/关键词筛选请求

**curl 常用选项表**:

| 命令 | 作用 |
|------|------|
| `curl https://api.com/users` | 发 GET 请求 |
| `curl -X POST https://api.com/users` | 指定方法 |
| `curl -H "Authorization: Bearer xxx" ...` | 加请求头 |
| `curl -d '{"name":"xiao"}' -H "Content-Type: application/json" ...` | 发 JSON Body |
| `curl -i` | 显示响应头 |
| `curl -o 文件名` | 保存响应到文件 |

```bash
# Windows PowerShell/Git Bash 里测自己写的 FastAPI 接口
curl http://localhost:8000/health
```

**Postman vs Apifox**:

| 对比 | Postman | Apifox |
|------|---------|--------|
| 界面 | 英文为主 | 中文友好 |
| 适用 | 国际通用 | 国内开发推荐 |
| 亮点 | 生态成熟 | 接口文档/调试/Mock 一体化 |

🎯 **使用场景**:自己写完 API 不知道对不对 → 用 Apifox 或 /docs(Swagger UI)测;前端说"调不通" → 用 F12 看请求到底发了什么。

---

## 第 1 章【错误原因 + 修复方案】模块

> 来源:Day22-23 实操中遇到的真实问题。

### ❌ 问题 1:httpbin.org 连接不上(SSL 证书/网络)

**错误原因**:国内网络访问 httpbin.org 不稳定,或本地环境 SSL 证书过期。

**修复方案**:换用 `postman-echo.com` 或本地自建 httpbin(用户做了 `my_httpbin.py`)。requests 里遇到证书问题可加 `verify=False`(仅调试用,生产禁用):
```python
resp = requests.get("https://httpbin.org/get", verify=False)  # 跳过证书校验
```

### ❌ 问题 2:Windows 上 curl 命令报错

**错误原因**:Windows 自带的是旧版 curl,不支持部分参数;或 PowerShell 把单引号解析掉了。

**修复方案**:优先用 PowerShell 的 `curl.exe`(新版),JSON 用双引号转义;或直接用 Apifox/Postman 替代命令行。

---

## 🎯 第 1 章 面试/开发高频考点

**必问(背下来)**:
1. 浏览器输入网址后发生了什么?→ DNS 解析 → TCP 连接 → TLS 握手 → 发 GET → 服务器处理 → 返回 HTML → 渲染
2. GET 和 POST 的区别?(参数位置 + **幂等性** + 安全性 + 缓存:GET 可缓存、POST 一般不缓存)
3. 401 vs 403 的区别?(未认证 vs 无权限)
4. 什么是幂等?哪些方法幂等?(GET/PUT/DELETE 幂等,POST/PATCH 不幂等)
5. HTTP 无状态怎么解决?(Cookie/Session/Token 三方案)

**加分项**:
- 能画出 HTTP 请求-响应的完整报文结构(请求行 + 请求头 + 空行 + 请求体)
- 知道 422 是 FastAPI 参数校验失败、304 走缓存
- 会解释 HTTPS 的加密/防篡改/身份验证三层作用

**冷门**:
- 405 与 404 的区别(方法错 vs 资源不存在)
- Cookie 和 Session 的存储位置(客户端 vs 服务器)

---

# 第 2 章 RESTful API 设计(Day24)

## 2.1 什么是 RESTful

### 🔴 RESTful 设计 6 条规则

> 📌 **知识点说明**:RESTful 是一套 **API 设计规范**(不是语法,不遵守不报错,但遵守了别人更好用)。核心一句话:**用 URL 表示资源,用 HTTP 方法表示动作**。
>
> 类比:把资源当成"图书馆的书",URL = 书的分类位置(名词),HTTP 方法 = 你想对书做什么(动词)。

| 规则 | ❌ 不推荐 | ✅ 推荐 | 说明 |
|------|----------|---------|------|
| 1. URL 只放名词 | `GET /getUsers` | `GET /users` | 动作交给 HTTP 方法 |
| 2. 名词用复数 | `/user/123` | `/users/123` | 统一复数,规范一致 |
| 3. 嵌套表示关系 | 无 | `/users/5/todos` | 嵌套 ≤ 2 层,过深拆开 |
| 4. 过滤用查询参数 | `GET /searchUsers?q=xx` | `GET /users?q=xx` | 搜索/分页/过滤都放查询参数 |
| 5. 版本放 URL | 无 | `GET /api/v1/users` | 升级不破坏老客户端 |
| 6. 统一返回格式 | 每家都不一样 | `{success, data, message}` | 前端好解析 |

**最简可运行示例** — 一个规范的资源路由设计:

```
# 用户 users 资源的完整 CRUD(注意全是复数名词 + 方法表动作)
GET    /users            # 用户列表(可带 ?page=1&size=10)
POST   /users            # 创建用户
GET    /users/{id}       # 查单个用户
PUT    /users/{id}       # 全量更新
PATCH  /users/{id}       # 部分更新
DELETE /users/{id}       # 删除用户

# 嵌套关系:某用户的待办
GET    /users/5/todos    # 用户 5 的待办列表(嵌套一层,合理)
```

🎯 **使用场景**:公司 API 文档、OpenAPI/Swagger 接口设计、简历项目里的接口规范。

⚠️ **易错点**:
```python
# ❌ URL 里塞动词(动作是方法的事,不是 URL 的事)
# GET /deleteUser?id=1
# GET /getUserById?id=1

# ✅ 正确姿势
# DELETE /users/1
# GET    /users/1
```

## 2.2 状态码正确使用

### 🔴 状态码与接口语义配对

> 📌 **知识点说明**:每个操作选对状态码,前端才能靠 `status_code` 判断结果,而不是解析 body 字符串。

| 操作 | 成功状态码 | 失败状态码 |
|------|-----------|-----------|
| POST 创建 | **201** Created | 400/422(参数错) |
| GET 查询 | **200** OK | 404(不存在) |
| PUT/PATCH 更新 | 200 OK | 404、403(无权限) |
| DELETE 删除 | **204** No Content | 404 |
| 未登录访问 | - | 401 |
| 已登录但无权 | - | 403 |

⚠️ **易错点**:返回 204 时**不能有响应体**(Body 必须为空),否则不符合规范。

## 2.3 JSON:序列化与反序列化

### 🔴 JSON vs Python dict

> 📌 **知识点说明**:JSON 是**前后端通信的标准格式**(一种文本格式);Python dict 是**内存里的对象**。两者长得像但不同:**JSON 是字符串,要传输/保存就必须转换**。

| 对比 | JSON | Python dict |
|------|------|------------|
| 本质 | 字符串(文本) | 内存对象 |
| 布尔值 | `true`/`false` | `True`/`False` |
| 空值 | `null` | `None` |
| 引用方法 | `import json` | 直接 `{}` |

**最简可运行示例** — json 四件套(loads/dumps/load/dump):

```python
import json

# --- 序列化:dict → JSON 字符串 ---
data = {"name": "小明", "age": 20, "completed": True}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)  # {"name": "小明", ...}(ensure_ascii=False 保留中文)

# --- 反序列化:JSON 字符串 → dict ---
back = json.loads(json_str)
print(back["name"])  # 小明

# --- 写文件/读文件(注意带 s 的是字符串,不带 s 的是文件)---
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)   # dump → 写文件
with open("data.json", "r", encoding="utf-8") as f:
    data2 = json.load(f)                                # load → 读文件
```

💡 **速记**:`dumps`/`loads` 结尾的 **s = String(字符串)**,操作的是字符串;`dump`/`load` 不带 s,操作的是**文件**。

⚠️ **易错点**:
```python
# ❌ 中文写入文件变 小 等乱码
json.dump(data, f)
# ✅ 加 ensure_ascii=False
json.dump(data, f, ensure_ascii=False)

# ❌ dumps/loads 和 dump/load 用反
with open("f.json", "w") as f:
    f.write(json.dumps(data))   # 硬要用字符串写法也行,但 dump 更省事
```

## 2.4 统一响应格式

### 🟡 成功/错误/分页三套响应

> 📌 **知识点说明**:让所有接口返回**相同结构**,前端只需写一次解析逻辑。这是 Day34 会完整实现的思路,这里先学设计。

```python
# 成功响应:success + data + message
{"success": True, "data": {...}, "message": "创建成功"}

# 错误响应:success + error(内含 code/message/path)
{"success": False, "error": {"code": 404, "message": "用户不存在", "path": "/users/999"}}

# 分页响应:data + pagination
{
    "data": [...],
    "pagination": {"page": 1, "size": 10, "total": 25, "total_pages": 3}
}
```

🎯 **使用场景**:自己搭项目时先定好这三套格式,前端(如 Streamlit)只用 `resp.json()["success"]` 就能判断成功失败,不用每个接口单独写。

---

## 🎯 第 2 章 面试/开发高频考点

**必问**:
1. 什么是 RESTful?核心原则是什么?(URL 名词 + 方法动词)
2. PUT 和 PATCH 的区别?(全量替换 vs 部分更新;PUT 要传全部字段)
3. 201 和 204 各自什么时候用?(创建 vs 删除无内容)
4. JSON 和 Python dict 有什么区别?dumps 和 dump 的区别?

**加分项**:
- 能说出"全部返回 200"为什么是坏设计
- 会设计统一响应格式(成功/错误/分页)

**冷门**:
- 嵌套 URL 为什么不超过 2 层(过深难维护,用查询参数代替)
- API 版本化几种方案(URL 路径 vs 请求头 Accept)

---

# 第 3 章 异步编程基础(Day25)

## 3.1 为什么需要异步

### 🔴 同步 vs 异步(排队 vs 叫号)

> 📌 **知识点说明**:**同步** = 一个一个排队办,前面的人慢你就干等(银行 1 个窗口排队);**异步** = 同时开多个窗口,谁先办完谁先走(医院叫号,你等待时可以刷手机)。IO 等待(网络/数据库/文件)是异步最大的收益来源。
>
> 实验数据(用户实测):5 个网站逐个请求 **同步 5.8s → 异步 2.0s**,节省 3.8s。

**最简可运行示例** — 同步 vs 异步耗时对比:

```python
import asyncio
import time

# ---------- 同步版本:一个个等 ----------
def sync_task(name, delay):
    time.sleep(delay)            # 同步等待(阻塞)
    return f"{name} 完成"

def run_sync():
    start = time.time()
    sync_task("A", 1)           # 等 A 完
    sync_task("B", 1)           # 再等 B
    sync_task("C", 1)
    return time.time() - start  # ≈ 3.0 秒

# ---------- 异步版本:一起等 ----------
async def async_task(name, delay):
    await asyncio.sleep(delay)   # 异步等待(不阻塞,让出控制权)
    return f"{name} 完成"

async def run_async():
    start = time.time()
    # gather 并发:三个任务同时开始,谁先好谁先返回
    results = await asyncio.gather(
        async_task("A", 1),
        async_task("B", 1),
        async_task("C", 1),
    )
    return time.time() - start  # ≈ 1.0 秒

# 注意:一个程序只能有一个 asyncio.run() 入口
# print(run_sync())
# print(asyncio.run(run_async()))
```

🎯 **使用场景**:爬虫抓多个网站、FastAPI 里并发查数据库、调用外部 LLM API(第三阶段的核心)。**只要涉及"等待网络/磁盘",异步就能提速。**

## 3.2 async / await / 协程 / 事件循环

### 🔴 四个核心概念

> 📌 **知识点说明**:
> - **协程(coroutine)**:一个可以被"暂停 + 恢复"的函数,用 `async def` 定义。它不是立刻执行,调用它只是创建一个"待执行对象"。
> - **await**:暂停当前协程,等待一个 IO 完成。**await 只能在 async 函数里用。**
> - **事件循环(event loop)**:调度器,负责"谁等完了就继续跑谁"。`asyncio.run()` 就是创建并启动事件循环。
> - 规则:**一个程序只有一个 `asyncio.run()` 入口,里面全部用 `await`**。

**最简可运行示例**:

```python
import asyncio

# 定义一个协程:注意它是 async def
async def hello(name):
    print(f"开始: {name}")
    await asyncio.sleep(1)      # 假装在做耗时 IO(网络请求/读数据库)
    print(f"结束: {name}")
    return f"你好, {name}"

# 错误:直接调用不会执行!只是创建一个协程对象
# hello("小明")  → RuntimeWarning: coroutine 'hello' was never awaited

# 正确:必须 await(或者放进 asyncio.run 里)
async def main():
    result = await hello("小明")   # await 真正执行协程
    print(result)

if __name__ == "__main__":
    asyncio.run(main())           # 唯一的入口
```

⚠️ **易错点**:
```python
# ❌ 忘写 await:函数没执行,只有警告/错误
# result = hello("小明")

# ❌ 在 async 函数里用同步的 time.sleep(会阻塞整个事件循环!)
# async def bad():
#     time.sleep(2)        # 应该用 await asyncio.sleep(2)

# ❌ 嵌套 asyncio.run(一个程序只能有一个)
# async def main():
#     asyncio.run(hello("A"))   # RuntimeError: asyncio.run() cannot be called from a running event loop
```

## 3.3 asyncio.gather 并发

### 🔴 gather:同时跑多个任务

> 📌 **知识点说明**:`gather` 把多个协程**同时调度**,整体等待它们**全部完成**,按完成顺序返回结果列表。适合"并发发多个请求、最后统一处理结果"的场景。

**最简可运行示例** — 异步并发模拟爬取 5 个网站:

```python
import asyncio

async def fetch_site(name, delay):
    """模拟请求一个网站,delay 表示网站响应快慢"""
    await asyncio.sleep(delay)          # 模拟网络 IO
    return f"{name} 返回了 {delay}s 的内容"

async def main():
    # 5 个网站同时请求(快的先返回,但 gather 等全部完成)
    results = await asyncio.gather(
        fetch_site("A站", 0.5),
        fetch_site("B站", 1.0),
        fetch_site("C站", 2.0),
        fetch_site("D站", 0.8),
        fetch_site("E站", 1.5),
    )
    for r in results:                    # 结果按传入顺序返回
        print(r)

asyncio.run(main())
```

🎯 **使用场景**:批量调 LLM、并发查多个表、爬虫并发抓取。**真实项目里很少手写 gather 并发 IO,更多是 FastAPI 自动把每个请求当协程并发处理。**

## 3.4 异步常见误区(找茬练习)

### 🟡 三个经典错误

> 📌 **知识点说明**:Day25 的"错误找茬"实验总结了最常见的三类异步错误,面试也常考。

| # | 错误 | 现象 | 修复 |
|---|------|------|------|
| 1 | 调用协程忘了 `await` | `RuntimeWarning: coroutine was never awaited` | 加 `await` |
| 2 | 普通函数里用 `await` | `SyntaxError: 'await' outside async function` | 把函数改成 `async def` |
| 3 | async 函数里用 `time.sleep` | 整个程序被阻塞,并发失效 | 改成 `await asyncio.sleep()` |

```python
# ❌ 错误 1:忘了 await
async def foo():
    return 1
# x = foo()          # 得到的是协程对象,不是 1
# x = await foo()    # ✅

# ❌ 错误 2:普通函数用 await
# def bar():
#     await asyncio.sleep(1)   # SyntaxError
# async def bar():             # ✅ 改成 async def
#     await asyncio.sleep(1)

# ❌ 错误 3:async 里用 time.sleep 阻塞
# async def baz():
#     time.sleep(2)            # 阻塞事件循环
#     await asyncio.sleep(2)   # ✅ 用异步版
```

## 3.5 异步与 FastAPI(def vs async def)

### 🟡 路由函数怎么写才不阻塞

> 📌 **知识点说明**:FastAPI 里路由可以是普通 `def` 也可以是 `async def`。**含 IO 等待(查数据库/调外部 API)用 async def,纯计算用 def**。数据库用异步引擎时,路由必须 async def(见 Day30-32)。

| 写法 | 何时用 | 特点 |
|------|--------|------|
| `def` 普通函数 | 纯计算、无 IO 等待 | 在"线程池"里跑,也能并发 |
| `async def` | 有 await 等待(网络/异步数据库) | 在"事件循环"里跑,高并发首选 |

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# 异步路由:遇到 await 时让出控制权,其他人可以先处理
@app.get("/async")
async def read_async():
    await asyncio.sleep(1)          # 模拟慢 IO(如查数据库)
    return {"message": "异步等待 1 秒"}

# 同步路由:纯计算用 def 即可
@app.get("/calc")
def calc(a: int, b: int):
    return {"result": a + b}
```

⚠️ **易错点**:**async def 里用了阻塞的同步库(如 requests、time.sleep),会把整个事件循环卡住**。异步路由里要调外部 HTTP,要么用异步库(httpx),要么用 `def` 路由(自动进线程池)。

---

## 第 3 章【错误原因 + 修复方案】模块

### ❌ 问题:exercise_2 异步爬虫模拟报错(嵌套事件循环)

**错误原因**:原代码在 `async def` 内部又写了 `asyncio.run(...)`,一个程序里出现**两个事件循环**,触发 `RuntimeError`。

**修复方案**:
```python
# ❌ 错误:async 函数里再开事件循环
# async def main():
#     asyncio.run(fetch("a"))     # RuntimeError!

# ✅ 正确:统一一个 asyncio.run 入口,内部全部用 await
async def main():
    results = await asyncio.gather(fetch("a"), fetch("b"))
asyncio.run(main())
```

---

## 🎯 第 3 章 面试/开发高频考点

**必问**:
1. 同步和异步的区别?异步为什么快?(IO 等待期间不阻塞,去干别的)
2. 协程是什么?async/await 的作用?
3. 为什么 `asyncio.run()` 只能有一个?嵌套会怎样?
4. `await` 后面必须跟什么?(可等待对象:协程/Task/Future)
5. FastAPI 里 `def` 和 `async def` 路由的区别?

**加分项**:
- 能解释事件循环的调度机制(谁先 await 完谁继续)
- 知道 gather 和 `asyncio.create_task` 的区别(gather 等全部,create_task 后台跑)

**冷门**:
- `asyncio.sleep` vs `time.sleep` 的本质区别(是否让出控制权)
- Python 3.11+ 的 asyncio 改进(任务组 TaskGroup)

---

# 📕 本册错题本

| # | 错误代码/场景 | 报错/现象 | 原因 | 修复 |
|---|--------------|----------|------|------|
| 1 | `requests.get(url)` 不设 timeout | 程序卡死/ConnectionError | 网络慢或挂了 | 加 `timeout=3` + try/except |
| 2 | URL 直接拼中文参数 | 乱码/编码错误 | 未 URL 编码 | 用 `params={"name": "小明"}` 自动编码 |
| 3 | 找不到用户返回 200 + body 里写 404 | 前端判断困难 | 状态码没用对 | `raise HTTPException(status_code=404, ...)` |
| 4 | `json.dump` 写中文 | `小` 乱码 | 默认 ASCII 编码 | `ensure_ascii=False` |
| 5 | 调用协程不 await | `coroutine was never awaited` | 忘 await | 加 `await` |
| 6 | async 里嵌套 asyncio.run | `RuntimeError: ... running event loop` | 双事件循环 | 统一一个 run 入口,内部用 await |
