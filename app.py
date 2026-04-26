import streamlit as st
import pandas as pd
import numpy as np
from loader import load_data
from stats import clean_data, basic_stats, dataset_info
from eda import get_heatmap_figure,detect_outliers_iqr


st.title("Data Viewer App")

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'uploaded_file_key' not in st.session_state:
    st.session_state.uploaded_file_key = None

page=st.sidebar.selectbox("Select a page", ["Basic Cleaning","Charts and Visualizations","EDA"])

# File uploader in sidebar (available on all pages)
data=st.sidebar.file_uploader("Upload your data",type=["csv","xlsx","xls"])
if data is not None:
    current_file_key = (data.name, data.size)
    if st.session_state.uploaded_file_key != current_file_key:
        st.session_state.df = load_data(data)
        st.session_state.df_cleaned = None
        st.session_state.uploaded_file_key = current_file_key

if page=="Basic Cleaning":
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df.head(10))
    
    
    if st.session_state.df is not None:
        st.write("Dataset Information:")
        dataset_info(st.session_state.df)
        if st.button("Clean data", key="clean_data_btn"):
            st.session_state.df_cleaned = clean_data(st.session_state.df)
    
    if st.session_state.df_cleaned is not None:
        st.write("Cleaned Data:")
        st.dataframe(st.session_state.df_cleaned)
        st.write("Basic Statistics:")
        basic_stats(st.session_state.df_cleaned)
        st.dataframe(basic_stats(st.session_state.df_cleaned))

elif page=="Charts and Visualizations":
    if st.session_state.df is not None:
        from plots import create_visualization
        create_visualization(st.session_state.df)
    else:
        st.write("Please upload data first on the Basic Analysis page")
elif page=="EDA":
    st.title("Exploratory Data Analysis (EDA)")
    st.write("In this page you can plot heatmap and find out outliers in your Dataset using the IQR method")
    if st.session_state.df is not None:
        if st.button("Show Heatmap"):
            fig, error = get_heatmap_figure(st.session_state.df)
            if error:
                st.error(error)
            else:
                st.plotly_chart(fig, use_container_width=True)
        if st.button("Detect Outliers (IQR)"):
            outliers = detect_outliers_iqr(st.session_state.df)
            # Create a structured summary table
            outlier_summary = []
            for col, info in outliers.items():
                outlier_summary.append({
                "Column": col,
                "Outlier Count": info['count'],
                "Lower Bound": round(info['lower_bound'], 2),
                "Upper Bound": round(info['upper_bound'], 2)
                })
    
            # Display summary table
            st.write("**Outlier Summary Table:**")
            summary_df = pd.DataFrame(outlier_summary)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
            # Show detailed outlier values in expandable sections
            st.write("**Detailed Outlier Values:**")
            for col, info in outliers.items():
                with st.expander(f"📊 {col} ({info['count']} outliers)"):
                    if info['count'] > 0:
                        outlier_data = pd.DataFrame({
                            "Outlier Values": info['outlier_values']
                        })
                        st.dataframe(outlier_data, use_container_width=True, hide_index=True)
                    else:
                        st.info("No outliers detected in this column")
    else:
        st.write("Please upload data first on the Basic Analysis page")