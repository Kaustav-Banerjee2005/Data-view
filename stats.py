import streamlit as st 
import pandas as pd
import numpy as np
def clean_data(df):
    ok=st.button("Clean data")
    if ok:
        df_cleaned = df.dropna()  # Remove rows with missing values
        df_cleaned = df_cleaned.drop_duplicates()  # Remove duplicate rows
        st.dataframe(df_cleaned)  # Display the cleaned data
        return df_cleaned
def basic_stats(df):
    stats= df.describe()  # Get basic statistics
    st.dataframe(stats)  # Display it
    return stats
def dataset_info(df):
    st.write("Basic Information about the dataset:", df.info())  # Get dataset info
    st.write("Dataset Shape:", df.shape)  # Get dataset shape
    st.write("Missing Values in each column:\n", df.isnull().sum())  # Get missing values count
    st.write("Correlation Matrix:\n", df.corr())  # Get correlation matrix