import pandas as pd
import streamlit as st
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(layout='wide')

# Load data
df = pd.read_excel("Trades.xlsx")
df["TradeDate"] = pd.to_datetime(df["TradeDate"], errors="coerce")
df = df.dropna(subset=["TradeDate"])

# Header
st.markdown("<h1 style='text-align:center;'>Trade Surveillance Dashboard</h1>", unsafe_allow_html=True)

# Top metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Trades", len(df))
with col2:
    st.metric("Total Trade Value", f"${df['TradeValue'].sum():,.0f}")
with col3:
    st.metric("Last Updated", datetime.datetime.now().strftime("%d %b %Y"))

st.divider()

# Trade Value by Trader
fig1 = px.bar(
    df,
    x="Trader",
    y="TradeValue",
    title="Total Trade Value by Trader",
    labels={"TradeValue": "Trade Value ($)"},
    template="plotly_dark"
)
st.plotly_chart(fig1, use_container_width=True)

# Number of Trades per Day
daily_trades = (df.groupby(df["TradeDate"].dt.date).size().reset_index(name="TradeCount"))

fig2 = px.bar(
    daily_trades,
    x="TradeDate",
    y="TradeCount",
    title="Number of Trades per Day",
    labels={"TradeDate": "Date", "TradeCount": "Number of Trades"},
    template="plotly_dark"
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Trade Value & Quantity by Region
state_summary = df.groupby("Region")[["TradeValue", "Quantity"]].sum().reset_index()

fig3 = go.Figure()

fig3.add_trace(go.Bar(x=state_summary["Region"], y=state_summary["TradeValue"], name="Trade Value"))

fig3.add_trace(go.Scatter(x=state_summary["Region"], y=state_summary["Quantity"], name="Quantity", yaxis="y2"))

fig3.update_layout(
    title="Trade Value and Quantity by Region",
    xaxis=dict(title="Region"),
    yaxis=dict(title="Trade Value"),
    yaxis2=dict(title="Quantity", overlaying="y", side="right"),
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Treemap: Trade Value by Region & City
treemap = df.groupby(["Region", "City"])["TradeValue"].sum().reset_index()

fig4 = px.treemap(
    treemap,
    path=["Region", "City"],
    values="TradeValue",
    title="Trade Value by Region and City",
    template="plotly_dark"
)

st.plotly_chart(fig4, use_container_width=True)

with st.expander("View Raw Trade Data"):
    st.dataframe(df)
