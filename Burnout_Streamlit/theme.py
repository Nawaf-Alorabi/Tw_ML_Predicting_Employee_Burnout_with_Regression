"""
theme.py  —  shared burnout-themed CSS, injected into every page.
"""
import streamlit as st

BURNOUT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f0f0f !important;
    font-family: 'Inter', sans-serif !important;
    color: #f5f5f5 !important;
}
[data-testid="stSidebar"] {
    background-color: #141414 !important;
    border-right: 1px solid #2e2e2e !important;
}
[data-testid="stHeader"] { background-color: #0f0f0f !important; }

h1, h2, h3, h4, h5 {
    color: #f5f5f5 !important;
    font-family: 'Inter', sans-serif !important;
}
h1 { font-size: 1.7rem !important; font-weight: 700 !important; }
h2 { font-size: 1.2rem !important; font-weight: 600 !important; color: #f97316 !important; }

.stButton > button {
    background: linear-gradient(135deg, #f97316, #ef4444) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
    background: #1e1e1e !important;
    color: #f5f5f5 !important;
    border: 1px solid #3a3a3a !important;
}

[data-testid="metric-container"] {
    background: #1a1a1a !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="stMetricLabel"] { color: #9ca3af !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: #f97316 !important; font-weight: 700 !important; }

[data-testid="stFileUploader"] {
    background: #1a1a1a !important;
    border: 1px dashed #3a3a3a !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] p { color: #9ca3af !important; }

[data-testid="stDataFrame"] {
    background: #1a1a1a !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 10px !important;
}

[data-testid="stAlert"] { border-radius: 10px !important; }

[data-baseweb="select"] * { background: #1e1e1e !important; color: #f5f5f5 !important; }
[data-baseweb="tag"] { background: #f97316 !important; color: #fff !important; }

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f5f5f5 !important; }

[data-testid="stCheckbox"] label { color: #d1d5db !important; }
[data-testid="stCaptionContainer"] p { color: #9ca3af !important; }

[data-testid="stDownloadButton"] > button {
    background: #1a1a1a !important;
    color: #f97316 !important;
    border: 1px solid #f97316 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #f97316 !important;
    color: #fff !important;
}

hr { border-color: #2e2e2e !important; }
details { background: #1a1a1a !important; border: 1px solid #2e2e2e !important; border-radius: 10px !important; }
details summary { color: #f5f5f5 !important; }
.vega-embed { background: transparent !important; }
canvas { background: transparent !important; }
[data-testid="stVegaLiteChart"] { background: transparent !important; }

table { color: #f5f5f5 !important; border-color: #2e2e2e !important; }
th { background: #1a1a1a !important; color: #f97316 !important; }
td { background: #0f0f0f !important; }

.burn-page-header {
    border-left: 4px solid #f97316;
    padding: 0.5rem 0 0.5rem 1rem;
    margin-bottom: 1.5rem;
}
.burn-page-header h1 { margin: 0 !important; font-size: 1.6rem !important; font-weight: 700 !important; color: #f5f5f5 !important; }
.burn-page-header p  { margin: 0.2rem 0 0 !important; color: #9ca3af !important; font-size: 0.88rem !important; }
.burn-section-label  { font-size: 0.7rem; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: #f97316; margin-bottom: 0.5rem; }
</style>
"""


def inject():
    st.markdown(BURNOUT_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="burn-page-header">
        <h1>{icon}&nbsp;{title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>""", unsafe_allow_html=True)


def section_label(text: str):
    st.markdown(f'<div class="burn-section-label">{text}</div>', unsafe_allow_html=True)
