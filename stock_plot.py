import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import json

with open ("./temp_file/stock_pair_hk_95.json", "r") as file:
    data = json.load(file)
    file.close()

def compare(ax, df, period = 0):
    ax.plot(df.iloc[-period:, 0].index, df.iloc[-period:, 0], label='y1')
    ax.plot(df.iloc[-period:, 1].index, df.iloc[-period:, 1], label='y2')
    ax.legend()

def get_threshold(ax, df, period = 0):
    ax.plot(df.iloc[-period:, 0].index, abs(df.iloc[-period:, 0] - df.iloc[-period:, 1]), label='gap')
    ax.axhline(y=abs(df.iloc[-period:, 0]-df.iloc[-period:, 1]).quantile(0.95), color='red', linestyle='--')
    ax.legend()
    print(abs(df.iloc[-period:, 0]-df.iloc[-period:, 1]).quantile(0.95))

def check(ax, df, period):
    #ax.plot(df.index, df.iloc[:, 0], label='y1')
    #ax.plot(df.index, df.iloc[:, 1], label='y2')
    ax.plot(df.iloc[-period:].index, abs(df.iloc[-period:, 0]-df.iloc[-period:, 1]), label='gap')
    ax.axhline(y=0.6914988679885864, color='red', linestyle='--')
    ax.legend()

def main():
    # data : 5-year   False  1.268436         1  1.421562      1.56057   1.76622
    # data : 3-year   False  1.419597         1  2.299964     1.477828  1.538809
    pair_num = 7
    print(data[pair_num])
    print(pd.DataFrame(data).sort_values(2))
    
    df = (pd.merge(yf.download(data[pair_num][0], start = "2005-01-01", end = "2023-12-31")["Adj Close"],
                            yf.download(data[pair_num][1], start = "2005-01-01", end = "2023-12-31")["Adj Close"], left_index=True, right_index=True))
    
    real_df = (pd.merge(yf.download(data[pair_num][0], start = "2005-01-01", end = "2024-2-19")["Adj Close"]+0.75,
                            yf.download(data[pair_num][1], start = "2005-01-01", end = "2024-2-19")["Adj Close"]*1.21, left_index=True, right_index=True))
    
    # upper : blue, lower : orange
    
    num_rows, num_cols = 1, 1
    fig, axes = plt.subplots(num_rows, num_cols)
    
    #check(axes, real_df, 1250)
    compare(axes, real_df, 0)
    #get_threshold(axes, real_df,250)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()