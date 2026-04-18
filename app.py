import streamlit as st
import pandas as pd
import numpy as np
from loader import load_data
from stats import clean_data, basic_stats, dataset_info
st.title("Data Viewer App")
data=st.file_uploader("Upload your data",type=["csv","xlsx","xls"])
df=load_data(data)
if df is not None:           # Only runs if df has data
    st.dataframe(df.head(10))
else:
    st.write("Please upload a CSV or Excel file")  # Show message if nothing uploaded
if df is not None:
    df_cleaned=clean_data(df)