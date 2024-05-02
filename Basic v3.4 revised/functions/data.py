import yfinance as yf
import pandas as pd
import datetime
import dateutil

from datetime import datetime
from dateutil.relativedelta import relativedelta

from functions import general, simulate, BT_fit

def data_transform(a, b, period = 1):
    period = int(period) if int(period) >= 1 else 1
    ref_no = 0 if period > 10 else 11 - period
    #ref_no = -1
    ref_set = general.read_json("functions/temp_exchange/pair_relationship.json")[2][ref_no]
    
    a = a*(float(ref_set[1]) if bool(ref_set[0]) else 1) + (float(ref_set[3]) if int(ref_set[2]) else 0)
    b = b*(float(ref_set[1]) if not bool(ref_set[0]) else 1) + (float(ref_set[3]) if not int(ref_set[2]) else 0)
    return pd.merge(a, b, left_index=True, right_index=True)

def price_trend(stockA, stockB, start_ = "2005", end_ = "2022"):
    a = yf.download(stockA, start = start_ + '-01-01', end = end_ + '-12-31')["Adj Close"]
    b = yf.download(stockB, start = start_ + '-01-01', end = end_ + '-12-31')["Adj Close"]
    
    BT_fit.fit(stockA, stockB, start_, end_)
    data, decision_log = simulate.simulator(stockA, stockB, start = start_, end = end_)
    return data, decision_log
