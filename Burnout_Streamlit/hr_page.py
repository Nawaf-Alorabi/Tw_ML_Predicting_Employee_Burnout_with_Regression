"""hr_page.py — Company-wide HR dashboard."""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import theme
from utils import load_model, predict, risk_label, back_button, RISK_ORDER, RISK_COLORS

plt.rcParams.update({
    "figure.facecolor": "#1a1a1a", "axes.facecolor": "#1a1a1a",
    "axes.edgecolor": "#2e2e2e",   "axes.labelcolor": "#9ca3af",
    "xtick.color": "#9ca3af",      "ytick.color": "#9ca3af",
    "text.color": "#f5f5f5",       "grid.color": "#2e2e2e",
    "font.family": "sans-serif",
})

BADGE_COLORS = {"🟢 Low": "#22c55e", "🟡 Moderate": "#eab308",
                "🟠 High": "#f97316", "🔴 Critical": "#ef4444"}


def show():
    theme.inject()
    back_button("home", "← Back to Portal")

    theme.page_header("🏢", "HR Dashboard", "Company-wide burnout prediction and risk analytics")

    model = load_model()
    if model is None:
        st.error("❌ `stacking_burnout_model.joblib` not found in the app folder.")
        return

    with st.sidebar:
        st.markdown("### 📂 Upload Dataset")
        data_file = st.file_uploader("Full Employee Dataset (.csv)", type=["csv"])
        st.markdown("---")
        use_role_mean = st.checkbox(
            "Recompute role_encoded from data",
            value=False,
            help="Derives role_encoded as mean burnout_score per role from uploaded data.",
        )

    if not data_file:
        st.markdown("""
        <div style="background:#1a1a1a; border:1px dashed #3a3a3a; border-radius:12px;
                    padding:2rem; text-align:center; color:#9ca3af;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📂</div>
            <div style="font-weight:600; color:#f5f5f5; margin-bottom:0.3rem;">No dataset loaded</div>
            <div style="font-size:0.87rem;">Upload the full employee CSV in the sidebar to begin.</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("ℹ️ Required CSV columns"):
            st.markdown("""
| Column | Description |
|---|---|
| `broad_department` | Finance · Tech · HR · Marketing |
| `role` | Job title |
| `role_encoded` | Numeric target-encoded role value |
| `workload_score` | Normalized workload 0–1 |
| `overtime_hours` | Overtime hours / week |
| `role_complexity_score` | Complexity 0–1 |
| `satisfaction_score` | Satisfaction 0–1 |
| `team_sentiment` | Team sentiment 0–1 |
| `career_progression_score` | Growth score 0–1 |
| `goal_achievement_rate` | Goal % 0–1 |
| `meeting_participation` | Participation 0–1 |
| `burnout_score` | *(optional)* Ground truth |
            """)
        return

    df_raw = pd.read_csv(data_file)

    if "broad_department" not in df_raw.columns:
        st.error("❌ Column `broad_department` not found in the uploaded file.")
        return

    with st.spinner("🔥 Generating burnout predictions…"):
        preds = predict(df_raw, model, use_role_mean)

    df_result = df_raw.copy()
    df_result["predicted_burnout"] = preds
    df_result["risk_level"]        = df_result["predicted_burnout"].apply(risk_label)
    departments = sorted(df_result["broad_department"].dropna().unique().tolist())

    st.markdown(f"""
    <div style="background:#1a1a1a; border:1px solid #2e2e2e; border-radius:10px;
                padding:0.8rem 1.2rem; margin-bottom:1.5rem; display:flex; align-items:center; gap:10px;">
        <span style="color:#22c55e; font-size:1.1rem;">✓</span>
        <span style="color:#d1d5db; font-size:0.9rem;">
            Loaded <strong style="color:#f5f5f5;">{len(df_raw):,} employees</strong>
            across <strong style="color:#f5f5f5;">{len(departments)}</strong> departments.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Risk badge row ───────────────────────────────────────────────
    risk_counts = df_result["risk_level"].value_counts()
    total = len(df_result)

    badges = '<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1.5rem;">'
    for rl in RISK_ORDER:
        cnt = int(risk_counts.get(rl, 0))
        pct = cnt / total * 100 if total > 0 else 0
        col = BADGE_COLORS[rl]
        badges += f"""
        <div style="flex:1; min-width:120px; background:#1a1a1a; border:1px solid #2e2e2e;
                    border-left:3px solid {col}; border-radius:10px; padding:0.9rem 1rem;">
            <div style="font-size:1.5rem; font-weight:700; color:{col};">{cnt:,}</div>
            <div style="font-size:0.78rem; color:#9ca3af; margin-top:2px;">{rl}</div>
            <div style="font-size:0.7rem; color:#6b7280; margin-top:1px;">{pct:.1f}% of workforce</div>
        </div>"""
    badges += "</div>"
    st.markdown(badges, unsafe_allow_html=True)

    # ── KPIs ─────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean Burnout Score",    f"{preds.mean():.3f}")
    c2.metric("Peak Burnout Score",    f"{preds.max():.3f}")
    c3.metric("Lowest Score",          f"{preds.min():.3f}")
    c4.metric("High / Critical %",     f"{(preds >= 0.60).mean()*100:.1f}%")

    # ── Donut chart ──────────────────────────────────────────────────
    st.markdown("---")
    theme.section_label("Company Risk Distribution")

    labels  = [r for r in RISK_ORDER if r in risk_counts.index]
    sizes   = [risk_counts[r] for r in labels]
    colors  = [BADGE_COLORS[r] for r in labels]

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _, _, autotexts = ax.pie(
        sizes, labels=None, colors=colors,
        autopct="%1.1f%%", startangle=140, pctdistance=0.72,
        wedgeprops=dict(width=0.52, edgecolor="#0f0f0f", linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(10); at.set_fontweight("bold"); at.set_color("#fff")
    ax.legend(
        handles=[mpatches.Patch(color=colors[i], label=f"{labels[i]}  —  {sizes[i]:,}")
                 for i in range(len(labels))],
        loc="lower center", bbox_to_anchor=(0.5, -0.08),
        ncol=2, frameon=False, fontsize=9, labelcolor="#d1d5db",
    )
    ax.set_title("Workforce Risk Level Breakdown", fontsize=12, fontweight="bold",
                 pad=14, color="#f5f5f5")
    fig.patch.set_facecolor("#1a1a1a"); ax.set_facecolor("#1a1a1a")
    col_pie, _ = st.columns([1, 1])
    with col_pie:
        st.pyplot(fig)
    plt.close(fig)

    # # ── Dept distribution ────────────────────────────────────────────
    # st.markdown("---")
    # theme.section_label("Risk Breakdown by Department")

    # col1, col2 = st.columns(2)
    # with col1:
    #     theme.section_label("Score Distribution")
    #     hist_counts = pd.cut(pd.Series(preds), bins=20).value_counts().sort_index()
    #     st.bar_chart(
    #         pd.DataFrame({"Employees": hist_counts.values},
    #                       index=[str(i) for i in hist_counts.index]),
    #         color="#f97316",
    #     )
    # with col2:
    #     theme.section_label("Risk Level Count by Department")
    #     pivot = (
    #         df_result.groupby(["broad_department", "risk_level"])
    #         .size().unstack(fill_value=0).reindex(departments)
    #     )
    #     st.bar_chart(pivot)

    # ── Role breakdown ───────────────────────────────────────────────
    if "role" in df_result.columns:
        st.markdown("---")
        theme.section_label("Burnout by Role (Top 20)")
        role_mean = (
            df_result.groupby("role")["predicted_burnout"]
            .mean().sort_values(ascending=False).head(20)
        )
        st.bar_chart(role_mean, color="#ef4444")

    # ── Actual vs Predicted ──────────────────────────────────────────
    if "burnout_score" in df_result.columns:
        st.markdown("---")
        theme.section_label("Model Accuracy")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<p style='color:#9ca3af; font-size:0.85rem; margin-bottom:4px;'>Actual vs Predicted</p>",
                        unsafe_allow_html=True)
            scatter_df = df_result[["burnout_score", "predicted_burnout"]].sample(
                min(500, len(df_result)), random_state=42
            )
            st.scatter_chart(scatter_df, x="burnout_score", y="predicted_burnout", color="#f97316")

        with col4:
            mae  = np.mean(np.abs(df_result["burnout_score"] - preds))
            rmse = np.sqrt(np.mean((df_result["burnout_score"] - preds) ** 2))
            r2   = np.corrcoef(df_result["burnout_score"], preds)[0, 1] ** 2
            st.markdown(f"""
            <div style="background:#1a1a1a; border:1px solid #2e2e2e; border-radius:12px;
                        padding:1.5rem; margin-top:0.4rem;">
                <div style="color:#9ca3af; font-size:0.7rem; letter-spacing:1px;
                            text-transform:uppercase; margin-bottom:1rem;">Performance Metrics</div>
                <div style="margin-bottom:0.8rem;">
                    <div style="color:#6b7280; font-size:0.78rem;">Mean Absolute Error</div>
                    <div style="color:#f97316; font-size:1.4rem; font-weight:700;">{mae:.4f}</div>
                </div>
                <div style="border-top:1px solid #2e2e2e; padding-top:0.8rem; margin-bottom:0.8rem;">
                    <div style="color:#6b7280; font-size:0.78rem;">RMSE</div>
                    <div style="color:#f97316; font-size:1.4rem; font-weight:700;">{rmse:.4f}</div>
                </div>
                <div style="border-top:1px solid #2e2e2e; padding-top:0.8rem;">
                    <div style="color:#6b7280; font-size:0.78rem;">R² Score</div>
                    <div style="color:#22c55e; font-size:1.4rem; font-weight:700;">{r2:.4f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        theme.section_label("Mean Actual vs Predicted by Department")
        dept_compare = (
            df_result.groupby("broad_department")[["burnout_score", "predicted_burnout"]]
            .mean().reindex(departments)
        )
        st.bar_chart(dept_compare)

    # ── Correlations ─────────────────────────────────────────────────
    st.markdown("---")
    theme.section_label("Feature Correlations with Predicted Burnout")
    non_feature = {"burnout_score", "role", "broad_department", "employee_id", "name",
                   "predicted_burnout", "risk_level"}
    numeric_cols = [c for c in df_result.select_dtypes(include="number").columns if c not in non_feature]
    corr = (
        df_result[numeric_cols + ["predicted_burnout"]].corr()["predicted_burnout"]
        .drop("predicted_burnout", errors="ignore").sort_values()
    )
    st.bar_chart(corr, color="#f59e0b")

    # ── Employee table ───────────────────────────────────────────────
    st.markdown("---")
    theme.section_label("Employee Risk Table")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        risk_filter = st.multiselect("Risk Level", options=RISK_ORDER,
                                     default=["🟠 High", "🔴 Critical"])
    with col_f2:
        dept_filter = st.multiselect("Department", options=departments, default=departments)

    display_cols = ["broad_department", "predicted_burnout", "risk_level"] + [
        c for c in ["role", "burnout_score", "workload_score", "overtime_hours", "satisfaction_score"]
        if c in df_result.columns
    ]
    filtered = df_result.copy()
    if risk_filter: filtered = filtered[filtered["risk_level"].isin(risk_filter)]
    if dept_filter: filtered = filtered[filtered["broad_department"].isin(dept_filter)]

    st.dataframe(filtered[display_cols].sort_values("predicted_burnout", ascending=False),
                 use_container_width=True)
    st.caption(f"Showing {len(filtered):,} of {total:,} employees.")

    # ── Download ─────────────────────────────────────────────────────
    st.markdown("---")
    st.download_button(
        label="⬇️ Export Full Predictions CSV",
        data=df_result.to_csv(index=False).encode("utf-8"),
        file_name="burnout_predictions_all.csv",
        mime="text/csv",
    )
