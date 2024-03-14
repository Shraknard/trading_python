import time
import datetime
import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_data(symbol, timeframe, since, limit):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_sma(df, period=20):
    return df['close'].rolling(window=period).mean()

def calculate_bollinger_bands(df, sma, period=20, std_factor=2):
    std = df['close'].rolling(window=period).std()
    upper_band = sma + std_factor * std
    lower_band = sma - std_factor * std
    return upper_band, lower_band

def backtest_strategy(df, initial_balance=1000):
    balance = initial_balance
    position = 0
    trades = []
    profits = []  # Initialize profits list

    for index, row in df.iterrows():
        if position == 0 and row['close'] > row['sma'] and row['close'] > row['upper_band'] and row['upper_band'] - row['lower_band'] > 0:
            # Buy condition
            position = balance / row['close']
            balance = 0
            trades.append(('buy', row['timestamp'], row['close']))

        elif position > 0 and (row['close'] < row['sma'] or row['close'] < row['lower_band']) and row['upper_band'] - row['lower_band'] > 0:
            # Sell condition
            sell_balance = position * row['close']
            profit = sell_balance - initial_balance
            profits.append(profit)  # Record profit at sell
            balance = sell_balance
            position = 0
            trades.append(('sell', row['timestamp'], row['close']))

    return trades, profits

# Fetch historical data
symbol = 'ETH/USDT'
timeframe = '1d'
since = int(time.mktime(datetime.datetime(2019, 1, 1).timetuple()) * 1000)
limit = 3000

df = fetch_data(symbol, timeframe, since, limit)
df['sma'] = calculate_sma(df)
df['upper_band'], df['lower_band'] = calculate_bollinger_bands(df, df['sma'])

# Backtest the strategy
trades, profits = backtest_strategy(df)
timestamps = [trade[1] for trade in trades if trade[0] == 'sell']

if len(timestamps) != len(profits):
    raise ValueError("Mismatch in number of sell trades and recorded profits")

# Prepare the dual-axis plot for ETH/USDT with SMA, Bollinger Bands, and Profit Curve
fig, ax1 = plt.subplots(figsize=(15, 8))

color = 'tab:blue'
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('ETH/USDT Price', color=color)
ax1.plot(df['timestamp'], df['close'], label='ETH/USDT', color=color)
ax1.plot(df['timestamp'], df['sma'], label='SMA', color='orange')
ax1.plot(df['timestamp'], df['upper_band'], label='Upper Bollinger Band', color='green')
ax1.plot(df['timestamp'], df['lower_band'], label='Lower Bollinger Band', color='red')
ax1.tick_params(axis='y', labelcolor=color)

# Plot buy and sell signals
for trade in trades:
    if trade[0] == 'buy':
        ax1.scatter(trade[1], trade[2], marker='^', color='green', s=100)
    elif trade[0] == 'sell':
        ax1.scatter(trade[1], trade[2], marker='v', color='red', s=100)

# Instantiate a second axes that shares the same x-axis
ax2 = ax1.twinx()  
color = 'black'
ax2.set_ylabel('Profit in $', color=color)  
ax2.plot(timestamps, profits, label='Profit in $', color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Title and legend
fig.tight_layout()  
plt.title('ETH/USDT with SMA, Bollinger Bands and Profit Curve')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show the plot
plt.show()