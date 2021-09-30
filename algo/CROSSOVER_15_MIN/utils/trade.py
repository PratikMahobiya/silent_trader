import talib
from . import zerodha_action

def place_ord(kite_conn_var,stock,flag):
  # Place Order in ZERODHA.
  # -------------------------------------------
  order_id, error_status = zerodha_action.place_regular_buy_order(kite_conn_var,stock,flag)
  flag[stock]['order_id'] = order_id
  flag[stock]['order_status'] = error_status
  # -------------------------------------------

def checking_stoploss_fixed(price):
  stoploss_val = 0
  per          = 0
  try:
    stoploss_val = price - price*0.005
    per = ((price-stoploss_val)/price)*100
  except Exception as e:
    per = 0.5
    pass
  return round(per,2), round(stoploss_val,2)

def checking_stoploss(price, atr):
  stoploss_val = price - atr[-1]*0.5
  return round(stoploss_val,2)

def trade_execution(data_frame, for_trade_stocks, intervals, flag, transactions, curr_time, kite_conn_var):
  for stock in for_trade_stocks.keys():
    ema_max     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[4])
    ema_min     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[5])
    rsi         = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[9])
    atr         = talib.ATR(data_frame[stock]['High'].iloc[:-1],data_frame[stock]['Low'].iloc[:-1],data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[10])
    if flag[stock]['buy'] is False:
      buys(stock, data_frame, ema_max, ema_min, rsi, atr, intervals, flag, transactions, curr_time, kite_conn_var)
    else:
      updatestoploss(stock, data_frame, atr, flag)
  return transactions

# UPDATE STOPLOSS
def updatestoploss(stock, data_frame, atr, flag):
  if data_frame[stock]['Close'].iloc[-2] > data_frame[stock]['Open'].iloc[-2]:
    flag[stock]['stoploss'] = checking_stoploss(data_frame[stock]['Close'].iloc[-2],atr)
  return 0

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, ema_max, ema_min, rsi, atr, intervals, flag, transactions , curr_time, kite_conn_var):
  # Difference btw ema-max-min is less or equal to 0.2 and price is above ema-min-max
  if ema_max[-1] > ema_min[-1]:
    if data_frame[stock]['Close'].iloc[-2] > ema_min[-1]:
      if data_frame[stock]['Close'].iloc[-2] > ema_max[-1]:
        if data_frame[stock]['Close'].iloc[-3] > ema_min[-2]:
          if data_frame[stock]['Close'].iloc[-3] > ema_max[-2]:
            if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.2):
              # Place Order in ZERODHA.
              place_ord(kite_conn_var,stock,flag)
              # -----------------------
              flag['Entry'].append(stock)
              flag[stock]['buy'] = True
              stoploss_per, flag[stock]['f_stoploss'] =  checking_stoploss_fixed(flag[stock]['buying_price'])
              flag[stock]['target']   = flag[stock]['buying_price'] + flag[stock]['buying_price'] * 0.01
              flag[stock]['stoploss'] =  checking_stoploss(flag[stock]['buying_price'],atr)
              transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['f_stoploss'],'target':flag[stock]['target'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.2, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] > ema_max[-1]:
    if ema_min[-2] < ema_max[-2]:
      if data_frame[stock]['Close'].iloc[-2] > ema_min[-1]:
        if data_frame[stock]['Close'].iloc[-2] > ema_max[-1]:
          if data_frame[stock]['Close'].iloc[-3] > ema_min[-2]:
            if data_frame[stock]['Close'].iloc[-3] > ema_max[-2]:
              if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.2):
                if rsi[-1] > rsi[-2] and rsi[-1] > rsi[-3]:
                  # Place Order in ZERODHA.
                  place_ord(kite_conn_var,stock,flag)
                  # ----------------------
                  flag['Entry'].append(stock)
                  flag[stock]['buy'] = True
                  stoploss_per, flag[stock]['f_stoploss'] =  checking_stoploss_fixed(flag[stock]['buying_price'])
                  flag[stock]['target']   = flag[stock]['buying_price'] + flag[stock]['buying_price'] * 0.01
                  flag[stock]['stoploss'] =  checking_stoploss(flag[stock]['buying_price'],atr)
                  transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['f_stoploss'],'target':flag[stock]['target'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})