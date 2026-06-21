import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import html

# ---------- 页面配置 ----------
st.set_page_config(page_title="命运人格测试", page_icon="🔮", layout="centered")

# ---------- 初始化 session_state ----------
if "page" not in st.session_state:
    st.session_state.page = "cover"
if "name" not in st.session_state:
    st.session_state.name = ""
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "scores" not in st.session_state:
    st.session_state.scores = {"fire": 0, "water": 0, "earth": 0, "air": 0}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "tarot_revealed" not in st.session_state:
    st.session_state.tarot_revealed = False
if "tarot_selected_card" not in st.session_state:
    st.session_state.tarot_selected_card = None
if "lucky_data" not in st.session_state:
    st.session_state.lucky_data = None

# ---------- 测试题库 ----------
questions = [
    {
        "question": "在团队项目中，你通常扮演什么角色？",
        "options": [
            ("领导者，指挥全局", "fire"),
            ("协调者，促进合作", "water"),
            ("执行者，踏实完成", "earth"),
            ("智囊，提供策略", "air")
        ]
    },
    {
        "question": "面对困难时，你的第一反应是？",
        "options": [
            ("迎难而上，立即行动", "fire"),
            ("寻求他人支持，共同面对", "water"),
            ("冷静分析，制定计划", "earth"),
            ("思考多种可能，寻找创新解法", "air")
        ]
    },
    {
        "question": "你更享受哪种休闲方式？",
        "options": [
            ("冒险运动或竞赛", "fire"),
            ("艺术创作或欣赏", "water"),
            ("园艺或手工制作", "earth"),
            ("阅读或学习新知识", "air")
        ]
    },
    {
        "question": "别人通常如何形容你？",
        "options": [
            ("充满激情，有感染力", "fire"),
            ("温柔体贴，善解人意", "water"),
            ("稳重可靠，值得信赖", "earth"),
            ("聪明机智，思维敏捷", "air")
        ]
    }
]

