import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from stats import clean_data, dataset_info

def deep_dive_analysis(df):
    column = st.selectbox("Select a column for deep dive analysis", df.columns)
    
    if pd.api.types.is_numeric_dtype(df[column]):
        numeric_deep_dive(df, column)
    else:
        categorical_deep_dive(df, column)

def numeric_deep_dive(df, column):
    st.title(f"📊 Deep Dive Analysis: {column} (Numeric)")
    
    # ===== DISTRIBUTION & SHAPE =====
    st.header("📈 Distribution & Shape")
    
    col1, col2 = st.columns(2)
    with col1:
        # Histogram with KDE
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df[column].dropna(),
            nbinsx=30,
            name='Histogram',
            opacity=0.7,
            marker_color='rgba(0, 100, 200, 0.7)'
        ))
        fig_hist.update_layout(
            title=f"Distribution of {column}",
            xaxis_title=column,
            yaxis_title="Frequency",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Boxplot
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=df[column].dropna(),
            name=column,
            marker_color='rgba(0, 100, 200, 0.7)'
        ))
        fig_box.update_layout(
            title=f"Boxplot of {column}",
            yaxis_title=column,
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Skewness & Kurtosis Interpretation
    skewness = df[column].skew()
    kurtosis = df[column].kurtosis()
    
    st.subheader("Shape Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Skewness", f"{skewness:.2f}")
        if abs(skewness) < 0.5:
            st.info("✓ Approximately symmetric distribution")
        elif skewness > 1:
            st.warning("⚠️ Strongly right-skewed — most values are low with few extreme high values")
        elif skewness < -1:
            st.warning("⚠️ Strongly left-skewed — most values are high with few extreme low values")
        elif skewness > 0:
            st.info("ℹ️ Moderately right-skewed")
        else:
            st.info("ℹ️ Moderately left-skewed")
    
    with col2:
        st.metric("Kurtosis", f"{kurtosis:.2f}")
        if abs(kurtosis) < 0.5:
            st.info("✓ Normal-like tail behavior (mesokurtic)")
        elif kurtosis > 1:
            st.warning("⚠️ Heavy tails with potential outliers (leptokurtic)")
        else:
            st.info("ℹ️ Light tails (platykurtic)")
    
    # ===== CENTRAL TENDENCY & SPREAD =====
    st.header("📍 Central Tendency & Spread")
    
    mean_val = df[column].mean()
    median_val = df[column].median()
    mode_val = df[column].mode()
    std_val = df[column].std()
    var_val = df[column].var()
    min_val = df[column].min()
    max_val = df[column].max()
    range_val = max_val - min_val
    
    stats_data = {
        "Metric": ["Mean", "Median", "Mode", "Standard Deviation", "Variance", "Min", "Max", "Range"],
        "Value": [
            f"{mean_val:.2f}",
            f"{median_val:.2f}",
            f"{mode_val.values[0]:.2f}" if len(mode_val) > 0 else "N/A",
            f"{std_val:.2f}",
            f"{var_val:.2f}",
            f"{min_val:.2f}",
            f"{max_val:.2f}",
            f"{range_val:.2f}"
        ]
    }
    st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)
    
    # Mean vs Median Interpretation
    diff = abs(mean_val - median_val)
    st.subheader("Mean vs Median Analysis")
    col1, col2 = st.columns(2)
    col1.metric("Mean", f"{mean_val:.2f}")
    col2.metric("Median", f"{median_val:.2f}")
    
    if diff > (0.1 * median_val):
        st.warning(f"⚠️ Significant difference ({diff:.2f}): Data is likely skewed or contains outliers pulling the mean away from the median")
    else:
        st.success(f"✓ Mean and median are close — data appears relatively symmetric")
    
    # ===== OUTLIERS =====
    st.header("🎯 Outlier Detection (IQR Method)")
    
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Lower Bound", f"{lower_bound:.2f}")
    col2.metric("Upper Bound", f"{upper_bound:.2f}")
    col3.metric("Outlier Count", f"{len(outliers)}")
    
    if len(outliers) > 0:
        st.warning(f"⚠️ Found {len(outliers)} outlier(s) ({(len(outliers)/len(df)*100):.1f}% of data)")
        with st.expander("📋 View Outlier Values"):
            outlier_df = pd.DataFrame({
                "Outlier Values": outliers.values,
                "Index": outliers.index
            })
            st.dataframe(outlier_df, use_container_width=True, hide_index=True)
    else:
        st.success("✓ No outliers detected using IQR method")
    
    # ===== PERCENTILES =====
    st.header("📊 Percentiles")
    
    percentiles = [10, 25, 50, 75, 90]
    percentile_data = {
        "Percentile": percentiles,
        "Value": [f"{df[column].quantile(p/100):.2f}" for p in percentiles],
        "Interpretation": [
            "10% of data below this",
            "25% of data below this (Q1)",
            "50% of data below this (Median)",
            "75% of data below this (Q3)",
            "90% of data below this"
        ]
    }
    st.dataframe(pd.DataFrame(percentile_data), use_container_width=True, hide_index=True)

