import json
import pandas as pd
import numpy as np

pathA = "temp_file/stock_pair_hk_90.json"
pathB = "temp_file/stock_pair_hk_95.json"
pathC = "temp_file/popular_stock.json"
pathE = 'temp_file/12-4-result_us.json'

with open (pathA, "r") as file:
    A = json.load(file)
    file.close()
    
with open (pathB, "r") as file:
    B = json.load(file)
    file.close()

with open (pathC, "r") as file:
    C = json.load(file)
    file.close()

with open (pathE, "r") as file:
    E = json.load(file)
    file.close()
    
#union_set = [pair[0:2] for pair in A if pair[0] in C and pair[0] in D and pair[1] in C and pair[1] in D]
union_set = [pair[0:2] for pair in E]
union_set = [list(x) for x in set(frozenset(pair) for pair in union_set)]
print((union_set))