import streamlit as st
import pandas as pd
import numpy as np
from loader import load_data
from stats import clean_data, basic_stats, dataset_info

st.title("Data Viewer App")

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None

page=st.sidebar.selectbox("Select a page", ["Basic Analysis","Charts and Visualizations"])

# File uploader in sidebar (available on all pages)
data=st.sidebar.file_uploader("Upload your data",type=["csv","xlsx","xls"])
if data is not None:
    st.session_state.df = load_data(data)

if page=="Basic Analysis":
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df.head(10))
    
    
    if st.session_state.df is not None:
        st.write("Dataset Information:")
        dataset_info(st.session_state.df)
        st.session_state.df_cleaned = clean_data(st.session_state.df)
    
    if st.session_state.df_cleaned is not None:
        st.write("Basic Statistics:")
        basic_stats(st.session_state.df_cleaned)

elif page=="Charts and Visualizations":
    if st.session_state.df is not None:
        from plots import create_visualization
        create_visualization(st.session_state.df)
    else:
        st.write("Please upload data first on the Basic Analysis page")