# ---------- 全局 CSS（包含所有动画） ----------
GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* 背景与星云（全局） */
    .stApp {
        background: radial-gradient(ellipse at 50% 30%, #1a1a3e 0%, #0f0c29 70%, #020011 100%) !important;
        font-family: 'Inter', sans-serif;
        color: #e0d0ff;
    }
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: 0;
        pointer-events: none;
        background:
            radial-gradient(2px 2px at 20% 30%, rgba(255,215,0,0.15), transparent),
            radial-gradient(2px 2px at 40% 70%, rgba(196, 76, 255, 0.12), transparent),
            radial-gradient(3px 3px at 60% 20%, rgba(255,215,0,0.08), transparent),
            radial-gradient(2px 2px at 80% 60%, rgba(196, 76, 255, 0.10), transparent),
            radial-gradient(2px 2px at 10% 80%, rgba(255,215,0,0.06), transparent),
            radial-gradient(3px 3px at 90% 10%, rgba(196, 76, 255, 0.08), transparent);
        background-size: 200% 200%;
        animation: nebulaDrift 40s ease-in-out infinite alternate;
    }
    @keyframes nebulaDrift {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }
    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            radial-gradient(2px 2px at 10% 10%, #ffd700, transparent),
            radial-gradient(3px 3px at 30% 40%, #ffd700, transparent),
            radial-gradient(2px 2px at 50% 80%, #ffd700, transparent),
            radial-gradient(4px 4px at 70% 20%, #ffd700, transparent),
            radial-gradient(2px 2px at 90% 60%, #ffd700, transparent),
            radial-gradient(3px 3px at 15% 90%, #ffd700, transparent),
            radial-gradient(2px 2px at 85% 15%, #ffd700, transparent),
            radial-gradient(4px 4px at 45% 50%, #ffd700, transparent);
        background-size: 250% 250%;
        animation: starFall 30s linear infinite;
        opacity: 0.6;
    }
    @keyframes starFall {
        0% { background-position: 0% -10%; }
        100% { background-position: 100% 110%; }
    }
    .main, .block-container { position: relative; z-index: 1; }

    /* 通用磨砂玻璃卡片 */
    .glass-card {
        background: rgba(20, 15, 40, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 215, 0, 0.25) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 20px rgba(255,215,0,0.05) !important;
        padding: 1.8rem 1.8rem !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(255, 215, 0, 0.5) !important;
        box-shadow: 0 8px 40px rgba(255,215,0,0.15) !important;
    }

    /* 标题字体 */
    h1, h2, h3, .main-title {
        font-family: 'Cinzel', serif !important;
        color: #ffd700 !important;
        text-shadow: 0 0 30px rgba(255,215,0,0.2), 0 0 60px rgba(255,215,0,0.1);
        letter-spacing: 1px;
    }

    /* ---------- 封面页专用动画 ---------- */
    .cover-title {
        animation: titlePulse 3s ease-in-out infinite, float 5s ease-in-out infinite;
    }
    @keyframes titlePulse {
        0%, 100% { text-shadow: 0 0 20px rgba(255,215,0,0.3), 0 0 40px rgba(255,215,0,0.1); }
        50% { text-shadow: 0 0 40px rgba(255,215,0,0.6), 0 0 80px rgba(255,215,0,0.2); }
    }
    .cover-icon {
        display: inline-block;
        animation: spinFloat 6s linear infinite, glowPulse 4s ease-in-out infinite;
        font-size: 5rem;
        filter: drop-shadow(0 0 30px rgba(255,215,0,0.4));
    }
    @keyframes spinFloat {
        0% { transform: rotate(0deg) translateY(0px); }
        25% { transform: rotate(5deg) translateY(-5px); }
        75% { transform: rotate(-5deg) translateY(5px); }
        100% { transform: rotate(0deg) translateY(0px); }
    }
    @keyframes glowPulse {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(255,215,0,0.3)); }
        50% { filter: drop-shadow(0 0 50px rgba(255,215,0,0.7)); }
    }

    /* 输入框聚焦动画 */
    .stTextInput > div > input {
        background: rgba(20, 15, 40, 0.6) !important;
        border: 1px solid rgba(255,215,0,0.3) !important;
        border-radius: 16px !important;
        color: #e0d0ff !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 30px rgba(255,215,0,0.2), 0 0 60px rgba(255,215,0,0.1) !important;
        transform: scale(1.02);
    }

    /* 按钮通用样式（含呼吸光晕） */
    .stButton > button {
        background: rgba(255, 215, 0, 0.12) !important;
        border: 1px solid rgba(255, 215, 0, 0.5) !important;
        border-radius: 40px !important;
        color: #ffe9a0 !important;
        font-family: 'Cinzel', serif !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 0 20px rgba(255,215,0,0.15) !important;
        backdrop-filter: blur(6px);
        animation: btnBreath 3s ease-in-out infinite;
    }
    @keyframes btnBreath {
        0%, 100% { box-shadow: 0 0 15px rgba(255,215,0,0.1); }
        50% { box-shadow: 0 0 30px rgba(255,215,0,0.3), 0 0 60px rgba(255,215,0,0.1); }
    }
    .stButton > button:hover {
        background: rgba(255, 215, 0, 0.2) !important;
        border-color: #ffd700 !important;
        box-shadow: 0 0 50px rgba(255,215,0,0.4), 0 0 100px rgba(255,215,0,0.15) !important;
        transform: scale(1.05);
        color: #fff8e0 !important;
        animation: none;
    }
    .stButton > button:active {
        transform: scale(0.95);
        transition-duration: 0.05s;
    }

    /* ---------- 做题页专用动画 ---------- */
    .question-card {
        animation: slideUp 0.6s ease-out;
    }
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(40px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* 进度条（自定义） */
    .progress-container {
        width: 100%;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #ffd700, #f0e68c);
        border-radius: 20px;
        width: 0%;
        animation: fillProgress 0.8s ease-out forwards;
    }
    @keyframes fillProgress {
        from { width: 0%; }
        to { width: var(--progress); }
    }

    /* 选项悬停动画 */
    .stRadio label {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 16px !important;
        padding: 0.8rem 1.2rem !important;
        border: 1px solid rgba(255,215,0,0.1) !important;
        transition: all 0.3s ease !important;
        cursor: pointer;
         color: #e0d0ff !important; 
    }
    .stRadio label:hover {
        background: rgba(255,215,0,0.08) !important;
        border-color: #ffd700 !important;
        transform: translateX(8px);
        box-shadow: 0 0 20px rgba(255,215,0,0.1);
    }
    .stRadio label:active {
        transform: scale(0.98);
    }
    /* 选中状态 */
    .stRadio label[data-checked="true"] {
        background: rgba(255,215,0,0.15) !important;
        border-color: #ffd700 !important;
        box-shadow: 0 0 30px rgba(255,215,0,0.2);
    }

    /* Tabs 等已有样式保留 */
    .stTabs [role="tablist"] { border-bottom: 1px solid rgba(255,215,0,0.2); }
    .stTabs [role="tab"] {
        font-family: 'Cinzel', serif;
        color: #b8a8e0 !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 20px 20px 0 0;
        transition: 0.3s;
    }
    .stTabs [role="tab"]:hover { color: #ffd700 !important; background: rgba(255,215,0,0.05); }
    .stTabs [role="tab"][aria-selected="true"] {
        color: #ffd700 !important;
        border-bottom: 2px solid #ffd700 !important;
        background: rgba(255,215,0,0.05);
    }
    .stAlert {
        background: rgba(20, 15, 40, 0.5) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,215,0,0.15);
        border-radius: 16px;
        color: #e0d0ff;
    }
    .deco-star { display: inline-block; font-size: 1.4rem; margin: 0 6px; color: #ffd700; opacity: 0.6; filter: drop-shadow(0 0 6px #ffd700); }
    .block-container { animation: fadeIn 1.2s ease-out; }
    @keyframes fadeIn { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 浮动动画（通用） */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
</style>
"""

# 注入全局 CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ---------- 封面页 ----------
def render_cover():
    """封面页（带交互动画）"""
    st.markdown("""
    <div style="text-align: center; padding-top: 2rem;">
        <div class="cover-icon">🔮</div>
        <h1 class="cover-title" style="font-size: 4rem; margin: 0.2rem 0;">命运人格测试</h1>
        <p style="color: #c0b0ff; font-size: 1.3rem; margin-top: -0.3rem;">探索你的灵魂元素 · 揭示星辰的指引</p>
        <div style="margin: 1rem 0; font-size: 1.2rem; color: #8a7aaa;">☽ 倾听内心的低语 ☾</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        with st.form("cover_form"):
            name = st.text_input("请输入你的名字", placeholder="例如：探索者", value=st.session_state.name)
            submitted = st.form_submit_button("开始旅程 ✨")
            if submitted and name.strip():
                st.session_state.name = name.strip()
                st.session_state.page = "quiz"
                st.rerun()
            elif submitted:
                st.warning("请先输入你的名字")

# ---------- 做题页 ----------
def render_quiz():
    """做题页（带交互动画）"""
    total = len(questions)
    idx = st.session_state.current_question
    if idx >= total:
        st.session_state.page = "results"
        st.rerun()
        return

    q = questions[idx]
    progress = (idx / total) * 100

    # 自定义进度条（使用CSS变量）
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; color: #b0a0d0; font-size: 0.9rem;">
            <span>问题 {idx+1} / {total}</span>
            <span>{int(progress)}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="--progress: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 题目卡片（带滑入动画）
    st.markdown(f"""
    <div class="glass-card question-card">
        <h3 style="margin-top: 0; color: #ffd700;">{q['question']}</h3>
    """, unsafe_allow_html=True)

    options = q["options"]
    labels = [opt[0] for opt in options]
    values = [opt[1] for opt in options]

    selected_label = st.radio(
        "选择你的答案：",
        labels,
        key=f"q_{idx}",
        index=None,
        label_visibility="collapsed"
    )

    # 查找选中的元素
    selected_element = None
    for label, elem in options:
        if label == selected_label:
            selected_element = elem
            break

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("下一题 ➤", use_container_width=True):
            if selected_element is not None:
                st.session_state.answers[idx] = selected_element
                st.session_state.scores[selected_element] += 1
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.warning("请选择一个选项")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- 结果页（您提供的完整函数，我将其整合并稍作调整） ----------
def show_results():
    """结果展示页 – 暗黑星空塔罗风格（完整）"""
    # 安全过滤
    raw_name = st.session_state.name or "探索者"
    safe_name = html.escape(raw_name)

    scores = st.session_state.scores
    element_names = {
        "fire": "🔥 烈焰型",
        "water": "💧 潮汐型",
        "earth": "🌍 大地型",
        "air": "💨 疾风型"
    }
    colors = {
        "fire": "#FF6B6B",
        "water": "#4ECDC4",
        "earth": "#57C84D",
        "air": "#74B9FF"
    }

    sorted_elems = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, primary_score = sorted_elems[0]
    secondary, secondary_score = sorted_elems[1]
    primary_type = element_names[primary]
    secondary_type = element_names[secondary]
    p_color = colors[primary]
    s_color = colors[secondary]

    # 分析数据（原样保留）
    analysis_data = {
        "fire": {
            "mbti": "ESTP / ENTJ",
            "holland": "企业型+现实型",
            "traits": ["热情行动派", "天生的领导者", "勇于冒险创新"],
            "career": ["企业家", "销售精英", "创业领袖", "体育教练"],
            "description": "烈焰型的你如同燃烧的火焰，充满激情与活力，是天生的领导者，敢于冒险，勇于创新。",
            "learning_style": "适合实践导向学习，边做边学，通过竞赛和挑战激发动力，喜欢有竞争性和互动性的学习方式",
            "hidden_talent": "领导力、危机处理、激励他人、谈判说服能力"
        },
        "water": {
            "mbti": "INFP / ISFJ",
            "holland": "艺术型+社会型",
            "traits": ["温柔细腻型", "善于倾听理解", "富有同理心"],
            "career": ["心理咨询师", "艺术创作者", "教育工作者", "护士"],
            "description": "潮汐型的你如同温柔的流水，细腻敏感，善于倾听，富有同理心，能够温暖他人的心灵。",
            "learning_style": "适合情感联结式学习，需要理解学习的意义和价值偏好小组讨论和案例分析，通过帮助他人学习获得满足感",
            "hidden_talent": "共情能力、艺术创作、心理咨询、调解冲突能力"
        },
        "earth": {
            "mbti": "ISFJ / ESFJ",
            "holland": "社会型+常规型",
            "traits": ["稳重务实型", "可靠值得信赖", "善于团队协作"],
            "career": ["人力资源", "项目管理", "行政主管", "建筑师"],
            "description": "大地型的你如同坚实的大地，稳重可靠，务实踏实，是团队中值得信赖的中坚力量。",
            "learning_style": "适合循序渐进的学习方式，重视扎实基础，喜欢有结构的学习材料，通过反复练习巩固知识",
            "hidden_talent": "项目管理、执行力、协调统筹、稳定大局能力"
        },
        "air": {
            "mbti": "INTJ / ENTP",
            "holland": "研究型+企业型",
            "traits": ["理性思考型", "逻辑分析强", "追求真理智慧"],
            "career": ["战略顾问", "数据分析师", "科学家", "工程师"],
            "description": "疾风型的你如同自由的风，思维敏捷，善于分析，追求真理与智慧，能够看透事物的本质。",
            "learning_style": "适合系统化学习，先搭建知识框架再深入，偏好独立研究和逻辑推理，通过解决复杂问题获得成就感",
            "hidden_talent": "战略规划、创新思维、跨领域整合、危机预判能力"
        }
    }
    p_ana = analysis_data[primary]
    s_ana = analysis_data[secondary]

    # 雷达图数据
    radar_dims = {
        "fire": [95, 70, 40, 60, 85, 90],
        "water": [40, 95, 60, 95, 50, 45],
        "earth": [60, 50, 95, 70, 70, 65],
        "air": [70, 40, 75, 55, 95, 85]
    }
    dim_names = ["领导力", "共情力", "稳定性", "创意力", "逻辑力", "行动力"]

    # 塔罗牌
    tarot_cards = [
        {"name": "太阳", "emoji": "☀️", "meaning": "光明与成功", "love": "感情升温，单身者有望遇到良缘", "career": "工作顺利，项目取得突破性进展", "health": "精力充沛，心情愉悦", "advice": "保持积极，好运正在降临"},
        {"name": "月亮", "emoji": "🌙", "meaning": "直觉与潜意识", "love": "感情需要用心经营，信任是关键", "career": "小心谨慎，避免冲动决策", "health": "注意休息，放松身心", "advice": "相信直觉，倾听内心声音"},
        {"name": "星星", "emoji": "⭐", "meaning": "希望与灵感", "love": "浪漫的邂逅正在等待", "career": "创意无限，新机会出现", "health": "状态良好，适合户外活动", "advice": "保持希望，梦想终将实现"},
        {"name": "命运之轮", "emoji": "🔄", "meaning": "转变与机遇", "love": "感情有新的转机", "career": "贵人相助，把握机会", "health": "注意变化带来的压力", "advice": "顺应时势，好运即将到来"},
        {"name": "恋人", "emoji": "💕", "meaning": "爱情与选择", "love": "甜蜜时光，感情更加稳固", "career": "团队合作顺利", "health": "心情愉悦，神采飞扬", "advice": "用心感受，珍惜身边人"},
        {"name": "魔术师", "emoji": "🧙", "meaning": "创造与潜能", "love": "魅力提升，吸引力增强", "career": "能力得到认可", "health": "充满活力", "advice": "相信自己，发挥潜能"},
        {"name": "女皇", "emoji": "👑", "meaning": "丰盛与滋养", "love": "感情甜蜜，备受宠爱", "career": "事业蒸蒸日上", "health": "身心舒畅", "advice": "享受当下，心怀感恩"},
        {"name": "力量", "emoji": "💪", "meaning": "勇气与内在力量", "love": "敢于表达，突破障碍", "career": "克服困难，展现能力", "health": "体能充沛", "advice": "相信自己的力量"}
    ]

    # 幸运数据
    if st.session_state.lucky_data is None:
        lucky_num = random.randint(1, 99)
        lucky_colors = ["#FFD700", "#C44CFF", "#4ECDC4", "#FF6B6B", "#74B9FF", "#FF6B9D", "#57C84D"]
        lucky_color = random.choice(lucky_colors)
        lucky_items = ["水晶球", "星形吊坠", "紫水晶", "月光石", "幸运符", "彩虹水晶", "四叶草"]
        lucky_item = random.choice(lucky_items)
        lucky_directions = ["东方", "西方", "南方", "北方", "东南", "西南", "东北", "西北"]
        lucky_direction = random.choice(lucky_directions)
        st.session_state.lucky_data = (lucky_num, lucky_color, lucky_item, lucky_direction)
    else:
        lucky_num, lucky_color, lucky_item, lucky_direction = st.session_state.lucky_data

    # ========== 全局 CSS ==========
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        .stApp {
            background: radial-gradient(ellipse at 50% 30%, #1a1a3e 0%, #0f0c29 70%, #020011 100%) !important;
            font-family: 'Inter', sans-serif;
            color: #e0d0ff;
        }
        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 0;
            pointer-events: none;
            background:
                radial-gradient(2px 2px at 20% 30%, rgba(255,215,0,0.15), transparent),
                radial-gradient(2px 2px at 40% 70%, rgba(196, 76, 255, 0.12), transparent),
                radial-gradient(3px 3px at 60% 20%, rgba(255,215,0,0.08), transparent),
                radial-gradient(2px 2px at 80% 60%, rgba(196, 76, 255, 0.10), transparent),
                radial-gradient(2px 2px at 10% 80%, rgba(255,215,0,0.06), transparent),
                radial-gradient(3px 3px at 90% 10%, rgba(196, 76, 255, 0.08), transparent);
            background-size: 200% 200%;
            animation: nebulaDrift 40s ease-in-out infinite alternate;
        }
        @keyframes nebulaDrift {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }
        .stApp::after {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 0;
            pointer-events: none;
            background-image:
                radial-gradient(2px 2px at 10% 10%, #ffd700, transparent),
                radial-gradient(3px 3px at 30% 40%, #ffd700, transparent),
                radial-gradient(2px 2px at 50% 80%, #ffd700, transparent),
                radial-gradient(4px 4px at 70% 20%, #ffd700, transparent),
                radial-gradient(2px 2px at 90% 60%, #ffd700, transparent),
                radial-gradient(3px 3px at 15% 90%, #ffd700, transparent),
                radial-gradient(2px 2px at 85% 15%, #ffd700, transparent),
                radial-gradient(4px 4px at 45% 50%, #ffd700, transparent);
            background-size: 250% 250%;
            animation: starFall 30s linear infinite;
            opacity: 0.6;
        }
        @keyframes starFall {
            0% { background-position: 0% -10%; }
            100% { background-position: 100% 110%; }
        }
        .main, .block-container { position: relative; z-index: 1; }
        .glass-card {
            background: rgba(20, 15, 40, 0.45) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 215, 0, 0.25) !important;
            border-radius: 24px !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 20px rgba(255,215,0,0.05) !important;
            padding: 1.8rem 1.8rem !important;
            margin-bottom: 1.5rem !important;
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            border-color: rgba(255, 215, 0, 0.5) !important;
            box-shadow: 0 8px 40px rgba(255,215,0,0.15) !important;
        }
        h1, h2, h3, .main-title {
            font-family: 'Cinzel', serif !important;
            color: #ffd700 !important;
            text-shadow: 0 0 30px rgba(255,215,0,0.2), 0 0 60px rgba(255,215,0,0.1);
            letter-spacing: 1px;
        }
        .main-title {
            font-size: 3.2rem !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #ffd700, #f0e68c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 40px rgba(255,215,0,0.3);
            display: inline-block;
        }
        body, p, div, span, li { color: #d4c8f0 !important; font-weight: 300; line-height: 1.6; }
        .stButton > button {
            background: rgba(255, 215, 0, 0.08) !important;
            border: 1px solid rgba(255, 215, 0, 0.4) !important;
            border-radius: 40px !important;
            color: #ffd700 !important;
            font-family: 'Cinzel', serif !important;
            padding: 0.6rem 1.8rem !important;
            transition: all 0.4s ease !important;
            box-shadow: 0 0 15px rgba(255,215,0,0.1) !important;
            backdrop-filter: blur(4px);
        }
        .stButton > button:hover {
            background: rgba(255, 215, 0, 0.2) !important;
            border-color: #ffd700 !important;
            box-shadow: 0 0 40px rgba(255,215,0,0.3), 0 0 80px rgba(255,215,0,0.1) !important;
            transform: scale(1.03);
            color: #fff8e0 !important;
        }
        .stTabs [role="tablist"] { border-bottom: 1px solid rgba(255,215,0,0.2); }
        .stTabs [role="tab"] {
            font-family: 'Cinzel', serif;
            color: #b8a8e0 !important;
            padding: 0.5rem 1.2rem !important;
            border-radius: 20px 20px 0 0;
            transition: 0.3s;
        }
        .stTabs [role="tab"]:hover { color: #ffd700 !important; background: rgba(255,215,0,0.05); }
        .stTabs [role="tab"][aria-selected="true"] {
            color: #ffd700 !important;
            border-bottom: 2px solid #ffd700 !important;
            background: rgba(255,215,0,0.05);
        }
        .stAlert {
            background: rgba(20, 15, 40, 0.5) !important;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,215,0,0.15);
            border-radius: 16px;
            color: #e0d0ff;
        }
        .deco-star { display: inline-block; font-size: 1.4rem; margin: 0 6px; color: #ffd700; opacity: 0.6; filter: drop-shadow(0 0 6px #ffd700); }
        .block-container { animation: fadeIn 1.2s ease-out; }
        @keyframes fadeIn { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # ---------- 标题 ----------
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 2.5rem 1rem;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 12px; flex-wrap: wrap;">
            <span class="deco-star">✦</span>
            <span class="main-title">✨ 命运的答案 ✨</span>
            <span class="deco-star">✦</span>
        </div>
        <p style="font-size: 1.3rem; color: #c0b0ff; margin-top: 0.5rem;">
            <span style="color: #ffd700;">{safe_name}</span>，星辰为你指引的方向是...
        </p>
        <div style="margin-top: 0.2rem; font-size: 0.9rem; color: #8a7aaa;">☽ 聆听宇宙的低语 ☾</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- 主/辅人格 ----------
    col1, col_mid, col2 = st.columns([2, 1, 2])
    elem_icon = {"fire": "🔥", "water": "💧", "earth": "🌍", "air": "💨"}

    with col1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 2rem 1rem;">
            <div style="font-size: 4.8rem; animation: float 3s ease-in-out infinite; filter: drop-shadow(0 0 20px {p_color}55);">{elem_icon[primary]}</div>
            <div style="font-size: 0.9rem; color: #b0a0d0; letter-spacing: 2px;">⚜ 主人格 ⚜</div>
            <h2 style="color: {p_color}; font-size: 2.4rem; text-shadow: 0 0 30px {p_color}55; margin: 0.2rem 0;">{primary_type}</h2>
            <div style="font-size: 1rem; color: #b8c6db;">得分: {primary_score}/20</div>
        </div>
        """, unsafe_allow_html=True)

    with col_mid:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%; font-size: 3rem; color: rgba(255,215,0,0.6);">
            <span style="filter: drop-shadow(0 0 20px #ffd700);">✦</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 2rem 1rem; opacity: 0.85;">
            <div style="font-size: 4.8rem; animation: float 3s ease-in-out infinite; filter: drop-shadow(0 0 20px {s_color}55);">{elem_icon[secondary]}</div>
            <div style="font-size: 0.9rem; color: #b0a0d0; letter-spacing: 2px;">⚜ 辅人格 ⚜</div>
            <h2 style="color: {s_color}; font-size: 2.4rem; text-shadow: 0 0 30px {s_color}55; margin: 0.2rem 0;">{secondary_type}</h2>
            <div style="font-size: 1rem; color: #b8c6db;">得分: {secondary_score}/20</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- Tabs ----------
    tab1, tab2, tab3 = st.tabs(["📊 人格分析", "💼 职业解读", "🔮 塔罗运势"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="glass-card">
                <h3 style="margin-top: 0;">🧠 MBTI与霍兰德类型</h3>
            """, unsafe_allow_html=True)
            st.info(f"**主人格 MBTI:** {p_ana['mbti']}")
            st.info(f"**主人格 霍兰德:** {p_ana['holland']}")
            if secondary != primary:
                st.success(f"**辅人格 MBTI:** {s_ana['mbti']}")
                st.success(f"**辅人格 霍兰德:** {s_ana['holland']}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card">
                <h3>📚 学习风格建议</h3>
            """, unsafe_allow_html=True)
            st.markdown(f"""<div style="background: rgba(255,215,0,0.06); padding: 15px; border-radius: 16px; border-left: 3px solid #ffd700; color: #d4c8f0;">{p_ana['learning_style']}</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card">
                <h3>🎯 隐藏天赋</h3>
            """, unsafe_allow_html=True)
            st.markdown(f"""<div style="background: rgba(255,215,0,0.06); padding: 15px; border-radius: 16px; border-left: 3px solid #ffd700; color: #d4c8f0;">{p_ana['hidden_talent']}</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown("""
            <div class="glass-card">
                <h3>🕸️ 人格雷达图</h3>
            """, unsafe_allow_html=True)
            angles = np.linspace(0, 2 * np.pi, len(dim_names), endpoint=False).tolist()
            values = radar_dims[primary]
            values += values[:1]
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
            ax.fill(angles, values, color=p_color, alpha=0.25)
            ax.plot(angles, values, color=p_color, linewidth=2)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(dim_names, fontsize=10, color='#d4c8f0')
            ax.set_ylim(0, 100)
            ax.set_yticks([25, 50, 75, 100])
            ax.set_yticklabels(['25', '50', '75', '100'], fontsize=8, color='#8a7aaa')
            ax.spines['polar'].set_edgecolor('#ffd700')
            ax.spines['polar'].set_alpha(0.2)
            ax.grid(color='#ffd700', alpha=0.1)
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            ax.tick_params(colors='#d4c8f0')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card">
                <h3>✨ 核心人格特质</h3>
            """, unsafe_allow_html=True)
            tag_html = "".join([f"<span style='display: inline-block; background: rgba({p_color[1:]},0.2); padding: 6px 18px; border-radius: 30px; margin: 4px 6px 4px 0; border: 1px solid {p_color}55; color: {p_color}; font-size: 0.95rem;'>{t}</span>" for t in p_ana['traits']])
            st.markdown(tag_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
            <h3>💼 命运指引的职业道路</h3>
        """, unsafe_allow_html=True)
        career_html = "<div style='display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;'>"
        for c in p_ana["career"]:
            career_html += f"<span style='background: rgba(255,215,0,0.08); padding: 10px 22px; border-radius: 30px; border: 1px solid rgba(255,215,0,0.2); color: #ffd700;'>✦ {c}</span>"
        career_html += "</div>"
        st.markdown(career_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            career_desc = {
                "fire": "你天生具有领导气质，适合需要魄力和决断力的工作。敢于冒险、追求刺激的性格让你在竞争中脱颖而出。",
                "water": "你的温柔和共情能力是你的最大优势。适合帮助他人、启发他人的职业，在创意和情感领域特别有天赋。",
                "earth": "你的稳定性和可靠性让你成为团队的中流砥柱。适合需要耐心和细致的工作，注重长期发展。",
                "air": "你的逻辑思维和分析能力是你的超能力。适合需要深度思考和创新的工作，追求智慧和真理。"
            }
            st.markdown(f"""
            <div class="glass-card">
                <h3>🔥 职业性格解析</h3>
                <div style="background: rgba(255,215,0,0.05); padding: 16px; border-radius: 16px; border-left: 3px solid #ffd700;">{career_desc[primary]}</div>
            </div>
            """, unsafe_allow_html=True)

            industry_tips = {
                "fire": ["新兴行业更容易发挥你的闯劲", "互联网/创业公司适合你", "避免过于稳定的传统行业"],
                "water": ["创意文化产业非常适合你", "教育/心理领域能发挥天赋", "艺术设计类工作让你快乐"],
                "earth": ["稳健发展的行业更适合你", "国企/事业单位是好的选择", "需要耐心的长期项目很适合"],
                "air": ["科研/技术领域是你的主场", "咨询顾问类工作能发挥优势", "需要不断学习的岗位最好"]
            }
            tip_html = "".join([f"<div style='padding: 6px 0; color: #c0b0ff;'>☽ {tip}</div>" for tip in industry_tips[primary]])
            st.markdown(f"""
            <div class="glass-card">
                <h3>📈 行业发展建议</h3>
                {tip_html}
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            core_skills = {
                "fire": ["领导力与决策力", "危机处理能力", "激励团队的魅力", "商业敏感度"],
                "water": ["深度共情能力", "艺术创作天赋", "人际沟通能力", "情感洞察力"],
                "earth": ["执行力和稳定性", "团队协调能力", "细节把控能力", "问题解决能力"],
                "air": ["逻辑分析能力", "创新思维", "战略规划能力", "独立研究能力"]
            }
            skill_html = "".join([f"<span style='display:inline-block; background: rgba(255,215,0,0.08); padding: 6px 16px; border-radius: 20px; margin: 4px; border: 1px solid rgba(255,215,0,0.2); color: #ffd700;'>{sk}</span>" for sk in core_skills[primary]])
            st.markdown(f"""
            <div class="glass-card">
                <h3>⚡ 核心竞争力</h3>
                <div style="display: flex; flex-wrap: wrap;">{skill_html}</div>
            </div>
            """, unsafe_allow_html=True)

            suggestions = {
                "fire": "发挥你的领导才能，但也要学会倾听团队声音",
                "water": "善用你的共情能力，同时也要学会表达自己",
                "earth": "保持务实精神，适度跳出舒适区尝试新事物",
                "air": "发挥分析优势，注意不要过于追求完美"
            }
            st.markdown(f"""
            <div class="glass-card">
                <h3>🌟 事业成长建议</h3>
                <div style="background: rgba(255,215,0,0.05); padding: 16px; border-radius: 16px; border-left: 3px solid #ffd700; color: #ffd700;">✨ {suggestions[primary]}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3>🔮 塔罗占卜</h3>
            <p style="color: #b0a0d0;">请集中精神，点击卡牌开启今日命运指引</p>
        </div>
        """, unsafe_allow_html=True)

        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            if not st.session_state.tarot_revealed:
                st.markdown("""
                <div style="perspective: 1000px; display: flex; justify-content: center; padding: 20px 0;">
                    <div style="width: 220px; height: 320px; background: linear-gradient(145deg, #2d1b4e, #1a1a3e);
                                border-radius: 24px; border: 2px solid rgba(255,215,0,0.5);
                                box-shadow: 0 0 50px rgba(255,215,0,0.2), 0 10px 40px rgba(0,0,0,0.6);
                                display: flex; align-items: center; justify-content: center;
                                transition: transform 0.6s;
                                animation: float 4s ease-in-out infinite;">
                        <div style="font-size: 6rem; color: rgba(255,215,0,0.3); text-shadow: 0 0 30px #ffd700;">☽</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🃏 抽取塔罗牌", use_container_width=True):
                    st.session_state.tarot_selected_card = random.choice(tarot_cards)
                    st.session_state.tarot_revealed = True
                    st.rerun()
            else:
                card = st.session_state.tarot_selected_card
                st.markdown(f"""
                <div class="glass-card" style="max-width: 360px; margin: 0 auto; padding: 2rem 1.5rem; text-align: center; animation: fadeIn 0.8s ease;">
                    <div style="font-size: 4.5rem; filter: drop-shadow(0 0 30px rgba(255,215,0,0.3));">{card['emoji']}</div>
                    <div style="color: #ffd700; font-size: 2.0rem; font-family: 'Cinzel', serif; margin: 0.2rem 0;">{card['name']}</div>
                    <div style="color: #c0b0ff; font-size: 1.1rem; font-style: italic; border-bottom: 1px dashed rgba(255,215,0,0.3); padding-bottom: 0.8rem; margin-bottom: 1.2rem;">「{card['meaning']}」</div>
                    <div style="text-align: left; background: rgba(255,255,255,0.03); border-radius: 16px; padding: 1.2rem;">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 1.8rem; margin-right: 12px;">💕</span>
                            <div><div style="color: #ff6b6b; font-weight: 600; font-size: 0.8rem;">爱情运势</div><div style="color: #d4c8f0;">{card['love']}</div></div>
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 1.8rem; margin-right: 12px;">💼</span>
                            <div><div style="color: #74b9ff; font-weight: 600; font-size: 0.8rem;">事业运势</div><div style="color: #d4c8f0;">{card['career']}</div></div>
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 1.8rem; margin-right: 12px;">💚</span>
                            <div><div style="color: #57c84d; font-weight: 600; font-size: 0.8rem;">健康运势</div><div style="color: #d4c8f0;">{card['health']}</div></div>
                        </div>
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 1.8rem; margin-right: 12px;">✨</span>
                            <div><div style="color: #ffd700; font-weight: 600; font-size: 0.8rem;">今日箴言</div><div style="color: #d4c8f0;">{card['advice']}</div></div>
                        </div>
                    </div>
                    <div style="margin-top: 1rem; color: rgba(255,215,0,0.4); font-size: 0.8rem; letter-spacing: 4px;">✦ 命运的低语 ✦</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔄 重新抽取", use_container_width=True):
                    st.session_state.tarot_revealed = False
                    st.session_state.tarot_selected_card = None
                    st.rerun()

        # 幸运指南
        st.markdown("---")
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3>🍀 今日幸运指南</h3>
        </div>
        """, unsafe_allow_html=True)
        col_l1, col_l2, col_l3, col_l4 = st.columns(4)
        with col_l1:
            st.markdown(f"""<div class="glass-card" style="text-align: center; padding: 1rem 0.5rem;"><div style="font-size: 2rem;">🔢</div><div style="color: #b0a0d0;">幸运数字</div><div style="color: #ffd700; font-size: 1.8rem; font-weight: bold;">{lucky_num}</div></div>""", unsafe_allow_html=True)
        with col_l2:
            st.markdown(f"""<div class="glass-card" style="text-align: center; padding: 1rem 0.5rem;"><div style="font-size: 2rem;">🎨</div><div style="color: #b0a0d0;">幸运颜色</div><div><span style="display: inline-block; width: 30px; height: 30px; background: {lucky_color}; border-radius: 50%; box-shadow: 0 0 30px {lucky_color};"></span></div></div>""", unsafe_allow_html=True)
        with col_l3:
            st.markdown(f"""<div class="glass-card" style="text-align: center; padding: 1rem 0.5rem;"><div style="font-size: 2rem;">📿</div><div style="color: #b0a0d0;">幸运物</div><div style="color: #ffd700;">{lucky_item}</div></div>""", unsafe_allow_html=True)
        with col_l4:
            st.markdown(f"""<div class="glass-card" style="text-align: center; padding: 1rem 0.5rem;"><div style="font-size: 2rem;">🧭</div><div style="color: #b0a0d0;">幸运方位</div><div style="color: #ffd700;">{lucky_direction}</div></div>""", unsafe_allow_html=True)

    # 重新测试按钮
    col1_reset, col2_reset, col3_reset = st.columns([1, 2, 1])
    with col2_reset:
        if st.button("🔮 再次探索命运的奥秘", use_container_width=True):
            for key in ["page", "name", "answers", "scores", "current_question", "tarot_revealed", "tarot_selected_card", "lucky_data"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ---------- 主路由 ----------
def main():
    page = st.session_state.get("page", "cover")
    if page == "cover":
        render_cover()
    elif page == "quiz":
        render_quiz()
    elif page == "results":
        show_results()
    else:
        render_cover()

if __name__ == "__main__":
    main()
