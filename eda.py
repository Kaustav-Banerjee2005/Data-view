import streamlit as st
import pandas as pd
import numpy as np
from loader import load_data
from stats import clean_data, basic_stats, dataset_info
import plotly.express as px


@st.cache_data
def get_heatmap_figure(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        return None, "Heatmap requires at least two numeric columns."
    corr_matrix = df[numeric_cols].corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title="Correlation Heatmap")
    return fig, None


def detect_outliers_iqr(df):
    results = {}
    num_cols = df.select_dtypes(include="number").columns

    for col in num_cols:
        Q1 = df[col].quantile(0.25)   # 25th percentile
        Q3 = df[col].quantile(0.75)   # 75th percentile
        IQR = Q3 - Q1                  # middle 50% range

        lower = Q1 - 1.5 * IQR         # anything below = outlier
        upper = Q3 + 1.5 * IQR         # anything above = outlier

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        results[col] = {
            "count": len(outliers),
            "lower_bound": lower,
            "upper_bound": upper,
            "outlier_values": outliers[col].tolist()
        }
    return results
