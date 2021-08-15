import talib

def target_percentile(stock,data_open, data_close, intervals, flag):
  temp_ = []
  for open,close in zip(data_open[-intervals[10]:],data_close[-intervals[10]:]):
    temp_.append(abs(((open-close)/open)*100))
  target_percent = sum(temp_)/len(temp_)
  flag[stock]['target_per'] = target_percent

def trending(data_frame,intervals,flag):
  trend = []
  for stock in data_frame['Close'].columns:
    rsi = talib.RSI(data_frame['Close'][stock], timeperiod = intervals[8])
    if rsi[-1] > 50:
      if (40 <= rsi[-2] <= 55):
        flag[stock]['trend_rsi'] = rsi[-1]
        target_percentile(stock,data_frame['Open'][stock], data_frame['Close'][stock], intervals, flag)
        trend.append(stock)
  return trend