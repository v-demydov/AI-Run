import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent

@st.cache_data
def load_data():
    sales = pd.read_parquet(BASE / "gold/daily_sales_by_category.parquet")
    returns = pd.read_parquet(BASE / "gold/returns_rate.parquet")
    sales["order_date"] = pd.to_datetime(sales["order_date"])
    returns["order_date"] = pd.to_datetime(returns["order_date"])
    return sales, returns

sales, returns = load_data()

st.title("Sales Performance Dashboard")

# ── Sidebar: date-range filter ────────────────────────────────────────────────
min_date = sales["order_date"].min().date()
max_date = sales["order_date"].max().date()
default_start = (sales["order_date"].max() - pd.Timedelta(days=30)).date()

st.sidebar.header("Filters")
start, end = st.sidebar.date_input(
    "Date range",
    value=(default_start, max_date),
    min_value=min_date,
    max_value=max_date,
)

sales_f   = sales[(sales["order_date"].dt.date >= start) & (sales["order_date"].dt.date <= end)]
returns_f = returns[(returns["order_date"].dt.date >= start) & (returns["order_date"].dt.date <= end)]

# ── Metric cards ──────────────────────────────────────────────────────────────
total_revenue = sales_f["total_revenue"].sum()
avg_returns   = returns_f["returns_rate_pct"].mean()

col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Returns Rate", f"{avg_returns:.1f}%")

# ── Chart 1: grouped bar — total_revenue by region, color by product_category ─
rev_by_region = (
    sales_f.groupby(["region", "product_category"], as_index=False)["total_revenue"].sum()
)

fig1 = px.bar(
    rev_by_region,
    x="region",
    y="total_revenue",
    color="product_category",
    barmode="group",
    title="Revenue by Region & Category",
    labels={"total_revenue": "Revenue ($)", "region": "Region", "product_category": "Category"},
)
fig1.update_layout(legend_title_text="Category")
st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2: line — returns_rate_pct over time ────────────────────────────────
fig2 = px.line(
    returns_f.sort_values("order_date"),
    x="order_date",
    y="returns_rate_pct",
    title="Returns Rate Over Time",
    labels={"returns_rate_pct": "Returns Rate (%)", "order_date": "Date"},
)
fig2.update_traces(line_color="#ef553b")
st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Data last updated: {max_date}")
