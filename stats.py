import streamlit as st 
import pandas as pd
import numpy as np
def clean_data(df):
    df_cleaned=df.dropna()  # Remove rows with missing values
    df_cleaned=df_cleaned.drop_duplicates()  # Remove duplicate rows
    return df_cleaned
def basic_stats(df):
    stats=df.describe()  # Get basic statistics
    return stats
def dataset_info(df):
    print("Basic Information about the dataset:", df.info())  # Get dataset info
    print("Dataset Shape:", df.shape)  # Get dataset shape
    print("Missing Values in each column:\n", df.isnull().sum())  # Get missing values count
    print("Correlation Matrix:\n", df.corr())  # Get correlation matrix