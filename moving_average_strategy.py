import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from MySQL or CSV
def load_data():
    # Replace this with your actual method of loading data (from MySQL or local file)
    file_path = "D:/Downloads/HINDALCO_1D.xlsx"  # Update with your path
    data = pd.read_excel(file_path)
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace=True)
    return data

# Generate Buy and Sell Signals
def moving_average_strategy(data, short_window=10, long_window=50):
    data['Short_MA'] = data['close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['close'].rolling(window=long_window).mean()

    # Generate Signals
    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(
        data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0
    )
    data['Position'] = data['Signal'].diff()

    # Buy/Sell Signals
    data['Buy Signal'] = np.where(data['Position'] == 1, data['close'], np.nan)
    data['Sell Signal'] = np.where(data['Position'] == -1, data['close'], np.nan)
    return data

# Plot Moving Average Crossover Strategy
def plot_strategy(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data['close'], label='Closing Price', color='blue', alpha=0.6)
    plt.plot(data['Short_MA'], label='Short-Term MA (10)', color='green', alpha=0.8)
    plt.plot(data['Long_MA'], label='Long-Term MA (50)', color='red', alpha=0.8)
    plt.scatter(data.index, data['Buy Signal'], label='Buy Signal', marker='^', color='green', alpha=1)
    plt.scatter(data.index, data['Sell Signal'], label='Sell Signal', marker='v', color='red', alpha=1)
    plt.title('Moving Average Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Calculate Performance Metrics
def evaluate_performance(data):
    # Calculate daily returns
    data['Daily Return'] = data['close'].pct_change()
    data['Strategy Return'] = data['Daily Return'] * data['Signal'].shift(1)

    # Cumulative returns
    cumulative_strategy_return = (1 + data['Strategy Return']).cumprod()
    cumulative_market_return = (1 + data['Daily Return']).cumprod()

    # Metrics
    total_strategy_return = cumulative_strategy_return.iloc[-1] - 1
    total_market_return = cumulative_market_return.iloc[-1] - 1
    win_rate = len(data[data['Signal'] > 0]) / len(data) * 100

    print(f"Total Strategy Return: {total_strategy_return * 100:.2f}%")
    print(f"Total Market Return: {total_market_return * 100:.2f}%")
    print(f"Strategy Win Rate: {win_rate:.2f}%")

    # Plot cumulative returns
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, cumulative_strategy_return, label='Strategy Returns', color='green')
    plt.plot(data.index, cumulative_market_return, label='Market Returns', color='blue')
    plt.legend()
    plt.title('Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.show()

if __name__ == "__main__":
    # Step 1: Load the data
    data = load_data()

    # Step 2: Apply the Moving Average Strategy
    data = moving_average_strategy(data)

    # Step 3: Plot the Moving Average Crossover Strategy
    plot_strategy(data)

    # Step 4: Evaluate the Performance
    evaluate_performance(data)
