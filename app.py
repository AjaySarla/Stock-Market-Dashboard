import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("📈 Stock Market Analysis Dashboard")

# Sidebar
st.sidebar.title("Settings")

ticker = st.sidebar.text_input("Ticker", "AAPL")

# Download Data
try:
    data = yf.download(ticker, period="1y")

    if data.empty:
        st.error("Unable to fetch stock data. Please try another stock later.")
        st.stop()

except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()
st.subheader("Stock Data")
st.write(data.tail())

# Closing Price Chart
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        name="Close Price"
    )
)

fig.update_layout(title=f"{ticker} Closing Price")

st.plotly_chart(fig)

# Moving Averages
data["MA50"] = data["Close"].rolling(50).mean()
data["MA200"] = data["Close"].rolling(200).mean()

fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close"))
fig2.add_trace(go.Scatter(x=data.index, y=data["MA50"], name="50 Day MA"))
fig2.add_trace(go.Scatter(x=data.index, y=data["MA200"], name="200 Day MA"))

st.plotly_chart(fig2)

# Daily Returns
data["Returns"] = data["Close"].pct_change()

st.subheader("Daily Returns")
st.line_chart(data["Returns"])

# Volume
st.subheader("Volume")
st.bar_chart(data["Volume"])

# Candlestick Chart
fig3 = go.Figure(
    data=[
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"]
        )
    ]
)

st.plotly_chart(fig3)

# Download CSV
csv = data.to_csv().encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "stock_data.csv",
    "text/csv"
)

st.subheader("Company Information")
st.info("Company details feature coming soon.")