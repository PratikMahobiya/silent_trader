import talib

def trade_execution(data_frame, intervals, flag, transactions, curr_time):
    for stock in data_frame.columns:
        ema_max     = talib.EMA(data_frame[stock], timeperiod=intervals[4])
        ema_min     = talib.EMA(data_frame[stock], timeperiod=intervals[5])
        rsi         = talib.RSI(data_frame[stock], timeperiod=intervals[9])
        if flag[stock]['buy'] is False:
            buys(stock, data_frame, ema_max, ema_min, rsi, intervals, flag, transactions, curr_time)
        else:
            sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time)
    return transactions

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, ema_max, ema_min, rsi, intervals, flag, transactions , curr_time):
    # In btw 50 and 55 and price is above ema-min-max and last 3 except curr rsi is below 55
    if data_frame.iloc[-2][stock] > ema_min[-2] and ema_min[-2] > ema_max[-2] and ((intervals[3] - 5) <= rsi[-2] <= intervals[3]):
      if rsi[-3] < intervals[3] and rsi[-4] < intervals[3] and rsi[-5] < intervals[3]:
        flag[stock]['buying_price'] = data_frame.iloc[-2][stock]
        flag[stock]['buy'] = True
        flag[stock]['stoploss'] = flag[stock]['buying_price'] - flag[stock]['buying_price']*0.0025
        flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
        flag['Entry'].append(stock)
        flag[stock]['ema_min'], flag[stock]['ema_max'] = ema_min[-2], ema_max[-2]
        transactions.append({'symbol':stock,'indicate':'Entry','type':'RSI_55','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-2],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':flag[stock]['ema_max'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'trend_rsi':flag[stock]['trend_rsi'],'target_hit':flag[stock]['target_hit']})
        flag[stock]['trend_rsi'] = 0
    
    # Difference btw ema-max-min is less or equal to 0.2 and price is above ema-min-max
    elif ema_max[-2] > ema_min[-2]:
      if data_frame.iloc[-2][stock] > ema_min[-2]:
        if data_frame.iloc[-2][stock] > ema_max[-2]:
          if ((((ema_max[-2]-ema_min[-2])/ema_max[-2])*100) <= 0.2):
            flag[stock]['buying_price'] = data_frame.iloc[-2][stock]
            flag[stock]['buy'] = True
            flag[stock]['stoploss'] = flag[stock]['buying_price'] - flag[stock]['buying_price']*0.0025
            flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
            flag['Entry'].append(stock)
            flag[stock]['ema_min'], flag[stock]['ema_max'] = ema_min[-2], ema_max[-2]
            transactions.append({'symbol':stock,'indicate':'Entry','type':'CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-2],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':flag[stock]['ema_max'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'trend_rsi':flag[stock]['trend_rsi'],'target_hit':flag[stock]['target_hit']})
            flag[stock]['trend_rsi'] = 0

# SELL STOCK ; EXIT
def sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time):
    # Price is below ema-min and rsi is below 50
    tr = intervals[3] - 5
    if data_frame.iloc[-2][stock] < ema_min[-2] and rsi[-2] < tr:
        flag[stock]['selling_price'] = data_frame.iloc[-2][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'E-R_EXIT','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-2],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
        flag['Entry'].remove(stock)
        flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
        flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
        flag[stock]['target_hit'] = 0

    # Update StopLoss by -0.25% of its curr price if it reaches its target% of its Buying price
    elif data_frame.iloc[-2][stock] >= flag[stock]['target']:
        flag[stock]['stoploss'] = data_frame.iloc[-2][stock] - data_frame.iloc[-2][stock]*0.0025
        flag[stock]['target'] = data_frame.iloc[-2][stock]
        flag[stock]['target_hit'] += 1
    
    # if price hits StopLoss, Exit
    elif data_frame.iloc[-2][stock] <= flag[stock]['stoploss']:
        flag[stock]['selling_price'] = data_frame.iloc[-2][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-2],'target':flag[stock]['target'],'emamin':flag[stock]['ema_min'],'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
        flag['Entry'].remove(stock)
        flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
        flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
        flag[stock]['target_hit'] = 0

# SQUARE OFF, EXIT
def square_off(stock_name,data_frame, intervals, flag, transactions, curr_time):
    # For more than one stock in a list
    if stock_name is None:
        for stock in data_frame.columns:
            rsi         = talib.RSI(data_frame[stock], timeperiod=intervals[9])
            flag[stock]['selling_price'] = data_frame.iloc[-2][stock]
            diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
            profit        = (diff/flag[stock]['buying_price']) * 100
            flag[stock]['buy']      = False
            transactions.append({'symbol':stock,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-2],'target':flag[stock]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock]['target_hit']})
            flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
            flag[stock]['ema_min'], flag[stock]['ema_max']       = 0, 0
            flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
            flag['Entry'].remove(stock)
            flag[stock]['target_hit'] = 0
    # for only one stock
    else:
        rsi         = talib.RSI(data_frame, timeperiod=intervals[9])
        flag[stock_name]['selling_price'] = data_frame.iloc[-2]
        diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
        profit        = (diff/flag[stock_name]['buying_price']) * 100
        flag[stock_name]['buy']      = False
        transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'stoploss':flag[stock_name]['stoploss'],'rsi':rsi[-2],'target':flag[stock_name]['target'],'emamin':None,'emamax':None,'target_percent':None,'difference':diff,'profit':profit,'trend_rsi':None,'target_hit':flag[stock_name]['target_hit']})
        flag[stock_name]['stoploss'], flag[stock_name]['target'], flag[stock_name]['target_per'] = 0, 0, 0
        flag[stock_name]['ema_min'], flag[stock_name]['ema_max']       = 0, 0
        flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
        flag['Entry'].remove(stock_name)
        flag[stock_name]['target_hit'] = 0
    return transactions