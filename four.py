import math
import streamlit as st

# ====================== 页面配置与样式（仅美化，不碰核心逻辑） ======================
st.set_page_config(
    page_title="元素人格测试仪",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS美化（仅改样式，不影响功能）
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
    }
    h1 {
        text-align: center;
        color: #00ff99;
        text-shadow: 0 0 8px #00ff99;
        font-size: 2.5rem;
    }
    h2, h3 {
        color: #66ccff;
    }
    /* 确保所有文本元素都有足够的对比度 */
    .stRadio label,
    .stTextInput label,
    .stMarkdown {
        color: #ffffff !important;
        font-weight: 500;
    }
    /* 选项文本颜色 */
    .stRadio div[role="radiogroup"] label {
        color: #ffffff !important;
    }
    /* 选中的选项样式 */
    .stRadio input[type="radio"]:checked + label {
        color: #00ff99 !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.8rem 2.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    .stSuccess {
        background: rgba(72, 219, 251, 0.15);
        border-radius: 12px;
        border: 1px solid #48dbfb;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ====================== 页面标题（仅加装饰，内容不变） ======================
st.title("✨ 元素人格测试仪 ✨")

# 初始化分数（避免未答题报错）
if "fire_score" not in st.session_state:
    st.session_state.fire_score = 0
    st.session_state.water_score = 0

# ====================== 1. 用户信息输入（完全保留原样） ======================
name = st.text_input("输入你的代号：", "见习炼金术士")

# ====================== 2. 题目作答（你的题目、选项、计分100%不变） ======================
st.subheader("📝 请完成以下3道题目，选择最符合你的选项")

# 题目1
q1 = st.radio(
    "【题目1】A door here",
    options=["选项A:open", "选项B:left"],
    key="q1",
    horizontal=True
)
if q1 == "选项A:open":
    st.session_state.fire_score += 5
    st.session_state.water_score += 0
else:
    st.session_state.fire_score += 0
    st.session_state.water_score += 5

# 题目2
q2 = st.radio(
    "【题目2】which one you want to use to fight",
    options=["选项A:book", "选项B:ball"],
    key="q2",
    horizontal=True
)
if q2 == "选项A:book":
    st.session_state.fire_score += 5
    st.session_state.water_score += 0
else:
    st.session_state.fire_score += 0
    st.session_state.water_score += 5

# 题目3
q3 = st.radio(
    "【题目3】a bottle of water on the table",
    options=["选项A:drink", "选项B:look"],
    key="q3",
    horizontal=True
)
if q3 == "选项A:drink":
    st.session_state.fire_score += 0
    st.session_state.water_score += 5
else:
    st.session_state.fire_score += 0
    st.session_state.water_score += 5

# 最终用户分数（保留原变量）
user = [st.session_state.fire_score, st.session_state.water_score]

# ====================== 3. 人格模板与匹配算法（核心逻辑完全不变） ======================
profiles = {
    "烈焰型": [10, 3],
    "潮汐型": [3, 10],
    "平衡游侠": [7, 7],
    "雷霆大王": [5, 9]
}

# ====================== 4. 结果展示（仅美化，逻辑不变） ======================
st.subheader("准备开始匹配")
if st.button("开始最终匹配"):
    min_dist = 999999.0
    best_match = ""

    for title, coords in profiles.items():
        dist = math.sqrt((user[0] - coords[0]) ** 2 + (user[1] - coords[1]) ** 2)
        st.write(f"{title}的距离为:{dist}")

        if dist < min_dist:
            min_dist = dist
            best_match = title

    st.balloons()
    st.success(f"{name}，你最接近的模板是：{best_match},最小距离为:{min_dist}")
