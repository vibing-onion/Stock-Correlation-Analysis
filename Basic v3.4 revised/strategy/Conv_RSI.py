def Convergence_RSI_Mix_Strategy(df, decision_log):
    stock_pair = df.columns[0:2]
    print(df.columns)
    print(df)
    
    bought = False
    hold = 0
    price = 0
    stock = ""
    for i in range(len(df)):
        if bought:
            if df.iloc[i,:].loc[stock] >= (price * 1.03):
                bought = False
                hold = 0
                decision_log.append(df.iloc[i,:])
            elif df.iloc[i,:].loc["10% Converge"] or df.iloc[i,:].loc["RSI_Sell_" + stock]:
                bought = False
                hold = 0
                decision_log.append(df.iloc[i,:])
            elif df.iloc[i,:].loc[stock] <= (price * 0.9):
                bought = False
                hold = 0
                decision_log.append(df.iloc[i,:])
            elif hold > 30:
                if df.iloc[i,:].loc[stock] > (price * 0.9) and df.iloc[i,:].loc[stock] <= (price * 1):
                    bought = False
                    hold = 0
                    decision_log.append(df.iloc[i,:])
                else:
                    hold += 1
            else:
                hold += 1
        else:
            if df.iloc[i,:].loc["90% Converge"]:
            #if True:
                stock = stock_pair[int(df.iloc[i,3] == True)] # Oversold stock assignment
                if df.iloc[i,:].loc["RSI_Buy_" + stock]:
                    bought = True
                    price = df.iloc[i,:].loc[stock]
                else:
                    stock = ""
                
    return decision_log