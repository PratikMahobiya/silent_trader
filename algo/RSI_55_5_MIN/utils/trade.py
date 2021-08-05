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
    if data_frame.iloc[-1][stock] > ema_min[-1] and ema_min[-1] > ema_max[-1] and ((intervals[3] - 5) <= rsi[-1] <= intervals[3]):
        flag[stock]['buying_price'] = data_frame.iloc[-1][stock]
        flag[stock]['buy'] = True
        flag[stock]['stoploss'] = flag[stock]['buying_price'] - flag[stock]['buying_price']*0.0010
        flag['Entry'].append(stock)
        transactions.append({'symbol':stock,'indicate':'Entry','type':'RSI','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':None,'difference':None,'profit':None})
    elif ema_max[-3] > ema_min[-3] and ema_max[-2] > ema_min[-2] and ema_max[-1] < ema_min[-1] and data_frame.iloc[-1][stock] > ema_min[-1]:
        flag[stock]['buying_price'] = data_frame.iloc[-1][stock]
        flag[stock]['buy'] = True
        flag[stock]['stoploss'] = flag[stock]['buying_price'] - flag[stock]['buying_price']*0.0010
        flag['Entry'].append(stock)
        transactions.append({'symbol':stock,'indicate':'Entry','type':'RSI','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-2],'rsi_exit_target':None,'difference':None,'profit':None})

# SELL STOCK ; EXIT
def sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time):
    # Selling Points Chart
    tr = intervals[2]
    selling_chart = {0:tr, 1:tr, 2:tr+0.5, 3:tr+1.0, 4:tr+1.5, 5:tr+2.0, 6:tr+2.5, 7:tr+3.0, 8:tr+3.5, 9:tr+4.0}

    if rsi[-1] >= tr:
        if rsi[-1] >= flag[stock]['upper_val']:
            counter         = int(rsi[-1] - tr)
            flag[stock]['selling_val']     = selling_chart[counter] if 0 <= counter <= 9 else rsi[-1] - 5
            flag[stock]['upper_val']       = rsi[-1]
        elif rsi[-1] <= flag[stock]['selling_val'] and data_frame.iloc[-1][stock] > flag[stock]['buying_price']:
            flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
            diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
            profit        = (diff/flag[stock]['buying_price']) * 100
            flag[stock]['buy']      = False
            transactions.append({'symbol':stock,'indicate':'Exit','type':'RSI','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
            flag['Entry'].remove(stock)
            flag[stock]['stoploss'] = 0
            flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
            flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0

    elif rsi[-2] > tr and rsi[-1] < tr:
        flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'DIP_RSI','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock)
        flag[stock]['stoploss'] = 0
        flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    
    elif data_frame.iloc[-1][stock] <= ema_min[-1] and data_frame.iloc[-2][stock] <= ema_min[-2]:
        flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'EMA_EXIT','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock)
        flag[stock]['stoploss'] = 0
        flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    
    elif data_frame.iloc[-1][stock] <= flag[stock]['stoploss']:
        flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock)
        flag[stock]['stoploss'] = 0
        flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0

# SQUARE OFF, EXIT
def square_off(stock_name,data_frame, intervals, flag, transactions, curr_time):
    if stock_name is None:
        for stock in data_frame.columns:
            rsi         = talib.RSI(data_frame[stock], timeperiod=intervals[9])
            flag[stock]['selling_price'] = data_frame.iloc[-1][stock]
            diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
            profit        = (diff/flag[stock]['buying_price']) * 100
            flag[stock]['buy']      = False
            transactions.append({'symbol':stock,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock]['selling_val'],'difference':diff,'profit':profit})
            flag[stock]['stoploss'] = 0
            flag[stock]['upper_val'], flag[stock]['selling_val']       = 0, 0
            flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
            flag['Entry'].remove(stock)
    else:
        rsi         = talib.RSI(data_frame, timeperiod=intervals[9])
        flag[stock_name]['selling_price'] = data_frame.iloc[-1]
        diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
        profit        = (diff/flag[stock_name]['buying_price']) * 100
        flag[stock_name]['buy']      = False
        transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['buying_price'],'stoploss':flag[stock_name]['stoploss'],'rsi':rsi[-1],'rsi_exit_target':flag[stock_name]['selling_val'],'difference':diff,'profit':profit})
        flag[stock_name]['stoploss'] = 0
        flag[stock_name]['upper_val'], flag[stock_name]['selling_val']       = 0, 0
        flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
        flag['Entry'].remove(stock_name)
    return transactions