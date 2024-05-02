from math import e, pow
from datetime import datetime
import pandas as pd
from functions import general

def ConvTrading(df, decision_log, status):
    #print(f'ConvTrading {status}')
    bought = status['bought']
    hold = status['hold']
    long_price = status['long_price']
    short_price = status['short_price']
    long_stock = status['long_stock']
    short_stock = status['short_stock']
    total_capital = status['total_capital']
    usable_capital = status['usable_capital']
    longHold = status['longHold']
    shortHold = status['shortHold']
    short_principal = status['short_principal']
    date = status['date']
    stockA = 0
    stockB = 1
    stockA_symbol = df.columns[0]
    stockB_symbol = df.columns[1] 
    
    #           long short
    # enter     00   01
    # out       10   11
    
    temp_col = df.columns.tolist()
    df['Action Date'] = df.index
    temp_col.append('Action Date')
    df = df.reset_index()
    df = df[temp_col]
    for i in range(len(df)):
        if bought:
            
            # 演算法漏洞，年尾退場
            '''if i == (len(df) - 1):
                if short_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 11
                    decision_log.append(temp_df)                          # append buy short-ed stock
                    short_stock = 2                                       # short-ed stock aka if any stock short-ed
                    short_price = 0
                if long_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 10
                    decision_log.append(temp_df)                          # append sell long-ed stock
                    long_stock = 2                                        # long-ed stock aka if any stock long-ed
                    long_price = 0
                    continue'''
                
            # 收斂交易 預期回報 or 持倉太耐 利息高 （假設 10% 利息， 大部分情況下比實際高？應該吧。。。）
            '''if df.iloc[i,:].loc["10% Converge"] or hold > 160:'''            # sell long-ed stock + buy short-ed stock
            if df.iloc[i,:].loc["10% Converge"]:
                if long_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 10
                    decision_log.append(temp_df)                          # append sell long-ed stock
                    long_stock = 2                                        # long-ed stock aka if any stock long-ed
                    long_price = 0
                if short_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 11
                    decision_log.append(temp_df)                          # append buy short-ed stock
                    short_stock = 2                                       # short-ed stock aka if any stock short-ed
                    short_price = 0
                bought = False if (long_stock == 2 and short_stock == 2) else True
                continue
            
            # 假設 借股人要回股票 at +10% 正回報 （同時以此為做空止損點 -- 股市向好）
            '''if df.iloc[i,short_stock] >= (1.10 * float(short_price)):
                if short_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 11
                    decision_log.append(temp_df)                          # append buy short-ed stock
                    short_stock = 2                                       # short-ed stock aka if any stock short-ed
                    short_price = 0
                if long_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 10
                    decision_log.append(temp_df)                          # append sell long-ed stock
                    long_stock = 2                                        # long-ed stock aka if any stock long-ed
                    long_price = 0
                    continue
            # 看好止損點
            if df.iloc[i,long_stock] <= (0.91 * long_price):
                if long_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 10
                    decision_log.append(temp_df)                          # append sell long-ed stock
                    long_stock = 2                                        # long-ed stock aka if any stock long-ed
                    long_price = 0
                if short_stock != 2:
                    temp_df = df.iloc[i,:].copy()
                    temp_df["Action Code"] = 11
                    decision_log.append(temp_df)                          # append buy short-ed stock
                    short_stock = 2                                       # short-ed stock aka if any stock short-ed
                    short_price = 0
                    continue'''
            hold += 1
        
        else:
            if df.iloc[i,:].loc["90% Converge"]:
                hold = 0
                long_stock = stockA if df.iloc[i,:].loc[stockA_symbol+" Oversold"] else stockB
                long_price = df.iloc[i,long_stock]
                short_stock = stockA if long_stock != stockA else stockB
                short_price = df.iloc[i,short_stock]
                temp_df = df.iloc[i,:].copy()
                temp_df["Action Code"] = 0
                decision_log.append(temp_df)                             # append buy long-ed stock
                temp_df = df.iloc[i,:].copy()
                temp_df["Action Code"] = 1
                decision_log.append(temp_df)                             # append sell short-ed stock
                bought = True
    
    status['hold'] = hold
    
    return [pd.DataFrame(decision_log), status]

