from . import ltp_zerodha_action

# SELL STOCK ; EXIT
def sell(stock, price, flag, transactions, curr_time, kite_conn_var):
  # Exit when Target Hits
  if price >= flag[stock]['target']:
    flag[stock]['selling_price'] = price
    diff          = round((flag[stock]['selling_price'] - flag[stock]['buying_price']),2)
    profit        = round(((diff/flag[stock]['buying_price']) * 100),2) * flag[stock]['quantity']
    diff          = diff * flag[stock]['quantity']
    # place an order for exit
    # -----------------------------------------------
    order_id, error_status = ltp_zerodha_action.place_regular_sell_order(kite_conn_var,stock,flag)
    flag[stock]['order_id'] = order_id
    flag[stock]['order_status'] = error_status
    # -----------------------------------------------
    if order_id != 0:
      flag[stock]['buy']      = False
      transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_HIT','date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':None})
      flag['Entry'].remove(stock)
      flag[stock]['stoploss'], flag[stock]['target'] = 0, 0
      flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
      flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
      flag[stock]['quantity'] = 0
  
  # if price hits StopLoss, Exit
  elif price <= flag[stock]['stoploss']:
    flag[stock]['selling_price'] = price
    diff          = round((flag[stock]['selling_price'] - flag[stock]['buying_price']),2)
    profit        = round(((diff/flag[stock]['buying_price']) * 100),2) * flag[stock]['quantity']
    diff          = diff * flag[stock]['quantity']
    # place an order for exit
    # -----------------------------------------------
    order_id, error_status = ltp_zerodha_action.place_regular_sell_order(kite_conn_var,stock,flag)
    flag[stock]['order_id'] = order_id
    flag[stock]['order_status'] = error_status
    # -----------------------------------------------
    if order_id != 0:
      flag[stock]['buy']      = False
      transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'difference':diff,'profit':profit,'order_id':None,'order_status':'STOPLOSS_HITTED','stoploss_percent':None})
      flag['Entry'].remove(stock)
      flag[stock]['stoploss'], flag[stock]['target'] = 0, 0
      flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
      flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
      flag[stock]['quantity'] = 0
  return transactions

# SQUARE OFF, EXIT
def square_off(stock_name, price, flag, transactions, curr_time, kite_conn_var):
  flag[stock_name]['selling_price'] = price
  diff          = round((flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']),2)
  profit        = round(((diff/flag[stock_name]['buying_price']) * 100),2) * flag[stock_name]['quantity']
  diff          = diff * flag[stock_name]['quantity']
  # place an order for exit
  # -----------------------------------------------
  order_id, error_status = ltp_zerodha_action.place_regular_sell_order(kite_conn_var,stock_name,flag)
  flag[stock_name]['order_id'] = order_id
  flag[stock_name]['order_status'] = error_status
  # -----------------------------------------------
  if order_id != 0:
    flag[stock_name]['buy']      = False
    transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'stoploss_percent':None})
    flag['Entry'].remove(stock_name)
    flag[stock_name]['stoploss'], flag[stock_name]['target'] = 0, 0
    flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
    flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
    flag[stock_name]['quantity'] = 0
  return transactions