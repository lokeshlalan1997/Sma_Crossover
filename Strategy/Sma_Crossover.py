# import backtrader as bt
# from datetime import datetime
# import pandas as pd
#
# class MyStrategy(bt.Strategy):
#     params = (
#         ('sma_period1', 9),
#         ('sma_period3', 40),
#     )
#
#     def __init__(self):
#         self.sma1 = bt.indicators.SMA(self.data, period=self.params.sma_period1)
#         self.sma3 = bt.indicators.SMA(self.data, period=self.params.sma_period3)
#         self.smabuy = bt.indicators.CrossUp(self.sma1, self.sma3)
#         self.smasell = bt.indicators.CrossDown(self.sma3, self.sma1)
#
#     def next(self):
#         if not self.position:
#             if self.smabuy:
#                 self.buy(size=25)
#                 print("Buy", self.position.size)
#         else:
#             if self.position.size > 0:
#                 if self.smasell:
#                     self.sell(size=25)
#                     print("Sell", self.position.size)
#
# # Load CSV data
# data = pd.read_csv('/Users/lokeshlalan/PycharmProjects/Crossover/Data/tata_motors_data.csv', parse_dates=True, index_col='Timestamp')
# data = bt.feeds.PandasData(dataname=data)
#
# cerebro = bt.Cerebro()
# startcash = 100000
# cerebro.addsizer(bt.sizers.SizerFix, stake=25)
# cerebro.addstrategy(MyStrategy)
# cerebro.adddata(data)
# cerebro.broker.set_cash(startcash)
# cerebro.broker.setcommission(commission=0.002)  # 0.2% commission
#
# print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.run()
# print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.plot(style='candlestick')


import backtrader as bt
import pandas as pd
from pytz import timezone


class MyStrategy(bt.Strategy):
    params = (
        ('sma_period1', 9),
        ('sma_period3', 40),
    )

    def __init__(self):
        self.sma1 = bt.indicators.SMA(self.data, period=self.params.sma_period1)
        self.sma3 = bt.indicators.SMA(self.data, period=self.params.sma_period3)
        self.smabuy = bt.indicators.CrossUp(self.sma1, self.sma3)
        self.smasell = bt.indicators.CrossDown(self.sma3, self.sma1)

        self.trading_signals = []

    def next(self):
        dt = self.data.datetime.datetime()
        # if not self.position:
        #     if self.smabuy:
        #         buy_size = 50
        #         self.buy(size=buy_size)
        #         print("Buy", buy_size)
        #         self.trading_signals.append({'datetime': dt, 'action': 'Buy','price': self.data.close[0], 'size': buy_size})
        # else:
        #     if self.position.size > 0:
        #         if self.smasell:
        #             sell_size = 50
        #             self.sell(size=sell_size)
        #             print("Sell", sell_size)
        #             self.trading_signals.append({'datetime': dt, 'action': 'Sell','price': self.data.close[0], 'size': sell_size})
        # # strategy_instance = cerebro.runstrats[0]
        # df_trading = pd.DataFrame(self.trading_signals)
        # df_trading.to_csv('trading.csv', index=False)
        if not self.position:
            if self.smabuy:
                buy_size = 50
                entry_price = self.data.close[0]
                self.buy(size=buy_size)
                print(f"Buy - Time: {dt}, Price: {entry_price}, Size: {buy_size}")
                self.trading_signals.append(
                    {'entry_time': dt, 'entry_price': entry_price, 'exit_time': None, 'exit_price': None,
                     'size': buy_size})
        else:
            if self.position.size > 0:
                if self.smasell:
                    sell_size = 50
                    exit_price = self.data.close[0]
                    self.sell(size=sell_size)
                    print(f"Sell - Time: {dt}, Price: {exit_price}, Size: {sell_size}")
                    self.trading_signals[-1]['exit_time'] = dt
                    self.trading_signals[-1]['exit_price'] = exit_price

            # Save trading signals to CSV after each iteration
        df_trading = pd.DataFrame(self.trading_signals)
        df_trading.to_csv('trading.csv', index=False)

# Load CSV data
data = pd.read_csv('/Users/lokeshlalan/PycharmProjects/Crossover/Data/tata_motors_data.csv', parse_dates=True, index_col='Timestamp')
data = bt.feeds.PandasData(dataname=data, tz=timezone('Asia/Kolkata'))

cerebro = bt.Cerebro()
startcash = 100000
cerebro.addsizer(bt.sizers.SizerFix, stake=25)
cerebro.addstrategy(MyStrategy)
cerebro.adddata(data)
cerebro.broker.set_cash(startcash)
cerebro.broker.setcommission(commission=0.002)  # 0.2% commission

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
