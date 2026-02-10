# STOCK PRICE ANALYZER - STREAMLIT VERSION
# --------------------------------------
# pip install streamlit yfinance pandas

import streamlit as st
import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        company_name = info.get('longName', symbol)
        current_price = info.get('currentPrice')
        previous_close = info.get('previousClose')

        if current_price and previous_close:
            change = current_price - previous_close
            pct_change = (change / previous_close) * 100
            daily_change = f"{change:+.2f} ({pct_change:+.2f}%)"
        else:
            daily_change = "N/A"

        return {
            'Company Name': company_name,
            'Current Price': f"₹{current_price:,.2f}" if current_price else "N/A",
            'Daily Change': daily_change
        }

    except Exception as e:
        st.error(f"Error: {e}")
        return None

st.title("📈 STOCK PRICE ANALYZER")
st.markdown("---")

symbol = st.text_input("Enter stock symbol (e.g. RELIANCE.NS)").strip().upper()

if st.button("Fetch Stock Data"):
    if symbol:
        st.write(f"Fetching **{symbol}** ...")
        data = get_stock_data(symbol)

        if data:
            st.subheader("Stock Data")
            st.write(f"**Symbol:** {symbol}")
            st.write(f"**Company:** {data['Company Name']}")
            st.write(f"**Price:** {data['Current Price']}")
            st.write(f"**Change:** {data['Daily Change']}")

            df = pd.DataFrame([data])
            df["Symbol"] = symbol

            st.markdown("### Download CSV")
            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False),
                file_name=f"{symbol}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data found.")
    else:
        st.warning("Please enter a stock symbol.")