import streamlit as st
import pandas as pd
import requests

# ============================================================
# 【实验 1】第一个 Streamlit 应用：文本与标题
# ============================================================

st.title("我的第一个 Streamlit 应用")  # 【填空 1】大标题
st.write("这是用 Python 写出来的网页！")  # 【填空 2】普通文本
st.markdown("**加粗** 和 *斜体*")  # 【填空 3】Markdown
st.markdown("## 小标题")

# ============================================================
# 【实验 2】文本输入交互
# ============================================================
name = st.text_input("你的名字", placeholder="请输入名字")
# ============================================================
# 【实验 3】滑块 / 下拉框 / 复选框
# ============================================================
age = st.slider("年龄", min_value=0, max_value=100, value=18)
city = st.selectbox("城市", ["北京", "上海", "广州"])
agree = st.checkbox("我同意条款")
print(type(name), type(age), type(city), type(agree))
st.write(f"你好,{name}, {age} 岁，在 {city}，同意={agree}")

# ============================================================
# 【实验 4】反馈消息：成功 / 提示 / 警告 / 错误
# ============================================================
score = 30
if score >= 60:
    st.success("恭喜，及格了！")  # 【填空 9】绿色成功
elif score >= 40:
    st.warning("注意：接近不及格")  # 【填空 10】黄色警告
else:
    st.error("不及格，需要补考")  # 【填空 11】红色错误

df = pd.DataFrame(
    {
        "姓名": ["张三", "李四", "王五"],
        "分数": [90, 85, 88],
    }
)
st.dataframe(df)
st.table(df)
st.json({"result": "模型输出", "time": 0.3})

API = "http://localhost:8000"
question = st.text_input("问点什么：")
if st.button("提问"):
    try:
        resp = requests.post(f"{API}/api/chat", json={"text": question})  # post
    except requests.exceptions.ConnectionError:
        st.error("服务器无法连接")
    result = resp.json()  # 解析json
    st.success(result.get("answer", "(无回答)"))
