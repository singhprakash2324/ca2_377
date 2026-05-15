# app.py
# Stock Market Analysis Dashboard using Streamlit

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #333;
}

h1, h2, h3 {
    color: #00FFAA;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📊 Stock Market Analysis Dashboard")
st.markdown("### Real-Time Financial Insights & Technical Analysis")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Dashboard Controls")

stock = st.sidebar.text_input("Enter Stock Symbol", "AAPL")

start_date = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2023-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date.today()
)

# ---------------- FETCH DATA ----------------
data = yf.download(stock, start=start_date, end=end_date)

if data.empty:
    st.error("No data found. Please check the stock symbol.")
    st.stop()

# ---------------- DATA PROCESSING ----------------
data["MA50"] = data["Close"].rolling(50).mean()
data["MA200"] = data["Close"].rolling(200).mean()

# Daily Returns
data["Daily Return"] = data["Close"].pct_change()

# ---------------- STOCK INFO ----------------
ticker = yf.Ticker(stock)
info = ticker.info

current_price = info.get("currentPrice", 0)
market_cap = info.get("marketCap", 0)
pe_ratio = info.get("trailingPE", 0)
volume = info.get("volume", 0)

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Current Price", f"${current_price}")

with col2:
    st.metric("🏢 Market Cap", f"{market_cap:,}")

with col3:
    st.metric("📊 P/E Ratio", f"{pe_ratio}")

with col4:
    st.metric("📦 Volume", f"{volume:,}")

# ---------------- PRICE CHART ----------------
st.subheader("📈 Stock Price Trend")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["Close"],
    mode='lines',
    name='Close Price',
    line=dict(color='#00FFAA', width=3)
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA50"],
    mode='lines',
    name='50-Day MA',
    line=dict(color='orange', width=2)
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA200"],
    mode='lines',
    name='200-Day MA',
    line=dict(color='red', width=2)
))

fig.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- CANDLESTICK CHART ----------------
st.subheader("🕯️ Candlestick Chart")

candlestick = go.Figure(data=[go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
)])

candlestick.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(candlestick, use_container_width=True)

# ---------------- DAILY RETURNS ----------------
st.subheader("📉 Daily Returns Distribution")

hist_fig = px.histogram(
    data,
    x="Daily Return",
    nbins=50,
    title="Daily Returns Histogram"
)

hist_fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(hist_fig, use_container_width=True)

# ---------------- VOLUME ANALYSIS ----------------
st.subheader("📦 Trading Volume")

volume_fig = go.Figure()

volume_fig.add_trace(go.Bar(
    x=data.index,
    y=data["Volume"],
    marker_color="#00CC96"
))

volume_fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Volume"
)

st.plotly_chart(volume_fig, use_container_width=True)

# ---------------- RAW DATA ----------------
st.subheader("📋 Historical Data")

st.dataframe(data.tail(20), use_container_width=True)

# ---------------- STATISTICS ----------------
st.subheader("📊 Statistical Summary")

st.dataframe(data.describe(), use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    """
    <center>
    Made with ❤️ using Streamlit, Plotly & Yahoo Finance API
    </center>
    """,
    unsafe_allow_html=True
)