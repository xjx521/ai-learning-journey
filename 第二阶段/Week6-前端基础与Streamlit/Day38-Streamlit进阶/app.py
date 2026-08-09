import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 【实验 1】布局：侧边栏 / 分栏 / 标签页 / 折叠面板
# ============================================================
st.sidebar.title("控制面板")
mode = st.sidebar.selectbox("模式", ["简洁", "完整"])

col1, col2 = st.columns(2)
with col1:
    st.write("左列")
    a = st.button("左按钮")
with col2:
    st.write("右列")
    b = st.button("右按钮")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["介绍", "数据分析", "登录", "文件上传", "图表展示", "会话状态"]
)
with tab1:
    st.write("这是介绍")
with tab2:
    st.write("这是详情")
    with st.expander("点击展开更多帮助"):
        st.write("藏起来的内容")

# ============================================================
# 【实验 2】表单：多个输入一起提交
# ============================================================
with tab3:
    with st.form("登录表单"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submit = st.form_submit_button("登录")

        if submit:
            st.success(f"登录成功：{username} ,密码已输入")

# ============================================================
# 【实验 3】文件上传
# ============================================================
with tab4:
    uploaded = st.file_uploader("上传一个文本文件", type=["txt", "csv"])
    if uploaded is not None:
        st.write(f"文件名：{uploaded.name}")
        content = uploaded.getvalue().decode("utf-8")
        st.text(content)

# ============================================================
# 【实验 4】图表展示
# ============================================================
with tab5:
    data = pd.DataFrame({"月份": [1, 2, 3, 4], "销量": [10, 20, 15, 30]})
    st.line_chart(data)
    st.bar_chart(data)

    fig, ax = plt.subplots()
    ax.plot(data["月份"], data["销量"])
    ax.set_title("销量趋势")
    st.pyplot(fig)

# ============================================================
# 【实验 5】会话状态 session_state（重点，最容易错）
# ============================================================
with tab6:
    if "count" not in st.session_state:
        st.session_state.count = 0

    if st.button("加一（session_state）"):
        st.session_state.count += 1

    st.write(f"session_state 计数：{st.session_state.count}")
