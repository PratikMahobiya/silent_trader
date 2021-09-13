from . import ltp_zerodha_action_slfema

def target_val(flag,stock):
  if flag[stock]['target_1_flag'] is True:
    return flag[stock]['target_2']
  else:
    return flag[stock]['target_1']

# SELL STOCK ; EXIT
def sell(stock, price, flag, transactions, curr_time, kite_conn_var):
  # Exit when Target Hits
  target = target_val(flag,stock)
  if price >= target:
    if flag[stock]['target_1_flag'] is not True:
      flag[stock]['target_1_flag'] = True
      flag[stock]['stoploss'] = price - (flag[stock]['atr_1']*0.5)
    else:
      flag[stock]['selling_price'] = price
      diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
      profit        = ((diff/flag[stock]['buying_price']) * 100) * flag[stock]['quantity']
      diff          = diff * flag[stock]['quantity']
      # place an order for exit
      # -----------------------------------------------
      order_id, error_status = ltp_zerodha_action_slfema.place_regular_sell_order(kite_conn_var,stock,flag)
      flag[stock]['order_id'] = order_id
      flag[stock]['order_status'] = error_status
      # -----------------------------------------------
      flag[stock]['buy']      = False
      transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_2','date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':None})
      flag['Entry'].remove(stock)
      flag[stock]['stoploss'], flag[stock]['target_1'], flag[stock]['target_1'] = 0, 0, 0
      flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
      flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
      flag[stock]['atr_1'], flag[stock]['atr_2'] = 0, 0
      flag[stock]['target_1_flag'], flag[stock]['quantity'] = False, 0
  
  # if price hits StopLoss, Exit
  elif price <= flag[stock]['stoploss']:
    flag[stock]['selling_price'] = price
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = ((diff/flag[stock]['buying_price']) * 100) * flag[stock]['quantity']
    diff          = diff * flag[stock]['quantity']
    # place an order for exit
    # -----------------------------------------------
    order_id, error_status = ltp_zerodha_action_slfema.place_regular_sell_order(kite_conn_var,stock,flag)
    flag[stock]['order_id'] = order_id
    flag[stock]['order_status'] = error_status
    # -----------------------------------------------
    flag[stock]['buy']      = False
    sell_type = 'StopLoss'
    if flag[stock]['target_1_flag'] is True:
      sell_type = 'T1_SL'
    transactions.append({'symbol':stock,'indicate':'Exit','type':sell_type,'date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target_1'], flag[stock]['target_1'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
    flag[stock]['atr_1'], flag[stock]['atr_2'] = 0, 0
    flag[stock]['target_1_flag'], flag[stock]['quantity'] = False, 0
  return transactions

# SQUARE OFF, EXIT
def square_off(stock_name, price, flag, transactions, curr_time, kite_conn_var):
  flag[stock_name]['selling_price'] = price
  diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
  profit        = ((diff/flag[stock_name]['buying_price']) * 100) * flag[stock_name]['quantity']
  diff          = diff * flag[stock_name]['quantity']
  # place an order for exit
  # -----------------------------------------------
  order_id, error_status = ltp_zerodha_action_slfema.place_regular_sell_order(kite_conn_var,stock_name,flag)
  flag[stock_name]['order_id'] = order_id
  flag[stock_name]['order_status'] = error_status
  # -----------------------------------------------
  flag[stock_name]['buy']      = False
  transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target_1':flag[stock_name]['target_1'],'target_2':flag[stock_name]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'stoploss_percent':None})
  flag['Entry'].remove(stock_name)
  flag[stock_name]['stoploss'], flag[stock_name]['target_1'], flag[stock_name]['target_1'] = 0, 0, 0
  flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
  flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
  flag[stock_name]['atr_1'], flag[stock_name]['atr_2'] = 0, 0
  flag[stock_name]['target_1_flag'], flag[stock_name]['quantity'] = False, 0
  return transactions