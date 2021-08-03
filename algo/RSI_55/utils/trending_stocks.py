import talib

def trending(data_frame,intervals):
    trend = []
    for stock in data_frame.columns:
        trend_ema         = talib.EMA(data_frame[stock], timeperiod=intervals[8])
        if data_frame.iloc[-1][stock] > trend_ema[-1] and data_frame.iloc[-1][stock] > data_frame.iloc[-2][stock] and trend_ema[-1] > trend_ema[-2] and trend_ema[-1] > trend_ema[-3]:
            trend.append(stock)
    return trend