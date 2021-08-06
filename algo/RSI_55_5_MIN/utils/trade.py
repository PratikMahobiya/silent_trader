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
    # In btw 50 and 55 and price is above ema-min-max
    if data_frame.iloc[-1][stock] > ema_min[-1] and ema_min[-1] > ema_max[-1] and ((intervals[3] - 5) <= rsi[-1] <= intervals[3]):
        flag[stock]['buying_price'] = data_frame.iloc[-1][stock]
        flag[stock]['buy'] = True
        flag[stock]['stoploss'] = flag[stock]['buying_price'] - flag[stock]['buying_price']*0.005
        flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*0.01
        flag['Entry'].append(stock)
        transactions.append({'symbol':stock,'indicate':'Entry','type':'RSI_55','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':None,'difference':None,'profit':None})
    
    # Difference btw ema-max-min is less or equal to 0.1 and price is above ema-min-max
    elif ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.1) and data_frame.iloc[-1][stock] > ema_min[-1] and data_frame.iloc[-1][stock] > ema_max[-1] and ema_max[-1] > ema_min[-1]:
        flag[stock]['buying_price'] = data_frame.iloc[-1][stock]
        flag[stock]['buy'] = True
        flag[stock]['stoploss'] = flag[stock]['buying_price'] - flag[stock]['buying_price']*0.005
        flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*0.01
        flag['Entry'].append(stock)
        transactions.append({'symbol':stock,'indicate':'Entry','type':'CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-2],'rsi_exit_target':None,'difference':None,'profit':None})

# SELL STOCK ; EXIT
def sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time):
    # Price is below ema-min and rsi is below 50
    tr = intervals[3] - 5
    if data_frame.iloc[-1][stock] < ema_min[-1] and rsi[-1] < tr:
        flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'E-R_EXIT','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock)
        flag[stock]['stoploss'], flag[stock]['target'] = 0, 0
        flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0

    # Update StopLoss by -0.3% of its curr price if it reaches 1% of its Buying price
    elif data_frame.iloc[-1][stock] >= flag[stock]['target']:
        flag[stock]['stoploss'] = data_frame.iloc[-1][stock] - data_frame.iloc[-1][stock]*0.003
        flag[stock]['target'] = data_frame.iloc[-1][stock]
    
    # if price hits StopLoss, Exit
    elif data_frame.iloc[-1][stock] <= flag[stock]['stoploss']:
        flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock)
        flag[stock]['stoploss'], flag[stock]['target'] = 0, 0
        flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0

# SQUARE OFF, EXIT
def square_off(stock_name,data_frame, intervals, flag, transactions, curr_time):
    # For more than one stock in a list
    if stock_name is None:
        for stock in data_frame.columns:
            rsi         = talib.RSI(data_frame[stock], timeperiod=intervals[9])
            flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
            diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
            profit        = (diff/flag[stock]['buying_price']) * 100
            flag[stock]['buy']      = False
            transactions.append({'symbol':stock,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
            flag[stock]['stoploss'], flag[stock]['target'] = 0, 0
            flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
            flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
            flag['Entry'].remove(stock)
    # for only one stock
    else:
        rsi         = talib.RSI(data_frame, timeperiod=intervals[9])
        flag[stock_name]['selling_price'] = data_frame.iloc[-1]
        diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
        profit        = (diff/flag[stock_name]['buying_price']) * 100
        flag[stock_name]['buy']      = False
        transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'stoploss':flag[stock_name]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock_name]['selling_val'],'difference':diff,'profit':profit})
        flag[stock_name]['stoploss'], flag[stock_name]['target'] = 0, 0
        flag[stock_name]['upper_val'], flag[stock_name]['selling_val']       = 0, 0
        flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
        flag['Entry'].remove(stock_name)
    return transactions