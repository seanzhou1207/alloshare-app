import streamlit as st
import pandas as pd
import json
from pathlib import Path

def setup():
    with st.form("manual_entry"):
        name = st.text_input("File name", placeholder="my_strategy")
        target = st.text_input("Target Budget ($)", placeholder="1000")
        tickers = st.text_input("Tickers (comma-separated)", placeholder="SPLG,DIVI,BND,VCIT,IAGG")
        categories = st.text_input("Categories (comma-separated)", placeholder="Stock,Stock,Bond,Bond,Bond")
        weights = st.text_input("Weights (repeat if same category)", placeholder="0.8,0.8,0.2,0.2,0.2")
        subweights = st.text_input("Subweights (comma-separated)", placeholder="0.8,0.2,0.4,0.4,0.2")
        submitted = st.form_submit_button("Save Strategy")

    file_path = Path(f"strategy/{name}.json")

    if submitted:
        df = pd.DataFrame({
            "Ticker": [t.strip() for t in tickers.split(",")],
            "Category": [c.strip() for c in categories.split(",")],
            "Weights": [w.strip() for w in weights.split(",")], 
            "Subweights": [s.strip() for s in subweights.split(",")]
        })

        # Convert numeric columns
        for col in ["Weights", "Subweights"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            if df[col].isna().any():
                st.warning(f"⚠️ Column **{col}** contains non-numeric values.")

        # Save as JSON (structured for future metadata)
        payload = {
            "strategy_name": name,
            "target": target,
            "portfolio": df.to_dict(orient="records")
        }
        with open(file_path, "w") as f:
            json.dump(payload, f, indent=2)

        st.success(f"Strategy saved to {file_path}")

    if file_path.exists():
        with open(file_path, "r") as f:
            payload = json.load(f)
        df = pd.DataFrame(payload["portfolio"])
        st.dataframe(df)
