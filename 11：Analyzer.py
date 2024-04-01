# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime

class stampDutyCommissionScheme(bt.CommInfoBase):
    params = (
        ("印花税",0.001),
        ("commission",0.001)
    )
    def _getcommission(self, size, price, pseudoexec):
        if size>0:
            return size*price*self.p.commission
        elif size<0:
            return abs(size) * (self.p.commission +self.p.印花税)


class AceStrategy(bt.Strategy):
    params = (
        ('三日线周期', 3),
        ('maperiod_5',5)
    )

    def __init__(self):
        # print(f'init___{self.datas[0].datetime.date(0)}')
        self.dataclose = self.data0.close
        self.sma_3 = bt.indicators.SimpleMovingAverage(
            self.dataclose, period=self.params.三日线周期)
        self.sma_5 = bt.indicators.SimpleMovingAverage(
            self.data0.close, period=self.params.maperiod_5)
        self.order = None

        self.买入条件 = bt.indicators.CrossOver(self.sma_3,self.sma_5)
        self.卖出条件 = bt.indicators.CrossDown(self.sma_3,self.sma_5)
        self.买入条件.plotinfo.plot = False
        self.卖出条件.plotinfo.plot = False

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
            if self.买入条件>0:
                self.order = self.buy(size=1000)
            # if self.sma_3[0]>self.sma_5[0]:
            #     self.order = self.buy(size=1000)
                print(f"{self.datas[0].datetime.date(0)},买入！价格为{self.dataclose[0]}")
        else:
            if self.卖出条件 >0:
                self.order = self.sell(size=1000)
            # if self.sma_3[0]<self.sma_5[0]:
            #     self.order = self.sell(size=1000)
                print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.dataclose[0]}")

    def stop(self):
        pass


if __name__ == '__main__':
    # cerebro = bt.Cerebro()
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    cerebro.broker.setcommission(0.01)
    # cerebro.addobserver(bt.observers.Broker)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.BuySell)
    # cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.Value)

    # cerebro.addobserver(bt.observers.TimeReturn)
    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"002342.csv")
    # print(数据地址)
    data =pd.read_csv(数据地址)
    data.index=pd.to_datetime(data.date)
    data.drop(columns=["date"],inplace=True)
    # print(data)
    日线 = bt.feeds.PandasData(     dataname=data,
                                    fromdate=datetime.datetime(2000, 1, 1),
                                    todate=datetime.datetime(2020, 10, 30)
                                    )
    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio,riskfreerate=0.02,annualize = True ,_name="夏普比率")
    cerebro.addanalyzer(bt.analyzers.DrawDown,  _name="回撤")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)

    策略分析汇总 = cerebro.run()
    策略_1 = 策略分析汇总[0]
    # print(f"夏普比率:{策略_1.analyzers.夏普比率.get_analysis()['sharperatio']}")
    # print(f"最大回撤:{策略_1.analyzers.回撤.get_analysis()}")
    # for 信息 in 策略_1.analyzers:
    #     信息.print()
    cerebro.addwriter(bt.WriterFile,rounding = 2)

    期末资金 =  cerebro.broker.getvalue()


    print(f'期末资金:{期末资金}')
    cerebro.plot(style = "candle")
