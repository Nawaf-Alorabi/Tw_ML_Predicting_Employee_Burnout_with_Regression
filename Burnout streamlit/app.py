import streamlit as st

st.set_page_config(
    page_title="Burnout Intelligence Platform",
    page_icon="🔥",
    layout="wide",
)

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "hr":
    import hr_page; hr_page.show()
elif st.session_state.page == "manager":
    import manager_page; manager_page.show()
elif st.session_state.page == "dep_hr":
    import hr_dep; hr_dep.show()
elif st.session_state.page == "dep_finance":
    import finance_dep; finance_dep.show()
elif st.session_state.page == "dep_marketing":
    import marketing_dep; marketing_dep.show()
elif st.session_state.page == "dep_tech":
    import technical_dep; technical_dep.show()
else:
    import theme; theme.inject()

    # ── Extra CSS to style the st.button inside each card column ─────
    st.markdown("""
    <style>
    /* Remove default Streamlit block padding so cards feel tight */
    [data-testid="column"] { padding: 0 !important; }

    /* Card wrappers */
    .portal-card-hr {
        background: #1a1a1a;
        border: 1px solid #2e2e2e;
        border-top: 3px solid #f97316;
        border-radius: 14px;
        padding: 1.8rem 1.5rem 1.2rem;
        margin-bottom: 0.75rem;
    }
    .portal-card-mgr {
        background: #1a1a1a;
        border: 1px solid #2e2e2e;
        border-top: 3px solid #f59e0b;
        border-radius: 14px;
        padding: 1.8rem 1.5rem 1.2rem;
        margin-bottom: 0.75rem;
    }
    .portal-card-icon  { font-size: 1.8rem; margin-bottom: 0.6rem; }
    .portal-card-title { font-size: 1.1rem; font-weight: 700; color: #f5f5f5; margin-bottom: 0.35rem; }
    .portal-card-desc  { color: #9ca3af; font-size: 0.86rem; line-height: 1.6; margin-bottom: 1rem; }
    .portal-tags       { display: flex; gap: 6px; flex-wrap: wrap; }
    .portal-tag        { font-size: 0.7rem; border-radius: 5px; padding: 3px 8px;
                         background: #111; border: 1px solid #2e2e2e; }

    /* Stats bar */
    .stats-bar {
        display: flex;
        gap: 0;
        max-width: 720px;
        margin: 1.5rem auto 0;
        padding: 1rem 2rem;
        background: #1a1a1a;
        border: 1px solid #2e2e2e;
        border-radius: 12px;
        justify-content: space-around;
        align-items: center;
    }
    .stats-bar-item { text-align: center; }
    .stats-bar-val   { font-size: 1.3rem; font-weight: 700; color: #f97316; }
    .stats-bar-label { font-size: 0.72rem; color: #9ca3af; margin-top: 2px; }
    .stats-divider   { width: 1px; background: #2e2e2e; height: 32px; }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:2.5rem 1rem 0.5rem;">
        <div style="font-size:3rem; line-height:1;">🔥</div>
        <h1 style="font-size:2.2rem; font-weight:700; color:#f97316;
                   margin:0.3rem 0 0; letter-spacing:-0.5px;">
            Burnout Intelligence Platform
        </h1>
        <p style="color:#9ca3af; font-size:0.95rem; margin-top:0.5rem;
                  max-width:460px; margin-inline:auto; line-height:1.6;">
            AI-powered burnout prediction to protect your people before the fire spreads.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ── Two-column card layout ────────────────────────────────────────
    _, col1, spacer, col2, _ = st.columns([0.5, 3, 0.3, 3, 0.5])

    with col1:
        st.markdown("""
        <div class="portal-card-hr">
            <div class="portal-card-icon">🏢</div>
            <div class="portal-card-title">HR Dashboard</div>
            <div class="portal-card-desc">
                Company-wide burnout view. Upload the full master dataset and get instant
                AI predictions, risk segmentation, and department comparisons.
            </div>
            <div class="portal-tags">
                <span class="portal-tag" style="color:#f97316;">All departments</span>
                <span class="portal-tag" style="color:#f97316;">AI predictions</span>
                <span class="portal-tag" style="color:#f97316;">Risk scoring</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏢  Enter as HR", use_container_width=True, type="primary", key="btn_hr"):
            st.session_state.page = "hr"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="portal-card-mgr">
            <div class="portal-card-icon">👔</div>
            <div class="portal-card-title">Manager Dashboard</div>
            <div class="portal-card-desc">
                Drill into your department. Choose HR, Finance, Tech, or Marketing
                for focused analysis, role-level insights, and high-risk alerts.
            </div>
            <div class="portal-tags">
                <span class="portal-tag" style="color:#f59e0b;">Per department</span>
                <span class="portal-tag" style="color:#f59e0b;">Role breakdown</span>
                <span class="portal-tag" style="color:#f59e0b;">Exportable CSV</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👔  Enter as Manager", use_container_width=True, key="btn_mgr"):
            st.session_state.page = "manager"
            st.rerun()

    # ── Stats bar ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="stats-bar">
        <div class="stats-bar-item">
            <div class="stats-bar-val">4</div>
            <div class="stats-bar-label">Departments</div>
        </div>
        <div class="stats-divider"></div>
        <div class="stats-bar-item">
            <div class="stats-bar-val">ML</div>
            <div class="stats-bar-label">Stacking ensemble</div>
        </div>
        <div class="stats-divider"></div>
        <div class="stats-bar-item">
            <div class="stats-bar-val">4</div>
            <div class="stats-bar-label">Risk levels</div>
        </div>
        <div class="stats-divider"></div>
        <div class="stats-bar-item">
            <div class="stats-bar-val">Live</div>
            <div class="stats-bar-label">Instant predictions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)