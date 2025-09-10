import streamlit as st
import pandas as pd

from utils.plots import *
from algo import *

def view_strategy():
    st.title("View Portfolio")

    uploaded_file = st.file_uploader(
        "Select a portfolio file (Parquet or CSV)", 
        type=["parquet", "csv"]
    )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".parquet"):
                df = pd.read_parquet(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            # Get pie data
            df["Split"] = df["Weights"] * df["Subweights"]

            st.subheader("Portfolio Data")


            col1, col2 = st.columns([7, 3])  # 70% / 30% split

            with col1:
                st.dataframe(df)

            with col2:
                fig = nested_pie_chart(df, category_col="Category", ticker_col="Ticker", value_col="Split")
                st.pyplot(fig)

            # Button to calculate shares
            if st.button("Calculate Shares"):
                # Compute shares using your existing function
                results_df = calculate()  # budget_total = user input
                
                # Show results in a new page/section
                st.header("Results")
                st.dataframe(results_df)

        except Exception as e:
            st.error(f"Failed to read file: {e}")
    else:
        st.info("Please upload a file to view your portfolio.")

view_strategy()
