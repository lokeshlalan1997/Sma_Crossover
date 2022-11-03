# Crossover_Strategy

The Python code you provided is designed to simulate an automated trading strategy using Backtrader, a popular library for algorithmic trading. Specifically, the strategy revolves around a common technical analysis concept known as moving average crossovers.

In simpler terms, the strategy looks at two types of average prices (called moving averages) calculated over different time periods. When the short-term average crosses above the long-term average, it suggests a potential opportunity to buy a financial instrument. Conversely, when the short-term average crosses below the long-term average, it signals a potential opportunity to sell.

The script not only defines this strategy but also sets up a simulated environment to test how well it would have performed in the past. It uses historical stock price data to mimic the buying and selling decisions the strategy would have made over time. The results, including the starting and ending values of the simulated portfolio, are printed for analysis.

Keep in mind that this script is a starting point for creating and testing trading strategies, and its success in real-world scenarios would depend on various factors, including market conditions and risk management.

### Importing Libraries

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C10.8954 4 10 4.89543 10 6H14C14 4.89543 13.1046 4 12 4ZM8.53513 4C9.22675 2.8044 10.5194 2 12 2C13.4806 2 14.7733 2.8044 15.4649 4H17C18.6569 4 20 5.34315 20 7V19C20 20.6569 18.6569 22 17 22H7C5.34315 22 4 20.6569 4 19V7C4 5.34315 5.34315 4 7 4H8.53513ZM8 6H7C6.44772 6 6 6.44772 6 7V19C6 19.5523 6.44772 20 7 20H17C17.5523 20 18 19.5523 18 19V7C18 6.44772 17.5523 6 17 6H16C16 7.10457 15.1046 8 14 8H10C8.89543 8 8 7.10457 8 6Z" fill="currentColor"></path></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">import backtrader as bt
import pandas as pd
from pytz import timezone
</code></div></div></pre>

* `backtrader`: This is a popular Python library for developing and testing algorithmic trading strategies.
* `pandas`: Used for handling and manipulating the stock data, which is read from a CSV file.
* `pytz`: Handles time zones.

### Defining the Strategy Class

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C10.8954 4 10 4.89543 10 6H14C14 4.89543 13.1046 4 12 4ZM8.53513 4C9.22675 2.8044 10.5194 2 12 2C13.4806 2 14.7733 2.8044 15.4649 4H17C18.6569 4 20 5.34315 20 7V19C20 20.6569 18.6569 22 17 22H7C5.34315 22 4 20.6569 4 19V7C4 5.34315 5.34315 4 7 4H8.53513ZM8 6H7C6.44772 6 6 6.44772 6 7V19C6 19.5523 6.44772 20 7 20H17C17.5523 20 18 19.5523 18 19V7C18 6.44772 17.5523 6 17 6H16C16 7.10457 15.1046 8 14 8H10C8.89543 8 8 7.10457 8 6Z" fill="currentColor"></path></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">class MyStrategy(bt.Strategy):
    params = (
        ('sma_period1', 9),
        ('sma_period3', 40),
    )
</code></div></div></pre>

* `MyStrategy`: This class inherits from `bt.Strategy` and defines the trading strategy. It uses two simple moving averages (SMAs) with periods specified in the parameters.
* `params`: This is a tuple of strategy parameters, including the periods for the two SMAs.

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C10.8954 4 10 4.89543 10 6H14C14 4.89543 13.1046 4 12 4ZM8.53513 4C9.22675 2.8044 10.5194 2 12 2C13.4806 2 14.7733 2.8044 15.4649 4H17C18.6569 4 20 5.34315 20 7V19C20 20.6569 18.6569 22 17 22H7C5.34315 22 4 20.6569 4 19V7C4 5.34315 5.34315 4 7 4H8.53513ZM8 6H7C6.44772 6 6 6.44772 6 7V19C6 19.5523 6.44772 20 7 20H17C17.5523 20 18 19.5523 18 19V7C18 6.44772 17.5523 6 17 6H16C16 7.10457 15.1046 8 14 8H10C8.89543 8 8 7.10457 8 6Z" fill="currentColor"></path></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">    def __init__(self):
        self.sma1 = bt.indicators.SMA(self.data, period=self.params.sma_period1)
        self.sma3 = bt.indicators.SMA(self.data, period=self.params.sma_period3)
        self.smabuy = bt.indicators.CrossUp(self.sma1, self.sma3)
        self.smasell = bt.indicators.CrossDown(self.sma3, self.sma1)

        self.trading_signals = []
</code></div></div></pre>

* `__init__`: This method is called when an instance of the strategy is created. It initializes the strategy by creating instances of SMAs and crossover indicators.
* `self.sma1` and `self.sma3`: These are SMAs based on the closing prices of the stock data.
* `self.smabuy` and `self.smasell`: These are crossover indicators. They become `True` when there is a crossover (upward or downward) between the two SMAs.
* `self.trading_signals`: This is a list to store information about trading signals (buy/sell orders).

        dt = self.data.datetime.datetime()
        if not self.position:
            if self.smabuy:
                # ... Buy logic
        else:
            if self.position.size > 0:
                if self.smasell:
                    # ... Sell logic
</code></div></div></pre>

