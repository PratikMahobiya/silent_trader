from datetime import datetime
import talib

def trending(data_frame,for_trend_stocks,intervals,flag):
  trend = []
  flag['Trend'].clear()
  if (15 <= datetime.now().time().minute < 30) or (45 <= datetime.now().time().minute < 59):
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
      atr = talib.ATR(data_frame[stock]['High'].iloc[:-1],data_frame[stock]['Low'].iloc[:-1],data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[10])
      if rsi[-1] > 50:
        trend.append(stock)
        flag['Trend'].append(stock)
        flag[stock]['atr_2'] = atr[-1]
  else:
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'], timeperiod = intervals[8])
      atr = talib.ATR(data_frame[stock]['High'],data_frame[stock]['Low'],data_frame[stock]['Close'], timeperiod=intervals[10])
      if rsi[-1] > 50:
        trend.append(stock)
        flag['Trend'].append(stock)
        flag[stock]['atr_2'] = atr[-1]
  return trend