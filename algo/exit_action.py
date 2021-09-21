from . import ltp_zerodha_action

# place a sell order for exit
def place_ord(kite_conn_var,stock,flag):
  # -----------------------------------------------
  order_id, error_status = ltp_zerodha_action.place_regular_sell_order(kite_conn_var,stock,flag)
  flag[stock]['order_id'] = order_id
  flag[stock]['order_status'] = error_status
  # -----------------------------------------------

# place a cancel order for exit
def cancel_ord(kite_conn_var,stock_name,flag):
  # -----------------------------------------------
  order_id, error_status = ltp_zerodha_action.exit_order(kite_conn_var,stock_name,flag)
  flag[stock_name]['order_id'] = order_id
  flag[stock_name]['order_status'] = error_status
  # -----------------------------------------------

# SELL STOCK ; EXIT
def sell(stock, price, flag, transactions, curr_time, kite_conn_var):
  # if price hits StopLoss, Exit
  if flag[stock]['trend'] == False:
    if price <= flag[stock]['stoploss']:
      if flag[stock]['order_id'] != 0:
        ord_det = kite_conn_var.order_history(order_id=flag[stock]['order_id'])
        if ord_det[-1]['status'] == 'COMPLETE':
          # CALL PLACE ORDER ----
          place_ord(kite_conn_var,stock,flag)
          # ---------------------
        else:
          # CALL CANCEL ORDER ----
          cancel_ord(kite_conn_var,stock,flag)
          # ----------------------
      flag[stock]['selling_price'] = price
      diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
      profit        = round((((diff/flag[stock]['buying_price']) * 100)),2)
      diff          = round((diff * flag[stock]['quantity']),2)
      flag[stock]['buy']      = False
      type_str = 'StopLoss'
      if flag[stock]['count'] != 0:
        type_str = 'HIT_{}'.format(flag[stock]['count'])
      transactions.append({'symbol':stock,'indicate':'Exit','type':type_str,'date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':None})
      flag['Entry'].remove(stock)
      flag[stock]['stoploss'], flag[stock]['count'],flag[stock]['target'] = 0, 0, 0
      flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
      flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
      flag[stock]['quantity'], flag[stock]['trend'] = 0, False
  
  # if price hits Target, Exit
  if price >= flag[stock]['target']:
    if flag[stock]['order_id'] != 0:
      ord_det = kite_conn_var.order_history(order_id=flag[stock]['order_id'])
      if ord_det[-1]['status'] == 'COMPLETE':
        # CALL PLACE ORDER ----
        place_ord(kite_conn_var,stock,flag)
        # ---------------------
      else:
        # CALL CANCEL ORDER ----
        cancel_ord(kite_conn_var,stock,flag)
        # ----------------------
    flag[stock]['selling_price'] = price
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = round((((diff/flag[stock]['buying_price']) * 100)),2)
    diff          = round((diff * flag[stock]['quantity']),2)
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'2-% AYA RE','date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['count'],flag[stock]['target'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
    flag[stock]['quantity'], flag[stock]['trend'] = 0, False
  return transactions

# SQUARE OFF, EXIT
def square_off(stock_name, price, flag, transactions, curr_time, kite_conn_var):
  if flag[stock_name]['order_id'] != 0:
    ord_det = kite_conn_var.order_history(order_id=flag[stock_name]['order_id'])
    if ord_det[-1]['status'] == 'COMPLETE':
      # CALL PLACE ORDER ----
      place_ord(kite_conn_var,stock_name,flag)
      # ---------------------
    else:
      # CALL CANCEL ORDER ----
      cancel_ord(kite_conn_var,stock_name,flag)
      # ----------------------
    flag[stock_name]['selling_price'] = price
    diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
    profit        = round((((diff/flag[stock_name]['buying_price']) * 100)),2)
    diff          = round((diff * flag[stock_name]['quantity']),2)
    flag[stock_name]['buy']      = False
    transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'stoploss_percent':None})
    flag['Entry'].remove(stock_name)
    flag[stock_name]['stoploss'], flag[stock_name]['count'],flag[stock_name]['target'] = 0, 0, 0
    flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
    flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
    flag[stock_name]['quantity'], flag[stock_name]['trend'] = 0, False
  else:
    flag[stock_name]['order_id'] = '0'
    flag[stock_name]['order_status'] = 'NOT PLACED'
    flag[stock_name]['selling_price'] = price
    diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
    profit        = round((((diff/flag[stock_name]['buying_price']) * 100)),2)
    diff          = round((diff * flag[stock_name]['quantity']),2)
    flag[stock_name]['buy']      = False
    transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'CANCELLED','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'stoploss_percent':None})
    flag['Entry'].remove(stock_name)
    flag[stock_name]['stoploss'], flag[stock_name]['count'],flag[stock_name]['target'] = 0, 0, 0
    flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
    flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
    flag[stock_name]['quantity'], flag[stock_name]['trend'] = 0, False
  return transactions