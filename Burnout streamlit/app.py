import streamlit as st

st.set_page_config(
    page_title="Burnout Prediction Portal",
    page_icon="🔥",
    layout="centered",
)

# ── Session state init ──────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── Router ──────────────────────────────────────────────────────────
if st.session_state.page == "hr":
    import hr_page
    hr_page.show()

elif st.session_state.page == "manager":
    import manager_page
    manager_page.show()

elif st.session_state.page == "dep_hr":
    import hr_dep
    hr_dep.show()

elif st.session_state.page == "dep_finance":
    import finance_dep
    finance_dep.show()

elif st.session_state.page == "dep_marketing":
    import marketing_dep
    marketing_dep.show()

elif st.session_state.page == "dep_tech":
    import technical_dep
    technical_dep.show()

else:
    # ── Home / Landing ───────────────────────────────────────────────
    st.markdown(
        """
        <style>
        .portal-title {
            font-size: 2.8rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .portal-sub {
            text-align: center;
            color: #888;
            margin-bottom: 2.5rem;
            font-size: 1.05rem;
        }
        .card {
            border: 1px solid #e0e0e0;
            border-radius: 14px;
            padding: 2rem 1.5rem;
            text-align: center;
            background: #fafafa;
        }
        .card-icon  { font-size: 3rem; }
        .card-title { font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0 0.3rem; }
        .card-desc  { color: #666; font-size: 0.9rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="portal-title">🔥 Burnout Prediction Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="portal-sub">Select your role to access the right dashboard</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">🏢</div>
                <div class="card-title">HR Dashboard</div>
                <div class="card-desc">Full company-wide burnout overview, predictions, and risk analytics across all departments.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Enter as HR", use_container_width=True, type="primary"):
            st.session_state.page = "hr"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">👔</div>
                <div class="card-title">Manager Dashboard</div>
                <div class="card-desc">Department-level view. Drill down into HR, Finance, Tech, or Marketing team insights.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Enter as Manager", use_container_width=True):
            st.session_state.page = "manager"
            st.rerun()
