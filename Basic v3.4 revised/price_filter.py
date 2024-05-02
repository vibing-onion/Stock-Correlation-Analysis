import json
import pandas as pd
import yfinance as yf

pathSrc = "temp_file/12-4-result_us.json"
pathRes = "temp_file/15-4-result_us_5_to_60.json"

with open(pathSrc, 'r') as file:
    data = json.load(file)
    file.close()
    
result = []
for pair in data:
    val_0 = yf.download(pair[0], start = "2024-04-12", end = "2024-04-13")['Adj Close'].values
    val_1 = yf.download(pair[1], start = "2024-04-12", end = "2024-04-13")['Adj Close'].values
    if (len(val_0) and len(val_1)) and (val_0[0] + val_1[0]) <= 120 and (val_0[0] + val_1[0]) >= 10:
        result.append(pair)

print(result)

with open(pathRes, 'w') as file:
    json.dump(result, file)
    file.close()