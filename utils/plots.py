import plotly.express as px

def nested_pie_chart(df, category_col="Category", ticker_col="Ticker", value_col="Split"):
    """
    Create a nested pie chart:
      - Outer ring: category allocation
      - Inner ring: ticker-level split

    Parameters:
        df : pandas.DataFrame with columns [category_col, ticker_col, value_col]
        category_col : str, column name for categories
        ticker_col   : str, column name for tickers
        value_col    : str, column name for numeric values (defaults to Split)
    """
    # Keep the same hierarchy: outer categories, inner tickers.
    fig = px.sunburst(
        df,
        path=[category_col, ticker_col],
        values=value_col,
        color=category_col,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    # Adapt text size based on smallest non-zero slice so tiny sections stay readable.
    values = df[value_col].astype(float)
    total = values.sum()
    min_ratio = (values[values > 0].min() / total) if total > 0 and (values > 0).any() else 1.0
    if min_ratio < 0.015:
        base_font_size = 8
    elif min_ratio < 0.03:
        base_font_size = 9
    else:
        base_font_size = 11

    # Style only top-level category labels (e.g., Stock/Bond).
    category_or_ticker_text = []
    for label, parent in zip(fig.data[0].labels, fig.data[0].parents):
        if parent == "":
            category_or_ticker_text.append(f"<span style='font-size:{base_font_size + 2}px'><b>{label}</b></span>")
        else:
            category_or_ticker_text.append(label)

    fig.update_traces(
        text=category_or_ticker_text,
        texttemplate="%{text}<br>%{percentParent:.1%}",
        textfont=dict(size=base_font_size, family="Arial"),
        insidetextorientation="auto",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Value: %{value:.4f}<br>"
            "Share: %{percentParent:.1%}<extra></extra>"
        ),
    )
    fig.update_layout(
        margin=dict(t=50, l=20, r=20, b=20),
        uniformtext=dict(minsize=base_font_size, mode="show"),
    )
    return fig
