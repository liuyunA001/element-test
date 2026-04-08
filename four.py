import math
import streamlit as st

# ====================== 页面配置与样式（优化单选按钮+背景） ======================
st.set_page_config(
    page_title="元素人格测试仪",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔧 优化后的CSS：彻底解决单选按钮颜色问题，增强对比度
st.markdown("""
<style>
    /* 全局背景：深蓝色渐变，保持视觉统一 */
    .stApp {
        background: linear-gradient(135deg, #165DFF 0%, #0F389E 100%);
        color: #ffffff;
    }

    /* 标题样式：高亮白色+发光效果，更醒目 */
    h1 {
        text-align: center;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255,255,255,0.8);
        font-size: 2.8rem;
        margin-bottom: 2rem;
    }

    h2, h3 {
        color: #ffffff;
        font-weight: 700;
    }

    /* 输入框标签：纯白加粗，绝对清晰 */
    label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* ====================== 核心优化：单选按钮样式 ====================== */
    /* 单选按钮容器：增加背景，提升层级 */
    div[role="radiogroup"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    /* 未选中的单选按钮：白色边框+透明填充，清晰可见 */
    div[role="radiogroup"] input[type="radio"] {
        accent-color: #ffffff !important;
        transform: scale(1.3);
        margin-right: 0.8rem !important;
    }

    /* 未选中的选项文字：纯白，高对比度 */
    div[role="radiogroup"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* 选中的单选按钮：亮黄色填充+白色边框，极致醒目 */
    div[role="radiogroup"] input[type="radio"]:checked {
        accent-color: #FFD700 !important;
    }

    /* 选中的选项文字：亮黄色，和按钮颜色呼应 */
    div[role="radiogroup"] input[type="radio"]:checked + label {
        color: #FFD700 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* ====================== 按钮样式优化 ====================== */
    button {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
        color: #0F389E !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4) !important;
    }

    button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6) !important;
    }

    /* ====================== 其他元素优化 ====================== */
    /* 成功提示框：白色边框+半透明背景 */
    .stSuccess {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        border: 2px solid #ffffff !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    /* 确保所有文本元素为白色 */
    .stMarkdown, .stWrite {
        color: #ffffff !important;
        font-size: 1.05rem !important;
    }

    /* 输入框样式：纯白背景+深蓝色文字，绝对清晰 */
    input[type="text"] {
        background-color: #ffffff !important;
        color: #0F389E !important;
        border: 2px solid #FFD700 !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    /* 输入框聚焦时高亮 */
    input[type="text"]:focus {
        border-color: #FFA500 !important;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== 页面标题 ======================
st.title("✨ 元素人格测试仪 ✨")

# 初始化分数
if "fire_score" not in st.session_state:
    st.session_state.fire_score = 0
    st.session_state.water_score = 0

# ====================== 1. 用户信息输入 ======================
name = st.text_input("输入你的代号：", "见习炼金术士")

# ====================== 2. 题目作答 ======================
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

# 最终用户分数
user = [st.session_state.fire_score, st.session_state.water_score]

# ====================== 3. 人格模板与匹配算法 ======================
profiles = {
    "🔥 烈焰型": [10, 3],
    "💧潮汐型": [3, 10],
    "⚖️平衡游侠": [7, 7],
    "⚡雷霆大王": [5, 9]
}

# ====================== 4. 结果展示 ======================
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
