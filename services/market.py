import streamlit as st
import pandas as pd
import yfinance as yf
from utils.ai_engine import llm_generate

def run_market():
    st.header("Market Prediction Advisor")
    st.write("Select a ticker (or use sample data). The app will fetch market data and provide a short analysis.")
    ticker = st.text_input("Ticker (e.g., ^IXIC for NASDAQ)", value="^IXIC")
    use_sample = st.checkbox("Use sample data (offline demo)", value=True)
    if st.button("Fetch & Analyze"):
        if use_sample:
            df = pd.read_csv('sample_data/sample_market.csv', parse_dates=['Date'])
        else:
            try:
                df = yf.download(ticker, period='1y', interval='1d')
                df = df.reset_index().rename(columns={'Date':'Date'})
            except Exception as e:
                st.error(f"Failed to fetch market data: {e}. Using sample data instead.")
                df = pd.read_csv('sample_data/sample_market.csv', parse_dates=['Date'])
        st.line_chart(df.set_index('Date')['Close'])
        df['MA7'] = df['Close'].rolling(7).mean()
        df['MA30'] = df['Close'].rolling(30).mean()
        st.line_chart(df.set_index('Date')[['Close','MA7','MA30']])
        summary = llm_generate(f"Provide a concise market analysis for ticker {ticker} based on latest close {df['Close'].iloc[-1]:.2f}. Show 3 actionable recommendations for a tech startup investment strategy.", max_tokens=180)
        st.subheader('Harper\'s Analysis & Advice')
        st.write(summary)
