import streamlit as st
from ultralytics import YOLO
from PIL import Image

st.set_page_config(
    page_title="手语识别系统",
    page_icon="✋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CSS 高级感 ==========
st.markdown("""
<style>
    /* ===== 全局 ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .stApp {
        background: #e8ecf1;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ===== 毛玻璃效果 ===== */
    .glass {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .glass:hover {
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.10);
        transform: translateY(-2px);
    }

    /* ===== 隐藏默认 ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ===== 侧边栏 ===== */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        margin: 16px 0 16px 16px;
        padding: 24px 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
    }

    /* ===== 顶部导航 ===== */
    .navbar {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 24px;
        padding: 16px 32px;
        margin-bottom: 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }

    .navbar .logo {
        font-size: 22px;
        font-weight: 700;
        color: #0a0a0a;
        letter-spacing: -0.3px;
    }

    .navbar .logo span {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .navbar .badge {
        background: rgba(79, 70, 229, 0.12);
        color: #4f46e5;
        padding: 6px 18px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 0.2px;
        border: 1px solid rgba(79, 70, 229, 0.08);
    }

    /* ===== 标题 ===== */
    .hero {
        margin-bottom: 32px;
    }

    .hero h1 {
        font-size: 40px;
        font-weight: 700;
        color: #0a0a0a;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .hero h1 span {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        font-size: 16px;
        color: #6b7280;
        margin-top: 6px;
        font-weight: 400;
    }

    /* ===== 卡片 ===== */
    .card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }

    .card:hover {
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.06);
        transform: translateY(-2px);
    }

    .card .label {
        font-size: 13px;
        font-weight: 500;
        color: #6b7280;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .card .value {
        font-size: 32px;
        font-weight: 700;
        color: #0a0a0a;
        letter-spacing: -0.5px;
    }

    .card .value.blue { color: #4f46e5; }
    .card .value.green { color: #16a34a; }
    .card .value.orange { color: #f59e0b; }

    /* ===== 上传区域 ===== */
    .upload-zone {
        border: 2px dashed rgba(79, 70, 229, 0.25);
        border-radius: 20px;
        padding: 48px 20px;
        text-align: center;
        background: rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .upload-zone:hover {
        border-color: rgba(79, 70, 229, 0.5);
        background: rgba(255, 255, 255, 0.6);
        transform: scale(1.01);
    }

    .upload-zone .icon {
        font-size: 44px;
        margin-bottom: 12px;
        display: block;
    }

    .upload-zone .text {
        font-size: 16px;
        color: #374151;
        font-weight: 500;
    }

    .upload-zone .hint {
        font-size: 13px;
        color: #9ca3af;
        margin-top: 6px;
    }

    /* ===== 按钮 ===== */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        font-weight: 500;
        font-size: 15px;
        border: none;
        border-radius: 14px;
        padding: 12px 32px;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.2);
        letter-spacing: 0.2px;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 32px rgba(79, 70, 229, 0.30);
    }

    .stButton > button:active {
        transform: scale(0.98);
    }

    /* ===== 结果标签 ===== */
    .result-tag {
        display: inline-block;
        background: rgba(79, 70, 229, 0.08);
        color: #4f46e5;
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 14px;
        font-weight: 500;
        border: 1px solid rgba(79, 70, 229, 0.06);
        margin: 2px 4px 2px 0;
    }

    /* ===== 状态栏 ===== */
    .status-bar {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 16px;
        padding: 14px 24px;
        margin-top: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        color: #6b7280;
    }

    .status-bar .dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 10px;
        background: #22c55e;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ===== 统计卡片行 ===== */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }

    @media (max-width: 768px) {
        .stat-grid { grid-template-columns: 1fr; }
        .navbar { flex-direction: column; gap: 12px; text-align: center; }
        .hero h1 { font-size: 28px; }
    }
</style>
""", unsafe_allow_html=True)

# ========== 顶部导航 ==========
st.markdown("""
<div class="navbar">
    <div class="logo">✋ 手语<span>识别</span></div>
    <div class="badge">YOLOv8 · 19 类手势</div>
</div>
""", unsafe_allow_html=True)

# ========== 标题 ==========
st.markdown("""
<div class="hero">
    <h1>智能<span>手语</span>识别系统</h1>
    <p>上传手势图片，AI 自动识别手语含义 · 基于 YOLOv8 深度学习</p>
</div>
""", unsafe_allow_html=True)

# ========== 统计卡片 ==========
st.markdown("""
<div class="stat-grid">
    <div class="card"><div class="label">手势类别</div><div class="value blue">19</div></div>
    <div class="card"><div class="label">模型输入</div><div class="value green">128×128</div></div>
    <div class="card"><div class="label">推理引擎</div><div class="value orange">YOLOv8</div></div>
</div>
""", unsafe_allow_html=True)

# ========== 映射表 ==========
name_map = {
    "morning": "早上好", "time": "时间", "happy": "开心",
    "new": "新", "wish": "愿望", "please": "拜托",
    "road": "公路", "birthday": "生日", "friend": "朋友",
    "know": "知道", "thank you": "谢谢你", "love": "爱",
    "good": "很好", "you": "你/你的", "stop": "停下",
    "walk": "步行", "name": "名称", "what": "什么",
    "person": "人", "introduce": "介绍", "safe": "安全",
    "door": "门", "today": "现今", "tea": "茶",
    "have": "拥有", "slow": "慢", "late": "深夜",
    "night": "深夜", "I": "我", "me": "我",
    "flat": "平面", "business card": "名片", "pea": "豌豆"
}


# ========== 加载模型 ==========
@st.cache_resource
def load_model():
    return YOLO("best.pt")


model = load_model()

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown('<div style="font-weight:600; font-size:16px; color:#0a0a0a; margin-bottom:16px;">⚙️ 控制面板</div>',
                unsafe_allow_html=True)
    confidence = st.slider("置信度阈值", 0.0, 1.0, 0.25, 0.05)
    st.markdown("---")
    st.markdown('<div style="font-weight:600; font-size:14px; color:#374151; margin-bottom:10px;">📋 可识别手势</div>',
                unsafe_allow_html=True)
    for item in sorted(set(name_map.values())):
        st.markdown(f'<div style="font-size:13px; color:#6b7280; padding:3px 0;">• {item}</div>',
                    unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:12px; color:#9ca3af;">📌 上传图片 → 点击识别 → 查看结果</div>',
                unsafe_allow_html=True)

# ========== 主区域 ==========
uploaded_file = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png", "bmp"],
    label_visibility="collapsed"
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        '<div class="card"><div style="font-weight:600; font-size:15px; color:#0a0a0a; margin-bottom:12px;">📷 原始图片</div>',
        unsafe_allow_html=True)
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    else:
        st.markdown("""
        <div class="upload-zone">
            <span class="icon">🖼️</span>
            <div class="text">点击上方按钮上传图片</div>
            <div class="hint">支持 JPG · PNG · BMP</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown(
        '<div class="card"><div style="font-weight:600; font-size:15px; color:#0a0a0a; margin-bottom:12px;">🎯 检测结果</div>',
        unsafe_allow_html=True)
    if uploaded_file is not None:
        if st.button("🚀 开始识别", use_container_width=True):
            with st.spinner("⏳ 正在分析..."):
                image = Image.open(uploaded_file)
                results = model(image, conf=confidence)
                annotated = results[0].plot()
                st.image(annotated, use_container_width=True)
                if results[0].boxes is not None:
                    st.markdown(
                        f'<div style="margin-top:12px; color:#16a34a; font-weight:500;">✅ 检测到 {len(results[0].boxes)} 个手势</div>',
                        unsafe_allow_html=True)
                    for box in results[0].boxes:
                        cls_id = int(box.cls[0])
                        cls_name = model.names[cls_id]
                        cn_name = name_map.get(cls_name, cls_name)
                        conf_val = float(box.conf[0])
                        st.markdown(
                            f'<div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f1f5f9; font-size:14px;"><span>{cn_name}</span><span style="color:#4f46e5; font-weight:600;">{conf_val:.1%}</span></div>',
                            unsafe_allow_html=True)
                else:
                    st.markdown('<div style="margin-top:12px; color:#d97706;">⚠️ 未检测到手势，请调整置信度或换图</div>',
                                unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#9ca3af; text-align:center; padding:40px 0;">👈 请先上传图片</div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 底部状态栏 ==========
st.markdown("""
<div class="status-bar">
    <span><span class="dot"></span>模型已加载，可开始识别</span>
    <span>✋ 手语识别 · YOLOv8 · 19 类</span>
</div>
""", unsafe_allow_html=True)