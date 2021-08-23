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
  if ema_max[-3] > ema_min[-3]:
    if data_frame['Close'].iloc[-3][stock] > ema_min[-3]:
      if data_frame['Close'].iloc[-3][stock] > ema_max[-3]:
        if data_frame['Close'].iloc[-4][stock] > ema_min[-4]:
          if data_frame['Close'].iloc[-4][stock] > ema_max[-4]:
            if ((((ema_max[-3]-ema_min[-3])/ema_max[-3])*100) <= 0.2):
              flag[stock]['buying_price'] = data_frame['Close'].iloc[-3][stock]
              flag[stock]['buy'] = True
              flag[stock]['stoploss'] = data_frame['Low'].iloc[-3][stock]
              flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
              flag['Entry'].append(stock)
              flag[stock]['ema_min'], flag[stock]['ema_max'] = ema_min[-3], ema_max[-3]
              transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-3],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':flag[stock]['ema_max'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'trend_rsi':flag[stock]['trend_rsi'],'target_hit':flag[stock]['target_hit']})
              flag[stock]['trend_rsi'] = 0

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.1, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-3] > ema_max[-3]:
    if ema_min[-4] < ema_max[-4]:
      if data_frame['Close'].iloc[-3][stock] > ema_min[-3]:
        if data_frame['Close'].iloc[-3][stock] > ema_max[-3]:
          if data_frame['Close'].iloc[-4][stock] > ema_min[-4]:
            if data_frame['Close'].iloc[-4][stock] > ema_max[-4]:
              if ((((ema_min[-3]-ema_max[-3])/ema_min[-3])*100) <= 0.2):
                if rsi[-3] > rsi[-4] and rsi[-3] > rsi[-5]:
                  flag[stock]['buying_price'] = data_frame['Close'].iloc[-3][stock]
                  flag[stock]['buy'] = True
                  flag[stock]['stoploss'] = data_frame['Low'].iloc[-3][stock]
                  flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
                  flag['Entry'].append(stock)
                  flag[stock]['ema_min'], flag[stock]['ema_max'] = ema_min[-3], ema_max[-3]
                  transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-3],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':flag[stock]['ema_max'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'trend_rsi':flag[stock]['trend_rsi'],'target_hit':flag[stock]['target_hit']})
                  flag[stock]['trend_rsi'] = 0

# SELL STOCK ; EXIT
def sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time):
  # Exit when Target Hits
  if data_frame['High'].iloc[-3][stock] >= flag[stock]['target']:
    flag[stock]['selling_price'] = data_frame['High'].iloc[-3][stock]
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_HIT','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-3],'target':flag[stock]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['target_hit'] = 0
  
  # if price hits StopLoss, Exit
  elif data_frame['Close'].iloc[-3][stock] <= flag[stock]['stoploss']:
    flag[stock]['selling_price'] = data_frame['Close'].iloc[-3][stock]
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-3],'target':flag[stock]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['target_hit'] = 0

# SQUARE OFF, EXIT
def square_off(data_frame,trade_stock_list, intervals, flag, transactions, curr_time):
  for stock in trade_stock_list:
    rsi         = talib.RSI(data_frame['Close'][stock], timeperiod=intervals[9])
    flag[stock]['selling_price'] = data_frame['Close'].iloc[-3][stock]
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-3],'target':flag[stock]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag['Entry'].remove(stock)
    flag[stock]['target_hit'] = 0
  return transactions