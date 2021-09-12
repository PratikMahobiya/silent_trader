from . import ltp_zerodha_action_ca_atr_s30

# SELL STOCK ; EXIT
def sell(stock, price, flag, transactions, curr_time, kite_conn_var):
  # Exit when Target Hits
  if price >= flag[stock]['target']:
    flag[stock]['selling_price'] = price
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = round(((diff/flag[stock]['buying_price']) * 100),2) * flag[stock]['quantity']
    diff          = diff * flag[stock]['quantity']
    # place an order for exit
    # -----------------------------------------------
    order_id, error_status = ltp_zerodha_action_ca_atr_s30.exit_cover_order(kite_conn_var,stock,flag)
    flag[stock]['order_id'] = order_id
    flag[stock]['order_status'] = error_status
    # -----------------------------------------------
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_HIT','date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'exit_id':None,'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
    flag[stock]['exit_id'], flag[stock]['quantity'] = 0, 0
  
  # if price hits StopLoss, Exit
  elif price <= flag[stock]['stoploss']:
    flag[stock]['selling_price'] = price
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = round(((diff/flag[stock]['buying_price']) * 100),2) * flag[stock]['quantity']
    diff          = diff * flag[stock]['quantity']
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':None,'order_status':'STOPLOSS_HITTED','exit_id':None,'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
    flag[stock]['exit_id'], flag[stock]['quantity'] = 0, 0
  return transactions

# SQUARE OFF, EXIT
def square_off(stock_name, price, flag, transactions, curr_time, kite_conn_var):
  if price <= flag[stock_name]['stoploss']:
    flag[stock_name]['selling_price'] = price
    diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
    profit        = round(((diff/flag[stock_name]['buying_price']) * 100),2) * flag[stock_name]['quantity']
    diff          = diff * flag[stock_name]['quantity']
    flag[stock_name]['buy']      = False
    transactions.append({'symbol':stock_name,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':None,'order_status':'STOPLOSS_HITTED','exit_id':None,'stoploss_percent':None})
    flag['Entry'].remove(stock_name)
    flag[stock_name]['stoploss'], flag[stock_name]['target'], flag[stock_name]['target_per'] = 0, 0, 0
    flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
    flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
    flag[stock_name]['exit_id'], flag[stock_name]['quantity'] = 0, 0
  else:
    flag[stock_name]['selling_price'] = price
    diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
    profit        = round(((diff/flag[stock_name]['buying_price']) * 100),2) * flag[stock_name]['quantity']
    diff          = diff * flag[stock_name]['quantity']
    # place an order for exit
    # -----------------------------------------------
    order_id, error_status = ltp_zerodha_action_ca_atr_s30.exit_cover_order(kite_conn_var,stock_name,flag)
    flag[stock_name]['order_id'] = order_id
    flag[stock_name]['order_status'] = error_status
    # -----------------------------------------------
    flag[stock_name]['buy']      = False
    transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target':flag[stock_name]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'exit_id':None,'stoploss_percent':None})
    flag['Entry'].remove(stock_name)
    flag[stock_name]['stoploss'], flag[stock_name]['target'], flag[stock_name]['target_per'] = 0, 0, 0
    flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
    flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
    flag[stock_name]['exit_id'], flag[stock_name]['quantity'] = 0, 0
  return transactions