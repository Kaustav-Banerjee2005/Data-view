import streamlit as st
import pandas as pd
def load_data(file):
    df=None
    if file is not None:
        file_name=file.name
        if file_name.endswith(".csv"):       
            df=pd.read_csv(file)
        elif file_name.endswith((".xlsx",".xls")):
            df=pd.read_excel(file)
    return df