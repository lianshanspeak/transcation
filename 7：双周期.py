import backtrader as bt
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHer']

class Platform(bt.Indicator):
    lines = ("上轨","下轨")
    params = (
        ("周期" , 5),
    )

    def __init__(self):
        self.addminperiod(self.params.周期 + 1)


    def next(self):
        self.上轨[0] = max(self.data.high.get(ago=-1, size=self.params.周期))
        self.下轨[0] = min(self.data.low.get(ago=-1, size=self.params.周期))

class AceStrategy(bt.Strategy):
    params = (
        ("周期", 5),
    )

    def __init__(self):
        self.上下轨 = Platform(self.data1 ,周期= self.params.周期)
        self.上下轨 = self.上下轨()
        self.上下轨.plotinfo.plotmaster = self.data0

        self.买入信号 = bt.indicators.CrossOver(self.data0.close,self.上下轨.上轨)
        self.卖出信号 = bt.indicators.CrossDown(self.data0.close,self.上下轨.下轨)
        self.买入信号.plotinfo.plot = False
        self.卖出信号.plotinfo.plot = False



    def start(self):
        pass

    def prenext(self):
        print(f'数据准备时间：{self.data0.datetime.datetime(0)}')

    def nextstart(self):
        pass

    def next(self):
        # # if self.order:
        # #     return
        if not self.position:
            if self.买入信号[0] ==1:
                self.order = self.buy(size=1000)
                print(f"{self.data1.datetime.date(0)},买入！价格为{self.data0.close[0]}")
        else:
            if self.卖出信号[0] == 1:
                self.order = self.sell(size=1000)
                print(f"{self.data1.datetime.date(0)},卖出！价格为{self.data0.close[0]}")
        # pass

    def stop(self):
        if  self.position:
            self.order = self.sell(size=1000)
            print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.data.close[0]},最终数据{cerebro.broker.getvalue()}")


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000.0)
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002388.csv")
    data = pd.read_csv(数据地址,index_col = "date",parse_dates=True)
    print(data)
    三十分钟线 = bt.feeds.PandasData(dataname=data,
                                fromdate = datetime.datetime(2022,3,1),
                                todate = datetime.datetime(2023,10,16),
                                timeframe = bt.TimeFrame.Minutes,
                                compression = 30
                             )
    cerebro.adddata(三十分钟线) #self.data
    cerebro.resampledata(三十分钟线,timeframe = bt.TimeFrame.Days)   #self.data1
    cerebro.addstrategy(AceStrategy)

    cerebro.run()
    期末资金 = cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    cerebro.plot(style = "candle")
