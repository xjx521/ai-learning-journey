import streamlit as st

import pandas as pd  # AI 应用常要展示表格/字典，Streamlit 有专门组件pandas

st.title("我的 Streamlit 应用")  # 大标题
st.header("这是一级小标题")  # 次级标题
st.subheader("这是二级小标题")  # 三级标题
st.write("这是普通文本")  # 万能输出：文本/数字/DataFrame/字典
st.markdown("**加粗** 和 *斜体* 和 ## 标题和 - 列表")  # 支持 Markdown 语法
st.caption("这是小字说明")  # 小字

name = st.text_input("你的名字", placeholder="请输入名字")  # 文本框
age = st.slider("年龄", min_value=0, max_value=100, value=18)  # 滑块
city = st.selectbox("城市", ["北京", "上海", "广州"])  # 下拉框
agree = st.checkbox("我同意")  # 复选框

# | 多行文本 | `st.text_area("标签")` | 输入的字符串 |
# | 单选 | `st.radio("标签", 列表)` | 选中的一项 |
# | 按钮 | `st.button("文案")` | 点击时 True，否则 False |
# | 数字输入 | `st.number_input("标签", min, max)` | 数字 |
st.write(f"你好，{name}！你 {age} 岁，在 {city}。")
st.success("操作成功！")
st.info("这是一条提示信息")
st.warning("注意，这里有问题")
st.error("出错了")

df = pd.DataFrame(
    {
        "姓名": ["张三", "李四"],
        "分数": [90, 85],
    }
)
st.dataframe(df)  # 可交互表格（可排序、滑动）
st.table(df)  # 静态表格（不可交互）
st.json({"response": "模型输出", "time": 0.3})  # JSON 展示
# st.code(example,language=python)#展示代码
# st.image*()#展示图片
## 完整示例：一个"温度换算"小应用
# st.title("摄氏 ↔ 华氏 换算器")

# c = st.slider("摄氏温度 °C", min_value=-50, max_value=100, value=25)

# f = c * 9 / 5 + 32

# st.write(f"华氏温度：{f:.1f} °F")

# if f > 100:
#     st.warning("好热！")
# elif f < 32:
#     st.info("结冰了！")
# else:
#     st.success("温度适中")
