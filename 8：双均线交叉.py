# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

class AceStrategy(bt.Strategy):
    params = (
        ('周期1',5),
        ('周期2', 20),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.sma_5 = bt.indicators.SimpleMovingAverage(
            self.dataclose, period=self.params.周期1)
        self.sma_60 = bt.indicators.SimpleMovingAverage(self.dataclose, period=self.params.周期2)

        self.买入信号 = bt.indicators.CrossOver(self.sma_5,self.sma_60)
        self.卖出信号 = bt.indicators.CrossDown(self.sma_5, self.sma_60)
        self.买入信号.plotinfo.plot = False
        self.卖出信号.plotinfo.plot = False


    def start(self):
        pass
        # print(f"start!___{self.datas[0].datetime.date(0)}")


    def prenext(self):
        pass
        # print(f"prenext___{self.datas[0].datetime.date(0)}")

    def nextstart(self):
        pass
        # print(f'nextstart___{self.datas[0].datetime.date(0)}')

    def next(self):
        if not self.position:
            if self.买入信号[0] > 0:
                self.order = self.buy()
                print(f"{self.data0.datetime.date(0)},买入！价格为{self.data0.close[0]}")
        else:
            if self.卖出信号[0] > 0:
                self.order = self.sell()
                print(f"{self.data0.datetime.date(0)},卖出！价格为{self.data0.close[0]}")

    def stop(self):
        print(f"stop___{self.datas[0].datetime.date(0)}")


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    cerebro.broker.setcommission(commission=0.0003)
    cerebro = bt.Cerebro(stdstats=False)
    # cerebro.addobserver(bt.observers.Broker)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.BuySell)
    # cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.Value)
    # cerebro.addobserver(bt.observers.TimeReturn)

    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002342.csv") #本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
    # print(数据地址)
    data =pd.read_csv(数据地址,index_col = "date",parse_dates = True)
    日线 = bt.feeds.PandasData(     dataname=data,
                                    fromdate=datetime.datetime(2018, 9, 10),
                                    todate=datetime.datetime(2020, 10, 12)
                                    )
    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    cerebro.plot()
