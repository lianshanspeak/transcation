# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

class AceStrategy(bt.Strategy):
    params = (
        ('maperiod_3', 3),
        ('maperiod_5',5)
    )

    def __init__(self):
        print(f'init___{self.datas[0].datetime.date(0)}')
        self.dataclose = self.datas[0].close
        self.sma_3 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod_3)
        self.sma_5 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod_5)
        self.order = None
        # self.sma_3.plotinfo.plot = False
        # self.sma_5.plotinfo.plot = False

    def start(self):
        pass

    def prenext(self):
        pass

    def nextstart(self):
        pass

    # def notify_order(self, order):
    #     if order.status in [order.Submitted, order.Accepted]:
    #         return
    #     if order.status in [order.Completed]:
    #         pass
    #         self.bar_executed = len(self)
    #     elif order.status in [order.Canceled, order.Margin, order.Rejected]:
    #         pass
    #     self.order = None # 无挂起

    def next(self):
        # if self.order:
        #     return
        if not self.position:
            if self.sma_3[0]>self.sma_5[0]:
                self.order = self.buy(size=1000)
                print(f"{self.datas[0].datetime.date(0)},买入！价格为{self.dataclose[0]}")
        else:
            if self.sma_3[0]<self.sma_5[0]:
                self.order = self.sell(size=1000)
                print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.dataclose[0]}")

    def stop(self):
        pass


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addobserver(bt.observers.Broker)
    # cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.BuySell)
    # cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.Value)
    # cerebro.addobserver(bt.observers.TimeReturn)
    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002342.csv") #本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
    # print(数据地址)
    data =pd.read_csv(数据地址)
    data.index=pd.to_datetime(data.date)
    data.drop(columns=["date"],inplace=True)
    # print(data)
    日线 = bt.feeds.PandasData(     dataname=data,
                                    fromdate=datetime.datetime(2020, 1, 1),
                                    todate=datetime.datetime(2020, 10, 12)
                                    )
    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    cerebro.plot(style = "candle")