* `next`: This method is called for each new data point in the time series.
* Inside `next`, it checks if there is no existing position. If true, it checks for a buy signal (`self.smabuy`). If a buy signal is detected, it executes a buy order.
* If there is an existing long position (`self.position.size > 0`), it checks for a sell signal (`self.smasell`). If a sell signal is detected, it executes a sell order.

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C10.8954 4 10 4.89543 10 6H14C14 4.89543 13.1046 4 12 4ZM8.53513 4C9.22675 2.8044 10.5194 2 12 2C13.4806 2 14.7733 2.8044 15.4649 4H17C18.6569 4 20 5.34315 20 7V19C20 20.6569 18.6569 22 17 22H7C5.34315 22 4 20.6569 4 19V7C4 5.34315 5.34315 4 7 4H8.53513ZM8 6H7C6.44772 6 6 6.44772 6 7V19C6 19.5523 6.44772 20 7 20H17C17.5523 20 18 19.5523 18 19V7C18 6.44772 17.5523 6 17 6H16C16 7.10457 15.1046 8 14 8H10C8.89543 8 8 7.10457 8 6Z" fill="currentColor"></path></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">        df_trading = pd.DataFrame(self.trading_signals)
        df_trading.to_csv('trading.csv', index=False)
</code></div></div></pre>

* After each iteration, it saves the trading signals to a CSV file named 'trading.csv'. As mentioned earlier, this can be resource-intensive and might be better placed in the `stop` method.

### Loading CSV Data and Setting Up Backtrader

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C10.8954 4 10 4.89543 10 6H14C14 4.89543 13.1046 4 12 4ZM8.53513 4C9.22675 2.8044 10.5194 2 12 2C13.4806 2 14.7733 2.8044 15.4649 4H17C18.6569 4 20 5.34315 20 7V19C20 20.6569 18.6569 22 17 22H7C5.34315 22 4 20.6569 4 19V7C4 5.34315 5.34315 4 7 4H8.53513ZM8 6H7C6.44772 6 6 6.44772 6 7V19C6 19.5523 6.44772 20 7 20H17C17.5523 20 18 19.5523 18 19V7C18 6.44772 17.5523 6 17 6H16C16 7.10457 15.1046 8 14 8H10C8.89543 8 8 7.10457 8 6Z" fill="currentColor"></path></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">data = pd.read_csv('/Users/lokeshlalan/PycharmProjects/Crossover/Data/tata_motors_data.csv', parse_dates=True, index_col='Timestamp')
data = bt.feeds.PandasData(dataname=data, tz=timezone('Asia/Kolkata'))
</code></div></div></pre>

* Reads historical stock data from a CSV file into a Pandas DataFrame.
* Creates a Backtrader data feed (`bt.feeds.PandasData`) from the Pandas DataFrame.

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C10.8954 4 10 4.89543 10 6H14C14 4.89543 13.1046 4 12 4ZM8.53513 4C9.22675 2.8044 10.5194 2 12 2C13.4806 2 14.7733 2.8044 15.4649 4H17C18.6569 4 20 5.34315 20 7V19C20 20.6569 18.6569 22 17 22H7C5.34315 22 4 20.6569 4 19V7C4 5.34315 5.34315 4 7 4H8.53513ZM8 6H7C6.44772 6 6 6.44772 6 7V19C6 19.5523 6.44772 20 7 20H17C17.5523 20 18 19.5523 18 19V7C18 6.44772 17.5523 6 17 6H16C16 7.10457 15.1046 8 14 8H10C8.89543 8 8 7.10457 8 6Z" fill="currentColor"></path></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">cerebro = bt.Cerebro()
startcash = 100000
cerebro.addsizer(bt.sizers.SizerFix, stake=25)
cerebro.addstrategy(MyStrategy)
cerebro.adddata(data)
cerebro.broker.set_cash(startcash)
cerebro.broker.setcommission(commission=0.002)  # 0.2% commission
</code></div></div></pre>

* Creates a `Cerebro` engine, the main component of Backtrader.
* Sets the initial cash amount for the portfolio (`startcash`).
* Adds a fixed-size sizer and the custom strategy (`MyStrategy`) to the engine.
* Adds the data feed to the engine.
* Sets the initial cash for the broker and specifies the commission for buying/selling.

### Running the Backtest

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex gap-1 items-center"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 4C10.8954 4 10 4.89543 10 6H14C14 4.89543 13.1046 4 12 4ZM8.53513 4C9.22675 2.8044 10.5194 2 12 2C13.4806 2 14.7733 2.8044 15.4649 4H17C18.6569 4 20 5.34315 20 7V19C20 20.6569 18.6569 22 17 22H7C5.34315 22 4 20.6569 4 19V7C4 5.34315 5.34315 4 7 4H8.53513ZM8 6H7C6.44772 6 6 6.44772 6 7V19C6 19.5523 6.44772 20 7 20H17C17.5523 20 18 19.5523 18 19V7C18 6.44772 17.5523 6 17 6H16C16 7.10457 15.1046 8 14 8H10C8.89543 8 8 7.10457 8 6Z" fill="currentColor"></path></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
</code></div></div></pre>

* Prints the starting portfolio value.
* Runs the backtest using `cerebro.run()`.
* Prints the ending portfolio value.

### Conclusion

This script sets up a Backtrader environment, defines a simple moving average crossover strategy, loads historical stock data, runs the backtest, and prints the starting and ending portfolio values. It also saves trading signals to a CSV file after each iteration. Remember to customize file paths, experiment with parameters, and thoroughly test before deploying any trading strategy.
