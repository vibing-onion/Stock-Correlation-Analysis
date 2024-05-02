def Conv_RSI_Indicator(df, conv90, conv10, period):
    
    stockA, stockB = df.columns[0], df.columns[1]
    df["PS_" + stockA] = df[stockA].shift(-1) - df[stockA]
    df["PS_" + stockB] = df[stockB].shift(-1) - df[stockB]
    df["Profit_" + stockA] = df["PS_" + stockA].agg(lambda x: x if x > 0 else 0).rolling(period).sum()
    df["Profit_" + stockB] = df["PS_" + stockB].agg(lambda x: x if x > 0 else 0).rolling(period).sum()
    df["Loss_" + stockA] = df["PS_" + stockA].agg(lambda x: abs(x) if x < 0 else 0).rolling(period).sum()
    df["Loss_" + stockB] = df["PS_" + stockB].agg(lambda x: abs(x) if x < 0 else 0).rolling(period).sum()
    df["RSI_" + stockA] = df["Profit_" + stockA] / (df["Profit_" + stockA] + df["Loss_" + stockA])
    df["RSI_" + stockB] = df["Profit_" + stockB] / (df["Profit_" + stockB] + df["Loss_" + stockB])
    
    lower_lim_A = df["RSI_" + stockA].quantile(0.16)
    upper_lim_A = df["RSI_" + stockA].quantile(0.84)
    lower_lim_B = df["RSI_" + stockB].quantile(0.16)
    upper_lim_B = df["RSI_" + stockB].quantile(0.84)
    
    df['RSI_Buy_' + stockA] = df["RSI_" + stockA] <= lower_lim_A
    df['RSI_Buy_' + stockB] = df["RSI_" + stockB] <= lower_lim_B
    df['RSI_Sell_' + stockA] = df["RSI_" + stockA] > upper_lim_A
    df['RSI_Sell_' + stockB] = df["RSI_" + stockB] > upper_lim_B
    
    return df