import backtrader as bt
#####################
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

class AcePandasData(bt.feeds.PandasData):
    lines = ("ma_5","ma_10","ma_20")
    params = (
        ("ma_5",6),
        ("ma_10",7),
        ("ma_20", 8),
    )


class AceStrategy(bt.Strategy):


    def __init__(self):
        self.ma_5 = self.datas[0].ma_5
        self.ma_10 = self.data0.ma_10
        self.ma_20 = self.data0.ma_20
        # self.买入信号 = bt.indicators.CrossOver(self.ma_5,self.ma_10)
        # self.卖出信号 = bt.indicators.CrossDown(self.ma_5, self.ma_10)



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
        print(self.data0.datetime.date(0),self.data0.ma_5[0])
        print(f"日期：{self.data0.datetime.date(0)},   5日线:{self.data0.ma_5[0]}   ,  10日线:{self.data0.ma_10[0]} ,  20日线:{self.data0.ma_20[0]} ")


        # print(self.data0.datetime.date(0),self.data0.ma_5[0])
        # print(self.data0.datetime.date(0), self.ma_5[0])
        # print(self.data0.datetime.date(0),self.ma_20[0])
        # if not self.position:
        #     if self.买入信号[0] > 0:
        #         self.order = self.buy()
        #         print(f"{self.data0.datetime.date(0)},买入！价格为{self.data0.close[0]}")
        # else:
        #     if self.卖出信号[0] > 0:
        #         self.order = self.sell()
        #         print(f"{self.data0.datetime.date(0)},卖出！价格为{self.data0.close[0]}")

    def stop(self):
        print(f"stop___{self.datas[0].datetime.date(0)}")

if __name__ == '__main__':
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    cerebro.broker.setcommission(commission=0.0003)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.Value)

    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002342_.csv") #本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
    # print(数据地址)
    data =pd.read_csv(数据地址,index_col = "date",parse_dates = True)
    # 日线 = bt.feeds.PandasData(             dataname=data,
    #                                 fromdate=datetime.datetime(2018, 9, 10),
    #                                 todate=datetime.datetime(2020, 10, 11)
    #                                 )
    日线 = AcePandasData(             dataname=data,
                                    fromdate=datetime.datetime(2018, 9, 10),
                                    todate=datetime.datetime(2020, 10, 19)
                                    )
    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    cerebro.plot()