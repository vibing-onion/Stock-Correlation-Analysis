import pandas as pd
import matplotlib.pyplot as plt

def plot_price(ax, df, stockA, stockB, period = 0):
    ax.plot(df.iloc[-period:, 0].index, df.iloc[-period:, 0], label = stockA)
    ax.plot(df.iloc[-period:, 1].index, df.iloc[-period:, 1], label = stockB)
    ax.plot(df.iloc[-period:, 0].index, 
            (df.iloc[-period:, 0]+df.iloc[-period:, 1])/2,
            label = "mean")
    ax.legend()

def get_threshold(ax, df, period = 0):
    ax.plot(df.iloc[-period:, 0].index, abs(df.iloc[-period:, 0] - df.iloc[-period:, 1]), label='gap')
    ax.axhline(y=abs(df.iloc[-period:, 0]-df.iloc[-period:, 1]).quantile(0.95), color='red', linestyle='--')
    ax.axhline(y=abs(df.iloc[-period:, 0]-df.iloc[-period:, 1]).quantile(0.90), color='red', linestyle='--')
    ax.legend()

