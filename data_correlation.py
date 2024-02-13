import pandas as pd
import numpy as np
import json

def set_df(data, col_list):
    sub_df = data[col_list]
    if 0 in sub_df.index:
        sub_df.columns = sub_df.iloc[0]
    if 1 in sub_df.index:
        sub_df = sub_df[1:].reset_index(drop = True)
    return sub_df.astype(float)

def main():
    with open ("./temp_file/industry_hk.json", "r") as file:
        file_name_list = json.load(file)
        file.close()
    folder = "./historical_data/hk/"
    for file_name in file_name_list:
        path = folder + file_name + ".csv"
        data = pd.read_csv(path, low_memory = False)
        
        col = data.columns.tolist()
        adj_close = col[:int(len(col)/2):]
        volume = col[int(len(col)/2)::]

        if -1 in data.index:
            drop_ac = data[adj_close].columns[data.iloc[-1][adj_close].isna()]
            drop_vol = [col.replace("Adj Close","Volume") for col in drop_ac]
            data = data.drop(columns=[col for tup in (drop_ac, drop_vol) for col in tup])
        else:
            drop_ac = []
            drop_vol = []

        col = data.columns.tolist()
        adj_close = col[:int(len(col)/2):]
        volume = col[int(len(col)/2)::]

        adj_close_df = set_df(data, adj_close)
        volume_df = set_df(data, volume)

        correlation_matrix = adj_close_df.corr(method = "pearson", numeric_only=True).replace(1, np.nan)
        correlation_matrix[:int(len(col)/2):]
        '''
        masked_matrix = correlation_matrix.where(correlation_matrix >= 0.9, np.nan)
        masked_matrix = masked_matrix.dropna(axis = 0, how = "all")
        masked_matrix = masked_matrix.dropna(axis = 1, how = "all")
        if not masked_matrix.empty:
            print(masked_matrix)
        '''
        stock_pair = []
        indices = np.where(correlation_matrix >= 0.95)
        row_indices, col_indices = indices[0], indices[1]

        for row_idx, col_idx in zip(row_indices, col_indices):
            row_label = correlation_matrix.index[row_idx]
            col_label = correlation_matrix.columns[col_idx]
            pair = [row_label,col_label, correlation_matrix.loc[col_label,row_label]]
            print(pair)
        
if __name__ == "__main__":
    main()