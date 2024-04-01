import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
import os

数据地址 = os.path.join(os.path.join(os.getcwd(), "数据地址"), "002342.csv")  # 本次是单个，未来可以用循环遍历，列表表达式用if 过滤CSV
# print(数据地址)
data = pd.read_csv(数据地址, index_col="date", parse_dates=True)
data = data.drop(columns="ma")
# data["MA_10"] = pd.rolling_mean(data["close"],10)
# data["MA_10"] = data["close"].rolling(10).mean()
# data["ma_10_talib"] = talib.MA(np.array(data["close"]),timeperiod = 10)

MA周期= [5,10,20,30,60,120,250]
for i in MA周期:
    name = "ma_" + str(i)
    data[name] = talib.MA(np.array(data["close"]),timeperiod = i)
data = data.fillna(0.00)
data = data.applymap(lambda x : round(x,2))
print(data)



data['MACD'],data['MACD信号'],data['MACD柱子'] = talib.MACD(np.array(data["close"]),
                            fastperiod=6, slowperiod=12, signalperiod=9)
data = data.fillna(0.00)
data = data.applymap(lambda x : round(x,2))



print(data)
path = os.path.join(os.path.join(os.getcwd(), "数据地址"),  "扩充002342.csv")
data.to_csv(  path)


