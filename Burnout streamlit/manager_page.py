"""
manager_page.py  –  Manager navigator: choose a department
"""
import streamlit as st
from utils import back_button


DEPARTMENTS = {
    "HR":        {"icon": "🧑‍💼", "desc": "Human Resources team burnout insights.",       "page": "dep_hr"},
    "Finance":   {"icon": "💰", "desc": "Finance department risk and workload trends.",    "page": "dep_finance"},
    "Tech":      {"icon": "💻", "desc": "Technical team burnout patterns and drivers.",    "page": "dep_tech"},
    "Marketing": {"icon": "📣", "desc": "Marketing team satisfaction and burnout scores.", "page": "dep_marketing"},
}


def show():
    back_button("home", "← Back to Portal")
    st.title("👔 Manager — Department Navigator")
    st.markdown("Select a department to view its detailed burnout dashboard.")
    st.markdown("---")

    cols = st.columns(2, gap="large")
    for idx, (dept, info) in enumerate(DEPARTMENTS.items()):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div style="border:1px solid #e0e0e0; border-radius:14px; padding:1.5rem;
                            background:#fafafa; margin-bottom:1rem; text-align:center;">
                    <div style="font-size:2.5rem;">{info['icon']}</div>
                    <div style="font-size:1.2rem; font-weight:700; margin:0.4rem 0 0.2rem;">{dept}</div>
                    <div style="color:#666; font-size:0.88rem;">{info['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {dept} Dashboard", key=f"btn_{dept}", use_container_width=True):
                st.session_state.page = info["page"]
                st.rerun()
