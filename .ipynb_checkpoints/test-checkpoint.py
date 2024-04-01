import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
import tushare as ts
import os


def get_data(code='002388',start='2020-1-1',end='2021-1-1'):
    # df=ts.get_k_data(code,autype='qfq',start=start,end=end)
    df = ts.get_k_data(code, autype='qfq', ktype="30",start=start, end=end)
    print(df,111)
    df.index=pd.to_datetime(df.date)
    df['ma']=0.0  #Backtrader需要用到
    df['openinterest'] = 0.0  # Backtrader需要用到
    df=df[['open','high','low','close','volume','openinterest',"ma"]]
    return df
get_data()