import talib

def trending(data_frame,intervals):
    trend = []
    for stock in data_frame.columns:
        trend_ema         = talib.EMA(data_frame[stock], timeperiod=intervals[8])
        if data_frame.iloc[-1][stock] > trend_ema[-1]:
          if trend_ema[-1] > trend_ema[-2]:
            if trend_ema[-2] > trend_ema[-3]:
              if data_frame.iloc[-1][stock] > data_frame.iloc[-2][stock]:
                if data_frame.iloc[-1][stock] > data_frame.iloc[-3][stock]:
                  trend.append(stock)
    return trend