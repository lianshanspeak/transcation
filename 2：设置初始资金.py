import backtrader as bt
if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000.00)    # 设置初始资金金额
    初始资金 = cerebro.broker.getvalue()
    print(f'初始资金:{初始资金}')
    cerebro.run()
    期末资金 =  cerebro.broker.getvalue()
    print(f'期末资金:{期末资金}')



