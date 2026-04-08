import math
import streamlit as st

# ====================== 页面配置与样式（仅美化，不碰核心逻辑） ======================
st.set_page_config(
    page_title="元素人格测试仪",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS美化（修改背景为蓝色系，调整字体颜色保证可读性）
st.markdown("""
<style>
    /* 全局背景和基础颜色 - 改为蓝色渐变背景 */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff; /* 全局字体改为白色，确保在蓝色背景上清晰 */
    }
    
    /* 标题样式 - 调整为更协调的亮色 */
    h1 {
        text-align: center;
        color: #87ceeb;
        text-shadow: 0 0 8px #87ceeb;
        font-size: 2.5rem;
    }
    
    h2, h3 {
        color: #b0e0e6;
    }
    
    /* 输入框标签 - 改为浅灰色确保清晰 */
    label {
        color: #f0f8ff !important;
        font-weight: 600 !important;
    }
    
    /* 单选按钮选项 - 白色字体 */
    div[role="radiogroup"] label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* 选中的单选按钮选项 - 高亮色调整 */
    div[role="radiogroup"] input[type="radio"]:checked + label {
        color: #87ceeb !important;
        font-weight: 600 !important;
    }
    
    /* 按钮样式 - 调整为与蓝色背景协调的配色 */
    button {
        background: linear-gradient(90deg, #4682b4, #5f9ea0) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(70, 130, 180, 0.6) !important;
    }
    
    /* 成功提示框 - 调整为蓝色系 */
    .stSuccess {
        background: rgba(135, 206, 235, 0.2) !important;
        border-radius: 12px !important;
        border: 1px solid #87ceeb !important;
        color: #ffffff !important;
    }
    
    /* 确保所有文本元素的颜色 */
    .stMarkdown, .stWrite {
        color: #ffffff !important;
    }
    
    /* 输入框样式优化 - 确保在蓝色背景上清晰 */
    input[type="text"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #1e3c72 !important;
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
    "🔥 烈焰型": [10, 3],
    "💧潮汐型": [3, 10],
    "⚖️平衡游侠": [7, 7],
    "⚡雷霆大王": [5, 9]
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
