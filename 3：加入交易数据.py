# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

#####################



class AceStrategy(bt.Strategy):
    pass

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro = bt.Cerebro(stdstats=False)
    # cerebro.addobserver(bt.observers.Broker)
    # cerebro.addobserver(bt.observers.Trades)
    # cerebro.addobserver(bt.observers.BuySell)
    # cerebro.addobserver(bt.observers.DrawDown)
    # cerebro.addobserver(bt.observers.Value)
    # cerebro.addobserver(bt.observers.TimeReturn)
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')


    #####################
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002342.csv") #本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
    # print(数据地址)
    data =pd.read_csv(数据地址,index_col ="date",parse_dates = True)
    # data.index=pd.to_datetime(data.date)
    # data.drop(columns=["date"],inplace=True)
    # print(data)
    日线 = bt.feeds.PandasData(     dataname=data,
                                    fromdate=datetime.datetime(2020, 1, 1),
                                    todate=datetime.datetime(2020,10, 18)
                                    )


    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)
    #####################
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    #####################
    cerebro.plot(style = "candle")
    #####################