def RealConvSimulate(decision_log_status):
    decision_log, status = decision_log_status[0], decision_log_status[1]
    bought = status['bought']
    print(decision_log)
    #print(f'ConvSimulate {status}')
    total_capital = status['total_capital']
    usable_capital = status['usable_capital']
    longHold = status['longHold']   # the number of set held but separate for short & long
    shortHold = status['shortHold']
    short_principal = status['short_principal']
    shortStock = status['short_stock']
    longStock = status['long_stock']
    long_price = status['long_price']
    short_price = status['short_price']
    date = status['date']
    hold = status['hold']
    
    refSet = general.read_json("functions/temp_exchange/pair_relation_by_time.json")[2]
    A_1, ratio= 1,1
    buyA = status['buyA']
    buyB = status['buyB']
    
    count = -1
    for i in range(len(decision_log)):
        count += 1
        usable_capital = total_capital * 2 / 3
        if decision_log.iloc[i,:].loc["Action Code"] < 10:
            year = decision_log.iloc[i,:].loc['Action Date'].strftime('%Y')
            A_1, ratio = bool(refSet[year]['A_multi']), float(refSet[year]['Ratio'])
            ratio = 1/ratio
            
            temp = [abs(ratio - i/20) for i in range(20)]
            buyA, buyB = (temp.index(min(temp))+1, 20) if A_1 == False else (20, temp.index(min(temp))+1)
            print(f"BuyA: {buyA} BuyB: {buyB}")
            
            
            setCost = decision_log.iloc[i,0] * buyA + decision_log.iloc[i,1] * buyB
            if setCost > usable_capital:
                print('Lack Money, Investment Failure !')
            elif decision_log.iloc[i,:].loc["Action Code"] == 0:
                bought = True
                long_price = decision_log.iloc[i,0] if decision_log.iloc[i,5] else decision_log.iloc[i,1]
                longHold = usable_capital // setCost
                longStock = 0 if decision_log.iloc[i,5] else 1
                #print(str(total_capital)+' '+str(float(long_price)*buyA)+' '+ str(float(long_price)*buyB)+' '+str(int(longHold)))
                total_capital = (total_capital - (longHold * long_price * buyA)) if longStock == 0 else (total_capital - (longHold * long_price * buyB))
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(longStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
            elif decision_log.iloc[i,:].loc["Action Code"] == 1:
                bought = True
                short_price = decision_log.iloc[i,0] if not decision_log.iloc[i,5] else decision_log.iloc[i,1]
                shortStock = 0 if not decision_log.iloc[i,5] else 1
                short_principal = short_price * buyA if not decision_log.iloc[i,5] else short_price * buyB
                shortHold = longHold
                date = decision_log.iloc[i,:].loc['Action Date']
                #print(str(total_capital)+' '+str(float(short_price)*buyA)+' '+ str(float(short_price)*buyB)+' '+str(int(shortHold)))
                total_capital += (short_principal * shortHold)
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(shortStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
            else:
                print('Error in decision code')
        else:
            bought = False
            if decision_log.iloc[i,:].loc["Action Code"] == 10:
                print(f'{buyA} {buyB}')
                temp = (decision_log.iloc[i,longStock] * buyA) if longStock == 0 else (decision_log.iloc[i,longStock] * buyB)
                #print(str(total_capital)+' '+str(float(temp))+' '+str(int(longHold)))
                total_capital += longHold * temp
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(longStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
            elif decision_log.iloc[i,:].loc["Action Code"] == 11:
                print(f'{buyA} {buyB}')
                temp = (decision_log.iloc[i,shortStock] * buyA) if shortStock == 0 else (decision_log.iloc[i,shortStock] * buyB)
                #print(str(total_capital)+' '+str(float(temp))+' '+str(int(shortHold)))
                total_capital -= (shortHold * temp + short_principal * (pow(e,abs((pd.to_datetime(date) - decision_log.iloc[i,:].loc['Action Date']).days)*0.1/365) - 1))
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(shortStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
    
    status['bought'] = bought
    status['total_capital'] = float(total_capital)
    status['usable_capital'] = float(usable_capital)
    status = {
        'bought' : bought,
        'hold' : hold,
        'long_price' : long_price,
        'short_price' : short_price,
        'long_stock' : longStock,
        'short_stock' : shortStock,
        'longHold' : longHold,
        'shortHold' : shortHold,
        'short_principal' : short_principal,
        'date' : date,
        'buyA' : buyA,
        'buyB' : buyB,
        'total_capital' : float(total_capital),
        'usable_capital' : float(usable_capital)
    }
    
    return total_capital, decision_log, status
                
            
    