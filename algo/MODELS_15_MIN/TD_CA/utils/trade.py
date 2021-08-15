import talib

def trade_execution(data_frame, trade_stock_list, intervals, flag, transactions, curr_time):
    for stock in trade_stock_list:
        ema_max     = talib.EMA(data_frame['Close'][stock], timeperiod=intervals[4])
        ema_min     = talib.EMA(data_frame['Close'][stock], timeperiod=intervals[5])
        rsi         = talib.RSI(data_frame['Close'][stock], timeperiod=intervals[9])
        if flag[stock]['buy'] is False:
            buys(stock, data_frame, ema_max, ema_min, rsi, intervals, flag, transactions, curr_time)
        else:
            sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time)
    return transactions

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, ema_max, ema_min, rsi, intervals, flag, transactions , curr_time):
  # Difference btw ema-max-min is less or equal to 0.1 and price is above ema-min-max
  if ema_max[-1] > ema_min[-1]:
    if data_frame['Close'].iloc[-1][stock] > ema_min[-1]:
      if data_frame['Close'].iloc[-1][stock] > ema_max[-1]:
        if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.2):
          flag[stock]['buying_price'] = data_frame['Close'].iloc[-1][stock]
          flag[stock]['buy'] = True
          flag[stock]['stoploss'] = data_frame['Low'].iloc[-1][stock]
          flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
          flag['Entry'].append(stock)
          flag[stock]['ema_min'], flag[stock]['ema_max'] = ema_min[-1], ema_max[-1]
          transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':flag[stock]['ema_max'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'trend_rsi':flag[stock]['trend_rsi'],'target_hit':flag[stock]['target_hit']})
          flag[stock]['trend_rsi'] = 0

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.1, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] > ema_max[-1] and ema_min[-2] < ema_max[-2]:
    if data_frame['Close'].iloc[-1][stock] > ema_min[-1]:
      if data_frame['Close'].iloc[-1][stock] > ema_max[-1]:
        if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.2):
          if rsi[-1] > rsi[-2] and rsi[-1] > rsi[-3]:
            flag[stock]['buying_price'] = data_frame['Close'].iloc[-1][stock]
            flag[stock]['buy'] = True
            flag[stock]['stoploss'] = data_frame['Low'].iloc[-1][stock]
            flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
            flag['Entry'].append(stock)
            flag[stock]['ema_min'], flag[stock]['ema_max'] = ema_min[-1], ema_max[-1]
            transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':flag[stock]['ema_max'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'trend_rsi':flag[stock]['trend_rsi'],'target_hit':flag[stock]['target_hit']})
            flag[stock]['trend_rsi'] = 0

# SELL STOCK ; EXIT
def sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time):
  # Exit when Target Hits
  if data_frame['High'].iloc[-1][stock] >= flag[stock]['target']:
    flag[stock]['target'] = data_frame['High'].iloc[-1][stock]
    flag[stock]['stoploss'] = data_frame['Low'].iloc[-1][stock]
    flag[stock]['target_hit'] += 1
  
  # if price hits StopLoss, Exit
  elif data_frame['Close'].iloc[-1][stock] <= flag[stock]['stoploss']:
    flag[stock]['selling_price'] = data_frame['Close'].iloc[-1][stock]
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'target':flag[stock]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['target_hit'] = 0

  # Price is below ema-min and rsi is below 50
  elif data_frame['Close'].iloc[-1][stock] < ema_min[-1] and rsi[-1] < (intervals[3] - 5):
    flag[stock]['selling_price'] = data_frame['Close'].iloc[-1][stock]
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'E-R_EXIT','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'target':flag[stock]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['target_hit'] = 0

# SQUARE OFF, EXIT
def square_off(data_frame,trade_stock_list, intervals, flag, transactions, curr_time):
  for stock in trade_stock_list:
    rsi         = talib.RSI(data_frame['Close'][stock], timeperiod=intervals[9])
    flag[stock]['selling_price'] = data_frame['Close'].iloc[-1][stock]
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'target':flag[stock]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag['Entry'].remove(stock)
    flag[stock]['target_hit'] = 0
  return transactions