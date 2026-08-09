"""
Day 38 练习题：Streamlit 进阶（布局/表单/上传/图表/会话状态）
============================================================

⚠️ 前置准备：
    pip install streamlit pandas matplotlib plotly

💡 学习方式：
    每个实验对照 学习笔记.md。把留白的 ____ 补全，存成 app.py 用 `streamlit run` 运行。

🛠 关于「留白」：
    关键行留 ____ 自己填，每题开头有 💡 提示。答案在文件最底部。

⚠️ 重点提醒：参考答案在【文件最底部】且隔开大量空行，做完再看！
"""

import streamlit as st  # 已导入

# ============================================================
# 【实验 1】布局：侧边栏 / 分栏 / 标签页 / 折叠面板
# ============================================================
"""
目标：把界面排整齐

💡 提示：侧边栏用 st.sidebar.组件；分栏 st.columns(2)；标签页 st.tabs；折叠 st.expander。

# 侧边栏
st._sidebar.title___("控制面板")                      # 【填空 1】侧边栏标题
mode = st._sidebar.selectbox___("模式", ["简洁", "完整"])  # 【填空 2】侧边栏下拉框

# 分栏
col1, col2 = st._columns___(2)                  # 【填空 3】分成两列
with col1:
    st.write("左列")
    a = st.button("左按钮")
with col2:
    st.write("右列")
    b = st.button("右按钮")

# 标签页
tab1, tab2 = st._tabs___(["介绍", "详情"])   # 【填空 4】两个标签页
with tab1:
    st.write("这是介绍")
with tab2:
    st.write("这是详情")

# 折叠面板
with st.__expander__("点击展开更多帮助"):        # 【填空 5】折叠面板
    st.write("藏起来的内容")
"""
st._sidebar.title___("控制面板")  # 填空 1
mode = st._sidebar.selectbox___("模式", ["简洁", "完整"])  # 填空 2

col1, col2 = st.__columns__(2)  # 填空 3
with col1:
    st.write("左列")
    a = st.button("左按钮")
with col2:
    st.write("右列")
    b = st.button("右按钮")

tab1, tab2 = st.__tabs__(["介绍", "详情"])  # 填空 4
with tab1:
    st.write("这是介绍")
with tab2:
    st.write("这是详情")

with st._expander___("点击展开更多帮助"):  # 填空 5
    st.write("藏起来的内容")

# 📝 测试 1.1：st.columns(2) 返回什么？为什么用 with 语句？
# 答：返回_容器___，用 with 是因为把组件_col1放___进这个容器里。
# 💡 提示：返回两个"容器对象"；with 是"放进去"。

# ❓ 问题 1.2：st.columns([1, 3]) 和 st.columns(2) 有什么区别？
# 答：__st.columns([1, 3])是两个columns对象 第一个对象占据位宽度1份 第二个占3份 __st.columns(2)代表两个容器对象默认两个占据的宽度平分____________________________________________________


# ============================================================
# 【实验 2】表单：多个输入一起提交
# ============================================================
"""
目标：用 st.form 让多个输入一次性提交，而不是每次改动都重跑

💡 提示：with st.form("名字") 包起来；提交按钮必须用 st.form_submit_button。

with st.__form__("登录表单"):               # 【填空 6】表单容器
    username = st.__text_input__("用户名")        # 【填空 7】文本框
    password = st.__text_input__("密码", type="password")  # 【填空 8】密码框
    submit = st._form_submit_button___("登录")            # 【填空 9】表单提交按钮
"""
with st._form___("登录表单"):  # 填空 6
    username = st._text_input___("用户名")  # 填空 7
    password = st._text_input___("密码", type="password")  # 填空 8
    submit = st.__form_submit_button__("登录")  # 填空 9

# 📝 测试 2.1：表单内用 st.button 可以吗？为什么？
# 答：_不可以___，因为表单内必须用__表单提交按钮____才能触发提交。
# 💡 提示：st.button 会单独触发重跑，破坏"一起提交"。

# ❓ 问题 2.2：submit 的值是什么类型？什么时候为 True？
# 答：____类型，点提交按钮时返回____。
# 💡 提示：和 st.button 一样是布尔值。


