# 🖥️ 第二阶段学习笔记(五):前端 Streamlit 与全栈

> 📅 学习周期:2026.08.09 - 2026.08.11 | 对应 Day36-40
> 📌 定位:AI 应用开发者**懂前端不必精通**——会用 Streamlit 快速搭界面 + 会前后端分离调接口即可
> 🎯 掌握后应能:用 Streamlit 写交互界面,用 requests 调 FastAPI 后端,拼出"前端 + 后端 + 数据库"的全栈应用

---

## 目录

- [第 14 章 HTML/CSS 速览(Day36)](#第-14-章-htmlcss-速览day36)
- [第 15 章 Streamlit 入门(Day37)](#第-15-章-streamlit-入门day37)
- [第 16 章 Streamlit 进阶(Day38)](#第-16-章-streamlit-进阶day38)
- [第 17 章 综合项目:AI 应用开发模板(Day39-40)【全栈核心】](#第-17-章-综合项目ai-应用开发模板day39-40全栈核心)
- [📕 本册错题本](#-本册错题本)

---

# 第 14 章 HTML/CSS 速览(Day36)

## 14.1 前端三大件

### 🔴 HTML 骨架 / CSS 皮肤 / JS 肌肉

> 📌 **知识点说明**:一个网页由三样东西组成:**HTML = 内容是啥(骨架)、CSS = 长啥样(皮肤)、JavaScript = 能干嘛(肌肉)**。AI 应用开发者要能看懂 HTML 结构,会用 CSS 调样式,不要求精通 JS。

| 三大件 | 类比 | 作用 | 例子 |
|--------|------|------|------|
| HTML | 骨架 | 内容结构 | `<h1>` 标题、`<p>` 段落、`<img>` 图片 |
| CSS | 皮肤 | 外观样式 | 颜色、字体、间距、布局 |
| JavaScript | 肌肉 | 行为交互 | 点击按钮弹窗、数据变化刷新 |

## 14.2 HTML 基本结构

### 🟡 标签 = 内容的"盒"

> 📌 **知识点说明**:HTML 用成对标签包内容:`<标签名 属性="值">内容</标签名>`。**`<head>` 给浏览器看(标题、样式),`<body>` 给用户看(实际内容)**。

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>我的第一个网页</title>   <!-- 浏览器标签页上的标题 -->
  </head>
  <body>
    <h1>一级标题</h1>        <!-- 最大,往下 h2~h6 越来越小 -->
    <h2>二级标题</h2>
    <a href="https://baidu.com">点我跳转</a>   <!-- 超链接 -->
    <img src="logo.png" alt="图片描述">        <!-- 图片:src 是路径 -->
    <p>这是一个段落</p>
  </body>
</html>
```

| 标签 | 作用 | 易错点 |
|------|------|--------|
| `<h1>` ~ `<h6>` | 标题(1 最大 6 最小) | 不是字号越大越好,是层级 |
| `<a href>` | 超链接 | href 是目标地址 |
| `<img src>` | 图片 | **src 路径错了显示破图** |
| `<div>` | 无意义容器(占位) | 配合 CSS 布局 |
| `<head>` | 浏览器看的元信息 | 用户看不到内容 |
| `<body>` | 用户看的全部内容 | 内容都放这里 |

## 14.3 CSS 三种写法

### 🟡 选中谁 → 设啥 → 设成啥

> 📌 **知识点说明**:CSS 核心套路:**选择器(选中谁)+ 属性(设啥)+ 值(设成啥)**。`class` 用 `.` 选中,`id` 用 `#` 选中。三种写法:内联 / 内部 / 外部。

```css
/* ① 外部样式表(推荐,写在 .css 文件) */
/* 选择器:  tag标签  .class类  #id */
body {
    background-color: #f0f0f0;   /* 背景颜色 */
    font-family: sans-serif;      /* 字体 */
}
.highlight {
    color: red;                   /* .类名 选中所有 class="highlight" */
}
#main-title {
    font-size: 24px;              /* #id名 选中唯一 id="main-title" */
}
```

| 写法 | 位置 | 适用 |
|------|------|------|
| 内联 | `<p style="color:red">` | 临时微调(不推荐) |
| 内部 | `<style>` 标签写在 HTML 里 | 单页面小项目 |
| 外部 | 单独 `.css` 文件 + `<link>` | 多页面(推荐) |

## 14.4 前端框架概念(了解即可)

### ⚪ 数据变 → 界面自动更新

> 📌 **知识点说明**:React / Vue 等框架解决核心痛点:**数据变了,页面自动跟着变**,不用手动操作 DOM。**Streamlit 就是迷你前端框架** —— 用纯 Python 写界面,自动生成 HTML/CSS/JS。

| 对比 | React / Vue | Streamlit |
|------|------------|-----------|
| 语言 | JavaScript | Python |
| 定位 | 大型前端应用 | 数据/AI 应用原型 |
| 谁用 | 前端工程师 | **数据/AI 开发者** |
| 特点 | 强大但复杂 | 简单但定制受限 |

💡 **定位总结**:AI 应用开发者**不需要**精通 React/Vue,会用 Streamlit 快速做出能交互的界面就够了。

---

## 🎯 第 14 章 面试/开发高频考点

**必问**(很少问前端细节):
- 前端三大件分别是什么?(HTML 结构 / CSS 样式 / JS 交互)

**加分项**:
- 能看懂 HTML 结构、会写基本 CSS 选择器
- 知道 Streamlit = 迷你前端框架(Python 自动生成前端)

**冷门**:
- `<head>` vs `<body>` 的区别
- class(.) vs id(#) 选择器区别

---

# 第 15 章 Streamlit 入门(Day37)

## 15.1 运行原理:每次交互从头重跑

### 🔴 脚本是从上到下整个重跑一遍

> 📌 **知识点说明**:Streamlit 最特别的地方:**你每次点按钮/拖滑块,整个脚本都会从头到尾重新执行一遍**。这就是为什么"普通变量会被重置",也解释了为什么要用 session_state(下一章)。
>
> 类比:点餐机——你每点一下,服务员(脚本)就重新按你的选择做一份新界面。

```python
import streamlit as st

st.title("我的第一个 Streamlit 应用")      # 标题

name = st.text_input("你的名字", "请输入")  # 文本输入框
# 每次点按钮 → 整个脚本重跑 → name 是新的值

if st.button("打招呼"):                    # 按钮
    st.write(f"你好,{name}!")              # 输出
```

💡 **速记**:Streamlit 脚本 = 每次交互都"刷新重跑",**界面永远是"当前状态"渲染出来的**。

## 15.2 常用控件速查表

### 🔴 六大控件

> 📌 **知识点说明**:控件 = 让用户输入/选择的组件。每个控件返回**用户当前选的值**,直接用变量接住。

```python
import streamlit as st

st.text_input("单行文本输入")         # 返回字符串
st.text_area("多行文本输入")          # 返回多行字符串
st.number_input("数字输入", min_value=0, max_value=100, value=50)  # 返回数字
st.slider("滑块", 0, 100, 50)        # 返回滑到的数字
st.selectbox("下拉选择", ["选项A", "选项B"])  # 返回选中的选项
st.checkbox("勾选框")                # 返回 True/False
st.radio("单选框", ["男", "女"])     # 返回选中的项
st.button("按钮")                    # 点一下返回 True(只这一次重跑为 True)
```

| 控件 | 返回值 | 常用场景 |
|------|--------|---------|
| st.text_input | 字符串 | 输入用户名、问题 |
| st.number_input | 数字 | 输入数量、价格 |
| st.slider | 数字 | 调参数(温度、数量) |
| st.selectbox | 选项值 | 下拉选分类 |
| st.checkbox | 布尔 | 开关选项 |
| st.button | 布尔(仅当次重跑) | 触发动作 |

## 15.3 反馈消息

### 🟡 success / warning / error 三色

> 📌 **知识点说明**:给用户反馈不同状态:**绿色成功、黄色警告、红色错误**。

```python
st.success("操作成功!")      # 绿色 ✓
st.warning("注意,数据会覆盖") # 黄色 ⚠
st.error("出错了!")          # 红色 ✕
st.info("提示信息")          # 蓝色 ℹ
```

## 15.4 展示数据:dataframe vs table

### 🟡 可交互 vs 静态

> 📌 **知识点说明**:`st.dataframe` 展示的是**可交互表格**(能排序、滚动、选择),`st.table` 是**静态快照**。数据展示首选 dataframe。

```python
import pandas as pd

df = pd.DataFrame({"姓名": ["张三", "李四"], "分数": [90, 85]})
st.dataframe(df)   # 可交互:能排序、滚动
st.table(df)       # 静态:固定不变
```

## 15.5 结合 FastAPI:requests 调后端

### 🔴 前后端分离的核心雏形(最重要!)

> 📌 **知识点说明**:Streamlit 是**前端**,FastAPI 是**后端**,两者通过 HTTP + JSON 通信。前端用 `requests.post/get` 调后端接口,**前端完全不碰数据库** —— 数据库只有后端碰。

```python
import streamlit as st
import requests

# 用户输入
question = st.text_input("问一个问题:")
if st.button("提问"):
    # 1. 前端把数据发给后端(POST + JSON)
    resp = requests.post(
        "http://localhost:8000/api/chat",   # 后端的地址
        json={"text": question},            # 用 json= 发 JSON(不是 data=!)
        timeout=10,                          # 超时保护
    )
    # 2. 后端返回 JSON,前端解析显示
    if resp.status_code == 200:
        answer = resp.json()["answer"]
        st.success(f"回答: {answer}")
    else:
        st.error(f"请求失败: {resp.status_code}")
```

⚠️ **易错点**:
```python
# ❌ 传参用 data=(字符串,后端收不到 JSON)
# requests.post(url, data={"text": question})
# ✅ 传 JSON 必须用 json=(requests 自动转 JSON + 设 Content-Type)
requests.post(url, json={"text": question})
```

| 对比 | 查询参数 | JSON 请求体 |
|------|---------|------------|
| requests 写法 | `params={"page": 2}` | `json={"text": "你好"}` |
| 对应 FastAPI | 查询参数 | 请求体 Pydantic |
| URL 示例 | `?page=2` | 在 body 里 |

---

## 🎯 第 15 章 面试/开发高频考点

**必问**:
1. Streamlit 运行原理?(每次交互整个脚本重跑)
2. 前端怎么调后端?(requests + json= 发 POST,resp.json() 收)

**加分项**:
- 会一套完整交互(输入 → 按钮 → 调后端 → 显示结果)
- 知道 dataframe 可交互 vs table 静态

**冷门**:
- st.button 只在"被点的这次重跑"返回 True
- 前端不碰数据库,只通过 HTTP 走后端

---

# 第 16 章 Streamlit 进阶(Day38)

## 16.1 session_state:跨交互记忆(核心!)

### 🔴 解决"脚本重跑丢数据"

> 📌 **知识点说明**:脚本每次重跑,普通变量都归零。**`st.session_state` 是存在"会话级"的内存,重跑不清空**,用来存"跨交互需要记住的状态"(计数器、当前页数、登录状态)。

```python
import streamlit as st

# 1. 初始化:先检查有没有,没有才赋值(重要!)
if "count" not in st.session_state:
    st.session_state.count = 0      # 第一次运行:建一个 count=0

# 2. 使用:每次按钮 +1
if st.button("点我"):
    st.session_state.count += 1     # 存在 session_state,重跑不清空

# 3. 显示:永远显示最新值
st.write(f"点击了 {st.session_state.count} 次")
```

⚠️ **易错点**:
```python
# ❌ 直接 st.session_state.count += 1(没初始化)→ AttributeError
# ❌ if 判断后忘了加 .state 前缀 → '<=' not supported
# ✅ 套路:if "键" not in st.session_state: 初始化 → 之后用 st.session_state.键
```

| 对比 | 普通变量 | st.session_state |
|------|---------|-----------------|
| 重跑后 | 清零 | 保留 |
| 存什么 | 单次计算的中间值 | 需要跨交互的状态 |
| 初始化 | 直接赋值 | `if 键 not in` 判断 |
| 页面刷新 | 重跑(仍会重置?否) | 开新会话才重置 |

## 16.2 布局:sidebar / columns / tabs

### 🟡 把界面排成结构

> 📌 **知识点说明**:Streamlit 布局组件:**sidebar 侧边栏、columns 分栏(可设宽度比例)、tabs 标签页、expander 折叠、container 容器**。

```python
import streamlit as st

# 侧边栏:放导航/设置
with st.sidebar:
    st.title("控制面板")
    page = st.selectbox("选择页面", ["首页", "数据", "设置"])

# 分栏:[1, 3] = 左栏占 1 份,右栏占 3 份
left, right = st.columns([1, 3])
with left:
    st.write("左栏(窄)")
with right:
    st.write("右栏(宽)")

# 标签页
tab1, tab2 = st.tabs(["提问", "历史"])
with tab1:
    st.write("这里是提问页")
with tab2:
    st.write("这里是历史页")

# 折叠容器:默认收起来
with st.expander("点击展开详情"):
    st.write("被折叠的内容")
```

| 组件 | 作用 | 常用场景 |
|------|------|---------|
| st.sidebar | 侧边栏 | 导航、设置项 |
| st.columns([1,3]) | 左右分栏(宽度比例) | 输入区 + 展示区 |
| st.tabs(["A","B"]) | 标签页 | 功能分区 |
| st.expander("标题") | 折叠面板 | 收起次要内容 |
| st.container() | 容器 | 逻辑分组 |

## 16.3 表单 st.form

### 🟡 多个输入一起提交

> 📌 **知识点说明**:`st.form` 把多个输入框包在一起,**点一个提交按钮,一次性全部提交**。**必须用 `st.form_submit_button` 不能用 `st.button`**(否则破坏 form 机制,页面会一直重跑)。

```python
with st.form("login_form"):
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")  # type="password" 显示圆点
    submitted = st.form_submit_button("登录")          # ← 关键:用 form 的按钮

if submitted:
    st.success(f"提交了 {username}")
```

## 16.4 文件上传

### 🟡 file_uploader + getvalue().decode

> 📌 **知识点说明**:上传文件用 `file_uploader`,返回文件对象。**读取内容:先判 `is not None`,再 `getvalue()` 拿字节,文本文件要 `.decode()` 成字符串**。

```python
uploaded = st.file_uploader("上传文件", type=["txt", "csv"])

if uploaded is not None:                    # 必须判断有没有传
    content = uploaded.getvalue().decode("utf-8")  # 字节 → 字符串
    st.text(content[:200])                   # 显示前 200 字
```

## 16.5 图表:line / bar / pyplot / plotly

### 🟡 四类图表对比

> 📌 **知识点说明**:Streamlit 原生图表(简单)+ matplotlib(静态图)+ plotly(交互图)。

```python
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

df = pd.DataFrame({"月份": ["1月", "2月", "3月"], "销量": [100, 150, 120]})

st.line_chart(df.set_index("月份"))   # 原生折线图(最简单)
st.bar_chart(df.set_index("月份"))    # 原生柱状图
st.area_chart(df.set_index("月份"))   # 原生面积图

# matplotlib 静态图
fig, ax = plt.subplots()
ax.plot(df["月份"], df["销量"])
st.pyplot(fig)                        # 用 st.pyplot 显示

# plotly 交互图(可悬停/缩放)
fig2 = px.line(df, x="月份", y="销量")
st.plotly_chart(fig2)
```

| 图表 | 交互性 | 复杂度 | 场景 |
|------|--------|--------|------|
| st.line_chart | 无 | 最低 | 快速看趋势 |
| st.pyplot(matplotlib) | 无 | 中 | 精细控制样式 |
| st.plotly_chart | 有(悬停/缩放) | 中高 | 需要交互的数据分析 |

## 16.6 综合案例:提问历史(多轮对话雏形)

### 🟡 把 session_state + 布局 + 调后端串起来

> 📌 **知识点说明**:一个"提问 → 记录历史 → 侧边栏查看全部"的小应用,是 Day39-40 全栈项目的前端雏形。

```python
import streamlit as st
import requests

# 历史存 session_state(重跑不清空)
if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("你的问题:")
if st.button("提问"):
    resp = requests.post("http://localhost:8000/api/chat", json={"text": question})
    answer = resp.json()["answer"]
    st.session_state.history.append({"q": question, "a": answer})  # 存进历史
    st.success(f"回答: {answer}")

# 侧边栏显示全部历史
with st.sidebar:
    st.title("历史记录")
    if st.checkbox("显示全部"):
        for item in st.session_state.history:
            st.write(f"**Q:** {item['q']}")
            st.write(f"A: {item['a']}")
            st.divider()
```

---

## 🎯 第 16 章 面试/开发高频考点

**必问**:
1. session_state 是干嘛的?为什么需要?(脚本重跑丢数据,用它跨交互记忆)
2. st.form 里为什么用 form_submit_button 不用 button?(否则破坏一次性提交)

**加分项**:
- 会用 columns 宽度比例、tabs 分区
- 会 file_uploader + getvalue().decode 读文件
- 会 st.plotly_chart 显示交互图表

**冷门**:
- `type="password"` 让输入显示为圆点
- 刷新页面 = 新会话, session_state 重置

---

# 第 17 章 综合项目:AI 应用开发模板(Day39-40)【全栈核心】

## 17.1 全栈架构总览

### 🔴 前端 + 后端 + 数据库三层分离

> 📌 **知识点说明**:Day39-40 把前面所有知识串成**可复用的全栈骨架**(AI 应用开发模板),后续接真 LLM 不用改架构。三层:**Streamlit 前端(发 HTTP)→ FastAPI 后端(管业务)→ MySQL 数据库(存数据)**。前端永远不直接碰数据库。

```
┌─────────────┐  HTTP+JSON  ┌─────────────┐  SQL  ┌─────────┐
│ Streamlit 前端 │ ──────────► │ FastAPI 后端  │ ─────► │  MySQL   │
│  (8501 端口)  │ ◄────────── │  (8000 端口)  │ ◄───── │ 数据库   │
└─────────────┘  响应 JSON   └─────────────┘       └─────────┘
  用户看到的界面               接口 + 业务逻辑            存数据
```

## 17.2 后端工程目录:四文件拆分

### 🔴 生产级结构(config / database / models / main)

> 📌 **知识点说明**:工程化标准结构——**职责分离,每个文件只管一件事**。这样代码能长大、能测试、能多人协作。

```
backend/
├── config.py        # 配置:读 .env 环境变量
├── database.py      # 数据库:引擎 + 会话工厂 + get_db + Base
├── models.py        # 模型:Pydantic 请求/响应 + SQLAlchemy ORM
├── main.py          # 路由:FastAPI 应用 + 所有接口
└── requirements.txt # 依赖清单
```

**① config.py(配置)**:
```python
import os
from dotenv import load_dotenv

load_dotenv()   # 加载 .env

# 数据库地址(异步 MySQL 驱动)
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL",
    "mysql+aiomysql://root:123456@localhost:3306/ai_app?charset=utf8mb4")

# CORS 白名单:逗号分隔 → 列表
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(",")

# Debug 开关:字符串 → 布尔
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

**② database.py(数据库)**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from config import ASYNC_DATABASE_URL

# 异步引擎
engine = create_async_engine(ASYNC_DATABASE_URL, pool_pre_ping=True)

# 会话工厂(expire_on_commit=False 是异步必配)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 基类:所有表自动带创建/更新时间
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

# 依赖注入:每个请求一个会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
```

**③ models.py(Pydantic + ORM)**:
```python
from pydantic import BaseModel
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# ---- ORM 模型(对应数据库表)----
class Prompt(Base):
    __tablename__ = "prompts"
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    question: Mapped[str] = mapped_column(Text, comment="问题")
    answer: Mapped[str] = mapped_column(Text, comment="回答")

# ---- Pydantic 模型(接口收发)----
class PromptCreate(BaseModel):        # 请求体:前端传来存什么
    question: str
    answer: str

class PromptOut(PromptCreate):        # 响应体:返回给前端什么
    id: int

class ChatRequest(BaseModel):         # chat 接口请求体
    text: str
```

## 17.3 接口设计

### 🔴 五个接口 = 一个全栈 API 的骨架

> 📌 **知识点说明**:模板提供健康检查 / 保存 / 查询(分页+按 ID)/ 对话(mock LLM)/ 删除。**接口格式定好后,把 mock 换成真 LLM,前端一行不用改** —— 这就是"接口先行"的好处。

| 方法 | 路径 | 作用 | 关键点 |
|------|------|------|--------|
| GET | /api/health | 健康检查 | 返回 {status: ok} |
| POST | /api/prompts | 保存提问 | 201 + response_model |
| GET | /api/prompts | 查询(分页/按ID) | 列表+总数两查询 |
| POST | /api/chat | 对话(mock LLM) | 只回答不存库 |
| DELETE | /api/prompts/{prompt_id} | 删除 | 204 |

```python
# ① 健康检查
@app.get("/api/health")
async def check_health():
    return {"status": "ok"}

# ② 保存提问:POST + 201 + Pydantic v2 model_dump
@app.post("/api/prompts", response_model=PromptOut, status_code=201)
async def save_prompts(prompt: PromptCreate, db: AsyncSession = Depends(get_db)):
    data = prompt.model_dump()          # v2 用 model_dump,不要用 __dict__
    prompt_obj = Prompt(**data)
    db.add(prompt_obj)
    await db.commit()
    await db.refresh(prompt_obj)
    return prompt_obj

# ③ 查询:分页 + 按 ID 过滤(列表查询和计数查询是两句话)
@app.get("/api/prompts")
async def get_prompts_list(
    db: AsyncSession = Depends(get_db),
    prompt_id: int | None = None,
    page: int = 1,
    size: int = 5,
):
    skip = (page - 1) * size                              # 分页偏移
    stmt = select(Prompt).order_by(Prompt.id.desc())      # 倒序
    count_stmt = select(func.count(Prompt.id)).select_from(Prompt)  # 计数
    if prompt_id:                                         # 按 ID 过滤时两个查询都要加
        stmt = stmt.where(prompt_id == Prompt.id)
        count_stmt = count_stmt.where(prompt_id == Prompt.id)
    result = await db.execute(stmt.offset(skip).limit(size))
    prompts = result.scalars().all()
    total = (await db.execute(count_stmt)).scalar_one()   # 取那一个数字
    return {
        "data": prompts,
        "pagination": {
            "page": page, "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if size > 0 else 0,
        },
    }

# ④ 对话(mock LLM):接口格式和真 LLM 一致 → 下周只换函数内部
def get_llm_answer(text: str) -> str:
    rules = {"你好": "你好!", "天气": "查不了天气", "python": "学得好!"}
    for keywords, answer in rules.items():   # ⚠️ 必须 .items(),直接遍历字典只拿 key
        if keywords in text:
            return answer
    return f"你问的是:{text},我是模拟回答"

@app.post("/api/chat", status_code=201)
async def get_llm_chat(req: ChatRequest):
    return {"answer": get_llm_answer(req.text)}

# ⑤ 删除:先查 → 404 → 删 → commit → 204
@app.delete("/api/prompts/{prompt_id}", status_code=204)
async def delete_prompts(prompt_id: int, db: AsyncSession = Depends(get_db)):
    prompt = await db.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="该提问不存在")
    await db.delete(prompt)
    await db.commit()
    return None
```

## 17.4 前端页面:提问 → 回答 → 历史

### 🔴 全链路:输入 → 调后端 → 存库 → 显示

> 📌 **知识点说明**:前端 app.py 的完整逻辑。**核心思想:前端只管"发请求 + 展示",存哪、怎么存全是后端的事。**

```python
import streamlit as st
import requests

BASE_URL = "http://localhost:8000"     # 后端地址

st.title("🤖 AI 助手(模板)")

# ① 提问 → 调后端 → 显示回答(走 /api/chat,mock LLM)
question = st.text_input("输入你的问题:")
if st.button("提问"):
    resp = requests.post(f"{BASE_URL}/api/chat", json={"text": question}, timeout=10)
    if resp.status_code == 201:
        answer = resp.json()["answer"]
        st.success(f"🤖 {answer}")
        # ② 同时存库:POST /api/prompts(前端打包问题+回答)
        requests.post(f"{BASE_URL}/api/prompts", json={"question": question, "answer": answer})
    else:
        st.error("请求后端失败")

# ③ 显示历史:GET /api/prompts(分页)
st.subheader("提问历史")
page = st.session_state.get("page", 1)      # 当前页存 session_state!
resp = requests.get(f"{BASE_URL}/api/prompts", params={"page": page, "size": 5})
data = resp.json()
for item in data["data"]:
    st.write(f"**Q:** {item['question']}")
    st.write(f"A: {item['answer']}")
    st.divider()
# 分页按钮(边界判断)
total_pages = data["pagination"]["total_pages"]
col1, col2 = st.columns(2)
with col1:
    if st.button("上一页", disabled=(page <= 1)):
        st.session_state.page -= 1
with col2:
    if st.button("下一页", disabled=(page >= total_pages)):
        st.session_state.page += 1
```

## 17.5 前后端分离的关键思想

### 🔴 三个"为什么"

> 📌 **知识点说明**:全栈项目最容易困惑的点,用三句话记牢:

| 问题 | 答案 |
|------|------|
| 前端为什么不直接连数据库? | 前后端分离:前端只通过 HTTP 调后端,数据库归后端管(安全 + 解耦) |
| 查询参数用什么传? | `requests.get(url, params={"page": 1})` → 对应后端查询参数 |
| 页数为什么必须存 session_state? | 脚本重跑普通变量清零,页数必须跨交互记忆 |
| id 为什么不是连续的序号? | id 是身份标识,删了就没了,不会重排(外键引用) |

## 17.6 SQLite → MySQL 改造对照

### 🟡 本地学习 → 生产数据库

> 📌 **知识点说明**:本地用 SQLite 练手,生产换 MySQL。**核心:驱动串变化 + 编码 charset=utf8mb4 + 连接池参数**。

| 对比 | SQLite | MySQL |
|------|--------|-------|
| 连接串 | `sqlite+aiosqlite:///./app.db` | `mysql+aiomysql://user:pass@host:3306/ai_app?charset=utf8mb4` |
| 建表 | create_all 够用 | 用 **Alembic 迁移**(上线表结构管理) |
| 编码 | 无 | 必须 `charset=utf8mb4`(支持 emoji/中文) |
| 连接保活 | 无 | `pool_pre_ping=True`(防止连接断开报错) |
| 容器连宿主库 | 直接用 localhost | `host.docker.internal`(Day41) |

---

## 第 17 章【错误原因 + 修复方案】模块

### ❌ 问题 1:mock 字典遍历只取到 key

**错误原因**:`for keywords, answer in rules:` 直接遍历字典,只拿到 key 不拿 value → "天气" 命中时 `answer` 是字符串 "天气" 里的字,回答返回 "气"。

**修复方案**:
```python
# ❌ for keywords, answer in rules:
# ✅ 遍历字典要用 .items()
for keywords, answer in rules.items():
```

### ❌ 问题 2:删除接口没 commit

**错误原因**:`await db.delete(prompt)` 后直接 return,忘了 `await db.commit()` → 删除不生效(重启后还在)。

**修复方案**:删完必须 commit:
```python
await db.delete(prompt)
await db.commit()   # ✅ 没有 commit 数据库不会变
```

### ❌ 问题 3:路由路径与函数参数不匹配

**错误原因**:路由写 `/api/prompts/{id}`,函数参数却是 `prompt_id` → FastAPI 找不到对应路径参数报错。

**修复方案**:两边保持一致:
```python
@app.delete("/api/prompts/{prompt_id}")   # ✅ 路径和参数都用 prompt_id
async def delete_prompts(prompt_id: int, ...):
```

### ❌ 问题 4:前端删除请求乱传 json body

**错误原因**:把 delete_id 塞进 JSON body,后端路径参数收不到。

**修复方案**:删除 id 放**路径**里:
```python
# ✅ id 走 URL 路径
requests.delete(f"{BASE_URL}/api/prompts/{delete_id}")
```

### ❌ 问题 5:session_state 初始化顺序错误

**错误原因**:页面还没 `page` 键就 `st.session_state.page += 1` → AttributeError;或漏写 `.state` 前缀 → `'<=' not supported`。

**修复方案**:
```python
if "page" not in st.session_state:      # 先初始化
    st.session_state.page = 1
# 之后统一用 st.session_state.page
```

---

## 🎯 第 17 章 面试/开发高频考点

**必问**:
1. 前后端分离架构怎么讲?(前端 HTTP 调后端,后端管数据库)
2. 为什么接口格式先定好再换真 LLM?(接口先行,mock 和真模型同格式)
3. 分页接口返回什么?(data + pagination{page,size,total,total_pages})

**加分项**:
- 会用四文件工程结构(config/database/models/main)
- 知道异步 get_db、expire_on_commit=False
- 知道 model_dump() 是 Pydantic v2 写法

**冷门**:
- 列表查询和计数查询要写两句(select + select(func.count))
- id 不连续是正常的(身份标识,不重排)

---

# 📕 本册错题本

| # | 错误代码/场景 | 报错/现象 | 原因 | 修复 |
|---|--------------|----------|------|------|
| 1 | `for k, v in rules` 遍历字典 | 回答只取到 key | 字典默认遍历 key | 用 `.items()` |
| 2 | 删除接口漏 `db.commit()` | 删除不生效 | 没提交事务 | 删完 commit |
| 3 | 路由 `{id}` 函数参数 prompt_id | 路径参数不匹配报错 | 命名不一致 | 路径参数名一致 |
| 4 | 前端删除 id 塞 json body | 后端收不到 | 删除 id 走路径 | `requests.delete(url/{id})` |
| 5 | session_state 未初始化就使用 | AttributeError | 先判断后使用 | `if 键 not in` 初始化 |
| 6 | `st.session_state.page` 漏 .state | `'<=' not supported` | 写成整个容器 | 统一 `.page` 前缀 |
| 7 | requests 传参用 data= | 后端收不到 JSON | 格式错误 | 用 `json=` |
| 8 | 内建 `id()` 当变量名 | 函数被覆盖 | 命名冲突 | 用 delete_id 等 |
| 9 | 分页按钮无边界判断 | 一直点下去报错 | 没禁用 | `disabled=(page<=1)` |
| 10 | 搜索后页数没重置 | 页数越界 | 状态没清 | 搜索时 page 重置 1 |
