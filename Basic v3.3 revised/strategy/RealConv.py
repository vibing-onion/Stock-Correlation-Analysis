from math import e, pow
from datetime import datetime
import pandas as pd
from functions import general

def ConvTrading(df, decision_log):
    print(df)
    print(df.columns)
    bought = False
    hold = 0
    long_price = 0
    short_price = 0
    long_stock = 2
    short_stock = 2
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
            # 收斂交易 預期回報 or 持倉太耐 利息高 （假設 10% 利息， 大部分情況下比實際高？應該吧。。。）
            if df.iloc[i,:].loc["10% Converge"] or hold > 160:            # sell long-ed stock + buy short-ed stock
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
                hold = 0
                bought = False if (long_stock == 2 and short_stock == 2) else True
                continue
            
            # 假設 借股人要回股票 at +10% 正回報 （同時以此為做空止損點 -- 股市向好）
            if df.iloc[i,short_stock] >= (1.10 * float(short_price)):
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
                    continue
            hold += 1
        
        else:
            if df.iloc[i,:].loc["90% Converge"]:
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
    
    return pd.DataFrame(decision_log)

def RealConvSimulate(decision_log):
    print(decision_log)
    total_capital = 3750
    usable_capital = 2500
    longHold = 0    # the number of set held but separate for short & long
    shortHold = 0
    short_principal = 0
    shortStock = 0
    longStock = 0
    date = ""
    
    refSet = general.read_json('functions/temp_exchange/pair_relationship.json')[2][-1]
    A_1, ratio = bool(refSet[0]), float(refSet[1])
    ratio = 1/ratio
    
    temp = [abs(ratio - i/20) for i in range(20)]
    buyA, buyB = (temp.index(min(temp)), 20) if A_1 == False else (20, temp.index(min(temp)))
    print(f"BuyA: {buyA} BuyB: {buyB}")
    
    count = -1
    for i in range(len(decision_log)):
        count += 1
        usable_capital = total_capital * 2 / 3
        if decision_log.iloc[i,:].loc["Action Code"] < 10:
            setCost = decision_log.iloc[i,0] * buyA + decision_log.iloc[i,1] * buyB
            if setCost > usable_capital:
                print('Lack Money, Investment Failure !')
            elif decision_log.iloc[i,:].loc["Action Code"] == 0:
                long_price = decision_log.iloc[i,0] if decision_log.iloc[i,5] else decision_log.iloc[i,1]
                longHold = usable_capital // setCost
                longStock = 0 if decision_log.iloc[i,5] else 1
                total_capital = (total_capital - (longHold * long_price * buyA)) if longStock == 0 else (total_capital - (longHold * long_price * buyB))
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(longStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
            elif decision_log.iloc[i,:].loc["Action Code"] == 1:
                short_price = decision_log.iloc[i,0] if not decision_log.iloc[i,5] else decision_log.iloc[i,1]
                shortStock = 0 if not decision_log.iloc[i,5] else 1
                short_principal = short_price * buyA if not decision_log.iloc[i,5] else short_price * buyB
                shortHold = longHold
                date = decision_log.iloc[i,:].loc['Action Date']
                total_capital += (short_principal * shortHold)
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(longStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
            else:
                print('Error in decision code')
        else:
            if decision_log.iloc[i,:].loc["Action Code"] == 10:
                temp = decision_log.iloc[i,longStock] * buyA if longStock == 0 else decision_log.iloc[i,longStock] * buyB
                total_capital += longHold * temp
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(longStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
            elif decision_log.iloc[i,:].loc["Action Code"] == 11:
                temp = decision_log.iloc[i,shortStock] * buyA if shortStock == 0 else decision_log.iloc[i,shortStock] * buyB
                total_capital -= (shortHold * temp + short_principal * (pow(e,abs((pd.to_datetime(date) - decision_log.iloc[i,:].loc['Action Date']).days)*0.1/365) - 1))
                print(str(count//4 + 1) + "trade: " + str(total_capital) + ' decision: ' + str(decision_log.iloc[i,:].loc["Action Code"]) + str(shortStock) + " Date: " + str(decision_log.iloc[i,:].loc['Action Date'].strftime('%Y-%m-%d %H:%M:%S')))
    
    return total_capital, decision_log
                
            
    