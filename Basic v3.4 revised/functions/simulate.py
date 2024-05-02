import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

from functions import general, plotting, gen_report
from strategy import Conv_RSI, RealConv

'''def simulate(data, initial_capital = 10000):
    total_capital = initial_capital
    usable_capital = total_capital*2/3
    longHoldSet = 0
    shortHoldSet = 0
    shortStock = 0
    longStock = 0
    date = ""'''

def trade(stockA, stockB, df, status):
    original_capital = status['total_capital']
    return_capital, sub_decision_log = 0, []
    return_capital, sub_decision_log, status = RealConv.RealConvSimulate(RealConv.ConvTrading(df, sub_decision_log, status))
    sub_RoR = (return_capital - original_capital)/original_capital
    return sub_decision_log, sub_RoR, status

def process(stockA, stockB, start_, end_):
    overall_ref_set = general.read_json("functions/temp_exchange/pair_relation_by_time.json")[2]
    df_list = {}
    RoR_list = {}
    trend_list = {}
    decision_log = []
    status = {
        'bought' : False,
        'hold' : 0,
        'long_price' : 0,
        'short_price' : 0,
        'long_stock' : 2,
        'short_stock' : 2,
        'longHold' : 0,
        'shortHold' : 0,
        'short_principal' : 0,
        'date' : '',
        'buyA' : 1,
        'buyB' : 1,
        'total_capital' : 100000,
        'usable_capital' : 66666
    }
    
    for s in range(int(end_)-int(start_)+1):
        s += int(start_)
        ref_set = overall_ref_set[str(s)]
        a = yf.download(stockA, start = str(s)+"-01-01", end = str(s)+"-12-31")["Adj Close"]
        b = yf.download(stockB, start = str(s)+"-01-01", end = str(s)+"-12-31")["Adj Close"]
        P_a = a*(float(ref_set['Ratio']) if (ref_set['A_multi'] == "1") else 1) + (float(ref_set['Offset_size']) if ((ref_set['A_offset']) == "1") else 0)
        P_b = b*(float(ref_set['Ratio']) if not (ref_set['A_multi'] == "1") else 1) + (float(ref_set['Offset_size']) if not ((ref_set['A_offset']) == "1") else 0)
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
        df = pd.merge(data, P_data, left_index = True, right_index = True)
            
        df[stockA + " Oversold"] = df["P_"+stockA] < df["P_Mean"]
        df[stockB + " Oversold"] = df["P_"+stockB] < df["P_Mean"]
        df["90% Converge"] = abs(df["P_"+stockA] - df["P_"+stockB]) > float(ref_set['Enter'])
        df["10% Converge"] = abs(df["P_"+stockA] - df["P_"+stockB]) <= float(ref_set['Out'])
        
        print(status)
        sub_decision_log, sub_RoR, status = trade(stockA, stockB, df, status)
        sub_trend = (df.iloc[-1,:].loc["P_Mean"] - df.iloc[0,:].loc["P_Mean"])/df.iloc[0,:].loc["P_Mean"] if len(df) else 1
        print(status)
        df_list[str(s)] = df
        RoR_list[str(s)] = sub_RoR
        trend_list[str(s)] = sub_trend
        decision_log = decision_log + sub_decision_log.values.tolist()
    
    df_list = pd.concat(df_list.values())
    return df_list, RoR_list, trend_list, decision_log
        
def simulator(stockA, stockB, start, end):
    data, RoR, delta, decision_log = process(stockA, stockB, start, end)
    gen_report.gen(RoR, delta, stockA, stockB)
    gen_report.gen_data(data, stockA, stockB, start, end)
    decision_log = pd.DataFrame(decision_log)
    decision_log.columns = [
        stockA, stockB, 'P_' + stockA, 'P_' + stockB, 'P_Mean', 
        stockA + ' Oversold', stockB + ' Oversold',
       '90% Converge', '10% Converge','Action Date', 'Action Code'
        ]
    return data, decision_log