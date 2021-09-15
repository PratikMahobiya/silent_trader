import talib
from . import zerodha_action

def checking_stoploss(stock,flag, atr):
  price = flag[stock]['buying_price']
  stoploss_val = price - atr[-1]*0.7
  per = ((price-stoploss_val)/price)*100
  return round(per,2), round(stoploss_val,2)

def trade_execution(data_frame, for_trade_stocks, intervals, flag, transactions, curr_time, kite_conn_var):
  for stock in for_trade_stocks.keys():
    ema_max     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[4])
    ema_min     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[5])
    rsi         = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[9])
    atr         = talib.ATR(data_frame[stock]['High'].iloc[:-1],data_frame[stock]['Low'].iloc[:-1],data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[10])
    if flag[stock]['buy'] is False:
        buys(stock, data_frame, ema_max, ema_min, rsi, atr, intervals, flag, transactions, curr_time, kite_conn_var)
  return transactions

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, ema_max, ema_min, rsi, atr, intervals, flag, transactions , curr_time, kite_conn_var):
  # Difference btw ema-max-min is less or equal to 0.2 and price is above ema-min-max
  if ema_max[-1] > ema_min[-1]:
    if data_frame[stock]['Close'].iloc[-2] > ema_min[-1]:
      if data_frame[stock]['Close'].iloc[-2] > ema_max[-1]:
        if data_frame[stock]['Close'].iloc[-3] > ema_min[-2]:
          if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.2):
            if atr[-1] < atr[-2] and atr[-2] < atr[-3] and atr[-1] < atr[-3]:
              pass
            else:
              # Place Order in ZERODHA.
              # -------------------------------------------
              order_id, error_status = zerodha_action.place_regular_buy_order(kite_conn_var,stock,flag)
              flag[stock]['order_id'] = order_id
              flag[stock]['order_status'] = error_status
              # -------------------------------------------
              flag['Entry'].append(stock)
              flag[stock]['buy'] = True
              stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(stock,flag,atr)
              flag[stock]['target'] = round((flag[stock]['buying_price'] + atr[-1]*0.9),2)
              transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.2, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] > ema_max[-1]:
    if ema_min[-2] < ema_max[-2]:
      if data_frame[stock]['Close'].iloc[-2] > ema_min[-1]:
        if data_frame[stock]['Close'].iloc[-2] > ema_max[-1]:
          if data_frame[stock]['Close'].iloc[-3] > ema_min[-2]:
            if data_frame[stock]['Close'].iloc[-3] > ema_max[-2]:
              if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.2):
                if atr[-1] < atr[-2] and atr[-2] < atr[-3] and atr[-1] < atr[-3]:
                  pass
                else:
                  # Place Order in ZERODHA.
                  # -------------------------------------------
                  order_id, error_status = zerodha_action.place_regular_buy_order(kite_conn_var,stock,flag)
                  flag[stock]['order_id'] = order_id
                  flag[stock]['order_status'] = error_status
                  # -------------------------------------------
                  flag['Entry'].append(stock)
                  flag[stock]['buy'] = True
                  stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(stock,flag,atr)
                  flag[stock]['target'] = round((flag[stock]['buying_price'] + atr[-1]*0.9),2)
                  transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})
