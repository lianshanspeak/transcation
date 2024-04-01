# -*- coding:utf-8 -*-
import backtrader as bt
#####################
import pandas as pd
import os
import datetime

class Acecommission(bt.CommInfoBase):
    params = (
        ("印花税",0.001),
        ("commission",0.00025),
    )
    def _getcommission(self, size, price, pseudoexec):
        if size > 0:
            return max(size*price*self.params.commission*100,5)
        elif size<0:
            return abs(size)*price*self.params.印花税 + max(size*price*self.params.commission*100,5)



class AceStrategy(bt.Strategy):
    params = (
        ('三日线周期', 3),
        ('五日线周期',5)
    )

    def __init__(self):
        self.dataclose = self.data0.close
        self.sma_3 = bt.indicators.SimpleMovingAverage(
            self.dataclose, period=self.params.三日线周期)
        self.sma_5 = bt.indicators.SimpleMovingAverage(
            self.data0.close, period=self.params.五日线周期)
        self.order = None

        self.买入条件 = bt.indicators.CrossOver(self.sma_3,self.sma_5)
        self.卖出条件 = bt.indicators.CrossDown(self.sma_3,self.sma_5)
        self.买入条件.plotinfo.plot = False
        self.卖出条件.plotinfo.plot = False

        self.order = None
        self.买入价 =None
        self.佣金 = None
        self.盈利_list=[]


    def start(self):
        pass

    def prenext(self):
        print("prenext")
        self.next()    #如果不写  会比最小周期多1个bar  或者直接覆盖也没关系

    def nextstart(self):
        pass

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"已经买入.价格为{order.executed.price}\n市值：{order.executed.value}\n佣金:{order.executed.comm}")
                self.买入价 = order.executed.price
                self.佣金 = order.executed.comm

            elif order.issell():
                print(f"已经卖出.价格为{order.executed.price}\n费用：{order.executed.value}\n佣金:{order.executed.comm}\n")
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
            print(f"毛收益：{round(trade.pnl,2)}......佣金：{round(trade.commission,2)}......收益:{round(trade.pnlcomm,2)}\n\n\n")
            self.盈利_list.append(round(trade.pnlcomm,2))


    def next(self):
        # if self.order:
        #     return
        if not self.position:
            if self.买入条件>0:
                self.order = self.buy(exectype=bt.Order.StopLimit,price=self.data0.close[-1],plimit=self.data0.close[-1]*0.98,size=100)
            # if self.sma_3[0]>self.sma_5[0]:
            #     self.order = self.buy(size=1000)
                print(f"{self.datas[0].datetime.date(0)},触发买入！收盘价格为{self.dataclose[0]}")
        else:
            if self.卖出条件 >0:
                self.order = self.sell(size=100)
            # if self.sma_3[0]<self.sma_5[0]:
            #     self.order = self.sell(size=1000)
                print(f"{self.datas[0].datetime.date(0)},触发卖出！收盘价格为{self.dataclose[0]}")

    def stop(self):
        print(f"总共交易了{len(self.盈利_list)}笔 ,收益损失详情如下:{self.盈利_list}\n")
        # for i in self._trades[self.data0][0]:
        #     print(f"{i.close_datetime()}毛利率：{i.pnl}")


if __name__ == '__main__':
    # cerebro = bt.Cerebro()
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.set_cash(100000.00)  # 设置初始资金金额
    cerebro.broker.addcommissioninfo(Acecommission(印花税=0.01,commission = 0.00025))
    # cerebro.broker.setcommission(0.00025)
    # cerebro.addobserver(bt.observers.Broker)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.BuySell)
    # cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.Value)

    # cerebro.addobserver(bt.observers.TimeReturn)
    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    数据地址= os.path.join(os.path.join(os.getcwd(),"数据地址"),"300579.csv")
    # print(数据地址)
    data =pd.read_csv(数据地址,index_col = "trade_date",parse_dates = True)
    data.rename(columns={"vol":"volume"},inplace=True)
    # data["date"] = data["date"].map(lambda x: pd.to_datetime(str(x)).strftime("%Y-%m-%d"))
    # data["date"] = data["date"].map(lambda x: pd.to_datetime(str(x)).strftime("%Y-%m-%d"))
    # data.index=pd.to_datetime(data.date)
    # data.drop(columns=["date"],inplace=True)
    # print(data)
    日线 = bt.feeds.PandasData(     dataname=data,
                                    fromdate=datetime.datetime(2019, 11, 1),
                                    todate=datetime.datetime(2020, 10, 30)
                                    )
    cerebro.adddata(日线)
    cerebro.addstrategy(AceStrategy)
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')
    # cerebro.plot(style = "candle")
    cerebro.plot()