def categorical_deep_dive(df, column):
    st.title(f"🏷️ Deep Dive Analysis: {column} (Categorical)")
    
    # ===== DATA QUALITY SIGNALS =====
    st.header("⚠️ Data Quality Signals")
    
    missing_count = df[column].isna().sum()
    missing_pct = (missing_count / len(df)) * 100
    unique_count = df[column].nunique()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Unique Values", unique_count)
    col2.metric("Missing Values", f"{missing_count} ({missing_pct:.1f}%)")
    col3.metric("Total Rows", len(df))
    
    # ID column detection
    if unique_count == len(df):
        st.error("🚩 This column appears to be an ID column (unique value per row) — likely not useful for analysis")
    
    # Rare categories
    value_counts = df[column].value_counts()
    rare_threshold = 0.01 * len(df)
    rare_categories = value_counts[value_counts < rare_threshold]
    
    if len(rare_categories) > 0:
        st.warning(f"⚠️ Found {len(rare_categories)} rare categories (appearing <1% of the time)")
        with st.expander("📋 View Rare Categories"):
            rare_data = pd.DataFrame({
                "Category": rare_categories.index,
                "Count": rare_categories.values,
                "Percentage": (rare_categories.values / len(df) * 100).round(2)
            })
            st.dataframe(rare_data, use_container_width=True, hide_index=True)
    
    # ===== FREQUENCY & DISTRIBUTION =====
    st.header("📊 Frequency & Distribution")
    
    # Create frequency table
    freq_df = df[column].value_counts().reset_index()
    freq_df.columns = [column, 'Count']
    freq_df['Percentage'] = (freq_df['Count'] / len(df) * 100).round(2)
    freq_df['Percentage_str'] = freq_df['Percentage'].astype(str) + '%'
    
    st.subheader("Frequency Table")
    st.dataframe(freq_df[[column, 'Count', 'Percentage_str']], use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig_bar = px.bar(
            freq_df.head(15),
            x=column,
            y='Count',
            title=f"Value Counts of {column} (Top 15)",
            labels={'Count': 'Frequency'},
            color='Count',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Pie chart (optional - show only if <10 categories)
        if unique_count <= 10:
            fig_pie = px.pie(
                freq_df,
                names=column,
                values='Count',
                title=f"Distribution of {column}"
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info(f"ℹ️ Pie chart hidden (too many categories: {unique_count}). View the bar chart above instead.")
    
    # ===== VARIETY & DOMINANCE =====
    st.header("🔍 Variety & Dominance")
    
    most_freq_cat = value_counts.index[0]
    most_freq_count = value_counts.iloc[0]
    most_freq_pct = (most_freq_count / len(df)) * 100
    
    least_freq_cat = value_counts.index[-1]
    least_freq_count = value_counts.iloc[-1]
    least_freq_pct = (least_freq_count / len(df)) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Most Frequent")
        st.metric(most_freq_cat, f"{most_freq_count} ({most_freq_pct:.1f}%)")
    
    with col2:
        st.subheader("Least Frequent")
        st.metric(least_freq_cat, f"{least_freq_count} ({least_freq_pct:.1f}%)")
    
    # Dominance flag
    if most_freq_pct > 80:
        st.warning(f"🚩 Category '{most_freq_cat}' dominates with {most_freq_pct:.1f}% of data — this column may have low predictive value")
    elif most_freq_pct > 50:
        st.info(f"ℹ️ Category '{most_freq_cat}' represents {most_freq_pct:.1f}% of data — somewhat imbalanced")
    else:
        st.success(f"✓ Data is well-distributed across categories")