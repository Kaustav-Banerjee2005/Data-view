import streamlit as st
import pandas as pd
import numpy as np


def clean_data(df):
    df_cleaned = df.dropna()
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned


def basic_stats(df):
    num_df = df.select_dtypes(include="number")
    stats = pd.DataFrame({
        "mean":     num_df.mean(),
        "median":   num_df.median(),
        "std":      num_df.std(),
        "skewness": num_df.skew(),     # skewness is a measure of asymmetry in the distribution
        "kurtosis": num_df.kurt(),     # kurtosis measures the "tailedness" of the distribution (higher kurtosis means more outliers)
    })

    # Interpret skewness for the user
    def skew_label(s):
        if s > 1:   return "Highly right-skewed"
        elif s > 0.5: return "Moderately right-skewed"
        elif s < -1: return "Highly left-skewed"
        else:        return "Approximately normal"

    stats["skew_label"] = stats["skewness"].apply(skew_label)
    return stats


def dataset_info(df):
    st.write("Basic Information about the dataset:", df.info())
    st.write("Dataset Shape:", df.shape)
    st.write("Missing Values in each column:\n", df.isnull().sum())
