# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd 
import numpy as np 
import talib as tb 
import datetime

os.chdir(r"E:\量化\ACE_backtrader\ACE量化回测学习\数据地址")

#SMA(X,N,M)，求X的N日移动平均，M为权重。算法：若Y=SMA(X,N,M) 则 Y=(M*X+(N-M)*Y')/N，其中Y'表示上一周期Y值，N必须大于M

def ace_sma(df,lb,n,m,倍数=1):
    df_1 = df.copy()
    value_list=[]
    close_list = df_1[str(lb)].to_list()
    for i in range(len(df_1)):
        if i < n:
            Y=sum(close_list[:i+1])/(i+1)
            value_list.append(Y)
        else:
            Y = (m*close_list[i] +(n-m)*value_list[i-1])/n
            value_list.append(Y)
    value_list = [i * 倍数 for i in value_list]
    name = "SMA_"+str(lb)+"_" +str(n)
    df_1[name] = value_list
    df_1 = df_1[[name]]
    df_2 = pd.merge(df,df_1,left_index = True,right_index = True,how="left")
    return df_2
                    
            

if __name__ == '__main__':
    data = pd.read_csv("002342.csv",index_col = "date",parse_dates = True)
    
    周期 = [5,10,20]
    for i in 周期:
            data= ace_sma(data,"close",i,1,1)
        
    
