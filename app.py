import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

# Title of the app
st.title("Moving Averages Crossover Strategy (demo app)")

# Input for stock symbol
stock_symbol = st.text_input("Enter Stock Symbol Only (Example: AAPL, TSLA, MSFT):", value="AAPL")

# Select the number of days to fetch data for
days_option = st.selectbox("Select Number of Days for Stock Data:", options=[7, 15, 30, 60, 90, 180, 365])
period = f"{days_option}d"  # Convert days to the format used by Yahoo Finance API

# Add Buy/Sell buttons
buy_button = st.button("Buy")
sell_button = st.button("Sell")

if buy_button:
    st.write(f"📈 You bought {stock_symbol}!")
    # Simulate buy logic here

if sell_button:
    st.write(f"📉 You sold {stock_symbol}!")
    # Simulate sell logic here

# Button to fetch and plot
if st.button("Fetch and Plot"):
    if stock_symbol:
        # Loop to auto-refresh the chart every 10 seconds
        while True:
            data = yf.download(tickers=stock_symbol, period=period, interval="15m", progress=False)
            if not data.empty:
                # Calculate Moving Averages
                data['SMA_Short'] = data['Close'].rolling(window=20).mean()
                data['SMA_Long'] = data['Close'].rolling(window=50).mean()

                # Plotting
                fig, ax = plt.subplots(figsize=(14,7))
                ax.plot(data['Close'], label='Close Price', alpha=0.5)
                ax.plot(data['SMA_Short'], label='Short SMA (20)', color='green')
                ax.plot(data['SMA_Long'], label='Long SMA (50)', color='red')

                # Show Buy/Sell signals (basic)
                for i in range(1, len(data)):
                    if (data['SMA_Short'].iloc[i] > data['SMA_Long'].iloc[i]) and (data['SMA_Short'].iloc[i-1] <= data['SMA_Long'].iloc[i-1]):
                        ax.scatter(data.index[i], data['Close'].iloc[i], marker='^', color='blue', s=100, label='Buy Signal' if 'Buy Signal' not in ax.get_legend_handles_labels()[1] else "")
                    elif (data['SMA_Short'].iloc[i] < data['SMA_Long'].iloc[i]) and (data['SMA_Short'].iloc[i-1] >= data['SMA_Long'].iloc[i-1]):
                        ax.scatter(data.index[i], data['Close'].iloc[i], marker='v', color='red', s=100, label='Sell Signal' if 'Sell Signal' not in ax.get_legend_handles_labels()[1] else "")

                ax.set_title(f"{stock_symbol} - Moving Averages Crossover")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price")
                ax.legend()
                ax.grid(True)

                # Show chart
                st.pyplot(fig)

                # Wait for 10 seconds before updating
                time.sleep(60)
            else:
                st.error("⚠️ No data found. Please check the symbol and try again.")
# To run "python -m streamlit run app.py"
