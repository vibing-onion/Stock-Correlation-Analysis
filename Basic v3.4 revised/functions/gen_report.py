import pandas as pd
import numpy as np
import yfinance as yf

def gen(RoR, Trend, stockA, stockB):
    VolA = {str(i+2010): yf.download(stockA, start = str(i+2010)+'-01-01', end = str(i+2010)+'-12-31')['Volume'].fillna(0).mean()/100000 for i in range(13)}
    VolB = {str(i+2010): yf.download(stockB, start = str(i+2010)+'-01-01', end = str(i+2010)+'-12-31')['Volume'].fillna(0).mean()/100000 for i in range(13)}
    result = pd.DataFrame([RoR, Trend, VolA, VolB], index = ['RoR', 'Trend', 'VolA', 'VolB'])
    print(result)
    result.to_csv('/Users/tsangtszling/Desktop/self_prog/invest/Basic v3/Basic v3.3/functions/report/'+stockA+'_'+stockB+'.csv', index = True)

def gen_data(df, stockA, stockB, start, end):
    df.to_csv('/Users/tsangtszling/Desktop/self_prog/invest/Basic v3/Basic v3.3/functions/report_data/'+stockA+'_'+stockB+'_'+str(start)+str(end)+'.csv', index = True)