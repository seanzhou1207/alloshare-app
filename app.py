import cvxpy as cp
import numpy as np
import pandas as pd
import yfinance as yf
import pytz
import streamlit as st
from investxact.setup_portfolio import setup
from investxact.view_strategy import Strategy
PAGE_ICON = "assets/logo.png"

# ------ Page Configuration ------ #
st.set_page_config(
    page_icon=PAGE_ICON,
    page_title="InvestXact",
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

with col_middle:
    st.markdown("<div style='text-align:center'>or</div>", unsafe_allow_html=True)
with col2:
    load_existing = st.button("📂 Load Existing Strategy", use_container_width=True)
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
    st.write(cp.installed_solvers())
    strategy = Strategy()   # calls function in view_strategy.py
    strategy.upload_file()
    strategy.show_portfolio()
    strategy.calculate_shares()

else:
    st.info("Choose an option above to get started.")