import streamlit as st

if "history" not in st.session_state:
    st.session_state.history = []

st.title("提问记录")

with st.sidebar:
    show_all = st.checkbox("显示全部")

prompt = st.text_input("输入你的问题：")
if st.button("提交"):
    st.session_state.history.append(prompt)
    st.success("已保存")

if show_all:
    for h in st.session_state.history:
        st.write(f"- {h}")
else:
    if st.session_state.history:
        st.write(f"最新一条：{st.session_state.history[-1]}")
