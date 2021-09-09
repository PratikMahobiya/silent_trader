import talib
from . import zerodha_action

def checking_stoploss(data_frame, stock, ema_max, ema_min):
  for i in range(len(data_frame['Close'][stock])):
    if i != 0:
      if (data_frame['Close'].iloc[-i][stock] < ema_min[-i]) or (data_frame['Close'].iloc[-i][stock] < ema_max[-i]):
        break
      stoploss_val = data_frame['Open'].iloc[-i][stock]
  per = ((data_frame['Close'].iloc[-1][stock] - stoploss_val)/data_frame['Close'].iloc[-1][stock])*100
  return round(per,1), round(stoploss_val,1)

def trade_execution(data_frame, intervals, flag, transactions, curr_time, kite_conn_var):
    for stock in data_frame['Close'].columns:
        ema_max     = talib.EMA(data_frame['Close'][stock], timeperiod=intervals[4])
        ema_min     = talib.EMA(data_frame['Close'][stock], timeperiod=intervals[5])
        rsi         = talib.RSI(data_frame['Close'][stock], timeperiod=intervals[9])
        atr         = talib.ATR(data_frame['High'][stock],data_frame['Low'][stock],data_frame['Close'][stock], timeperiod=intervals[10])
        if flag[stock]['buy'] is False:
            buys(stock, data_frame, ema_max, ema_min, rsi, atr, intervals, flag, transactions, curr_time, kite_conn_var)
    return transactions

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, ema_max, ema_min, rsi, atr, intervals, flag, transactions , curr_time, kite_conn_var):
  # Difference btw ema-max-min is less or equal to 0.1 and price is above ema-min-max
  if ema_max[-1] > ema_min[-1]:
    if data_frame['Close'].iloc[-1][stock] > ema_min[-1]:
      if data_frame['Close'].iloc[-1][stock] > ema_max[-1]:
        if data_frame['Close'].iloc[-2][stock] > ema_min[-2]:
          # if data_frame['Close'].iloc[-2][stock] > ema_max[-2]:
            if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.2):
              flag[stock]['buying_price'] = round(data_frame['Close'].iloc[-1][stock],1)
              stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(data_frame,stock,ema_max,ema_min)
              flag[stock]['target'] = round((flag[stock]['buying_price'] + atr[-1]),1) # flag[stock]['buying_price']*(flag[stock]['target_per']/100)
              # Place Order in ZERODHA.
              # -------------------------------------------
              # order_id, error_status, exit_id = zerodha_action.place_cover_order(kite_conn_var,stock,flag[stock]['stoploss'])
              order_id, error_status, exit_id = 1, 'SUCCESSFULLY_PLACED', 1
              flag[stock]['order_id'] = order_id
              flag[stock]['exit_id'] = exit_id
              flag[stock]['order_status'] = error_status
              # -------------------------------------------
              if order_id != 0:
                flag['Entry'].append(stock)
                flag[stock]['buy'] = True
                transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'exit_id':flag[stock]['exit_id'],'stoploss_percent':stoploss_per})

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.1, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] > ema_max[-1]:
    if ema_min[-2] < ema_max[-2]:
      if data_frame['Close'].iloc[-1][stock] > ema_min[-1]:
        if data_frame['Close'].iloc[-1][stock] > ema_max[-1]:
          if data_frame['Close'].iloc[-2][stock] > ema_min[-2]:
            # if data_frame['Close'].iloc[-2][stock] > ema_max[-2]:
              if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.2):
                if rsi[-1] > rsi[-2] and rsi[-1] > rsi[-3]:
                  flag[stock]['buying_price'] = round(data_frame['Close'].iloc[-1][stock],1)
                  stoploss_per, flag[stock]['stoploss'] = checking_stoploss(data_frame,stock,ema_max,ema_min)
                  flag[stock]['target'] = round((flag[stock]['buying_price'] + atr[-1]),1) # flag[stock]['buying_price']*(flag[stock]['target_per']/100)
                  # Place Order in ZERODHA.
                  # -------------------------------------------
                  # order_id, error_status, exit_id = zerodha_action.place_cover_order(kite_conn_var,stock,flag[stock]['stoploss'])
                  order_id, error_status, exit_id = 1, 'SUCCESSFULLY_PLACED', 1
                  flag[stock]['order_id'] = order_id
                  flag[stock]['exit_id'] = exit_id
                  flag[stock]['order_status'] = error_status
                  # -------------------------------------------
                  if order_id != 0:
                    flag['Entry'].append(stock)
                    flag[stock]['buy'] = True
                    transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'exit_id':flag[stock]['exit_id'],'stoploss_percent':stoploss_per})