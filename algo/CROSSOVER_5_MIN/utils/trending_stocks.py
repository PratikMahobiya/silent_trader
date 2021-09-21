from datetime import datetime
import talib

def trending(data_frame,for_trend_stocks,intervals,flag):
  trend = []
  flag['Trend'].clear()
  flag['Trend_2'].clear()
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] > 50:
      trend.append(stock)
      flag['Trend'].append(stock)
      flag[stock]['trend'] = True
    elif 40 <= rsi[-1] <= 50:
      flag['Trend_2'].append(stock)
      flag[stock]['trend'] = False      
    else:
      flag[stock]['trend'] = False
  return trend