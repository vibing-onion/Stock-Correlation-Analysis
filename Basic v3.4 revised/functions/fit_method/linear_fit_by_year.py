import pandas as pd
import numpy as np
import yfinance as yf

def reject_fit(df, reject = 0.05):
    high_point = 1 - reject
    low_point = reject
    range_x = df["Adj Close_x"].quantile(high_point) - df["Adj Close_x"].quantile(low_point)
    range_y = df["Adj Close_y"].quantile(high_point) - df["Adj Close_y"].quantile(low_point)
    x_coe, ratio = (0, range_x/range_y) if range_x > range_y else (1, range_y/range_x)
    if ratio == float("inf"):
        ratio = 1
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
    return str(x_coe), str(ratio), str(x_padding), str(offset), df

def set_threshold(df, upper_limit, lower_limit):
    df["Gap"] = abs(df["Adj Close_x"] - df["Adj Close_y"])
    enter_line = df["Gap"].quantile(upper_limit)
    out_line = df["Gap"].quantile(lower_limit)
    return (enter_line, out_line)

def fitting(stockA, stockB, start, end, enter = 0.90, out = 0.10, period = 1):
    start = int(start)
    end = int(end)
    s = start - period
    e = s + period
    relation_set = {}
    
    for year in range(end - start + 1):
        SYear = year + s
        EYear = year + e - 1
        df = pd.merge(yf.download(stockA, start = str(SYear) + '-01-01', end = str(EYear) + '-12-31')['Adj Close'],
                      yf.download(stockB, start = str(SYear) + '-01-01', end = str(EYear) + '-12-31')['Adj Close'],
                      left_index=True, right_index=True)
        
        if df.empty:
            print('df empty')
            relation = {
                'A_multi' : '0',
                'Ratio' : '1',
                'A_offset' : '0',
                'Offset_size' : '0',
                'Enter' : '0',
                'Out' : '0'
            }
        else:
            print('df not empty')
            A_multi, Ratio, A_offset, Offset_size, df = reject_fit(df)
            Enter, Out = set_threshold(df, upper_limit = enter, lower_limit = out)
            relation = {
                'A_multi' : A_multi,
                'Ratio' : Ratio,
                'A_offset' : A_offset,
                'Offset_size' : Offset_size,
                'Enter' : Enter,
                'Out' : Out
            }
        relation_set[str(start + year)] = relation
    
    return relation_set