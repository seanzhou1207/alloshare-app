def show():
    import streamlit as st
    import pandas as pd
    from pathlib import Path

    with st.form("manual_entry"):
        name = st.text_input("File name", value="my_strategy")
        tickers = st.text_input("Tickers (comma-separated)", "SPLG,DIVI,BND,VCIT,IAGG")
        categories = st.text_input("Categories (comma-separated)", "Stock,Stock,Bond,Bond,Bond")
        weights = st.text_input("Weights (repeat if same category)", "0.8, 0.8, 0.2, 0.2, 0.2")
        subweights = st.text_input("Subweights (comma-separated)", "0.8,0.2,0.4,0.4,0.2")
        submitted = st.form_submit_button("Save Strategy")

    file_path = Path(f"strategy/{name}.parquet")

    if submitted:
        df = pd.DataFrame({
            "Ticker": [t.strip() for t in tickers.split(",")],
            "Category": [c.strip() for c in categories.split(",")],
            "Weights": [w.strip() for w in weights.split(",")], 
            "Subweights": [float(s.strip()) for s in subweights.split(",")]
        })
        # Validation + conversion for numeric columns
        numeric_cols = ["Weights", "Subweights"]  # adjust to your schema
        for col in numeric_cols:
            if col in df.columns:
                # Force conversion
                df[col] = pd.to_numeric(df[col], errors="coerce")

                # Warn if conversion produced NaN
                if df[col].isna().any():
                    st.warning(f"⚠️ Column **{col}** contains non-numeric values. Check your data.")

        df.to_parquet(file_path, index=False)
        st.success(f"Strategy saved to {file_path}")

    if file_path.exists():
        st.dataframe(pd.read_parquet(file_path))

# Call the function
show()
