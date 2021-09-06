from . import ltp_zerodha_action

# SELL STOCK ; EXIT
def sell(stock, price, flag, transactions, curr_time, kite_conn_var):
  # Exit when Target Hits
  if price >= flag[stock]['target']:
    flag[stock]['selling_price'] = price
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    # place an order for exit
    # -----------------------------------------------
    order_id, error_status = ltp_zerodha_action.exit_cover_order(kite_conn_var,flag[stock]['exit_id'])
    flag[stock]['order_id'] = order_id
    flag[stock]['order_status'] = error_status
    # -----------------------------------------------
    if order_id != 0:
      flag[stock]['buy']      = False
      transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_HIT','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'exit_id':None,'stoploss_percent':None})
      flag['Entry'].remove(stock)
      flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
      flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
      flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
      flag[stock]['exit_id'] = 0
  
  # if price hits StopLoss, Exit
  elif price <= flag[stock]['stoploss']:
    flag[stock]['selling_price'] = flag[stock]['stoploss']
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = (diff/flag[stock]['buying_price']) * 100
    flag[stock]['buy']      = False
    transactions.append({'symbol':stock,'indicate':'Exit','type':'StopLoss','date':curr_time,'close':flag[stock]['selling_price'],'stoploss':flag[stock]['stoploss'],'target':flag[stock]['target'],'target_percent':None,'difference':diff,'profit':profit,'order_id':None,'order_status':'STOPLOSS_HITTED','exit_id':None,'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target'], flag[stock]['target_per'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
    flag[stock]['exit_id'] = 0
  return transactions