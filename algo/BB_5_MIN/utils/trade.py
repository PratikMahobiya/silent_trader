import talib

def trade_execution(data_frame, intervals, flag, transactions, curr_time):
    for stock in data_frame['Close'].columns:
        ub,mb,lb    = talib.BBANDS(data_frame['Close'][stock], timeperiod=intervals[4])
        rsi         = talib.RSI(data_frame['Close'][stock], timeperiod=intervals[5])
        atr         = talib.ATR(data_frame['High'][stock],data_frame['Low'][stock],data_frame['Close'][stock], timeperiod=intervals[6])
        if flag[stock]['buy'] is False:
            buys(curr_time,stock, data_frame, rsi, ub, mb, lb, atr, intervals, flag, transactions)
        else:
            sell(curr_time,stock, data_frame, rsi, ub, mb, lb, atr, intervals, flag, transactions)
    return transactions

# BUYS STOCKS ; ENTRY
def buys(curr_time,stock, data_frame, rsi, ub, mb, lb, atr, intervals, flag, transactions):
  # If Perv Price is less than LowerBand and Curr Price is Greater Than LowerBand, Curr RSI is less than 40 and Curr RSI is Greater Than Prev RSI, Diff of High and Low is in BtW (ATR and ATR*2)
  if rsi[-1] < intervals[3] and rsi[-1] > rsi[-2]:
    if lb[-1] < data_frame['Close'].iloc[-1][stock] and lb[-2] > data_frame['Close'].iloc[-2][stock]:
      if (atr[-1] <= (data_frame['High'].iloc[-1][stock] - data_frame['Low'].iloc[-1][stock]) <= (atr[-1]*1.4)):
        flag[stock]['buying_price'] = data_frame['Close'].iloc[-1][stock]
        flag[stock]['buy'] = True
        flag['Entry'].append(stock)
        flag[stock]['stoploss'] = data_frame['Open'].iloc[-1][stock]
        transactions.append({'symbol':stock,'indicate':'Entry','type':'BB','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'difference':None,'profit':None})

# SELL STOCK ; EXIT
def sell(curr_time,stock, data_frame, rsi, ub, mb, lb, atr, intervals, flag, transactions):
    # Selling Points Chart
    tr = intervals[2]
    selling_chart = {0:tr, 1:tr, 2:tr+0.5, 3:tr+1.0, 4:tr+1.5, 5:tr+2.0, 6:tr+2.5, 7:tr+3.0, 8:tr+3.5, 9:tr+4.0}

    # If Price is Greater than UpperBand
    if data_frame['High'].iloc[-1][stock] > ub[-1]:
        flag[stock]['selling_price'] = data_frame['High'].iloc[-1][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'Up_Cross','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock)
        flag[stock]['upper_val'],flag[stock]['selling_val']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
        flag[stock]['stoploss'] = 0

    # When StopLoss Hits Exits
    elif data_frame['Close'].iloc[-1][stock] <= flag[stock]['stoploss']:
        flag[stock]['selling_price'] = data_frame['Close'].iloc[-1][stock]
        diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
        profit        = (diff/flag[stock]['buying_price']) * 100
        flag[stock]['buy']      = False
        transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock)
        flag[stock]['upper_val'],flag[stock]['selling_val']       = 0, 0
        flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
        flag[stock]['stoploss'] = 0

    # for Above 60 RSI Chart SYSTEM
    elif rsi[-1] >= tr:
        if rsi[-1] >= flag[stock]['upper_val']:
            counter         = int(rsi[-1] - tr)
            flag[stock]['selling_val']     = selling_chart[counter] if 0 <= counter <= 9 else rsi[-1] - 5
            flag[stock]['upper_val']       = rsi[-1]
            flag[stock]['stoploss']        = data_frame['Open'].iloc[-1][stock]
        elif rsi[-1] <= flag[stock]['selling_val'] and data_frame['Close'].iloc[-1][stock] > flag[stock]['buying_price']:
            flag[stock]['selling_price'] = data_frame['Close'].iloc[-1][stock]
            diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
            profit        = (diff/flag[stock]['buying_price']) * 100
            flag[stock]['buy']      = False
            transactions.append({'symbol':stock,'indicate':'Exit','type':'RSI','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'difference':diff,'profit':profit})
            flag['Entry'].remove(stock)
            flag[stock]['upper_val'],flag[stock]['selling_val']       = 0, 0
            flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
            flag[stock]['stoploss'] = 0

# SQUARE OFF, EXIT
def square_off(stock_name,data_frame, intervals, flag, transactions, curr_time):
    # For more than one stock in a list
    if stock_name is None:
        for stock in data_frame['Close'].columns:
            flag[stock]['selling_price'] = data_frame['Close'].iloc[-1][stock]
            diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
            profit        = (diff/flag[stock]['buying_price']) * 100
            flag[stock]['buy']      = False
            transactions.append({'symbol':stock,'indicate':'SquareOff','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'difference':diff,'profit':profit})
            flag['Entry'].remove(stock)
            flag[stock]['upper_val'],flag[stock]['selling_val']       = 0, 0
            flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
            flag[stock]['stoploss'] = 0
    # for only one stock
    else:
        flag[stock_name]['selling_price'] = data_frame['Close'].iloc[-1]
        diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
        profit        = (diff/flag[stock_name]['buying_price']) * 100
        flag[stock_name]['buy']      = False
        transactions.append({'symbol':stock_name,'indicate':'SquareOff','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'stoploss':flag[stock_name]['stoploss'],'difference':diff,'profit':profit})
        flag['Entry'].remove(stock_name)
        flag[stock_name]['upper_val'],flag[stock_name]['selling_val']       = 0, 0
        flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
        flag[stock_name]['stoploss'] = 0
    return transactions