import cvxpy as cp
import numpy as np
import pandas as pd
import yfinance as yf
import pytz
import streamlit as st
from investxact.setup_portfolio import setup
from investxact.view_strategy import Strategy


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

PAGE_ICON = "assets/AlloShare.png"

# ------ Page Configuration ------ #
st.set_page_config(
    page_title="InvestXact",
    page_icon=PAGE_ICON,
    layout="centered"
)

st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0;'>InvestXact</h1>
    <p style='text-align: center; margin-top: 0; color: #6b7280;'>portfolio allocation calculator</p>
    """,
    unsafe_allow_html=True,
)

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "secret_key" not in st.session_state:
    st.session_state.secret_key = "" 

# ------ Start-up Page Configuration ------ #
col1, col_middle, col2 = st.columns([1, 0.2, 1])

with col1:
    create_new = st.button("➕ Create New Strategy", use_container_width=True)

    # Input field
    api_input = st.text_input(
        "Enter your Alpaca authentication",
        value=st.session_state.api_key or "",
        type="password",
        placeholder="Paste your API key here"
    )

with col_middle:
    st.markdown("<div style='text-align:center'>or</div>", unsafe_allow_html=True)
with col2:
    load_existing = st.button("📂 Load Existing Strategy", use_container_width=True)

    # Input field
    secret_key_input = st.text_input(
        "", 
        value=st.session_state.secret_key or "",
        type="password",
        placeholder="Paste your API secret key here"
    )

# Save every new entry
if api_input != st.session_state.api_key:
    st.session_state.api_key = api_input
    st.success("API key saved!")

if secret_key_input != st.session_state.secret_key:
    st.session_state.secret_key = api_input
    st.success("Secret key saved!")


# ------ Set Sessions ------ #
if "page" not in st.session_state:
    st.session_state.page = None
if "strategy_df" not in st.session_state:
    st.session_state.strategy_df = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None
if "target" not in st.session_state:
    st.session_state.target = 1000



if create_new:
    st.session_state.page = "setup"
elif load_existing:
    st.session_state.page = "view"

st.markdown("---") 
if st.session_state.page == "setup":
    setup()  # calls function in setup_portfolio.py
elif st.session_state.page == "view":
    strategy = Strategy()   # calls function in view_strategy.py
    strategy.upload_file()
    strategy.show_portfolio()
    strategy.calculate_shares()

else:
    st.info("Choose an option above to get started.")