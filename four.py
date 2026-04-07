import math
import streamlit as st

# ====================== 最小美化：页面配置（只改布局，不改逻辑） ======================
st.set_page_config(
    page_title="元素人格测试仪",
    page_icon="🧪",
    layout="centered",  # 居中布局，更美观，不影响功能
    initial_sidebar_state="collapsed"
)

# 极简自定义 CSS：只加深色背景和文字美化，不改动任何组件逻辑
st.markdown("""
<style>
    /* 全局深色背景，不影响原有组件布局 */
    .stApp {
        background: #121212;
        color: #ffffff;
    }
    /* 标题美化，居中发光，不碰原有标题文字 */
    h1 {
        text-align: center;
        color: #00ff99;
        text-shadow: 0 0 8px #00ff99;
        font-size: 2.5rem;
    }
    /* 子标题颜色，更清晰 */
    h2 {
        color: #66ccff;
    }
    /* 按钮渐变美化，hover 有动画，不改变点击逻辑 */
    .stButton>button {
        background: linear-gradient(90deg, #00ccff, #0066ff);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 204, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ====================== 以下是你的核心代码，一字未改 ======================
st.title("✨ 元素人格测试仪 ✨")  # 只加了两个星星装饰，标题内容不变

# 初始化分数，避免未答题时报错（保留你原本的逻辑）
if "fire_score" not in st.session_state:
    st.session_state.fire_score = 0
    st.session_state.water_score = 0

# ====================== 1. 用户基础信息输入（保留原样） ======================
name = st.text_input("输入你的代号：", "见习炼金术士")

# ====================== 2. 题目作答与计分模块（你的题目、选项、计分完全不变） ======================
st.subheader("📝 请完成以下3道题目，选择最符合你的选项")

# 题目1：完全保留你的原内容
q1 = st.radio(
    "【题目1】A door here",
    options=[
        "选项A:open",
        "选项B:left"
    ],
    key="q1",
    horizontal=True
)
if q1 == "选项A:open":
    st.session_state.fire_score += 5
    st.session_state.water_score += 0
else:
    st.session_state.fire_score += 0
    st.session_state.water_score += 5

# 题目2：完全保留你的原内容
q2 = st.radio(
    "【题目2】which one you want to use to fight",
    options=[
        "选项A:book",
        "选项B:ball"
    ],
    key="q2",
    horizontal=True
)
if q2 == "选项A:book":
    st.session_state.fire_score += 5
    st.session_state.water_score += 0
else:
    st.session_state.fire_score += 0
    st.session_state.water_score += 5

# 题目3：完全保留你的原内容
q3 = st.radio(
    "【题目3】a bottle of water on the table",
    options=[
        "选项A:drink",
        "选项B:look"
    ],
    key="q3",
    horizontal=True
)
if q3 == "选项A:drink":
    st.session_state.fire_score += 0
    st.session_state.water_score += 5
else:
    st.session_state.fire_score += 0
    st.session_state.water_score += 5

# 最终用户分数（保留你原本的变量）
user = [st.session_state.fire_score, st.session_state.water_score]

# ====================== 3. 人格模板与匹配算法（你的核心逻辑完全不变） ======================
profiles = {
    "烈焰型": [10, 3],
    "潮汐型": [3, 10],
    "平衡游侠": [7, 7],
    "雷霆大王": [5, 9]
}

# ====================== 4. 匹配结果展示（保留原样，只加个标题） ======================
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
                st.experimental_rerun()
