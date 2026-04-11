"""
hr_page.py  –  Company-wide HR dashboard (full dataset)
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from utils import load_model, predict, risk_label, back_button, RISK_ORDER, RISK_COLORS


def show():
    # ── Back button ──────────────────────────────────────────────────
    back_button("home", "← Back to Portal")
    st.title("🏢 HR — Company-Wide Burnout Dashboard")
    st.markdown("Upload the **full employee dataset** to generate company-wide predictions.")

    # ── Load model ───────────────────────────────────────────────────
    model = load_model()
    if model is None:
        st.error("❌ Model file `stacking_burnout_model.joblib` not found. Place it in the app folder.")
        return

    # ── Sidebar ──────────────────────────────────────────────────────
    with st.sidebar:
        st.header("📂 Upload Dataset")
        data_file = st.file_uploader("Full Employee Dataset (.csv)", type=["csv"])
        st.markdown("---")
        use_role_mean = st.checkbox(
            "Recompute role_encoded from data",
            value=False,
            help="Re-derives role_encoded as the mean burnout_score per role.",
        )

    if not data_file:
        st.info("👈 Upload the full company employee CSV in the sidebar to get started.")
        with st.expander("ℹ️ Required CSV Columns"):
            st.markdown("""
| Column | Description |
|---|---|
| `broad_department` | Department name (Finance, Tech, HR, Marketing) |
| `role` | Job title |
| `role_encoded` | Numeric target-encoded role value |
| `workload_score` | Normalized workload (0–1) |
| `overtime_hours` | Overtime hours per week |
| `role_complexity_score` | Role complexity (0–1) |
| `satisfaction_score` | Job satisfaction (0–1) |
| `team_sentiment` | Team sentiment score (0–1) |
| `career_progression_score` | Career growth score (0–1) |
| `goal_achievement_rate` | % of goals achieved (0–1) |
| `meeting_participation` | Meeting participation rate (0–1) |
| `burnout_score` | *(optional)* Ground truth |
            """)
        return

    df_raw = pd.read_csv(data_file)
    st.success(f"✅ Loaded **{len(df_raw):,} employees** across all departments.")

    if "broad_department" not in df_raw.columns:
        st.error("❌ Column `broad_department` not found.")
        return

    # ── Predict ──────────────────────────────────────────────────────
    with st.spinner("Generating predictions…"):
        preds = predict(df_raw, model, use_role_mean)

    df_result = df_raw.copy()
    df_result["predicted_burnout"] = preds
    df_result["risk_level"]        = df_result["predicted_burnout"].apply(risk_label)
    departments = sorted(df_result["broad_department"].dropna().unique().tolist())

    # ── KPIs ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📊 Company-Wide Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean Burnout Score",     f"{preds.mean():.3f}")
    c2.metric("Max Burnout Score",      f"{preds.max():.3f}")
    c3.metric("Min Burnout Score",      f"{preds.min():.3f}")
    c4.metric("High / Critical Risk %", f"{(preds >= 0.60).mean()*100:.1f}%")

    # ── Pie chart ─────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🥧 Company Risk Level Distribution")

    risk_counts = df_result["risk_level"].value_counts()
    labels  = [r for r in RISK_ORDER if r in risk_counts.index]
    sizes   = [risk_counts[r] for r in labels]
    colors  = [RISK_COLORS[RISK_ORDER.index(r)] for r in labels]

    fig, ax = plt.subplots(figsize=(5, 5))
    _, _, autotexts = ax.pie(
        sizes, labels=None, colors=colors,
        autopct="%1.1f%%", startangle=140, pctdistance=0.75,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(11); at.set_fontweight("bold"); at.set_color("white")

    ax.legend(
        handles=[mpatches.Patch(color=colors[i], label=f"{labels[i]}  ({sizes[i]:,})") for i in range(len(labels))],
        loc="lower center", bbox_to_anchor=(0.5, -0.12),
        ncol=2, frameon=False, fontsize=10,
    )
    ax.set_title("Company-Wide Risk Level Breakdown", fontsize=13, fontweight="bold", pad=15)
    fig.patch.set_facecolor("none"); ax.set_facecolor("none")

    col_pie, _ = st.columns([1, 1])
    with col_pie:
        st.pyplot(fig)
    plt.close(fig)

    # ── Distributions ─────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📈 Distributions")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Predicted Burnout Score Distribution**")
        hist_counts = pd.cut(pd.Series(preds), bins=20).value_counts().sort_index()
        st.bar_chart(pd.DataFrame({"Count": hist_counts.values},
                                   index=[str(i) for i in hist_counts.index]))

    with col2:
        st.markdown("**Risk Level Count by Department**")
        pivot = (
            df_result.groupby(["broad_department", "risk_level"])
            .size().unstack(fill_value=0).reindex(departments)
        )
        st.bar_chart(pivot)

    # ── Role breakdown ─────────────────────────────────────────────────
    if "role" in df_result.columns:
        st.markdown("---")
        st.subheader("👤 Burnout by Role (Top 20)")
        role_mean = (
            df_result.groupby("role")["predicted_burnout"]
            .mean().sort_values(ascending=False).head(20)
        )
        st.bar_chart(role_mean)

    # ── Actual vs Predicted ────────────────────────────────────────────
    if "burnout_score" in df_result.columns:
        st.markdown("---")
        st.subheader("🎯 Actual vs Predicted")
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Scatter: Actual vs Predicted**")
            scatter_df = df_result[["burnout_score", "predicted_burnout"]].sample(
                min(500, len(df_result)), random_state=42
            )
            st.scatter_chart(scatter_df, x="burnout_score", y="predicted_burnout")

        with col4:
            mae  = np.mean(np.abs(df_result["burnout_score"] - preds))
            rmse = np.sqrt(np.mean((df_result["burnout_score"] - preds) ** 2))
            r2   = np.corrcoef(df_result["burnout_score"], preds)[0, 1] ** 2
            st.markdown("**Model Performance**")
            st.metric("MAE",  f"{mae:.4f}")
            st.metric("RMSE", f"{rmse:.4f}")
            st.metric("R²",   f"{r2:.4f}")

        st.markdown("**Mean Actual vs Predicted Burnout by Department**")
        dept_compare = (
            df_result.groupby("broad_department")[["burnout_score", "predicted_burnout"]]
            .mean().reindex(departments)
        )
        st.bar_chart(dept_compare)

    # ── Feature correlations ───────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔗 Feature Correlations with Predicted Burnout")
    non_feature = {"burnout_score", "role", "broad_department", "employee_id", "name",
                   "predicted_burnout", "risk_level"}
    numeric_cols = [c for c in df_result.select_dtypes(include="number").columns
                    if c not in non_feature]
    corr = (
        df_result[numeric_cols + ["predicted_burnout"]].corr()["predicted_burnout"]
        .drop("predicted_burnout", errors="ignore").sort_values()
    )
    st.bar_chart(corr)

    # ── Employee table ─────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Employee Predictions Table")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        risk_filter = st.multiselect(
            "Filter by Risk Level", options=RISK_ORDER,
            default=["🟠 High", "🔴 Critical"],
        )
    with col_f2:
        dept_filter = st.multiselect(
            "Filter by Department", options=departments, default=departments,
        )

    display_cols = ["broad_department", "predicted_burnout", "risk_level"] + [
        c for c in ["role", "burnout_score", "workload_score",
                    "overtime_hours", "satisfaction_score"]
        if c in df_result.columns
    ]
    filtered = df_result.copy()
    if risk_filter:
        filtered = filtered[filtered["risk_level"].isin(risk_filter)]
    if dept_filter:
        filtered = filtered[filtered["broad_department"].isin(dept_filter)]

    st.dataframe(
        filtered[display_cols].sort_values("predicted_burnout", ascending=False),
        use_container_width=True,
    )
    st.caption(f"Showing {len(filtered):,} of {len(df_result):,} employees.")

    # ── Download ───────────────────────────────────────────────────────
    st.markdown("---")
    st.download_button(
        label="⬇️ Download Full Predictions CSV",
        data=df_result.to_csv(index=False).encode("utf-8"),
        file_name="burnout_predictions_all.csv",
        mime="text/csv",
    )
