import yfinance as yf
import json
import multiprocessing as mp
import os

def download(industry_list_, ticker_list_):
    tickerchain_list = [" ".join(element) for element in ticker_list_]
    result = {}
    for i in range(len(tickerchain_list)):
        result[industry_list_[i]] = yf.download(tickerchain_list[i], start = "2005-01-01", end = "2023-12-31")[["Adj Close", "Volume"]]
    return result

def get_csv(**kwargs):
    result = kwargs.get("result_")
    for industry, data in result.items():
        folder = "./historical_data/us/"
        path = str(industry) + ".csv"
        path = os.path.join(folder, path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data.to_csv(path, index = False)

def main():
    with open ("./temp_file/ticker.json", "r") as file:
        ticker = json.load(file)
        ticker_hk = ticker["ticker_hk"]
        ticker_us = ticker["ticker_us"]
        file.close()

    industry_hk = []
    industry_us = []
    tick_hk = []
    tick_us = []
    for key, value in ticker_hk.items():
        industry_hk.append(key)
        tick_hk.append(value)
    for key, value in ticker_us.items():
        industry_us.append(key)
        tick_us.append(value)
    
    [p1, p2, p3, p4] = [mp.Process(target = download, args = (industry_hk[i::4],tick_hk[i::4])) for i in range(4)]
    
    jobs = [p1, p2, p3, p4]
    for job in jobs:
        job.start()

    result = [download(industry_hk[i::4], tick_hk[i::4]) for i in range(4)]
    
    [p1, p2, p3, p4] = [mp.Process(target = get_csv, kwargs = {"result_": result[i]}) for i in range(4)]
    jobs = [p1, p2, p3, p4]
    for job in jobs:
        job.start()
    
    with open ("./temp_file/industry_hk.json", "w") as file:
        json.dump(industry_hk,file)
    
    
if __name__ == "__main__":
    main()