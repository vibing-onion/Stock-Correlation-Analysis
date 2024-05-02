import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import json
from datetime import date

with open ("./temp_file/stock_pair_US_90.json", "r") as file:
    data = json.load(file)
    data = [combo[0:2] for combo in data]
    data = [list(x) for x in set(frozenset(pair) for pair in data)]
    print(data)
    file.close()

today = date.today().strftime("%Y-%m-%d")

def high_low_fit(df):
    range_x = df["Adj Close_x"].quantile(0.95) - df["Adj Close_x"].quantile(0.05)
    range_y = df["Adj Close_y"].quantile(0.95) - df["Adj Close_y"].quantile(0.05)
    x_coe, ratio = (False, range_x/range_y) if range_x > range_y else (True, range_y/range_x)
    if ratio == float("inf"):
        ratio = 0
    if x_coe:
        df.loc[:,"Adj Close_x"] = df.loc[:,"Adj Close_x"]*ratio
    else:
        df.loc[:,"Adj Close_y"] = df.loc[:,"Adj Close_y"]*ratio
    
    offset = abs(df["Adj Close_x"].quantile(0.05) - df["Adj Close_y"].quantile(0.05))
    x_padding = 0
    if df["Adj Close_x"].quantile(0.05) > df["Adj Close_y"].quantile(0.05):
        df["Adj Close_y"] = df["Adj Close_y"] + offset
    else:
        df["Adj Close_x"] = df["Adj Close_x"] + offset
        x_padding = 1
    return x_coe, ratio, x_padding, offset, df

def set_threshold(df):
    df["Gap"] = abs(df["Adj Close_x"] - df["Adj Close_y"])
    threshold = df["Gap"].quantile(0.95)
    pre_trs = df["Gap"].quantile(0.90)
    return (pre_trs, threshold, df)

def testing(df, pre_trs, threshold):
    print(df["Gap"])
    last = df["Gap"].iloc[-1]
    return (last > pre_trs), (last > threshold)

def review(stock_A, stock_B):
    df = (pd.merge(yf.download(stock_A, start = "2005-01-01", end = today)["Adj Close"],
                            yf.download(stock_B, start = "2005-01-01", end = today)["Adj Close"], left_index=True, right_index=True))

    stock_result = []
    for period in [0, 2500, 1250, 750, 250]:
        if (len(df) < period):
            stock_result.append([np.nan for x in range(8)])
            continue
        else:
            df_ = df.iloc[-period:].copy()
            x_coe, ratio, x_padding, offset, df_ = high_low_fit(df_)
            
            pre_trs, threshold, df_ = set_threshold(df_)
            pre_test, test = testing(df_, pre_trs, threshold)
            result = [x_coe, ratio, x_padding, offset, pre_trs, threshold, pre_test, test]
            stock_result.append(result)
    
    period_list = ["full", "10-year", "5-year", "3-year", "1-year"]
    temp = pd.DataFrame({period_list[i]:stock_result[i] for i in range(5)}).T
    temp.columns = ["X_coe", "Ratio", "X_padding", "Offset", "Warning line", "Threshold", "Pre-test", "Test"]
    return temp

def main():
    total_result = []
    for pair in data:
        total_result.append([pair[0], pair[1], review(pair[0],pair[1])])
    
    for i, result in enumerate(total_result):
        print(i, result)
    
if __name__ == "__main__":
    main()