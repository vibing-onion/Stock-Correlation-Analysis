import pandas as pd
import numpy as np
import yfinance as yf
import sys

import general

def high_low_fit(df):
    high_point = 0.98
    low_point = 1 - high_point
    range_x = df["Adj Close_x"].quantile(high_point) - df["Adj Close_x"].quantile(low_point)
    range_y = df["Adj Close_y"].quantile(high_point) - df["Adj Close_y"].quantile(low_point)
    x_coe, ratio = (False, range_x/range_y) if range_x > range_y else (True, range_y/range_x)
    if ratio == float("inf"):
        ratio = 0
    if x_coe:
        df.loc[:,"Adj Close_x"] = df.loc[:,"Adj Close_x"]*ratio
    else:
        df.loc[:,"Adj Close_y"] = df.loc[:,"Adj Close_y"]*ratio
    
    offset = abs(df["Adj Close_x"].quantile(low_point) - df["Adj Close_y"].quantile(low_point))
    x_padding = 0
    if df["Adj Close_x"].quantile(low_point) > df["Adj Close_y"].quantile(low_point):
        df["Adj Close_y"] = df["Adj Close_y"] + offset
    else:
        df["Adj Close_x"] = df["Adj Close_x"] + offset
        x_padding = 1
    return x_coe, ratio, x_padding, offset, df

def set_threshold(df):
    df["Gap"] = abs(df["Adj Close_x"] - df["Adj Close_y"])
    threshold = df["Gap"].quantile(0.95)
    pre_trs = df["Gap"].quantile(0.90)
    sell_trs = df["Gap"].quantile(0.10)
    return (pre_trs, threshold, sell_trs, df)

def testing(df, pre_trs, threshold):
    last = df["Gap"].iloc[-1] if not df["Gap"].empty else 0
    return (last > pre_trs), (last > threshold)

def review(stock_A, stock_B, start_ = "2005-01-01", end_ = "2023-12-31"):
    df = (pd.merge(yf.download(stock_A, start = start_, end = end_)["Adj Close"],
                            yf.download(stock_B, start = start_, end = end_)["Adj Close"], left_index=True, right_index=True))
    #df = AF.fitting(df)

    stock_result = []
    period_daycount = [250*(i+1) for i in range(10)]
    period_daycount.append(0)
    period_daycount = period_daycount[::-1]
    for period in period_daycount:
        if (len(df) < period):
            stock_result.append([np.nan for x in range(9)])
            continue
        else:
            df_ = df.iloc[-period:].copy()
            x_coe, ratio, x_padding, offset, df_ = high_low_fit(df_)
            
            pre_trs, threshold, selling_pt, df_ = set_threshold(df_)
            pre_test, test = testing(df_, pre_trs, threshold)
            result = [x_coe, ratio, x_padding, offset, pre_trs, threshold, selling_pt, pre_test, test]
            stock_result.append(result)
    
    period_list = ["Full", '10-year', '9-year', '8-year', '7-year', '6-year', '5-year', '4-year', '3-year', '2-year', '1-year']
    temp = pd.DataFrame({period_list[i]:stock_result[i] for i in range(len(period_list))}).T
    temp.columns = ["X_coe", "Ratio", "X_padding", "Offset", "Warning line", "Threshold", "Selling point","Pre-test", "Test"]
    return temp

def linear_fit(stockA, stockB):
    result = [stockA, stockB, review(stockA, stockB).astype(str).values.tolist()]
    general.export_json("functions/temp_exchange/pair_relationship.json", result)

#linear_fit('1052.HK', '0177.HK')