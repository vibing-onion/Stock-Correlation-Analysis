from functions.fit_method import linear_fit_by_year
import general

def fit(stockA, stockB, start, end, enter = 0.90, out = 0.10, period = 3):
    result = [stockA, stockB, linear_fit_by_year.fitting(
        stockA, 
        stockB, 
        start, 
        end, 
        enter = 0.90, 
        out = 0.10, 
        period = period
    )]
    general.export_json('functions/temp_exchange/pair_relation_by_time.json',result)