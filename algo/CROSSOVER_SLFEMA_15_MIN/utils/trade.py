import talib
from . import zerodha_action

def checking_stoploss(data_frame, stock, flag, ema_max, ema_min):
  for i in range(len(data_frame['Close'][stock])):
    if i != 0:
      if (data_frame['Close'].iloc[-i][stock] < ema_min[-i]) or (data_frame['Close'].iloc[-i][stock] < ema_max[-i]):
        break
      stoploss_val = data_frame['Open'].iloc[-i][stock]
  buy_price = flag[stock]['buying_price']
  per = ((buy_price - stoploss_val)/buy_price)*100
  return round(per,2), stoploss_val

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
  # Difference btw ema-max-min is less or equal to 0.2 and price is above ema-min-max
  if ema_max[-1] > ema_min[-1]:
    if data_frame['Close'].iloc[-1][stock] > ema_min[-1]:
      if data_frame['Close'].iloc[-1][stock] > ema_max[-1]:
        if data_frame['Close'].iloc[-2][stock] > ema_min[-2]:
          if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.2):
            # Place Order in ZERODHA.
            # -------------------------------------------
            order_id, error_status = zerodha_action.place_regular_buy_order(kite_conn_var,stock,flag)
            flag[stock]['order_id'] = order_id
            flag[stock]['order_status'] = error_status
            # -------------------------------------------
            flag['Entry'].append(stock)
            flag[stock]['buy'] = True
            stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(data_frame,stock,flag,ema_max,ema_min)
            flag[stock]['target_1'] = flag[stock]['buying_price'] + flag[stock]['atr_1']
            flag[stock]['target_2'] = flag[stock]['buying_price'] + flag[stock]['atr_2']
            transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.1, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] > ema_max[-1]:
    if ema_min[-2] < ema_max[-2]:
      if data_frame['Close'].iloc[-1][stock] > ema_min[-1]:
        if data_frame['Close'].iloc[-1][stock] > ema_max[-1]:
          if data_frame['Close'].iloc[-2][stock] > ema_min[-2]:
            if data_frame['Close'].iloc[-2][stock] > ema_max[-2]:
              if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.2):
                if rsi[-1] > rsi[-2] and rsi[-1] > rsi[-3]:
                  # Place Order in ZERODHA.
                  # -------------------------------------------
                  order_id, error_status = zerodha_action.place_regular_buy_order(kite_conn_var,stock,flag)
                  flag[stock]['order_id'] = order_id
                  flag[stock]['order_status'] = error_status
                  # -------------------------------------------
                  flag['Entry'].append(stock)
                  flag[stock]['buy'] = True
                  flag[stock]['target_1'] = flag[stock]['buying_price'] + flag[stock]['atr_1']
                  flag[stock]['target_2'] = flag[stock]['buying_price'] + flag[stock]['atr_2']
                  stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(data_frame,stock,flag,ema_max,ema_min)
                  flag[stock]['target'] = flag[stock]['buying_price'] + atr[-1]
                  transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})
