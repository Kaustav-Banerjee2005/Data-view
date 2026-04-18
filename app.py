import streamlit as st
import pandas as pd
import numpy as np
from loader import load_data
from stats import clean_data, basic_stats, dataset_info
df_cleaned=None
st.title("Data Viewer App")


page=st.sidebar.selectbox("Select a page", ["Basic Analysis","Charts and Visualizations"])
if page=="Basic Analysis":
    data=st.file_uploader("Upload your data",type=["csv","xlsx","xls"])
    df=load_data(data)
    if df is not None:           # Only runs if df has data
        st.dataframe(df.head(10))
    else:
        st.write("Please upload a CSV or Excel file")  # Show message if nothing uploaded
    if df is not None:
        st.write("Dataset Information:")
        dataset_info(df)
        df_cleaned=clean_data(df)
    if df_cleaned is not None:
        st.write("Basic Statistics:")
        basic_stats(df_cleaned)