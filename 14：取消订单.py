# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

class Acecommission(bt.CommInfoBase):
    params = (
        ("印花税",0.001),
        ("commission",0.001)
    )
    def _getcommission(self, size, price, pseudoexec):
        if size>0:
            return max(size*price*self.p.commission*100,5)
            # return size * price * self.p.commission
        elif size<0:
            return  abs(size) * price*self.p.印花税 +  max(abs(size)*price*self.p.commission*100,5)
            # return abs(size) * price * self.p.印花税


class AceDataframe(bt.feeds.PandasData):
    lines = ("三十分钟买点日线支撑",)
    params = (
        ("三十分钟买点日线支撑",10),
    )


class AceStrategy(bt.Strategy):

    def __init__(self):
        self.dic = dict()   #用于辨别code
        for i ,d in enumerate(self.datas):
            self.dic[d] = dict()
            self.dic[d]["三十分钟买点日线支撑"] = d.三十分钟买点日线支撑
            self.dic[d]["买入价"]=0
            self.dic[d]["卖出价"]=0
            self.dic[d]["order"] = None
            # self.dic[d]["orderstatus"]=[]




            # self.dic[d].order = None
            # self.dic[d].买点买价 = 0.0
            # self.dic[d].买点触发 = 0.0


    def start(self):
        pass

    def prenext(self):
        self.next()

    def nextstart(self):
        pass

    def notify_order(self, order):


        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"已经买入.价格为{order.executed.price}\n市值：{order.executed.value}\n佣金:{order.executed.comm}\n{self.datetime.datetime()}\n")
                self.买入价 = order.executed.price
                self.佣金 = order.executed.comm

            elif order.issell():
                print(f"已经卖出.价格为{order.executed.price}\n费用：{order.executed.value}\n佣金:{order.executed.comm}\n{self.datetime.datetime()}\n")
            self.bar_executed = len(self)

        # elif order.status in [order.Canceled, order.Margin, order.Rejected]
        elif order.status in [order.Canceled]:
            print("订单取消\n")

        elif order.status in [order.Margin]:
            print("订单超时\n")

        elif order.status in [order.Rejected]:
            print("订单拒绝\n")

        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            print(f"毛收益：{round(trade.pnl, 2)}......佣金：{round(trade.commission, 2)}......收益:{round(trade.pnlcomm,2)}\n\n\n")



    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.datetime(), d._name           # 获取时间及股票代码
            pos = self.getposition(d).size
            if not pos:
                if self.dic[d]['三十分钟买点日线支撑'][0]>0:
                    if d.close[0] >= self.dic[d]['三十分钟买点日线支撑'][0]:
                        self.dic[d]["买入价"] = self.dic[d]['三十分钟买点日线支撑'][0]
                        validday = dt+datetime.timedelta(days=3)
                        self.dic[d]["order"]=self.cancel(self.dic[d]["order"])
                        self.dic[d]["order"]  = self.buy(exectype=bt.Order.Limit,data=d, size=1000,price=self.dic[d]["买入价"],valid=validday)

                        self.dic[d]["卖出价"]=self.dic[d]["买入价"]

                        print(dt, dn)
            #
            elif pos >0:
                if  self.dic[d]["卖出价"]*1.05<=d.close[0] or  self.dic[d]["卖出价"]*0.98>=d.close[0]:
                    self.order = self.close()
                    self.dic[d]["买入价"] = 0




            #
            # elif pos<0:
            #     pass
            #     self.order = self.sell(data = d,size=1000)



    def stop(self):
        pass
        # for i, d in enumerate(self.datas):
        #     dt, dn = self.datetime.datetime(), d._name  # 获取时间及股票代码
        #     pos = self.getposition(d).size
        #     if  pos>0:
        #         self.order = self.close()
        #         print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.data.close[0]}")


if __name__ == '__main__':
    cerebro = bt.Cerebro(stdstats = False)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.Value)
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    cerebro.broker.addcommissioninfo(Acecommission(印花税=0.001,commission = 0.00025))
    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')

    股票池 = [ os.path.join(r"D:\股票数据\三十支撑",i) for i in os.listdir(r"D:\股票数据\三十支撑") ]
    for i in range(len(股票池)):
        stk_code = 股票池[i].split("\\")[-1].split("_")[0]
        data = pd.read_csv(股票池[i], index_col="date", parse_dates=True)
        三十分钟线 = AceDataframe(dataname=data,
                                 fromdate=datetime.datetime(2019, 1, 1),
                                 todate=datetime.datetime(2020, 11, 30),
                                 timeframe = bt.TimeFrame.Minutes,

                                 )
        cerebro.adddata(三十分钟线, name=stk_code)
    cerebro.addstrategy(AceStrategy)
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    # cerebro.plot(style = "candle")
