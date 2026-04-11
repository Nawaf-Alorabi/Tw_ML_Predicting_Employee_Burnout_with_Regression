"""
dep_dashboard.py  –  reusable department-level dashboard renderer
Call render(df_result, dept_name, preds) after filtering by department.
"""
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import RISK_ORDER, RISK_COLORS, risk_label


def render(df_result: pd.DataFrame, dept_name: str, preds: np.ndarray):
    """
    df_result : already department-filtered DataFrame with 'predicted_burnout' & 'risk_level'
    dept_name : display name e.g. "HR"
    preds     : np.ndarray of predicted scores (same length as df_result)
    """
    st.subheader(f"📊 {dept_name} Department — Overall Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean Burnout",         f"{preds.mean():.3f}")
    c2.metric("Max Burnout",          f"{preds.max():.3f}")
    c3.metric("Min Burnout",          f"{preds.min():.3f}")
    c4.metric("High / Critical %",    f"{(preds >= 0.60).mean()*100:.1f}%")

    # ── Pie chart ────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🥧 Risk Level Distribution")

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
    ax.set_title(f"{dept_name} Risk Level Breakdown", fontsize=13, fontweight="bold", pad=15)
    fig.patch.set_facecolor("none"); ax.set_facecolor("none")

    col_pie, _ = st.columns([1, 1])
    with col_pie:
        st.pyplot(fig)
    plt.close(fig)

    # ── Score distribution ────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📈 Predicted Burnout Score Distribution")
    hist_counts = pd.cut(pd.Series(preds), bins=15).value_counts().sort_index()
    st.bar_chart(pd.DataFrame({"Count": hist_counts.values},
                               index=[str(i) for i in hist_counts.index]))

    # ── Role breakdown ────────────────────────────────────────────────
    if "role" in df_result.columns:
        st.markdown("---")
        st.subheader("👤 Burnout by Role")
        role_mean = (
            df_result.groupby("role")["predicted_burnout"]
            .mean().sort_values(ascending=False)
        )
        st.bar_chart(role_mean)

    # ── Actual vs Predicted ───────────────────────────────────────────
    if "burnout_score" in df_result.columns:
        st.markdown("---")
        st.subheader("🎯 Actual vs Predicted")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("**Scatter: Actual vs Predicted**")
            scatter_df = df_result[["burnout_score", "predicted_burnout"]].sample(
                min(300, len(df_result)), random_state=42
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

    # ── Feature correlations ──────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔗 Feature Correlations with Predicted Burnout")
    numeric_cols = df_result.select_dtypes(include="number").columns.tolist()
    if "predicted_burnout" in numeric_cols:
        corr = (
            df_result[numeric_cols].corr()["predicted_burnout"]
            .drop("predicted_burnout", errors="ignore")
            .sort_values()
        )
        st.bar_chart(corr)

    # ── Employee table ────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Employee Predictions Table")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            options=RISK_ORDER,
            default=["🟠 High", "🔴 Critical"],
            key=f"risk_{dept_name}",
        )

    display_cols = ["predicted_burnout", "risk_level"] + [
        c for c in ["role", "burnout_score", "workload_score",
                    "overtime_hours", "satisfaction_score"]
        if c in df_result.columns
    ]
    filtered = df_result[df_result["risk_level"].isin(risk_filter)] if risk_filter else df_result
    st.dataframe(
        filtered[display_cols].sort_values("predicted_burnout", ascending=False),
        use_container_width=True,
    )
    st.caption(f"Showing {len(filtered):,} of {len(df_result):,} {dept_name} employees.")

    # ── Download ──────────────────────────────────────────────────────
    st.markdown("---")
    st.download_button(
        label=f"⬇️ Download {dept_name} Predictions CSV",
        data=df_result.to_csv(index=False).encode("utf-8"),
        file_name=f"{dept_name.lower()}_burnout_predictions.csv",
        mime="text/csv",
        key=f"dl_{dept_name}",
    )