# ============================================================
# 【实验 3】文件上传
# ============================================================
"""
目标：上传并读取一个文件

💡 提示：st.file_uploader(标签, type=[...])；判断 uploaded is not None；用 .getvalue() 读内容。

uploaded = st._file_uploader___("上传一个文本文件", type=["txt", "csv"])  # 【填空 10】文件上传
if uploaded is not _None___:              # 【填空 11】没上传时是 None，要判断
    st.write(f"文件名：{uploaded.__name__}")      # 【填空 12】文件名属性
    content = uploaded._getvalue___().decode("utf-8")  # 【填空 13】读字节内容
    st.text(content)
"""
uploaded = st._file_uploader___("上传一个文本文件", type=["txt", "csv"])  # 填空 10
if uploaded is not __None__:  # 填空 11
    st.write(f"文件名：{uploaded._name___}")  # 填空 12
    content = uploaded.__getvalue__().decode("utf-8")  # 填空 13
    st.text(content)

# 📝 测试 3.1：没上传文件时，uploaded 的值是什么？为什么代码要判断它？
# 答：值是_None___，因为不判断直接访问会__报错__。
# 💡 提示：返回 None（不是一个对象）。

# ❓ 问题 3.2：type=["txt","csv"] 的作用是什么？
# 答：___________声明上传文件的类型是txt,csv_____________________________________________


# ============================================================
# 【实验 4】图表展示
# ============================================================
"""
目标：画折线图、柱状图、Matplotlib 图

💡 提示：st.line_chart / st.bar_chart / st.pyplot。

import pandas as pd
data = pd.DataFrame({"月份": [1,2,3,4], "销量": [10, 20, 15, 30]})
st._line_chart___(data)      # 【填空 14】折线图
st._bar_chart___(data)      # 【填空 15】柱状图

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(data["月份"], data["销量"])
ax.set_title("销量趋势")
st.__pyplot__(fig)       # 【填空 16】把 matplotlib 图显示出来
"""
import pandas as pd

data = pd.DataFrame({"月份": [1, 2, 3, 4], "销量": [10, 20, 15, 30]})
st._line_chart___(data)  # 填空 14
st._bar_chart___(data)  # 填空 15

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(data["月份"], data["销量"])
ax.set_title("销量趋势")
st._pyplot___(fig)  # 填空 16

# 📝 测试 4.1：st.line_chart 和 st.bar_chart 的区别是什么？
# 答：______line_chart是折线图 bar_chart是柱状图__________________________________________________

# ❓ 问题 4.2（选做）：st.pyplot 和 st.plotly_chart 有什么区别？
# 答：_________st.pyplot是静态图只能下载等____st.plotly_chart可交互可悬停缩放___________________________________________
# 💡 提示：一个静态图，一个可交互（悬停/缩放）。


# ============================================================
# 【实验 5】会话状态 session_state（重点，最容易错）
# ============================================================
"""
目标：理解脚本每次重跑，普通变量会丢，用 session_state 记住数据

先运行下面这段，观察"计数"是否永远停在 1：
"""
count = 0
if st.button("加一（普通变量）"):
    count += 1
st.write(f"普通变量计数：{count}")

# 📝 测试 5.1：为什么普通变量 count 永远停在 1？
# 答：因为每次点按钮，脚本从头重跑，count = 0 ____被执行。
# 💡 提示：重跑会让赋值语句重新执行。

# 现在用 session_state 改对：
# 💡 提示：先初始化 if "count" not in st.session_state: st.session_state.count = 0
#         再在按钮里用 st.session_state.count 累加。

if "count" not in st._session_state.count___:  # 【填空 17】判断键是否存在
    st._session_state___.count = 0  # 【填空 18】初始化

if st._button___("加一（session_state）"):  # 【填空 19】按钮
    st.__session_state__.count += 1  # 【填空 20】累加

st.write(f"session_state 计数：{st._session_state___.count}")  # 【填空 21】读取
"""
# 提示：上面实验5的留白，用：

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("加一（session_state）"):
    st.session_state.count += 1

st.write(f"session_state 计数：{st.session_state.count}")
"""
# 📝 测试 5.2：改成 session_state 后，点多次按钮，计数会持续累加吗？
# 答：会。因为初始化只在_第一次不存在___时执行。
# 💡 提示：if "count" not in ... 只在第一次为 True。

# ❓ 问题 5.3：session_state 最适合解决 AI 应用的什么问题？
# 答：_____对话上下文，用户的选择，程序保持的状态___________________________________________________
# 💡 提示：想想多轮对话、记住用户点过什么。


# ============================================================
# 【实验 6】综合：用 session_state 做一个"提问记录"
# ============================================================
"""
目标：把 session_state + 输入 + 展示串起来（接近 Day39-40 项目雏形）

💡 提示：用 st.session_state.history 存列表；初始化；提交时 append；循环展示。

if "history" not in st._session_state___:           # 【填空 22】初始化列表
    st._session_state___.history = []

prompt = st.__text_input__("输入你的问题：")      # 【填空 23】文本框
if st._button___("提交"):                    # 【填空 24】按钮
    st._session_state___.history.append(prompt)     # 【填空 25】记住本次提问
    st.__success__("已保存")                  # 【填空 26】成功提示

st.write("历史记录：")
for h in st._session_state___.history:              # 【填空 27】遍历历史
    st.write(f"- {h}")
"""
if "history" not in st._session_state___:  # 填空 22
    st.____.history = []

