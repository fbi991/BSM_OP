import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from model import black_scholes_call, black_scholes_put, black_scholes_delta

def main():
    st.title("Options Pricing (Black-Scholes Model)")
    st.write("Calculate European Call and Put option prices based on the inputs")

    st.header("Stock Selection")
    use_real_price = st.checkbox("Use Real Stock Price", value=False)

    if use_real_price:
        ticker = st.text_input("Stock Ticker", value="AAPL")
        if ticker:
            stock = yf.Ticker(ticker)
            todays_data = stock.history(period='1d')
            if not todays_data.empty:
                S = todays_data['Close'][0]
                st.success(f"Current {ticker.upper()} Price: ${S:.2f}")
            else:
                st.error("Could not find data. Check ticker symbol.")
                S = st.slider("Stock Price (S)", 50.0, 500.0, 100.0)
    else:
        S = st.slider("Stock Price (S)", 50.0, 500.0, 100.0)

    K = st.slider("Strike Price (K)", 50.0, 500.0, 100.0)
    T = st.slider("Time to Maturity (T, in years)", 0.01, 5.0, 1.0)
    r = st.slider("Risk-Free Rate (r)", 0.0, 0.1, 0.01)
    sigma = st.slider("Volatility (σ)", 0.01, 1.0, 0.2)

    if st.button("Calculate and Plot"):
        call = black_scholes_call(S, K, T, r, sigma)
        put = black_scholes_put(S, K, T, r, sigma)

        st.success(f"Call Option Price: ${call:.2f}")
        st.success(f"Put Option Price: ${put:.2f}")

        # Plot Option Prices
        stock_prices = np.linspace(S * 0.8, S * 1.2, 50)
        call_prices = [black_scholes_call(s, K, T, r, sigma) for s in stock_prices]
        put_prices = [black_scholes_put(s, K, T, r, sigma) for s in stock_prices]

        fig, ax = plt.subplots()
        ax.plot(stock_prices, call_prices, label="Call Price", color="blue")
        ax.plot(stock_prices, put_prices, label="Put Price", color="green")
        ax.axvline(S, linestyle="--", color="gray", label="Current S")
        ax.set_xlabel("Stock Price")
        ax.set_ylabel("Option Price ($)")
        ax.set_title("Option Prices vs Stock Price")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # Plot Delta
        delta_values = [black_scholes_delta(s, K, T, r, sigma) for s in stock_prices]

        fig2, ax2 = plt.subplots()
        ax2.plot(stock_prices, delta_values, label="Call Delta", color="purple")
        ax2.axhline(0.5, linestyle="--", color="grey")
        ax2.axvline(S, linestyle="--", color="grey")
        ax2.set_xlabel("Stock Price")
        ax2.set_ylabel("Delta")
        ax2.set_title("Delta vs Stock Price")
        ax2.legend()
        ax2.grid(True)

        st.pyplot(fig2)

if __name__ == "__main__":
    main()
