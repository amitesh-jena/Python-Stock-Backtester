# Python-Stock-Backtester

A simple yet effective Python script for backtesting a Simple Moving Average (SMA) crossover trading strategy on historical stock data using the `yfinance` library.

## 📜 Description

This tool allows users to input multiple stock tickers and a date range. It then fetches the historical price data, calculates the 20-day and 50-day SMAs, and generates buy/sell signals based on when the short-term SMA crosses the long-term SMA. Finally, it runs a simple backtest to calculate the potential return on an initial investment and visualizes the strategy on a chart.

## ✨ Features

-   **Fetch Data**: Downloads historical stock data from Yahoo Finance.
-   **Generate Signals**: Implements an SMA Crossover strategy (20-day vs. 50-day).
-   **Backtest Strategy**: Simulates trades and calculates the final capital and percentage return.
-   **Visualize**: Plots the close price, SMAs, and buy/sell signals using `matplotlib`.
-   **Export Results**: Saves detailed signal data and a summary of returns to CSV files in an `outputs` directory.


