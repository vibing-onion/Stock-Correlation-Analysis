import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import json

import BT_main, BT_fit, general

def mean_filter(data, min = -1, max = -1):
    if min != -1:
        if (data.iloc[:,0].mean() < min) or (data.iloc[:,1].mean() < min):
            return False
    if max != -1:
        if (data.iloc[:,0].mean() > max) or (data.iloc[:,1].mean() > max):
            return False
    return True

def stock_filter(stockA, stockB):
    data = (pd.merge(yf.download(stockA, start = "2010-01-01", end = "2019-12-31")["Adj Close"],
                            yf.download(stockB, start = "2010-01-01", end = "2019-12-31")["Adj Close"], left_index=True, right_index=True))
    
    filters = [
        mean_filter(data, 1, 200)
    ]
    
    return False if False in filters else True


stock_pair = ''
with open("functions/stock_pair_hk_90.json", 'r') as file:
    stock_pair = json.load(file)

x = []
s = []
y = []
z = []
result = []

for combo in stock_pair:
    stockA = combo[0]
    stockB = combo[1]
    corr = combo[2]
    if not stock_filter(stockA, stockB):
        continue
    BT_fit.linear_fit(stockA, stockB)
    
    data, decision_log, RoR, delta = BT_main.process(stockA, stockB, swap = bool(0))
    data2, decision_log2, RoR2, delta2 = BT_main.process(stockA, stockB, swap = bool(1))
    (data, decision_log, RoR, delta) = (data, decision_log, RoR, delta) if RoR > RoR2 else (data2, decision_log2, RoR2, delta2)
    if RoR == 0:
        continue
    
    x.append(data.iloc[:,0].mean())
    x.append(data.iloc[:,1].mean())
    s.append(RoR)
    s.append(RoR)
    rate = abs((1+RoR)/(1+delta)) if RoR > delta else -abs((1+RoR)/(1+delta))
    y.append(rate)
    y.append(rate)
    z.append(delta)
    z.append(delta)
    result.append([stockA, stockB])
    
    print("\n" + str(stockA) + "\t" + str(stockB) + "\t" + str(corr))
    print("ROR = " + str(RoR))
    print("Delta = " + str(delta))
    print("\n==============================\n")


fig = plt.figure()
NROR = fig.add_subplot(3,1,1)
NROR.scatter(x, y, color = "red", label = "Net Rate of Return")    # net rate of return

SP = fig.add_subplot(3,1,2)
SP.scatter(x, z, color = "blue", label = "Change of Price")   # trend of stock price

ROR = fig.add_subplot(3,1,3)
ROR.scatter(x, s, color = "green", label = "Rate of Return")  # rate of return

NROR.axhline(y = 1.1, color = "salmon")  # good net return
SP.axhline(y = 0.15, color = "aqua")   # stable stock: upper limit
SP.axhline(y = -0.15, color = "aqua")  # stable stock: lower limit
ROR.axhline(y = -0.15, color = "limegreen") # generally not too bad return
plt.show()

print(result)