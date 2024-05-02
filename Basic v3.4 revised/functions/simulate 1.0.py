import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

from functions import general,plotting
from strategy import Conv_RSI

                
def direct_suspension_strategy2(data, decision_log, bought, price, hold_time, stock, suspension):
    for i in range(len(data)):
        if (suspension > 0 and data.iloc[i,int(data.iloc[i,3] == True)] < price) and suspension < 10:
            suspension -= 1
            continue
        suspension -= 1
        if not bought and data.iloc[i,:].loc["Converge"] == True:
            bought = True
            stock = int(data.iloc[i,3] == True)
            price = data.iloc[i,stock]
            hold_time += 1
            decision_log.append(data.iloc[i,:])
            continue
        if bought:
            if data.iloc[i,stock] >= (price * 1.03):
                bought = False
                hold_time = 0
                decision_log.append(data.iloc[i,:])
                suspension = 15
                continue
            if data.iloc[i,:].loc["Below 10%"] == True:
                bought = False
                hold_time = 0
                decision_log.append(data.iloc[i,:])
                continue
            if data.iloc[i,stock] <= (price * 0.9):
                bought = False
                hold_time = 0
                decision_log.append(data.iloc[i,:])
                suspension = 15
                continue
            if hold_time > 30:
                if data.iloc[i,stock] > (price * 0.9) and data.iloc[i,stock] <= (price * 1):
                    bought = False
                    hold_time = 0
                    decision_log.append(data.iloc[i,:])
                elif data.iloc[i,:].loc["Below 10%"] == True:
                    bought = False
                    hold_time = 0
                    decision_log.append(data.iloc[i,:])
                else:
                    hold_time += 1
                continue
            if data.iloc[i,:].loc["Below 10%"] == True:
                bought = False
                hold_time = 0
                decision_log.append(data.iloc[i,:])
            hold_time += 1
    return decision_log
    

def direct_suspension_strategy(data, decision_log, bought, price, hold_time, stock, suspension):
    for i in range(len(data)):
        if (suspension > 0 and data.iloc[i,int(data.iloc[i,3] == True)] < price) and suspension < 10:
            suspension -= 1
            continue
        suspension -= 1
        if not bought and data.iloc[i,:].loc["Converge"] == True:
            bought = True
            stock = int(data.iloc[i,3] == True)
            price = data.iloc[i,stock]
            hold_time += 1
            decision_log.append(data.iloc[i,:])
            continue
        if bought:
            if data.iloc[i,stock] >= (price * 1.03):
                bought = False
                hold_time = 0
                decision_log.append(data.iloc[i,:])
                suspension = 15
                continue
            if data.iloc[i,stock] <= (price * 0.9):
                bought = False
                hold_time = 0
                decision_log.append(data.iloc[i,:])
                suspension = 15
                continue
            if hold_time > 30:
                if data.iloc[i,stock] > (price * 0.9) and data.iloc[i,stock] <= (price * 1):
                    bought = False
                    hold_time = 0
                    decision_log.append(data.iloc[i,:])
                elif data.iloc[i,:].loc["Below 10%"] == True:
                    bought = False
                    hold_time = 0
                    decision_log.append(data.iloc[i,:])
                else:
                    hold_time += 1
                continue
            if data.iloc[i,:].loc["Below 10%"] == True:
                bought = False
                hold_time = 0
                decision_log.append(data.iloc[i,:])
            hold_time += 1
    return decision_log

def decider(data):
    decision_log = []
    bought = False
    price = 0
    hold_time = 0
    stock = 0
    suspension = 0
    
    #decision_log = direct_suspension_strategy2(data, decision_log, bought, price, hold_time, stock, suspension)
    decision_log = Conv_RSI.Convergence_RSI_Mix_Strategy(data, decision_log)
    
    #return pd.DataFrame(decision_log) if len(decision_log)%2 == 0 else pd.DataFrame(decision_log[:-1:])
    return pd.DataFrame(decision_log)
            
