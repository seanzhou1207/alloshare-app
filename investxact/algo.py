import cvxpy as cp
import numpy as np
import pandas as pd
import yfinance as yf
import pytz

from datetime import datetime, timedelta, time

def get_adjusted_today():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    current_time = now.time()
    
    # Weekend handling
    if now.weekday() >= 5:
        return (now - timedelta(days=now.weekday() - 4)).date()
    
    # Trading hours check (9:30 AM - 4:00 PM EST)
    if time(9, 30) <= current_time <= time(16, 0):
        # Use previous business day
        return (now - timedelta(days=1 if now.weekday() > 0 else 3)).date()
    
    # Regular weekday outside trading hours
    return now.date()

def _get_latest_prices(tickers: np.ndarray) -> np.ndarray:
    """Fetch latest close prices from Yahoo Finance in ticker order."""
    ticker_list = [str(t).strip() for t in tickers]
    if not ticker_list:
        raise ValueError("No tickers provided for price fetch.")

    if len(ticker_list) == 1:
        # Single ticker returns a one-symbol DataFrame shape.
        history = yf.Ticker(ticker_list[0]).history(period="5d")
        if history.empty or "Close" not in history:
            raise ValueError(f"Price fetch failed for ticker: {ticker_list[0]}")
        last_close = history["Close"].dropna()
        if last_close.empty:
            raise ValueError(f"No valid close price for ticker: {ticker_list[0]}")
        return np.array([float(last_close.iloc[-1])])

    data = yf.download(
        ticker_list,
        period="5d",
        auto_adjust=False,
        progress=False,
        group_by="column",
    )
    if data.empty or "Close" not in data:
        raise ValueError("Price fetch failed from Yahoo Finance.")

    close_df = data["Close"]
    latest_close = close_df.ffill().iloc[-1]
    missing = [ticker for ticker in ticker_list if ticker not in latest_close.index or pd.isna(latest_close[ticker])]
    if missing:
        raise ValueError(f"Price fetch failed for tickers: {sorted(missing)}")

    return np.array([float(latest_close[ticker]) for ticker in ticker_list])

def run_optimization(budget: float, strategy_df: pd.DataFrame):
    """Original optimization logic with budget_range support"""
        
    # Original input extraction (unchanged)
    tickers = strategy_df["Ticker"].to_numpy()
    subweights = strategy_df["Subweights"].to_numpy()
    
    # for asset_class in assets:
    #     subweights.extend([sw/100 for sw in asset_class["subweights"]])
    #     for ticker in asset_class["tickers"]:
    #         tickers.append(ticker)
    #         weights.append(asset_class["allocation"]/100)

    # Original parameter setup (now using range)
    T = budget
    T_min, T_max = budget * 0.95, budget * 1.05  # Using renamed variable
    lambda_ = 1
    n = len(tickers)
    weights = [float(w) for w in strategy_df["Weights"]]

    # Price fetching from Yahoo Finance only
    p = _get_latest_prices(tickers)

    P = np.diag(p)  # Diagonal price matrix
    w = np.array(weights)
    R = np.diag(subweights)
    prop = R @ w
    q = cp.Variable(n, integer=True)
    cost_total = p @ q
    allocation_deviation = P @ q - cost_total * prop

    # Problem formulation (unchanged except budget_range usage)
    problem = cp.Problem(
        cp.Minimize(cp.square(cost_total - T) + lambda_ * cp.norm(allocation_deviation, 2)),
        [
            cost_total >= T_min,
            cost_total <= T_max,  # Using budget_range values here
            q >= 0
        ]
    )

    # Solve with original solver preference
    try:
        problem.solve(solver=cp.GUROBI, verbose=False)
    except:
        problem.solve()

    # Prepare your preferred return structure
    shares = q.value.round().astype(int)
    allocations = (P @ q.value / cost_total.value).round(4)
    prop_real = P @ q.value / cost_total.value
    
    # After solving, add this print statement:
    print("\n=== Optimization Results ===", flush=True)
    print(f"Budget: ${budget:.2f} (Range: ${T_min:.2f}-${T_max:.2f})", flush=True)
    print(f"Actual Cost: ${cost_total.value:.2f}", flush=True)
    print("\nTicker Details:", flush=True)
    print(f"{'Ticker':<10}{'Target %':>10}{'Shares':>10}{'Actual %':>10}{'Price':>10}", flush=True)

    for i in range(len(tickers)):
        print(f"{tickers[i]:<10}{prop[i]*100:>9.1f}%{int(q.value[i]):>10}"
            f"{prop_real[i]*100:>9.1f}%{p[i]:>9.2f}", flush=True)    

    return {
        "summary": {
            "budget": float(T),
            "actual_cost": float(cost_total.value),
            "solver_status": problem.status
        },
        "assets": [
            {
                "ticker": tickers[i],
                "target_weight": float(prop[i]),
                "shares": int(q.value[i]),
                "allocation": float(prop_real[i]),
                "price": float(p[i])
            } for i in range(len(tickers))
        ]
    }


