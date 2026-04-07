import math
import streamlit as st

# ====================== 页面配置与样式 ======================
# 设置页面配置
st.set_page_config(
    page_title="元素人格测试仪",
    page_icon="🧪",
    layout="wide"
)

# 添加渐变背景
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
    }
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
</style>
""", unsafe_allow_html=True)

# ====================== 页面标题与初始化 ======================
# 添加星星装饰效果
stars = "✨" * 5
st.title(f"{stars} 🧪 元素人格测试仪 {stars}")

# 初始化分数，避免未答题时报错
if "fire_score" not in st.session_state:
    st.session_state.fire_score = 0
    st.session_state.water_score = 0

# ====================== 1. 用户基础信息输入 ======================
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='color: #4ecdc4;'>请输入你的信息</h3>", unsafe_allow_html=True)
        name = st.text_input("输入你的代号：", "见习炼金术士")

# ====================== 2. 题目作答与计分模块 ======================
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='color: #ff6b6b;'>📝 请完成以下3道题目,选择最符合你的选项</h3>", unsafe_allow_html=True)
        
        # 题目1（可自行修改题目和选项、对应分数）
        q1 = st.radio(
            "【题目1】A door here",
            options=[
                "选项A:open",
                "选项B:left"
            ],
            key="q1",
            horizontal=True
        )
        # 选项计分逻辑（可根据需求调整分值）
        if q1 == "选项A:open":
            st.session_state.fire_score += 3
            st.session_state.water_score += 0
        else:
            st.session_state.fire_score += 0
            st.session_state.water_score += 3
        
        st.divider()
        
        # 题目2（可自行修改题目和选项、对应分数）
        q2 = st.radio(
            "【题目2】which one you want to use to fight",
            options=[
                "选项A:book",
                "选项B:ball"
            ],
            key="q2",
            horizontal=True
        )
        if q2 == "选项B:ball":
            st.session_state.fire_score += 3
            st.session_state.water_score += 0
        else:
            st.session_state.fire_score += 0
            st.session_state.water_score += 3
        
        st.divider()
        
        # 题目3（可自行修改题目和选项、对应分数）
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
            st.session_state.fire_score += 4
            st.session_state.water_score += 0
        else:
            st.session_state.fire_score += 0
            st.session_state.water_score += 4

# 最终用户分数（由题目自动计算得出）
user = [st.session_state.fire_score, st.session_state.water_score]

# ====================== 3. 人格模板与匹配算法 ======================

profiles = {
    "🔥 烈焰型": [10, 3],
    "💧 潮汐型": [3, 10],
    "⚖️ 平衡游侠": [7, 7],
    "⚡ 雷霆大王": [5, 9]
}

# ====================== 4. 匹配结果展示 ======================
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='color: #45b7d1;'>准备开始匹配</h3>", unsafe_allow_html=True)
        if st.button("开始最终匹配"):
            min_dist = 999999.0
            best_match = ""

            # 遍历所有人格模板，计算欧氏距离
            for title, coords in profiles.items():
                dist = math.sqrt(
                    (user[0] - coords[0]) ** 2 + (user[1] - coords[1]) ** 2
                )
                st.write(f"{title}的匹配距离为：{round(dist, 2)}")

                if dist < min_dist:
                    min_dist = dist
                    best_match = title

            # 展示最终结果
            st.balloons()
            st.success(
                f"{name}，你的最终火属性分数：{user[0]} | 水属性分数：{user[1]}\n"
                f"你最接近的人格模板是：{best_match}，最小匹配距离：{round(min_dist, 2)}"
            )

            # 可选：重置分数按钮，方便用户重新测试
            if st.button("重新测试"):
                st.session_state.fire_score = 0
                st.session_state.water_score = 0
                st.experimental_rerun()
