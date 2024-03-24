import yfinance as yf
import pandas as pd
import datetime
import dateutil
import sys

from datetime import datetime
from dateutil.relativedelta import relativedelta

from functions import general

def data_transform(a, b, period = 1):
    period = int(period) if int(period) >= 1 else 1
    ref_no = 0 if period > 10 else 11 - period
    ref_set = general.read_json("functions/temp_exchange/pair_relationship.json")[2][ref_no]
    
    a = a*(float(ref_set[1]) if bool(ref_set[0]) else 1) + (float(ref_set[3]) if int(ref_set[2]) else 0)
    b = b*(float(ref_set[1]) if not bool(ref_set[0]) else 1) + (float(ref_set[3]) if not int(ref_set[2]) else 0)
    return pd.merge(a, b, left_index=True, right_index=True)

def price_trend(stockA, stockB, start_ = "2005-01-01", end_ = "2022-12-31"):
    period = relativedelta(datetime.strptime(end_, "%Y-%m-%d") - datetime.strptime(start_, "%Y-%m-%d")).years
    
    a = yf.download(stockA, start = start_, end = end_)["Adj Close"]
    b = yf.download(stockB, start = start_, end = end_)["Adj Close"]
    data = data_transform(a, b)
    data["Mean"] = (data["Adj Close_x"] + data["Adj Close_y"])/2
    return data

def spread_threshold(data):
    data["Spread"] = abs(data["Adj CLose_x"] - data["Adj Close_y"])
    line_90 = data["Spread"].quantile(0.90)
    line_95 = data["Spread"].quantile(0.95)
    return data, line_90, line_95