prompt = st._text_input___("输入你的问题：")  # 填空 23
if st.__button__("提交"):  # 填空 24
    st._session_state___.history.append(prompt)  # 填空 25
    st.__success__("已保存")  # 填空 26

st.write("历史记录：")
for h in st._session_state___.history:  # 填空 27
    st.write(f"- {h}")

# 写在ask.py
# 📝 测试 6.1：提交几次后，历史记录会累积吗？刷新页面后还在吗？
# 答：提交几次会_累积___；刷新页面后_不存在 会开新的会话___（因为刷新会开新会话）。
# 💡 提示：session_state 是"会话内"保持，刷新页面会重置。

# ❓ 问题 6.2：这个"提问记录"能力，稍作改造就能变成什么 AI 应用？
# 答：___________多轮对话/聊天记录/问答AI_____________________________________________
# 💡 提示：多轮对话/聊天记录。


# ============================================================
# 💡 参考答案（完成所有练习后再看！注意这一行下面空了很多行）
# ============================================================


"""


（参考答案在下面，先别急着翻）




实验 1 参考答案
--------------
填空 1: st.sidebar.title
填空 2: st.sidebar.selectbox
填空 3: st.columns
填空 4: st.tabs
填空 5: st.expander
测试 1.1: 返回两个"容器对象"；用 with 是把组件"放进去"这个容器。
问题 1.2: st.columns(2) 两列等宽；st.columns([1,3]) 指定宽度比例（左1份右3份）。


实验 2 参考答案
--------------
填空 6: st.form
填空 7: st.text_input
填空 8: st.text_input
填空 9: st.form_submit_button
测试 2.1: 不可以。表单内必须用 st.form_submit_button，否则 st.button 会破坏"一起提交"机制。
问题 2.2: 布尔类型（bool），点提交按钮时返回 True。


实验 3 参考答案
--------------
填空 10: st.file_uploader
填空 11: None
填空 12: .name
填空 13: .getvalue()
测试 3.1: 没上传时是 None，不判断直接访问会报错（AttributeError）。
问题 3.2: type=["txt","csv"] 限制用户只能上传这两种类型。


实验 4 参考答案
--------------
填空 14: st.line_chart
填空 15: st.bar_chart
填空 16: st.pyplot
测试 4.1: 折线图 vs 柱状图，展示方式不同，数据相同。
问题 4.2: st.pyplot 是 matplotlib 静态图；st.plotly_chart 是交互图（可悬停/缩放）。


实验 5 参考答案
--------------
填空 17: st.session_state
填空 18: st.session_state
填空 19: st.button
填空 20: st.session_state
填空 21: st.session_state
测试 5.1: 每次点按钮脚本从头重跑，count=0 又重新执行，所以永远是 1。
测试 5.2: 会持续累加。初始化只在"第一次"（键不存在时）执行。
问题 5.3: 多轮对话的上下文、记住用户数据/选择、页面切换保持状态。


实验 6 参考答案
--------------
填空 22: st.session_state
填空 23: st.text_input
填空 24: st.button
填空 25: st.session_state
填空 26: st.success
填空 27: st.session_state
测试 6.1: 提交几次会累积；刷新页面后"不在"（刷新开新会话，session_state 重置）。
问题 6.2: 多轮对话 / 聊天记录 / 问答历史等 AI 应用。
"""


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 1 - 两数之和（Easy）
#    思路：哈希表存值→下标。
#    今天的长文件/组件嵌套，可练"容器与状态"的思维。
#
# 2. LeetCode 20 - 有效的括号（Easy）
#    思路：栈。嵌套组件 / 表单的进入退出，像括号进出栈。
# ============================================================


# ============================================================
# 学习记录
# ============================================================
"""
📝 Day 38 学习打卡

完成时间：____年____月____日

我完成了：
[ ] 实验 1：布局（侧边栏/分栏/标签页/折叠）
[ ] 实验 2：表单
[ ] 实验 3：文件上传
[ ] 实验 4：图表
[ ] 实验 5：session_state
[ ] 实验 6：提问记录综合

遇到的问题：
_____________________________________________
_____________________________________________

学到的最重要的一点：
_____________________________________________
"""
