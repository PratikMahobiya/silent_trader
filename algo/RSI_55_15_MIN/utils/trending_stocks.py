import talib

def trending(data_frame,intervals):
  trend = []
  for stock in data_frame.columns:
    rsi = talib.RSI(data_frame[stock], timeperiod = intervals[8])
    if rsi[-1] > 50:
      if rsi[-1] > rsi[-2]:
        if rsi[-1] > rsi[-3]:
          if rsi[-2] > rsi[-3]:
            trend.append(stock)
  return trend