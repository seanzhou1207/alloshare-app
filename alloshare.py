import cvxpy as cp
import numpy as np
import pandas as pd
import yfinance as yf
import pytz
import streamlit as st

from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta, time
from alpaca.data.historical import StockHistoricalDataClient

# st.title("AlloShare: Portfolio Allocation Calculator")

# # get nearist trading day for price fetch
# @st.cache_data
# def get_adjusted_today():
#     est = pytz.timezone('US/Eastern')
#     now = datetime.now(est)
#     current_time = now.time()
    
#     # Weekend handling
#     if now.weekday() >= 5:
#         return (now - timedelta(days=now.weekday() - 4)).date()
    
#     # Trading hours check (9:30 AM - 4:00 PM EST)
#     if time(9, 30) <= current_time <= time(16, 0):
#         # Use previous business day
#         return (now - timedelta(days=1 if now.weekday() > 0 else 3)).date()
    
#     # Regular weekday outside trading hours
#     return now.date()

# today = get_adjusted_today()

# st.write(f"{today}")

# # Inputs
# T = st.number_input("Target total investment ($)", min_value=0, value=1000)
# # T_min = st.number_input("Min allowable investment ($)", min_value=0, value=900)
# # T_max = st.number_input("Max allowable investment ($)", min_value=T, value=1100)
# lambda_ = st.slider("Trade-off parameter (lambda)", min_value=0.0, max_value=10.0, value=1.0)

# tickers_input = st.text_area("Enter tickers separated by commas", value="SPLG,DIVI,VCIT,IAGG")
# tickers = [t.strip().upper() for t in tickers_input.split(",")]
# n = len(tickers)


from pages import setup_portfolio, view_strategy

# Set page config
st.set_page_config(page_title="AlloShare", layout="wide")

# Sidebar for navigation
page = st.sidebar.selectbox("Go to page", ["Setup Portfolio", "View Portfolio"])

# Initialize session state for portfolio
if "portfolio_df" not in st.session_state:
    st.session_state.portfolio_df = None

# Navigate pages
if page == "Setup Portfolio":
    setup_portfolio.show()
elif page == "View Portfolio":
    view_strategy.view_strategy()