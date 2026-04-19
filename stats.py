import streamlit as st
import pandas as pd
import numpy as np


def clean_data(df):
    df_cleaned = df.dropna()
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned


def basic_stats(df):
    stats = df.describe()
    st.dataframe(stats)
    st.write("Correlation Matrix:\n", df.select_dtypes(include=[np.number]).corr())
    return stats


def dataset_info(df):
    st.write("Basic Information about the dataset:", df.info())
    st.write("Dataset Shape:", df.shape)
    st.write("Missing Values in each column:\n", df.isnull().sum())
