from datetime import datetime
import talib

def trending_30(data_frame,for_trend_stocks,intervals,flag):
  trend = []
  flag['Trend_30'].clear()
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] > 50:
      trend.append(stock)
      flag['Trend_30'].append(stock)
  return trend

def trending_15(data_frame,for_trend_stocks,intervals,flag):
  trend = []
  flag['Trend_15'].clear()
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] > 50:
      trend.append(stock)
      flag['Trend_15'].append(stock)
      flag[stock]['trend'] = True
    else:
      flag[stock]['trend'] = False
  return trend

