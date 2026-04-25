import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


@st.cache_data
def process_data(df, column, operation="none"):
    """Cache expensive data operations."""
    if operation == "groupby" and len(df.columns) > 0:
        return df
    return df


def create_visualization(df):
    """Create interactive visualizations based on user selection."""
    if df is None or df.empty:
        st.write("Please upload data first")
        return

    st.write("### Create Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Pie Chart", "Histogram","Box Plot","Count Plot"],
        key="chart_type",
    )

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    if "chart_generated" not in st.session_state:
        st.session_state.chart_generated = False

    if chart_type == "Bar Chart":
        if not numeric_cols:
            st.error("Bar chart requires at least one numeric column.")
            return

        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox(
                "Select X-axis (Category)",
                categorical_cols + numeric_cols,
                key="bar_x",
            )
        with col2:
            y_axis = st.selectbox("Select Y-axis (Value)", numeric_cols, key="bar_y")

        if st.button("Generate Bar Chart", key="bar_btn"):
            
            grouped_df=df.groupby(x_axis)[y_axis].sum().reset_index()
            fig = px.bar(grouped_df, x=x_axis, y=y_axis, color=x_axis, title=f"{y_axis} by {x_axis}")
            fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis)
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":
        if not categorical_cols:
            st.error("Pie chart requires at least one categorical column.")
            return

        if not numeric_cols:
            st.error("Pie chart requires at least one numeric column.")
            return

        cat_col = st.selectbox("Select Category Column", categorical_cols, key="pie_cat")
        num_col = st.selectbox("Select Value Column", numeric_cols, key="pie_val")

        if st.button("Generate Pie Chart", key="pie_btn"):

            pie_data = df.groupby(cat_col)[num_col].sum().reset_index()

            # Filter positive values
            pie_data = pie_data[pie_data[num_col] > 0]

            if pie_data.empty:
                st.error("No positive values available for pie chart")

            else:
                if len(pie_data) > 6:
                    st.warning("Too many categories. Pie chart may not be readable (recommended <= 6)")

                fig = px.pie(
                    pie_data,
                    names=cat_col,
                    values=num_col,
                    title=f"{num_col} distribution by {cat_col}"
                )

                st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Histogram":
        if not numeric_cols:
            st.error("Histogram requires at least one numeric column.")
            return

        column = st.selectbox("Select Column", numeric_cols, key="hist_col")
        bins = st.slider("Number of Bins", min_value=5, max_value=50, value=20, key="hist_bins")

        if st.button("Generate Histogram", key="hist_btn"):
            fig = px.histogram(df, x=column, nbins=bins,marginal="box", title=f"Distribution of {column}")
            fig.update_layout(xaxis_title=column, yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "Box Plot":
        if not numeric_cols:
            st.error("Box plot requires at least one numeric column.")
            return

        column = st.selectbox("Select Column", numeric_cols, key="box_col")

        if st.button("Generate Box Plot", key="box_btn"):
            fig = px.box(df, y=column, title=f"Box Plot of {column}")
            fig.update_layout(yaxis_title=column)
            st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "Count Plot":
        if not categorical_cols:
            st.error("Count plot requires at least one categorical column.")
            return

        column = st.selectbox("Select Column", categorical_cols, key="count_col")

        if st.button("Generate Count Plot", key="count_btn"):
            fig = px.histogram(df, x=column, title=f"Count Plot of {column}")
            fig.update_layout(xaxis_title=column, yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)

 
