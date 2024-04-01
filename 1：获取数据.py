import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
import tushare as ts
import os


# ts.set_token('680e3143516bf465904de3818dbdaa996cb4a9e7656c9b291a148db4')

def get_data(code='002388',start='2020-1-1',end='2021-1-1'):
    df=ts.get_k_data(code,autype='qfq',start=start,end=end)
    # df = ts.get_k_data(code, autype='qfq', ktype="30",start=start, end=end)
    # print(df,111)
    df.index=pd.to_datetime(df.date)
    df['ma']=0.0  #Backtrader需要用到
    df['openinterest'] = 0.0  # Backtrader需要用到
    df=df[['open','high','low','close','volume','openinterest',"ma"]]
    return df
# get_data()
def acquire_code():   #只下载一只股票数据，且只用CSV保存   未来可以有自己的数据库
    inp_code =input("请输入股票代码:\n")
    inp_start = input("请输入开始时间:\n")
    inp_end = input("请输入结束时间:\n")
    df = get_data(inp_code,inp_start,inp_end)
    print(df.info())
    print("—"*30)
    print(df.describe())

    path = os.path.join(os.path.join(os.getcwd(),"数据地址"),inp_code+".csv")
    # path = os.path.join(os.path.join(os.getcwd(),"数据地址"),inp_code+"_30M.csv")
    df.to_csv(path  )

acquire_code()
