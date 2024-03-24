import pandas as pd
import numpy as np
import json
import yfinance as yf

def set_df(data, col_list):
    sub_df = data[col_list]
    if 0 in sub_df.index:
        sub_df.columns = sub_df.iloc[0]
    if 1 in sub_df.index:
        sub_df = sub_df[1:].reset_index(drop = True)
    return sub_df.astype(float)

def filter_length_lastRow(folder, file_name_list, period = 250):
    total_vol = {}
    for file_name in file_name_list:
        path = folder + file_name + ".csv"
        data = pd.read_csv(path, low_memory = False)
        
        col = data.columns.tolist()
        l = int((len(col)+1)/2)
        adj_close = col[0:l:]
        volume = col[l::]

        if -1 in data.index:
            drop_ac = data[adj_close].columns[data.iloc[-1][adj_close].isna()]
            drop_vol = [col.replace("Adj Close","Volume") for col in drop_ac]
            data = data.drop(columns=[col for tup in (drop_ac, drop_vol) for col in tup])
        else:
            drop_ac = []
            drop_vol = []

        col = data.columns.tolist()

        adj_close_df = set_df(data, adj_close)
        volume_df = set_df(data, volume)
        
        sub_vol = {col: volume_df[col].iloc[-period:,].reset_index(drop=True) for col in volume_df.columns if len(volume_df[col]) >= period}
        sub_vol = {key: value.tolist() for key, value in sub_vol.items() if not (pd.isna(value.iloc[-1]) or (value.iloc[-1] == 0.0).all())}
        
        for key, value in sub_vol.items():
            if key not in total_vol:
                total_vol[key] = value
    
    volume_lower_limit = pd.DataFrame([sum(value)/len(value) for key, value in total_vol.items()]).quantile(0.9)
    target_stock = [key for key,value in total_vol.items() if sum(value)/len(value) > volume_lower_limit.iloc[0]] #popular stock with high volume
    return target_stock

def load_adj_close(target_stock, period):
    print(target_stock)
    target_stock_close = {
        key:
            yf.download(key, start = "2023-01-01", end = "2023-12-31")["Adj Close"].iloc[-period:]
        for key in target_stock if str(key).endswith(".HK")
    }
    return target_stock_close

def main():
    with open ("./temp_file/industry_hk.json", "r") as file:
        file_name_list = json.load(file)
        file.close()
    folder = "./historical_data/hk/"
    target_stock = filter_length_lastRow(folder, file_name_list, period = 10)
    target_stock = [key for key in target_stock if str(key).endswith(".HK")]
    
    with open ("./temp_file/popular_stock.json", "w") as file:
        json.dump(target_stock, file)
        file.close()
    
if __name__ == "__main__":
    main()