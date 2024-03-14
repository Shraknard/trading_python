# Trading bot


## Strategy in use

- Bollinger band
- SMA

Buying when the closing price of the asset is above the SMA and the upper band of the Bollinger Bands, and the difference between the upper and lower bands is greater than 0.


**GPT prompt :**   
Create python script that backtest this strategy on Binance for the ETH/USDT pair. The scrijpt must provide a chart showing the evolution of the profits over time for an initial investment of $1000. The condition for a buy signal are that the closing price of the asset is above the SMA and the upper band of the Bollinger Bands, and the difference between the upper and lower bands is greater than 0. The condition for a sell signal is that the closing price of the asset is below the SMA and the lower band of the Bollinger Bands, and the difference between the upper and lower bands is greater than 0. 










