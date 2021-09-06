import talib

def checking_stoploss(data_frame, stock):
  per = ((data_frame['Close'].iloc[-2][stock]-data_frame['Low'].iloc[-2][stock])/data_frame['Close'].iloc[-2][stock])*100
  if per > 0.3:
    stoploss_val = data_frame['Close'].iloc[-2][stock] - (data_frame['Close'].iloc[-2][stock] * 0.002)
    per = 0.2
  else:
    stoploss_val = data_frame['Low'].iloc[-2][stock]
  return per, stoploss_val


def trade_execution(data_frame, intervals, flag, transactions, curr_time):
    for stock in data_frame['Close'].columns:
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
  if ema_max[-2] > ema_min[-2]:
    if data_frame['Close'].iloc[-2][stock] > ema_min[-2]:
      if data_frame['Close'].iloc[-2][stock] > ema_max[-2]:
        if data_frame['Close'].iloc[-3][stock] > ema_min[-3]:
          if data_frame['Close'].iloc[-3][stock] > ema_max[-3]:
            if ((((ema_max[-2]-ema_min[-2])/ema_max[-2])*100) <= 0.2):
              flag[stock]['buying_price'] = data_frame['Close'].iloc[-2][stock]
              flag[stock]['buy'] = True
              stoploss_per, flag[stock]['stoploss'] = checking_stoploss(data_frame,stock) # data_frame['Low'].iloc[-2][stock]
              flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
              flag['Entry'].append(stock)
              transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'stoploss_percent':stoploss_per})

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.1, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-2] > ema_max[-2]:
    if ema_min[-3] < ema_max[-3]:
      if data_frame['Close'].iloc[-2][stock] > ema_min[-2]:
        if data_frame['Close'].iloc[-2][stock] > ema_max[-2]:
          if data_frame['Close'].iloc[-3][stock] > ema_min[-3]:
            if data_frame['Close'].iloc[-3][stock] > ema_max[-3]:
              if ((((ema_min[-2]-ema_max[-2])/ema_min[-2])*100) <= 0.2):
                if rsi[-2] > rsi[-3] and rsi[-2] > rsi[-4]:
                  flag[stock]['buying_price'] = data_frame['Close'].iloc[-2][stock]
                  flag[stock]['buy'] = True
                  stoploss_per, flag[stock]['stoploss'] = checking_stoploss(data_frame,stock) # data_frame['Low'].iloc[-2][stock]
                  flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
                  flag['Entry'].append(stock)
                  transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'stoploss_percent':stoploss_per})

# SELL STOCK ; EXIT
def sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time):
  # Exit when Target Hits
  if data_frame['High'].iloc[-2][stock] >= flag[stock]['target']:
    flag[stock]['selling_price'] = data_frame['High'].iloc[-2][stock]
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_HIT','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
  
  # if price hits StopLoss, Exit
  elif data_frame['Low'].iloc[-2][stock] <= flag[stock]['stoploss']:
    flag[stock]['selling_price'] = flag[stock]['stoploss']
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0

# SQUARE OFF, EXIT
def square_off(stock_name,data_frame, intervals, flag, transactions, curr_time):
  # For more than one stock in a list
  if stock_name is None:
    for stock in data_frame['Close'].columns:
      rsi         = talib.RSI(data_frame['Close'][stock], timeperiod=intervals[9])
      flag[stock]['selling_price'] = data_frame['Close'].iloc[-2][stock]
      diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
      profit        = (diff/flag[stock]['buying_price']) * 100
      flag[stock]['buy']      = False
      transactions.append({'symbol':stock,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'stoploss_percent':None})
      flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
      flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
      flag['Entry'].remove(stock)
  # for only one stock
  else:
    rsi         = talib.RSI(data_frame['Close'], timeperiod=intervals[9])
    flag[stock_name]['selling_price'] = data_frame['Close'].iloc[-2]
    diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
    profit        = (diff/flag[stock_name]['buying_price']) * 100
    flag[stock_name]['buy']      = False
    transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'target_percent':None,'difference':diff,'profit':profit,'stoploss_percent':None})
    flag[stock_name]['stoploss'], flag[stock_name]['target'], flag[stock_name]['target_per'] = 0, 0, 0
    flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
    flag['Entry'].remove(stock_name)
  return transactions