import streamlit as st
import pandas as pd
import json

from utils.plots import *
from investxact.algo import *

class Strategy:
    def __init__(self):
        self.df = None  # Store uploaded dataset
    
    def upload_file(self):
        """Handle file upload and store dataset."""
        uploaded_file = st.file_uploader(
            "Select a portfolio file (json, Parquet, CSV)", 
            type=["parquet", "csv", "json"]
        )

        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".parquet"):
                    df = pd.read_parquet(uploaded_file)

                elif uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)

                elif uploaded_file.name.endswith(".json"):
                    payload = json.load(uploaded_file)
                    df = pd.DataFrame(payload["portfolio"]) 
                    
                else:
                    st.error("Unsupported file format. Please upload CSV, Parquet, or JSON.")
                    df = None

                if df is not None:
                    # Compute split column
                    df["Split"] = df["Weights"] * df["Subweights"]
                    
                    # Save in session_state
                    st.session_state.strategy_df = df
                    st.session_state.file_name = uploaded_file.name
                    st.session_state.target = int(payload.get("target", 1000))  # default if missing

            except Exception as e:
                st.error(f"Failed to read file: {e}")

        # elif st.session_state.strategy_df:
        #     st.info("Please upload a file to view your strategy.")


    def show_portfolio(self):
        """Display portfolio table and pie chart."""
        df = st.session_state.strategy_df
        if df is None:
            st.warning("No dataset loaded. Please upload a file first.")
            return

        file_name = st.session_state.file_name or "strategy"
        strategy_name = file_name.rsplit(".", 1)[0]
        st.subheader(f"Strategy: {strategy_name}")

        # Make the pie chart section more prominent.
        left, center, right = st.columns([0.5, 4, 0.5])
        with center:
            fig = nested_pie_chart(df, category_col="Category", ticker_col="Ticker", value_col="Split")
            fig.update_layout(height=680)
            st.plotly_chart(fig, use_container_width=True)

        budget_col, _ = st.columns([1, 4])
        with budget_col:
            st.session_state.target = st.number_input(
                "Investment Budget",
                min_value=1,
                max_value=1_000_000,
                step=100,
                value=st.session_state.target,
                format="%d"
            )
        st.dataframe(df, use_container_width=True)

    def calculate_shares(self):
        target = st.session_state.target
        df = st.session_state.strategy_df
        """Button to calculate shares using stored strategy."""
        if st.button("Calculate Shares"):
            results = run_optimization(target, df)  # pass dataset to calculate
            st.header("Results")
            summary = results.get("summary", {})
            assets = results.get("assets", [])

            col1, col2, col3 = st.columns(3)
            col1.metric("Budget", f"${summary.get('budget', 0):,.2f}")
            col2.metric("Actual Cost", f"${summary.get('actual_cost', 0):,.2f}")
            col3.metric("Solver Status", str(summary.get("solver_status", "unknown")))

            st.subheader("Asset Breakdown")
            if assets:
                assets_df = pd.DataFrame(assets)
                st.dataframe(assets_df, use_container_width=True)
            else:
                st.info("No asset allocations were returned.")
