import talib

def trending(data_frame,intervals,flag):
  trend = []
  flag['Trend'].clear()
  for stock in data_frame['Close'].columns:
    rsi = talib.RSI(data_frame['Close'][stock], timeperiod = intervals[8])
    if rsi[-1] > 50:
      trend.append(stock)
      flag['Trend'].append(stock)
  return trend