import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

### 1. 侧边栏 `st.sidebar`
st.sidebar.title("控制面板")
mode = st.sidebar.selectbox("模式", ["简洁", "完整"])
threshold = st.sidebar.slider("阈值", 0, 100, 50)

st.title("主页面")
st.write(f"当前模式：{mode},阈值：{threshold}")

### 2. 分栏 `st.columns`
col1, col2 = st.columns(
    2
)  # st.columns(2) 返回两个"容器   也可以用 `st.columns([1, 3])` 指定宽度比例（左边 1 份、右边 3 份）。
with col1:  # with col1:` 把组件放进去
    st.write("左边")
    st.button("左按钮")
with col2:
    st.write("右边")
    st.button("右按钮")

### 3. 标签页 `st.tabs`

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["介绍", "数据分析", "登录", "文件上传", "图表展示", "会话状态"],
    width=600,
    height=900,
)
with tab1:
    st.write("这是介绍页")
    with st.expander("点击展开更多"):
        st.write("藏在里面的内容")


with tab2:
    st.write("这是数据分析页")
    ### 4. 折叠面板 `st.expander`
    with st.expander("点击展开更多"):
        st.write("藏在里面的内容")
    ### 5. 容器 `st.container`
    with st.container():
        st.write("这段在盒子里")  # 不带边框肉眼看不出
    st.write("这段在盒子外")

with tab3:
    st.write("这是登录页")
    ## 二、表单 `st.form`：多个输入一起提交
    with st.form("登录表单"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submit = st.form_submit_button("登录")  # 表单内唯一的提交按钮

    if submit:
        st.success(f"登录：{username}，密码已输入")

with tab4:
    st.write("这是文件上传页")
    uploaded = st.file_uploader("上传一个文件", type=["csv", "txt", "png"])
    if uploaded is not None:
        st.write(f"文件名：{uploaded.name}")
        # 读取内容
        content = uploaded.getvalue().decode(
            "utf-8"
        )  # 文本文件 uploaded.getvalue()获取文件全部二进制字节数据（bytes）
        st.text(
            content
        )  # 纯文本展示，保留换行，但不支持 markdown 渲染 如果想要支持 markdown 格式显示，换成：st.markdown(content)

        ### 上传 CSV 并展示

        # import pandas as pd
        # uploaded = st.file_uploader("上传 CSV", type=["csv"])
        # if uploaded is not None:
        #     df=pd.read_csv(uploaded)
        #     st.dataframe(df)

with tab5:
    st.write("这是图表展示页")
    ### 1. 快速图表（传入数据即可）
    st.write("快速图表（传入数据即可）")
    data = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 20, 30, 40]})

    st.line_chart(data)  # 折线图
    st.bar_chart(data)  # 柱状图
    st.area_chart(data)  # 面积图

    ### 2. Matplotlib 图（`st.pyplot`）
    st.write("2. Matplotlib 图（`st.pyplot`）")

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])  # 在坐标系上绘制折线图，x=[1,2,3]，y=[4,5,6]
    ax.set_title("我的图")
    st.pyplot(fig)  # 将matplotlib绘制好的图像渲染到Streamlit页面

    ### 3. Plotly 交互图（`st.plotly_chart`，可缩放/悬停）
    st.write(" Plotly 交互图（`st.plotly_chart`，可缩放/悬停")
    fig = go.Figure(
        data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6])
    )  # 创建Plotly图表对象，数据为散点/折线轨迹
    st.plotly_chart(fig)

with tab6:
    st.write("这是会话状态页")
    if "count" not in st.session_state:
        st.session_state.count = 0

    if st.button("加一"):
        st.session_state.count += 1

    st.write(f"计数：{st.session_state.count}")
