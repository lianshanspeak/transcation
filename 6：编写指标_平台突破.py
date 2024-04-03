# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

class Platform(bt.Indicator):
    # 五日线，最高价，五日线最低价
    lines = ("上轨","下轨")

    def __init__(self):
        self.addminperiod(4)   #5天的平台

    def next(self):
        # -1是昨天，前五天的k线，上轨[0]是数据流中取数
        self.上轨[0]= max(self.data.high.get(ago = -1,size =3))
        self.下轨[0] = min(self.data.low.get(ago=-1, size=3))

class AceStrategy(bt.Strategy):

    def __init__(self):
        self.上下轨 = Platform(self.data)
        self.买入信号 = bt.indicators.CrossOver(self.datas[0].close,self.上下轨.上轨)
        self.卖出信号 = bt.indicators.CrossDown(self.data.close, self.上下轨.下轨)
        # self.order = None
        self.买入信号.plotinfo.plot = False
        self.卖出信号.plotinfo.plot = False
        self.上下轨.plotinfo.plotmaster = self.data  #类似通达信的 是否在主图显示
        # self.卖出信号.plotinfo.plot = False



    def start(self):
        pass

    def prenext(self):
        pass

    def nextstart(self):
        pass

    def next(self):
        # if self.order:
        #     return
        # 没有持仓
        if not self.position:
            if self.买入信号[0] ==1:
                self.order = self.buy(size=200)
                print(f"{self.datas[0].datetime.date(0)},买入！价格为{self.data.close[0]}")
        else:
            if self.卖出信号[0] == 1:
                self.order = self.sell(size=200)
                print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.data.close[0]}")
        pass

    def stop(self):
        if  self.position:
            self.order = self.sell(size=200)
            print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.data.close[0]}")


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(10000.00)  # 设置初始资金金额
    cerebro.broker.setcommission(0.0001)

    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002388.csv") #本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
    # print(数据地址)
    data =pd.read_csv(数据地址)
    data.index=pd.to_datetime(data.date)
    data.drop(columns=["date"],inplace=True)
    print(data)
    日线 = bt.feeds.PandasData(     dataname=data,
                                    fromdate=datetime.datetime(2022, 10, 28),
                                    todate=datetime.datetime(2023, 10, 28)
                                    )
    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    cerebro.plot(style = "candle")
