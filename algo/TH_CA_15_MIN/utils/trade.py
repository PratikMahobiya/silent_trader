import talib
from . import zerodha_action

def checking_stoploss(data_frame, stock):
  per = ((data_frame['Close'].iloc[-1][stock]-data_frame['Low'].iloc[-1][stock])/data_frame['Close'].iloc[-1][stock])*100
  if per > 0.3:
    stoploss_val = data_frame['Close'].iloc[-1][stock] - (data_frame['Close'].iloc[-1][stock] * 0.002)
    per = 0.2
  else:
    stoploss_val = data_frame['Low'].iloc[-1][stock]
  return per, stoploss_val

def trade_execution(data_frame, intervals, flag, transactions, curr_time, kite_conn_var):
    for stock in data_frame['Close'].columns:
        ema_max     = talib.EMA(data_frame['Close'][stock], timeperiod=intervals[4])
        ema_min     = talib.EMA(data_frame['Close'][stock], timeperiod=intervals[5])
        rsi         = talib.RSI(data_frame['Close'][stock], timeperiod=intervals[9])
        if flag[stock]['buy'] is False:
            buys(stock, data_frame, ema_max, ema_min, rsi, intervals, flag, transactions, curr_time, kite_conn_var)
        # else:
        #     sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time, kite_conn_var)
    return transactions

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, ema_max, ema_min, rsi, intervals, flag, transactions , curr_time, kite_conn_var):
  # Difference btw ema-max-min is less or equal to 0.1 and price is above ema-min-max
  if ema_max[-1] > ema_min[-1]:
    if data_frame['Close'].iloc[-1][stock] > ema_min[-1]:
      if data_frame['Close'].iloc[-1][stock] > ema_max[-1]:
        if data_frame['Close'].iloc[-2][stock] > ema_min[-2]:
          if data_frame['Close'].iloc[-2][stock] > ema_max[-2]:
            if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.2):
              flag[stock]['buying_price'] = data_frame['Close'].iloc[-1][stock]
              stoploss_per, flag[stock]['stoploss'] =  checking_stoploss(data_frame,stock) # data_frame['Low'].iloc[-1][stock]
              flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
              # Place Order in ZERODHA.
              # -------------------------------------------
              order_id, error_status, exit_id = zerodha_action.place_cover_order(kite_conn_var,stock,flag[stock]['stoploss'])
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
            if data_frame['Close'].iloc[-2][stock] > ema_max[-2]:
              if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.2):
                if rsi[-1] > rsi[-2] and rsi[-1] > rsi[-3]:
                  flag[stock]['buying_price'] = data_frame['Close'].iloc[-1][stock]
                  stoploss_per, flag[stock]['stoploss'] = checking_stoploss(data_frame,stock) # data_frame['Low'].iloc[-1][stock]
                  flag[stock]['target'] = flag[stock]['buying_price'] + flag[stock]['buying_price']*(flag[stock]['target_per']/100)
                  # Place Order in ZERODHA.
                  # -------------------------------------------
                  order_id, error_status, exit_id = zerodha_action.place_cover_order(kite_conn_var,stock,flag[stock]['stoploss'])
                  flag[stock]['order_id'] = order_id
                  flag[stock]['exit_id'] = exit_id
                  flag[stock]['order_status'] = error_status
                  # -------------------------------------------
                  if order_id != 0:
                    flag['Entry'].append(stock)
                    flag[stock]['buy'] = True
                    transactions.append({'symbol':stock,'indicate':'Entry','type':'AF_CROSS_OVER','date':curr_time,'close':flag[stock]['buying_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':flag[stock]['target_per'],'difference':None,'profit':None,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'exit_id':flag[stock]['exit_id'],'stoploss_percent':stoploss_per})

# # SELL STOCK ; EXIT
# def sell(stock, data_frame, ema_min, rsi, intervals,flag, transactions, curr_time, kite_conn_var):
#   # Exit when Target Hits
#   if data_frame['High'].iloc[-2][stock] >= flag[stock]['target']:
#     flag[stock]['selling_price'] = data_frame['High'].iloc[-2][stock]
#     diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
#     profit        = (diff/flag[stock]['buying_price']) * 100
#     # place an order for exit
#     # -----------------------------------------------
#     order_id, error_status = zerodha_action.exit_cover_order(kite_conn_var,flag[stock]['exit_id'])
#     flag[stock]['order_id'] = order_id
#     flag[stock]['order_status'] = error_status
#     # -----------------------------------------------
#     if order_id != 0:
#       flag[stock]['buy']      = False
#       transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_HIT','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'exit_id':None,'stoploss_percent':None})
#       flag['Entry'].remove(stock)
#       flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
#       flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
#       flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
#       flag[stock]['exit_id'] = 0
  
#   # if price hits StopLoss, Exit
#   elif data_frame['Low'].iloc[-2][stock] <= flag[stock]['stoploss']:
#     flag[stock]['selling_price'] = flag[stock]['stoploss']
#     diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
#     profit        = (diff/flag[stock]['buying_price']) * 100
#     flag[stock]['buy']      = False
#     transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':None,'order_status':'STOPLOSS_HITTED','exit_id':None,'stoploss_percent':None})
#     flag['Entry'].remove(stock)
#     flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
#     flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
#     flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
#     flag[stock]['exit_id'] = 0

# # SQUARE OFF, EXIT
# def square_off(stock_name,data_frame, intervals, flag, transactions, curr_time, kite_conn_var):
#   # For more than one stock in a list
#   if stock_name is None:
#     for stock in data_frame['Close'].columns:
#       if data_frame['Low'].iloc[-2][stock] <= flag[stock]['stoploss']:
#         flag[stock]['selling_price'] = flag[stock]['stoploss']
#         diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
#         profit        = (diff/flag[stock]['buying_price']) * 100
#         flag[stock]['buy']      = False
#         transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':None,'order_status':'STOPLOSS_HITTED','exit_id':None,'stoploss_percent':None})
#         flag['Entry'].remove(stock)
#         flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
#         flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
#         flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
#         flag[stock]['exit_id'] = 0
#       else:
#         flag[stock]['selling_price'] = data_frame['Close'].iloc[-2][stock]
#         diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
#         profit        = (diff/flag[stock]['buying_price']) * 100
#         # place an order for exit
#         # -----------------------------------------------
#         order_id, error_status = zerodha_action.exit_cover_order(kite_conn_var,flag[stock]['exit_id'])
#         flag[stock]['order_id'] = order_id
#         flag[stock]['order_status'] = error_status
#         # -----------------------------------------------
#         if order_id != 0:
#           flag[stock]['buy']      = False
#           transactions.append({'symbol':stock,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'exit_id':None,'stoploss_percent':None})
#           flag['Entry'].remove(stock)
#           flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
#           flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
#           flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
#           flag[stock]['exit_id'] = 0
#   # for only one stock
#   else:
#     if data_frame['Low'].iloc[-2][stock_name] <= flag[stock_name]['stoploss']:
#       flag[stock_name]['selling_price'] = flag[stock_name]['stoploss']
#       diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
#       profit        = (diff/flag[stock_name]['buying_price']) * 100
#       flag[stock_name]['buy']      = False
#       transactions.append({'symbol':stock_name,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock_name]['selling_price'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':None,'order_status':'STOPLOSS_HITTED','exit_id':None,'stoploss_percent':None})
#       flag['Entry'].remove(stock_name)
#       flag[stock_name]['stoploss'], flag[stock_name]['target'], flag[stock_name]['target_per'] = 0, 0, 0
#       flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
#       flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
#       flag[stock_name]['exit_id'] = 0
#     else:
#       flag[stock_name]['selling_price'] = data_frame['Close'].iloc[-2]
#       diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
#       profit        = (diff/flag[stock_name]['buying_price']) * 100
#       # place an order for exit
#       # -----------------------------------------------
#       order_id, error_status = zerodha_action.exit_cover_order(kite_conn_var,flag[stock_name]['exit_id'])
#       flag[stock_name]['order_id'] = order_id
#       flag[stock_name]['order_status'] = error_status
#       # -----------------------------------------------
#       if order_id != 0:
#         flag[stock_name]['buy']      = False
#         transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'exit_id':None,'stoploss_percent':None})
#         flag['Entry'].remove(stock_name)
#         flag[stock_name]['stoploss'], flag[stock_name]['target'], flag[stock_name]['target_per'] = 0, 0, 0
#         flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
#         flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
#         flag[stock_name]['exit_id'] = 0
#   return transactions