# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime


class AceStrategy(bt.Strategy):
    params = (
        ('maperiod',20),
    )

    def log(self):
        pass


    def __init__(self):
        print(f'init___{self.datas[0].datetime.date(0)}')
        # self.dataclose = self.datas[0].close
        self.sma_5 = bt.indicators.SimpleMovingAverage(
            self.data0.close, period=self.params.maperiod)


    def start(self):
        print(f"start!___{self.datas[0].datetime.date(0)}")

    def prenext(self):
        print(f"prenext___{self.datas[0].datetime.date(0)}")

    def nextstart(self):
        print(f'nextstart___{self.datas[0].datetime.date(0)}')

    def notify_order(self):
        pass

    def notify_trade(self):
        pass


    def next(self):
        print(f'next___{self.datas[0].datetime.date(0)}, ma_5:{round(self.sma_5[0],2)}, 前一天MA_5:{round(self.sma_5[-1],2)}')

    def stop(self):
        print(f"stop___{self.datas[0].datetime.date(0)}")


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002388.csv") #本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
    print(数据地址)
    data =pd.read_csv(数据地址)
    data.index=pd.to_datetime(data.date)
    data.drop(columns=["date"],inplace=True)
    print(data)
    日线 = bt.feeds.PandasData(     dataname=data,
                                    fromdate=datetime.datetime(2022, 10, 28),
                                    todate=datetime.datetime(2023, 10, 20)
                                    )
    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    cerebro.plot()
