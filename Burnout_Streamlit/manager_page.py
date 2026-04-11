"""manager_page.py — Manager navigator: choose a department."""
import streamlit as st
import theme
from utils import back_button

DEPARTMENTS = [
    {"name": "HR",        "icon": "🧑‍💼", "color": "#f97316", "page": "dep_hr",
     "desc": "Human resources team burnout risk and wellness indicators."},
    {"name": "Finance",   "icon": "💰", "color": "#f59e0b", "page": "dep_finance",
     "desc": "Finance department workload pressure and risk trends."},
    {"name": "Tech",      "icon": "💻", "color": "#ef4444", "page": "dep_tech",
     "desc": "Technical team burnout patterns, overtime, and satisfaction."},
    {"name": "Marketing", "icon": "📣", "color": "#a855f7", "page": "dep_marketing",
     "desc": "Marketing team goal pressure and engagement analysis."},
]


def show():
    theme.inject()
    back_button("home", "← Back to Portal")
    theme.page_header("👔", "Manager Dashboard", "Select a department to view detailed burnout insights")

    st.markdown("""
    <div style="background:#1a1a1a; border:1px solid #2e2e2e; border-radius:10px;
                padding:0.9rem 1.2rem; margin-bottom:1.8rem; display:flex; align-items:center; gap:10px;">
        <span style="font-size:1rem;">⚠️</span>
        <span style="color:#9ca3af; font-size:0.87rem;">
            Upload a department CSV or the full master dataset — the dashboard will filter automatically.
        </span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2, gap="large")
    for idx, dept in enumerate(DEPARTMENTS):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="background:#1a1a1a; border:1px solid #2e2e2e;
                        border-top:3px solid {dept['color']}; border-radius:14px;
                        padding:1.6rem 1.4rem; margin-bottom:0.8rem;">
                <div style="font-size:1.8rem; margin-bottom:0.6rem;">{dept['icon']}</div>
                <div style="font-size:1.05rem; font-weight:700; color:#f5f5f5; margin-bottom:0.3rem;">
                    {dept['name']} Department
                </div>
                <div style="color:#9ca3af; font-size:0.85rem; line-height:1.5;">
                    {dept['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {dept['name']} Dashboard →", key=f"btn_{dept['name']}",
                         use_container_width=True):
                st.session_state.page = dept["page"]
                st.rerun()
