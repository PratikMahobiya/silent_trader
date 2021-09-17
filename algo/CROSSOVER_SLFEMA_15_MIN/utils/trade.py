import talib
from . import zerodha_action

def checking_stoploss(data_frame, stock, flag, ema_max, ema_min):
  for i in range(len(data_frame[stock]['Close'])):
    if i >= 2:
      if (data_frame[stock]['Close'].iloc[-i] < ema_min[-i]) or (data_frame[stock]['Close'].iloc[-i] < ema_max[-i]):
        break
      stoploss_val = data_frame[stock]['Open'].iloc[-i]
  per = ((flag[stock]['buying_price'] - stoploss_val)/flag[stock]['buying_price'])*100
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
            # Place Order in ZERODHA.
            # -------------------------------------------
            order_id, error_status = zerodha_action.place_regular_buy_order(kite_conn_var,stock,flag)
            flag[stock]['order_id'] = order_id
            flag[stock]['order_status'] = error_status
            # -------------------------------------------
            flag['Entry'].append(stock)
            flag[stock]['buy'] = True
            flag[stock]['atr_1'] = atr[-1]
            stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(data_frame,stock,flag,ema_max,ema_min)
            flag[stock]['target_05'] = round((flag[stock]['buying_price'] + (flag[stock]['atr_1']*0.6)),2)
            flag[stock]['target_075'] = round((flag[stock]['buying_price'] + (flag[stock]['atr_1']*0.8)),2)
            flag[stock]['target_1'] = round((flag[stock]['buying_price'] + flag[stock]['atr_1']),2)
            flag[stock]['target_2'] = round((flag[stock]['buying_price'] + flag[stock]['atr_2']),2)
            transactions.append({'symbol':stock,'indicate':'Entry','type':'BF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_05':flag[stock]['target_05'],'target_075':flag[stock]['target_075'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.2, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] > ema_max[-1]:
    if ema_min[-2] < ema_max[-2]:
      if data_frame[stock]['Close'].iloc[-2] > ema_min[-1]:
        if data_frame[stock]['Close'].iloc[-2] > ema_max[-1]:
          if data_frame[stock]['Close'].iloc[-3] > ema_min[-2]:
            if data_frame[stock]['Close'].iloc[-3] > ema_max[-2]:
              if data_frame[stock]['Close'].iloc[-2] > data_frame[stock]['Open'].iloc[-2]:
                if data_frame[stock]['Close'].iloc[-3] > data_frame[stock]['Open'].iloc[-3]:
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
                    flag[stock]['atr_1'] = atr[-1]
                    stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(data_frame,stock,flag,ema_max,ema_min)
                    flag[stock]['target_06'] = round((flag[stock]['buying_price'] + (flag[stock]['atr_1']*0.6)),2)
                    flag[stock]['target_08'] = round((flag[stock]['buying_price'] + (flag[stock]['atr_1']*0.9)),2)
                    flag[stock]['target_1'] = round((flag[stock]['buying_price'] + flag[stock]['atr_1']),2)
                    flag[stock]['target_2'] = round((flag[stock]['buying_price'] + flag[stock]['atr_2']),2)
                    transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_05':flag[stock]['target_05'],'target_075':flag[stock]['target_075'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':stoploss_per})
