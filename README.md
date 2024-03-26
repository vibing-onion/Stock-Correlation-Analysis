# Stock Correlation Analysis (partnered)
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

# Latest Update
There are more to explore in warrents, inline or derivative. May change our target products after further research.

#What is convergence trade?
Convergence Trade
(non-academic / professional article)

Convergence trade, or relative value strategy, is a well known trading strategy used by many institutional and quantitative investors, such as Long Term Capital Management (LTCM, which was closed in 2000). In fact, convergence strategy aims to produce a considerable amount of rate of return while bearing a very low risk. In the following article, we will look into the idea, the detail, and the assumption taken for this strategy.

Idea of Convergence Trade:

Unlike most of the approaches adopted by most funds, convergence strategies do not take emphasis on either financial information of a company or financial news. Instead, it is a quantitative approach which analyzes the price movement of hundreds and thousands of stocks and bonds in the market by modeling and forecasting. Let’s think about a normal investment: we long a stock, and we gain money when the price of the stock increases. However, you will bear a loss when its price drops. In this case, we bear a risk when we seek a return, and the risk of the investment is hard to be quantified as there are many many factors affecting the price movement. 

Therefore, here comes the idea of convergence trade: first we have to find a pair of very similar assets which implies a very similar price movement, with a small price difference, for most of the time (theoretically, both assets valuation should be similar). Then, we have to wait and spot the significant price difference for this pair of assets, and that’s when you can have arbitrage opportunities by longing the one with lower price and shorting the one with higher price. As long as the price of two assets return to the previous trends and become similar again, we can earn an arbitrage profit equivalent to the price difference at the beginning of the position. Even if the price of the assets diverge further in a long time, we can earn an arbitrage profit once it converges some day in the future.

Let’s give a simple example to demonstrate the strategy. Today we observe two kinds of eggs, one is white egg and another is brown egg. Their flavor, size and hygiene standards are identical. Presumably, both eggs should share the same or very similar price and almost the same price movement. One day you observe that the price of a brown egg is $8.00 but the price of a white egg is $6.00, which is greatly deviated compared to the historical performance. In this case, we can apply a convergence trade strategy, in which we long the white egg and short the brown egg. Consider when (1) both eggs’ prices converge at $9.00, the loss from shorting brown eggs will be $1.00, and the gain of longing white eggs will be $3.00, and the total gain will be $2.00; (2) both eggs’ prices converge at $4.00, the gain from shorting brown eggs will be $4.00, and the loss of longing white eggs will be $2.00, and the total gain will be $2.00; (3) both eggs’ prices converge at $7.00, the gain from shorting brown eggs will be $1.00, and the gain of longing white eggs will be $1.00, and the total gain will be $2.00. No matter if the price increases or decreases, there exists an arbitrage opportunity once their prices converge at last.
Real life examples:

Shell Transportation vs Royal Dutch Shell: In this case, Royal Dutch Shell and Shell Transportation both share the same parent company, voting rights and preemptive rights. The only slight difference between these 2 companies is the tax treatment. In fact, they share an extremely high correlation in stock price, which are a metaphor to the brown eggs and white eggs in the aforementioned examples. Long Term Capital Management observed a more deviated price difference between them and applied a convergence trade strategy, betting that their price will converge in the future and earn an arbitrage profit from it.

Government bond: As a matter of fact, since the correlation of bonds is much higher than that of stocks, most of the convergence trade is applied in the bond market. Using 30-year US Treasury Bill as an example, it should share a very similar price to the the US Treasury bill which 29 years to maturity theoretically. However, as the newer 30-year US Treasury Bill is a more liquid financial product in the market, it should be slightly higher than the 29-year US T-bill when it is just issued. Recall the criteria to apply convergence trade: high correlation and difference in price movement. In this case, we can long the 29-year T-bill and short the newly issued 30-year T-bill and earn the arbitrage profit. 


Prerequisite of Convergence Trade:

High correlation: Sometimes people may mix up convergence trade with a long-short strategy. Long short strategy is another hedging strategy which seeks profit under a controlled risk. However, for most of the time, the long short strategy is not functioning the same as the convergence strategy. It is because convergence strategy aims more at finding assets with extremely high correlations, at the extent higher than most of the long short strategy, by math modeling and programming. This explains why I would specify that the characteristics of eggs are almost identical in the previous example. Only a high correlation in asset price can have a better guarantee that their price will converge in the future and we can undergo nearly risk-free arbitrage.

Cheap leverage cost: If we observe most of the convergence trade opportunities, the arbitrage yield is actually very small, say 0.15%. Therefore, we need to multiply our yield by leverage. However, leverage itself has a cost, and you need to pay interest for the loan. Given a low arbitrage yield, we need to have an even lower lending interest rate, which is highly dependent on your credit level. If your credit level is extremely high (say 0.001% probability that you are unable to repay the loan), the broker or bank will offer an extremely low interest rate. In short, only those with a higher credit level, like institutional investors or high net-worth individuals, are more likely to have a cheap leverage cost to realize the convergence trade.

Volatility minimization: Although institutional investors and high net worth individuals can have a very small leverage cost, large scale leverage can increase the risk very greatly within a short time. In this case, diversification needs to be considered. In usual, standard deviation is the common quantitative indicator of risk profile. A high standard deviation of portfolio indicates a higher volatility in return. For instance, a portfolio (e.g. that worths 10 million dollars) with daily standard deviation of 10% indicates that it may have a 10% positive return (earn 1 million dollars) or 10% negative return (lose 1 million dollars). To reduce the standard deviation, we have to find multiple correlated pairs of assets, but uncorrelated among the pairs. This can greatly reduce the overall standard deviation of the entire portfolio. In a nutshell, we have to construct a very diversified portfolio to reduce the risk of the portfolio. 

Important assumption - No black swan event exists:

With cheap leverage, low standard deviation, and almost riskless arbitrage profit, the strategy is actually close to flawless. However, to ensure a sustainable arbitrage, there is actually a very important assumption behind: No black swan event happens.

A black swan refers to a very negative event that has a very low probability – not likely to happen but still has a small chance to happen. In the financial market, typical black swans examples are the default of national debt and large scale financial crises. These black swan events usually result in a market panic, which people cash out from the stock market since they lose faith in it. As a result, all the strategies in the portfolio will basically share the higher correlation (due to the systematic risk) and the probability of convergence will be much smaller in the short run. From the perspective of unrealised loss in accounting, the investors will bear loss for a long time. And given a surge in standard deviation and leverage, the loss of portfolio will be greatly multiplied.

