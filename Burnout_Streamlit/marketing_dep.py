"""marketing_dep.py — Marketing department dashboard."""
import streamlit as st
import pandas as pd
import theme
from utils import load_model, predict, risk_label, back_button
from dep_dashboard import render

DEPT_NAME = "Marketing"
DEPT_KEY  = "Marketing"
ICON      = "📣"
COLOR     = "#a855f7"


def show():
    theme.inject()
    back_button("manager", "← Back to Departments")
    theme.page_header(ICON, f"{DEPT_NAME} Department",
                      "Burnout risk, workload pressure, and wellness signals for Marketing employees")

    model = load_model()
    if model is None:
        st.error("❌ `stacking_burnout_model.joblib` not found in the app folder.")
        return

    with st.sidebar:
        st.markdown(f"### {ICON} {DEPT_NAME} Data")
        data_file = st.file_uploader(f"{DEPT_NAME} Dataset (.csv)", type=["csv"])
        st.markdown("---")
        use_role_mean = st.checkbox("Recompute role_encoded from data", value=False)

    if not data_file:
        st.markdown(f"""
        <div style="background:#1a1a1a; border:1px dashed {COLOR}44; border-radius:12px;
                    padding:2rem; text-align:center;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">{ICON}</div>
            <div style="font-weight:600; color:#f5f5f5; margin-bottom:0.3rem;">Upload {DEPT_NAME} data</div>
            <div style="font-size:0.87rem; color:#9ca3af;">
                Upload the {DEPT_NAME} CSV (or full master CSV) in the sidebar.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    df_raw = pd.read_csv(data_file)
    if "broad_department" in df_raw.columns:
        vals = df_raw["broad_department"].unique().tolist()
        if DEPT_KEY in vals and len(vals) > 1:
            st.info(f"ℹ️ Full dataset detected — filtering to **{DEPT_KEY}** employees only.")
            df_raw = df_raw[df_raw["broad_department"] == DEPT_KEY].reset_index(drop=True)

    if len(df_raw) == 0:
        st.warning(f"⚠️ No employees found for department '{DEPT_KEY}'.")
        return

    st.markdown(f"""
    <div style="background:#1a1a1a; border:1px solid #2e2e2e; border-left:3px solid {COLOR};
                border-radius:10px; padding:0.7rem 1.2rem; margin-bottom:1.2rem;
                display:flex; align-items:center; gap:10px;">
        <span style="color:#22c55e;">✓</span>
        <span style="color:#d1d5db; font-size:0.9rem;">
            <strong style="color:#f5f5f5;">{len(df_raw):,}</strong> {DEPT_NAME} employees loaded.
        </span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(f"🔥 Scoring {DEPT_NAME} team…"):
        preds = predict(df_raw, model, use_role_mean)

    df_result = df_raw.copy()
    df_result["predicted_burnout"] = preds
    df_result["risk_level"]        = df_result["predicted_burnout"].apply(risk_label)

    render(df_result, DEPT_NAME, preds)