def simulate(data):
    capital = 10000
    hold = 0
    stock = 0
    for i in range(len(data)):
        if i%2 == 0:
            stock = int(data.iloc[i, 2] == False)
            price = data.iloc[i,int(data.iloc[i, 2] == False)]
            hold = capital // price
            capital = capital % price
        else:
            price = data.iloc[i,stock]
            capital = hold * price + capital
            print(str(i//2 + 1) + "trade: " + str(capital) + " Sell: " + str(stock) + " Date: " + str(data.index[i]))
    return capital

def trade(stockA, stockB, data):
    data_90 = data[[stockA, stockB, stockA + " Oversold", stockB + " Oversold", "90% Converge", "10% Converge"]]
    data_95 = data[[stockA, stockB, stockA + " Oversold", stockB + " Oversold", "95% Converge", "10% Converge"]]
    data_90.columns = [stockA, stockB, stockA + " Oversold", stockB + " Oversold", "Converge", "Below 10%"]
    data_95.columns = [stockA, stockB, stockA + " Oversold", stockB + " Oversold", "Converge", "Below 10%"]
    
    temp = decider(data_90)
    decision_log = [] if temp.empty else temp[[stockA, stockB, stockA + " Oversold", stockB + " Oversold"]]
    print(decision_log)
    
    r = simulate(decision_log)
    RoR = (r - 10000)/10000
    return decision_log, RoR
    

def process(stockA, stockB, swap, start_, end_):
    (stockA, stockB) = (stockB, stockA) if swap == True else (stockA, stockB)
    ref_set = general.read_json("functions/temp_exchange/pair_relationship.json")[2][-1]
    
    a = yf.download(stockA, start = start_, end = end_)["Adj Close"]
    b = yf.download(stockB, start = start_, end = end_)["Adj Close"]
    P_a = a*(float(ref_set[1]) if (ref_set[0] == "True") else 1) + (float(ref_set[3]) if ((ref_set[2]) == "1") else 0)
    P_b = b*(float(ref_set[1]) if not (ref_set[0] == "True") else 1) + (float(ref_set[3]) if not ((ref_set[2]) == "1") else 0)
    
    data = pd.merge(
        a,
        b,
        left_index = True,
        right_index = True
    )
    P_data = pd.merge(
        P_a,
        P_b,
        left_index = True,
        right_index = True
    )
    P_data["Mean"] = (P_data.iloc[:,0] + P_data.iloc[:,1]) / 2
    data.columns = [stockA, stockB]
    P_data.columns = ["P_" + stockA, "P_" + stockB, "P_Mean"]
    data_view = pd.merge(data, P_data, left_index = True, right_index = True)
    
    data_view[stockA + " Oversold"] = data_view["P_"+stockA] < data_view["P_Mean"]
    data_view[stockB + " Oversold"] = data_view["P_"+stockB] < data_view["P_Mean"]
    data_view["90% Converge"] = abs(data_view["P_"+stockA] - data_view["P_"+stockB]) > float(ref_set[4])
    data_view["95% Converge"] = abs(data_view["P_"+stockA] - data_view["P_"+stockB]) > float(ref_set[5])
    data_view["10% Converge"] = abs(data_view["P_"+stockA] - data_view["P_"+stockB]) <= float(ref_set[6])
    
    decision_log, RoR = trade(stockA, stockB, data_view[[stockA, stockB, stockA + " Oversold", stockB + " Oversold", "90% Converge", "95% Converge", "10% Converge"]])
    delta = (data_view.iloc[-1,:].loc["P_Mean"] - data_view.iloc[0,:].loc["P_Mean"])/data_view.iloc[0,:].loc["P_Mean"] if len(decision_log) else 1
    
    return data_view, decision_log, RoR, delta

def simulator(stockA, stockB, start, end):
    data, decision_log, RoR, delta = process(stockA, stockB, bool(0), start, end)
    return data, decision_log