import pandas as pd
import json

def groupby_dict(df, col_name):
    df = list(df.groupby(col_name))
    result = {}
    for group, value in df:
        result[group] = value["YAHOO TICKER"].tolist()
    return result

data = pd.read_csv("./yf_StocklistScrap/yahoo_stocklist.csv")

data = data[["YAHOO TICKER","INDUSTRY","COUNTRY TRADED"]]

ticker_hk = data[data["COUNTRY TRADED"] == "Hong Kong"].reset_index()
ticker_hk = groupby_dict(ticker_hk, "INDUSTRY")

ticker_us = data[data["COUNTRY TRADED"] == "United States of America"].reset_index()
ticker_us = groupby_dict(ticker_us, "INDUSTRY")

ticker = {"ticker_hk": ticker_hk, "ticker_us": ticker_us}

with open('./temp_file/ticker.json', 'w') as file:
    json.dump(ticker, file)
    
