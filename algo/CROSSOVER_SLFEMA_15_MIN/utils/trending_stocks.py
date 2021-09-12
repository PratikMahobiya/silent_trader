import talib

def trending(data_frame,intervals,flag):
  trend = []
  flag['Trend'].clear()
  for stock in data_frame['Close'].columns:
    rsi = talib.RSI(data_frame['Close'][stock], timeperiod = intervals[8])
    atr = talib.ATR(data_frame['High'][stock],data_frame['Low'][stock],data_frame['Close'][stock], timeperiod=intervals[10])
    if rsi[-1] > 50:
      flag[stock]['atr_2'] = atr[-1]
      trend.append(stock)
      flag['Trend'].append(stock)
  return trend