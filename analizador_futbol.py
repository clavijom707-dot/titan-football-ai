import streamlit as st

st.set_page_config(page_title="Titan Football AI PRO", page_icon="⚽", layout="wide")

# Todo el CSS debe estar dentro de estas comillas triples:
st.markdown("""
    <style>
    /* 1. CABECERA */
    [data-testid="stHeader"] {
        background-color: #0e1117 !important;
    }
    
    /* 2. OCULTAR ELEMENTOS */
    [data-testid="stToolbar"] { display: none !important; }
    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* 3. FLECHITA DEL SIDEBAR */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stExpandSidebarButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 50% !important;
        left: 0 !important;
        transform: translateY(-50%) !important;
        z-index: 999999 !important;
        background-color: #161b22 !important;
        border: 1px solid #00ff87 !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 10px 8px !important;
        cursor: pointer !important;
    }

    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #00ff87 !important;
        color: #00ff87 !important;
        width: 22px !important;
        height: 22px !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* 4. ESTILOS GENERALES */
    html, body, [data-testid="stAppViewContainer"], .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Helvetica Neue', sans-serif; }
    
    .big-title { font-size: 3.5rem; font-weight: 900; color: #00ff87 !important; text-align: center; margin-bottom: 0; }
    .sub-title { font-size: 1.2rem; color: #a0aab5 !important; text-align: center; margin-bottom: 30px; }
    
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stNumberInput input { background-color: #1e2530 !important; color: #ffffff !important; border: 1px solid #00ff87 !important; border-radius: 8px !important; }
    
    ul[data-testid="stSelectboxVirtualDropdown"] { background-color: #1e2530 !important; }
    li[role="option"] { color: #ffffff !important; }
    li[role="option"]:hover { background-color: #00ff87 !important; color: #0e1117 !important; }

    .stButton > button { background-color: #00ff87 !important; color: #0e1117 !important; font-weight: bold !important; font-size: 1.2rem !important; border-radius: 8px !important; width: 100% !important; border: none !important; }
    .stButton > button:hover { background-color: #00cc6a !important; color: #0e1117 !important; border: none !important; }
    
    [data-testid="stSidebar"] { background-color: #161b22 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.2rem; font-weight: bold; color: #ffffff; }
    .stTabs [aria-selected="true"] { color: #00ff87 !important; border-bottom-color: #00ff87 !important; }

    .contexto-box { background-color: #1e2530; border: 1px solid #00ff87; border-radius: 8px; padding: 10px 15px; margin-bottom: 15px; font-size: 0.9rem; color: #a0aab5 !important; }
    .sidebar-info { background-color: #1e2530; border-radius: 8px; padding: 10px; color: #a0aab5 !important; font-size: 0.9rem; }
    .stAlert > div { background-color: #1e2530 !important; color: #00ff87 !important; border: 1px solid #00ff87 !important; }
    .stAlert p { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# ... El resto de tu código (token, memoria, funciones, etc.) continúa normal aquí abajo ...
