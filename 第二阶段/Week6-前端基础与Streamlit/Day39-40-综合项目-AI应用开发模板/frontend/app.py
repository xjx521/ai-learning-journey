import streamlit as st
import requests

API = "http://localhost:8000"

# ===== 第 1 块：初始化（永远在最上面）=====
if "page" not in st.session_state:
    st.session_state.page = 1
if "total_pages" not in st.session_state:
    st.session_state.total_pages = 1
if "search_id" not in st.session_state:
    st.session_state.search_id = None


# 从后端拉取历史记录
def load_history():
    """调用 GET /api/prompts，把数据库里的提问记录存进 session_state"""
    try:
        params = {
            "page": st.session_state.page,
            "size": 5,
        }  # 页数 + 每页条数 # 关键点：当前页要放在 session_state 避免点击下一页时脚本重跑页数变回1
        if st.session_state.get("search_id"):
            params["prompt_id"] = st.session_state["search_id"]
        resp = requests.get(f"{API}/api/prompts", params=params)
        data = resp.json()  # 解析json
        st.session_state.history = data[
            "data"
        ]  # 后端返回 {"data": [...], "pagination": {...}} # 存这条页的记录
        st.session_state.total_pages = data["pagination"][
            "total_pages"
        ]  # 存总页数 #total_pages 也存进 session_state，这样按钮能判断"还有没有下一页"
        return True
    except requests.exceptions.ConnectionError:
        st.error("服务器无法链接")
        return False


# 验证提问记录是否存在
if "history" not in st.session_state:
    st.session_state.history = []
    load_history()

st.title("AI 应用开发模板")

# 输入框
text = st.text_input("请输入提问的问题")

# 提交问题
if st.button("提交问题"):
    try:
        # 第 1 步：调 /api/chat 拿回答（返回 {"answer": "..."}）
        chat_resp = requests.post(
            f"{API}/api/chat", json={"text": text}
        )  # 提交请求 text
        answer = chat_resp.json()["answer"]  # 解析json 获取回答

        # 第 2 步：调用/api/prompts 把"问题 + 回答"一起存进数据库
        requests.post(f"{API}/api/prompts", json={"text": text, "response": answer})
        # 第 3 步：存完重新拉一次历史，界面立刻显示新的一条
        load_history()
        # 第 4 步：展示回答
        st.success(f"你的提问是:**{text}**\n\n AI回答:**{answer}**")
    except requests.exceptions.ConnectionError:
        st.error("服务器无法连接")

# 删除
delete_id = st.text_input("请输入要删除的提问ID")

if st.button("删除"):
    try:
        requests.delete(f"{API}/api/prompts/{delete_id}", json={"prompt_id": delete_id})
        # 删除完重新拉一次历史
        load_history()
        st.success("删除成功")
    except requests.exceptions.ConnectionError:
        st.error("服务器无法连接")

# 展示历史
with st.sidebar:
    st.header("操作")
    # 刷新历史按钮：点一下，重新从后端拉一遍历史
    if st.button("🔄 刷新历史"):
        load_history()

    show_all = st.checkbox("展示全部历史")

if show_all:
    for item in st.session_state.history:
        st.write(f"提问ID:**{item['id']}**")
        st.write(f"你的提问:**{item['text']}**")
        st.write(f"AI回答:**{item['response']}**")
        st.divider()
else:
    if st.session_state.history:
        latest = st.session_state.history[0]
        st.write(f"最新一条ID:**{latest['id']}**")
        st.write(f"最新一条提问:**{latest['text']}**")
        st.write(f"最新一条AI回答:**{latest['response']}**")

# 分页搜索
col1, col2 = st.columns(2)
if col1.button(
    "⬅ 上一页", disabled=(st.session_state.page <= 1)
):  # disabled=(page <= 1)：第 1 页时"上一页"灰掉点不了
    st.session_state.page -= 1
    load_history()
if col2.button(
    "下一页 ➡", disabled=(st.session_state.page >= st.session_state.total_pages)
):
    st.session_state.page += 1
    load_history()
st.write(f"第{st.session_state.page}/{st.session_state.total_pages}页")

search_id = st.number_input("按 ID 搜索（留空显示全部）", min_value=1, step=1)
if st.button("搜索"):
    st.session_state.search_id = search_id
    st.session_state.page = 1
    load_history()
