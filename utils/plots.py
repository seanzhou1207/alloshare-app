import matplotlib.pyplot as plt

def nested_pie_chart(df, category_col="Category", ticker_col="Ticker", value_col="Allocation"):
    """
    Create a nested pie chart:
      - Outer ring: category allocation
      - Inner ring: ticker-level split

    Parameters:
        df : pandas.DataFrame with columns [category_col, ticker_col, value_col]
        category_col : str, column name for categories
        ticker_col   : str, column name for tickers
        value_col    : str, column name for numeric values (allocation)
    """
    # --- Outer (category split) ---
    outer_vals = df.groupby(category_col)[value_col].sum()
    outer_labels = outer_vals.index

    # --- Inner (ticker split) ---
    inner_vals = df[value_col]
    inner_labels = df[ticker_col]

    # --- Colors ---
    tab20c = plt.get_cmap("tab20c").colors
    outer_colors = [tab20c[i] for i in range(0, len(outer_vals) * 4, 4)]
    inner_colors = [tab20c[i] for i in range(1, len(inner_vals) + 1)]

    # --- Plot ---
    fig, ax = plt.subplots()
    size = 0.3

    # Outer ring
    ax.pie(
        outer_vals, radius=1, labels=outer_labels,
        colors=outer_colors, wedgeprops=dict(width=size, edgecolor="w")
    )

    # Inner ring
    ax.pie(
        inner_vals, radius=1 - size, labels=inner_labels,
        colors=inner_colors, wedgeprops=dict(width=size, edgecolor="w")
    )

    ax.set(aspect="equal", title="Portfolio Allocation (Nested)")
    return fig
