"""
dep_dashboard.py — reusable department dashboard renderer (burnout theme).
"""
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from utils import RISK_ORDER, RISK_COLORS, risk_label

# Matplotlib dark style matching the theme
plt.rcParams.update({
    "figure.facecolor":  "#1a1a1a",
    "axes.facecolor":    "#1a1a1a",
    "axes.edgecolor":    "#2e2e2e",
    "axes.labelcolor":   "#9ca3af",
    "xtick.color":       "#9ca3af",
    "ytick.color":       "#9ca3af",
    "text.color":        "#f5f5f5",
    "grid.color":        "#2e2e2e",
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "font.family":       "sans-serif",
})


def _risk_badge_html(label: str, count: int, pct: float, color: str) -> str:
    return f"""
    <div style="flex:1; min-width:110px; background:#1a1a1a; border:1px solid #2e2e2e;
                border-left:3px solid {color}; border-radius:10px; padding:0.9rem 1rem;">
        <div style="font-size:1.4rem; font-weight:700; color:{color};">{count:,}</div>
        <div style="font-size:0.78rem; color:#9ca3af; margin-top:2px;">{label}</div>
        <div style="font-size:0.72rem; color:#6b7280; margin-top:1px;">{pct:.1f}% of team</div>
    </div>"""


def render(df_result: pd.DataFrame, dept_name: str, preds: np.ndarray):
    total = len(df_result)

    # ── Risk badges ──────────────────────────────────────────────────
    risk_counts = df_result["risk_level"].value_counts()
    badge_colors = {"🟢 Low": "#22c55e", "🟡 Moderate": "#eab308",
                    "🟠 High": "#f97316", "🔴 Critical": "#ef4444"}

    badges_html = '<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1.5rem;">'
    for rl in RISK_ORDER:
        cnt = int(risk_counts.get(rl, 0))
        pct = cnt / total * 100 if total > 0 else 0
        badges_html += _risk_badge_html(rl, cnt, pct, badge_colors[rl])
    badges_html += "</div>"
    st.markdown(badges_html, unsafe_allow_html=True)

    # ── KPI row ──────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean Burnout",       f"{preds.mean():.3f}")
    c2.metric("Peak Burnout",       f"{preds.max():.3f}")
    c3.metric("Lowest Score",       f"{preds.min():.3f}")
    c4.metric("High / Critical %",  f"{(preds >= 0.60).mean()*100:.1f}%")

    # ── Donut chart ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="burn-section-label">Risk Distribution</div>', unsafe_allow_html=True)

    labels  = [r for r in RISK_ORDER if r in risk_counts.index]
    sizes   = [risk_counts[r] for r in labels]
    colors  = [badge_colors[r] for r in labels]

    fig, ax = plt.subplots(figsize=(5, 4.5))
    _, _, autotexts = ax.pie(
        sizes, labels=None, colors=colors,
        autopct="%1.1f%%", startangle=140, pctdistance=0.72,
        wedgeprops=dict(width=0.52, edgecolor="#0f0f0f", linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(10); at.set_fontweight("bold"); at.set_color("#fff")

    ax.legend(
        handles=[mpatches.Patch(color=colors[i], label=f"{labels[i]}  —  {sizes[i]:,} employees")
                 for i in range(len(labels))],
        loc="lower center", bbox_to_anchor=(0.5, -0.08),
        ncol=2, frameon=False, fontsize=9,
        labelcolor="#d1d5db",
    )
    ax.set_title(f"{dept_name} Team Risk Breakdown", fontsize=12, fontweight="bold",
                 pad=14, color="#f5f5f5")
    fig.patch.set_facecolor("#1a1a1a"); ax.set_facecolor("#1a1a1a")

    col_pie, _ = st.columns([1, 1])
    with col_pie:
        st.pyplot(fig)
    plt.close(fig)

    # ── Score histogram ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="burn-section-label">Score Distribution</div>', unsafe_allow_html=True)
    hist_counts = pd.cut(pd.Series(preds), bins=15).value_counts().sort_index()
    st.bar_chart(
        pd.DataFrame({"Employees": hist_counts.values},
                     index=[str(i) for i in hist_counts.index]),
        color="#f97316",
    )

    # ── Role breakdown ───────────────────────────────────────────────
    if "role" in df_result.columns:
        st.markdown("---")
        st.markdown('<div class="burn-section-label">Burnout by Role</div>', unsafe_allow_html=True)
        role_mean = (
            df_result.groupby("role")["predicted_burnout"].mean()
            .sort_values(ascending=False)
        )
        st.bar_chart(role_mean, color="#ef4444")

    # ── Actual vs Predicted ──────────────────────────────────────────
    if "burnout_score" in df_result.columns:
        st.markdown("---")
        st.markdown('<div class="burn-section-label">Model Accuracy</div>', unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<p style='color:#9ca3af; font-size:0.85rem; margin-bottom:6px;'>Actual vs Predicted Scatter</p>", unsafe_allow_html=True)
            scatter_df = df_result[["burnout_score", "predicted_burnout"]].sample(
                min(300, len(df_result)), random_state=42
            )
            st.scatter_chart(scatter_df, x="burnout_score", y="predicted_burnout", color="#f97316")

        with col4:
            mae  = np.mean(np.abs(df_result["burnout_score"] - preds))
            rmse = np.sqrt(np.mean((df_result["burnout_score"] - preds) ** 2))
            r2   = np.corrcoef(df_result["burnout_score"], preds)[0, 1] ** 2

            st.markdown(f"""
            <div style="background:#1a1a1a; border:1px solid #2e2e2e; border-radius:12px; padding:1.5rem; margin-top:0.5rem;">
                <div style="color:#9ca3af; font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:1rem;">Model Performance</div>
                <div style="margin-bottom:0.8rem;">
                    <div style="color:#6b7280; font-size:0.78rem;">Mean Absolute Error</div>
                    <div style="color:#f97316; font-size:1.4rem; font-weight:700;">{mae:.4f}</div>
                </div>
                <div style="margin-bottom:0.8rem; border-top:1px solid #2e2e2e; padding-top:0.8rem;">
                    <div style="color:#6b7280; font-size:0.78rem;">Root Mean Sq. Error</div>
                    <div style="color:#f97316; font-size:1.4rem; font-weight:700;">{rmse:.4f}</div>
                </div>
                <div style="border-top:1px solid #2e2e2e; padding-top:0.8rem;">
                    <div style="color:#6b7280; font-size:0.78rem;">R² Score</div>
                    <div style="color:#22c55e; font-size:1.4rem; font-weight:700;">{r2:.4f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Feature correlations ─────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="burn-section-label">Feature Correlations with Burnout</div>', unsafe_allow_html=True)
    numeric_cols = df_result.select_dtypes(include="number").columns.tolist()
    if "predicted_burnout" in numeric_cols:
        corr = (
            df_result[numeric_cols].corr()["predicted_burnout"]
            .drop("predicted_burnout", errors="ignore").sort_values()
        )
        st.bar_chart(corr, color="#f59e0b")

    # ── Employee table ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="burn-section-label">Employee Risk Table</div>', unsafe_allow_html=True)

    risk_filter = st.multiselect(
        "Filter by Risk Level",
        options=RISK_ORDER,
        default=["🟠 High", "🔴 Critical"],
        key=f"risk_filter_{dept_name}",
    )

    display_cols = ["predicted_burnout", "risk_level"] + [
        c for c in ["role", "burnout_score", "workload_score", "overtime_hours", "satisfaction_score"]
        if c in df_result.columns
    ]
    filtered = df_result[df_result["risk_level"].isin(risk_filter)] if risk_filter else df_result
    st.dataframe(
        filtered[display_cols].sort_values("predicted_burnout", ascending=False),
        use_container_width=True,
    )
    st.caption(f"Showing {len(filtered):,} of {total:,} employees in {dept_name}.")

    # ── Download ─────────────────────────────────────────────────────
    st.markdown("---")
    st.download_button(
        label=f"⬇️ Export {dept_name} Predictions",
        data=df_result.to_csv(index=False).encode("utf-8"),
        file_name=f"{dept_name.lower()}_burnout_predictions.csv",
        mime="text/csv",
        key=f"dl_{dept_name}",
    )
