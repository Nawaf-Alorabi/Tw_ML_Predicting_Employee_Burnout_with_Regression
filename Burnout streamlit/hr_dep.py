"""
hr_dep.py  –  HR department-level dashboard
"""
import streamlit as st
import pandas as pd
from utils import load_model, predict, risk_label, back_button
from dep_dashboard import render


DEPT_NAME   = "HR"
DEPT_KEY    = "HR"   # value in broad_department column


def show():
    back_button("manager", "← Back to Manager Navigator")
    st.title(f"🧑‍💼 {DEPT_NAME} Department Dashboard")
    st.markdown("Upload the **HR department dataset** to view burnout insights for HR employees.")

    model = load_model()
    if model is None:
        st.error("❌ Model file `stacking_burnout_model.joblib` not found. Place it in the app folder.")
        return

    with st.sidebar:
        st.header(f"📂 Upload {DEPT_NAME} Data")
        data_file = st.file_uploader(f"{DEPT_NAME} Employee Dataset (.csv)", type=["csv"])
        st.markdown("---")
        use_role_mean = st.checkbox("Recompute role_encoded from data", value=False)

    if not data_file:
        st.info(f"👈 Upload the {DEPT_NAME} department CSV in the sidebar.")
        return

    df_raw = pd.read_csv(data_file)

    # Filter to this department if the file is the full master dataset
    if "broad_department" in df_raw.columns:
        dept_vals = df_raw["broad_department"].unique().tolist()
        if DEPT_KEY in dept_vals and len(dept_vals) > 1:
            st.info(f"ℹ️ Full dataset detected — filtering to **{DEPT_KEY}** employees only.")
            df_raw = df_raw[df_raw["broad_department"] == DEPT_KEY].reset_index(drop=True)

    if len(df_raw) == 0:
        st.warning(f"⚠️ No employees found for department '{DEPT_KEY}'.")
        return

    st.success(f"✅ Loaded **{len(df_raw):,} {DEPT_NAME} employees**.")

    with st.spinner("Generating predictions…"):
        preds = predict(df_raw, model, use_role_mean)

    df_result = df_raw.copy()
    df_result["predicted_burnout"] = preds
    df_result["risk_level"]        = df_result["predicted_burnout"].apply(risk_label)

    render(df_result, DEPT_NAME, preds)
