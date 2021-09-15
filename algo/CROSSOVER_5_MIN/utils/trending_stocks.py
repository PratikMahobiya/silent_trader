from datetime import datetime
import talib

def trending_15(data_frame,for_trend_stocks,intervals,flag):
  trend = []
  flag['Trend'].clear()
  if (0 <= datetime.now().time().minute < 4) or (15 <= datetime.now().time().minute < 19) or (30 <= datetime.now().time().minute < 34) or (45 <= datetime.now().time().minute < 49):
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
      if rsi[-1] > 50:
        trend.append(stock)
        flag['Trend'].append(stock)
  else:
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'], timeperiod = intervals[8])
      if rsi[-1] > 50:
        trend.append(stock)
        flag['Trend'].append(stock)
  return trend

def trending_30(data_frame,for_trend_stocks,intervals,flag):
  trend = []
  flag['Trend'].clear()
  if (15 <= datetime.now().time().minute < 30) or (45 <= datetime.now().time().minute < 59):
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
      if rsi[-1] > 50:
        trend.append(stock)
        flag['Trend'].append(stock)
  else:
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'], timeperiod = intervals[8])
      if rsi[-1] > 50:
        trend.append(stock)
        flag['Trend'].append(stock)
  return trend
