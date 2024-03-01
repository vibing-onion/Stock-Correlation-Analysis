# Stock Correlation Analysis 
The idea is brought up by my partner, Victor Ng, who also explains the business knowledge involved in this project. Meanwhile, here is basically the technical part...ya, just codes.

# Background & Methodology
The strategy studies the correlation among stocks in the same industry. Combining with pair trading technique, a mid-to-long term strategy of trading option is formed.
For historical data, Yfinance API is used and data (if the stock was listed in or before 2005) between 2005 and 2023 are extracted for the study.
*For the ticker used in Yfinance API, a list of tickers uploaded in Github (the username was lost) was used to skip the searching process of valid tickers.

# Findings
Out of ~1000 stocks, we have spotted ~150 pairs (90%) and ~25 pairs (95%) of stocks which are highly correlated, based on historical data.

# Result
We regret to say that none of the 95% correlated pairs are option listed in HKEX while the 90% pairs are not statistically-significant enough to give a more guaranteed rate of return.
The hidden opportunities in US market are left to be discovered.
