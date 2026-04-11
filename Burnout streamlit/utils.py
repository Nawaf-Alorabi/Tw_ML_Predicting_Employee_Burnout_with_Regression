"""
utils.py  –  shared helpers for all burnout dashboard pages
"""
import pandas as pd
import numpy as np
import joblib
import os
import streamlit as st

MODEL_PATH = "stacking_burnout_model.joblib"


@st.cache_resource(show_spinner="Loading model…")
def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        return None
    return joblib.load(path)


def preprocess(df: pd.DataFrame, use_data_role_mean: bool = False) -> pd.DataFrame:
    df = df.copy()

    if use_data_role_mean and "role" in df.columns and "burnout_score" in df.columns:
        role_mean = df.groupby("role")["burnout_score"].mean()
        df["role_encoded"] = df["role"].map(role_mean)

    if all(c in df.columns for c in ["workload_score", "overtime_hours"]):
        df["pressure_index"] = df["workload_score"] * (1 + df["overtime_hours"] / 40)

    if all(c in df.columns for c in ["satisfaction_score", "career_progression_score", "role_complexity_score"]):
        df["burnout_propensity"] = (
            df["role_complexity_score"]
            - df["satisfaction_score"]
            - df["career_progression_score"]
        )

    if all(c in df.columns for c in ["goal_achievement_rate", "workload_score", "overtime_hours"]):
        df["effort_efficiency"] = df["goal_achievement_rate"] / (
            df["workload_score"] * (1 + df["overtime_hours"] / 40) + 1e-9
        )

    if "pressure_index" in df.columns and "burnout_propensity" in df.columns:
        df["burnout_pressure"] = df["pressure_index"] * df["burnout_propensity"]

    if all(c in df.columns for c in ["team_sentiment", "satisfaction_score"]):
        df["culture_shield"] = df["team_sentiment"] * df["satisfaction_score"]

    return df


def predict(df: pd.DataFrame, model, use_data_role_mean: bool = False) -> np.ndarray:
    df_proc = preprocess(df, use_data_role_mean)
    non_feature = {"burnout_score", "role", "broad_department", "employee_id", "name"}
    if hasattr(model, "feature_names_in_"):
        feature_cols = list(model.feature_names_in_)
        missing = [c for c in feature_cols if c not in df_proc.columns]
        if missing:
            st.error(f"❌ Missing columns required by the model: `{missing}`")
            st.stop()
    else:
        feature_cols = [c for c in df_proc.columns if c not in non_feature and df_proc[c].dtype != object]
    X = df_proc[feature_cols]
    return model.predict(X).clip(0, 1)


def risk_label(score: float) -> str:
    if score <= 0.49:
        return "🟢 Low"
    elif score <= 0.69:
        return "🟡 Moderate"
    elif score < 0.89:
        return "🟠 High"
    else:
        return "🔴 Critical"


RISK_ORDER  = ["🟢 Low", "🟡 Moderate", "🟠 High", "🔴 Critical"]
RISK_COLORS = ["#4CAF50", "#FFC107", "#FF9800", "#F44336"]


def back_button(dest: str = "home", label: str = "← Back"):
    if st.button(label):
        st.session_state.page = dest
        st.rerun()
