import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Fetch historical data
def fetch_data(stock_symbol, start, end):
    data = yf.download(stock_symbol, start=start, end=end)
    if not data.empty:
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
    return data

# Generate buy-sell signals
def generate_signals(data):
    data['Signal'] = 0
    data['Signal'][20:] = [1 if data['SMA20'].iloc[i] > data['SMA50'].iloc[i] else 0 for i in range(20, len(data))]
    data['Position'] = data['Signal'].diff()
    return data

# Plot the signals
def plot_signals(data, stock_symbol):
    plt.figure(figsize=(14, 6))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['SMA20'], label='SMA 20', linestyle='--')
    plt.plot(data['SMA50'], label='SMA 50', linestyle='--')
    plt.plot(data[data['Position'] == 1].index, data['SMA20'][data['Position'] == 1], '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(data[data['Position'] == -1].index, data['SMA20'][data['Position'] == -1], 'v', markersize=10, color='r', label='Sell Signal')
    plt.title(f"{stock_symbol} SMA Crossover Strategy")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Backtest logic
def backtest(data, initial_capital=100000):
    capital = initial_capital
    position = 0
    for i in range(len(data)):
        if data['Position'].iloc[i] == 1 and position == 0:
            buy_price = data['Close'].iloc[i]
            position = capital / buy_price
        elif data['Position'].iloc[i] == -1 and position > 0:
            sell_price = data['Close'].iloc[i]
            capital = position * sell_price
            position = 0
    if position > 0:
        capital = position * data['Close'].iloc[-1]
    return round(capital, 2)

# Create output directory
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Main
if __name__ == "__main__":
    stocks = input("Enter stock symbols (comma separated): ")
    stocks = [s.strip().upper() for s in stocks.split(",")]
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    initial_capital = 100000

    summary = []

    for symbol in stocks:
        print(f"\n Processing: {symbol}")
        df = fetch_data(symbol, start_date, end_date)
        if df.empty:
            print(f" No data for {symbol}")
            continue

        df = generate_signals(df)
        final_capital = backtest(df, initial_capital)
        return_pct = ((final_capital - initial_capital) / initial_capital) * 100

        # Save data to CSV
        filename = f"outputs/{symbol}_signals.csv"
        df.to_csv(filename)
        print(f" Saved signal data to {filename}")

        # Add to summary
        summary.append({
            "Stock": symbol,
            "Final Capital": final_capital,
            "Return (%)": round(return_pct, 2)
        })

        plot_signals(df, symbol)

    # Summary DataFrame
    summary_df = pd.DataFrame(summary).sort_values(by="Return (%)", ascending=False)
    summary_file = "outputs/summary_returns.csv"
    summary_df.to_csv(summary_file, index=False)

    print("\n Final Performance Summary:")
    print(summary_df.to_string(index=False))
    print(f"\n Summary saved to: {summary_file}")