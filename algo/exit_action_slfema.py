from . import ltp_zerodha_action_slfema

def target_val(flag,stock):
  if flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is False and flag[stock]['target_1_flag'] is False:
    return flag[stock]['target_09']
  elif flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is True and flag[stock]['target_1_flag'] is False:
    return flag[stock]['target_1']
  elif flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is True and flag[stock]['target_1_flag'] is True:
    return flag[stock]['target_2']
  else:
    return flag[stock]['target_06']

# SELL STOCK ; EXIT
def sell(stock, price, flag, transactions, curr_time, kite_conn_var):
  # Exit when Target Hits
  target = target_val(flag,stock)
  if price >= target:
    if flag[stock]['target_06_flag'] is False and flag[stock]['target_09_flag'] is False and flag[stock]['target_1_flag'] is False:
      flag[stock]['target_06_flag'] = True
      flag[stock]['stoploss'] = round((flag[stock]['buying_price'] + (flag[stock]['atr_1']*0.1)),2)
    elif flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is False and flag[stock]['target_1_flag'] is False:
      flag[stock]['target_09_flag'] = True
      flag[stock]['stoploss'] = round((flag[stock]['buying_price'] + (flag[stock]['atr_1']*0.5)),2)
    elif flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is True and flag[stock]['target_1_flag'] is False:
      flag[stock]['target_1_flag'] = True
      flag[stock]['stoploss'] = round((flag[stock]['buying_price'] + (flag[stock]['atr_1']*0.75)),2)
    else:
      if flag[stock]['order_id'] != 0:
        ord_det = kite_conn_var.order_history(order_id=flag[stock]['order_id'])
        if ord_det[-1]['status'] == 'COMPLETE':
          # place an order for exit
          # -----------------------------------------------
          order_id, error_status = ltp_zerodha_action_slfema.place_regular_sell_order(kite_conn_var,stock,flag)
          flag[stock]['order_id'] = order_id
          flag[stock]['order_status'] = error_status
          # -----------------------------------------------
      flag[stock]['selling_price'] = price
      diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
      profit        = round((((diff/flag[stock]['buying_price']) * 100)),2)
      diff          = round((diff * flag[stock]['quantity']),2)
      flag[stock]['buy']      = False
      transactions.append({'symbol':stock,'indicate':'Exit','type':'TARGET_2','date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_05':flag[stock]['target_06'],'target_075':flag[stock]['target_09'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':None})
      flag['Entry'].remove(stock)
      flag[stock]['stoploss'], flag[stock]['target_1'], flag[stock]['target_1'] = 0, 0, 0
      flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
      flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
      flag[stock]['atr_1'], flag[stock]['atr_2'] = 0, 0
      flag[stock]['quantity'] = 0
      flag[stock]['target_06_flag'], flag[stock]['target_09_flag'] = False, False
      flag[stock]['target_1_flag'] = False
  
  # if price hits StopLoss, Exit
  elif price <= flag[stock]['stoploss']:
    if flag[stock]['order_id'] != 0:
      ord_det = kite_conn_var.order_history(order_id=flag[stock]['order_id'])
      if ord_det[-1]['status'] == 'COMPLETE':
        # place an order for exit
        # -----------------------------------------------
        order_id, error_status = ltp_zerodha_action_slfema.place_regular_sell_order(kite_conn_var,stock,flag)
        flag[stock]['order_id'] = order_id
        flag[stock]['order_status'] = error_status
        # -----------------------------------------------
    flag[stock]['selling_price'] = price
    diff          = flag[stock]['selling_price'] - flag[stock]['buying_price']
    profit        = round((((diff/flag[stock]['buying_price']) * 100)),2)
    diff          = round((diff * flag[stock]['quantity']),2)
    flag[stock]['buy']      = False
    if flag[stock]['target_06_flag'] is False and flag[stock]['target_09_flag'] is False and flag[stock]['target_1_flag'] is False:
      sell_type = 'StopLoss'
    elif flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is False and flag[stock]['target_1_flag'] is False:
      sell_type = 'T01_SL'
    elif flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is True and flag[stock]['target_1_flag'] is False:
      sell_type = 'T05_SL'
    elif flag[stock]['target_06_flag'] is True and flag[stock]['target_09_flag'] is True and flag[stock]['target_1_flag'] is True:
      sell_type = 'T075_SL'
    transactions.append({'symbol':stock,'indicate':'Exit','type':sell_type,'date':curr_time,'close':flag[stock]['selling_price'],'quantity':flag[stock]['quantity'],'stoploss':flag[stock]['stoploss'],'target_05':flag[stock]['target_06'],'target_075':flag[stock]['target_09'],'target_1':flag[stock]['target_1'],'target_2':flag[stock]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock]['order_id'],'order_status':flag[stock]['order_status'],'stoploss_percent':None})
    flag['Entry'].remove(stock)
    flag[stock]['stoploss'], flag[stock]['target_1'], flag[stock]['target_1'] = 0, 0, 0
    flag[stock]['selling_price'], flag[stock]['buying_price']  = 0, 0
    flag[stock]['order_id'], flag[stock]['order_status'] = 0, None
    flag[stock]['atr_1'], flag[stock]['atr_2'] = 0, 0
    flag[stock]['quantity'] = 0
    flag[stock]['target_06_flag'], flag[stock]['target_09_flag'] = False, False
    flag[stock]['target_1_flag'] = False
  return transactions

# SQUARE OFF, EXIT
def square_off(stock_name, price, flag, transactions, curr_time, kite_conn_var):
  if flag[stock_name]['order_id'] != 0:
    ord_det = kite_conn_var.order_history(order_id=flag[stock_name]['order_id'])
    if ord_det[-1]['status'] == 'COMPLETE':
      # place an order for exit
      # -----------------------------------------------
      order_id, error_status = ltp_zerodha_action_slfema.place_regular_sell_order(kite_conn_var,stock_name,flag)
      flag[stock_name]['order_id'] = order_id
      flag[stock_name]['order_status'] = error_status
      # -----------------------------------------------
      flag[stock_name]['selling_price'] = price
      diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
      profit        = round((((diff/flag[stock_name]['buying_price']) * 100)),2)
      diff          = round((diff * flag[stock_name]['quantity']),2)
      flag[stock_name]['buy']      = False
      transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target_05':flag[stock_name]['target_06'],'target_075':flag[stock_name]['target_09'],'target_1':flag[stock_name]['target_1'],'target_2':flag[stock_name]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'stoploss_percent':None})
      flag['Entry'].remove(stock_name)
      flag[stock_name]['stoploss'], flag[stock_name]['target_1'], flag[stock_name]['target_1'] = 0, 0, 0
      flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
      flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
      flag[stock_name]['atr_1'], flag[stock_name]['atr_2'] = 0, 0
      flag[stock_name]['quantity'] = 0
      flag[stock_name]['target_06_flag'], flag[stock_name]['target_09_flag'] = False, False
      flag[stock_name]['target_1_flag'] = False
    else:
      # place an order for exit
      # -----------------------------------------------
      order_id, error_status = ltp_zerodha_action_slfema.exit_order(kite_conn_var,stock_name,flag)
      flag[stock_name]['order_id'] = order_id
      flag[stock_name]['order_status'] = error_status
      # -----------------------------------------------
      flag[stock_name]['selling_price'] = price
      diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
      profit        = round((((diff/flag[stock_name]['buying_price']) * 100)),2)
      diff          = round((diff * flag[stock_name]['quantity']),2)
      flag[stock_name]['buy']      = False
      transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target_05':flag[stock_name]['target_06'],'target_075':flag[stock_name]['target_09'],'target_1':flag[stock_name]['target_1'],'target_2':flag[stock_name]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'stoploss_percent':None})
      flag['Entry'].remove(stock_name)
      flag[stock_name]['stoploss'], flag[stock_name]['target_1'], flag[stock_name]['target_1'] = 0, 0, 0
      flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
      flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
      flag[stock_name]['atr_1'], flag[stock_name]['atr_2'] = 0, 0
      flag[stock_name]['quantity'] = 0
      flag[stock_name]['target_06_flag'], flag[stock_name]['target_09_flag'] = False, False
      flag[stock_name]['target_1_flag'] = False
  else:
    flag[stock_name]['selling_price'] = price
    diff          = flag[stock_name]['selling_price'] - flag[stock_name]['buying_price']
    profit        = round((((diff/flag[stock_name]['buying_price']) * 100)),2)
    diff          = round((diff * flag[stock_name]['quantity']),2)
    flag[stock_name]['buy']      = False
    transactions.append({'symbol':stock_name,'indicate':'Square_Off','type':'END_OF_DAY','date':curr_time,'close':flag[stock_name]['selling_price'],'quantity':flag[stock_name]['quantity'],'stoploss':flag[stock_name]['stoploss'],'target_05':flag[stock_name]['target_06'],'target_075':flag[stock_name]['target_09'],'target_1':flag[stock_name]['target_1'],'target_2':flag[stock_name]['target_2'],'difference':diff,'profit':profit,'order_id':flag[stock_name]['order_id'],'order_status':flag[stock_name]['order_status'],'stoploss_percent':None})
    flag['Entry'].remove(stock_name)
    flag[stock_name]['stoploss'], flag[stock_name]['target_1'], flag[stock_name]['target_1'] = 0, 0, 0
    flag[stock_name]['selling_price'], flag[stock_name]['buying_price']  = 0, 0
    flag[stock_name]['order_id'], flag[stock_name]['order_status'] = 0, None
    flag[stock_name]['atr_1'], flag[stock_name]['atr_2'] = 0, 0
    flag[stock_name]['quantity'] = 0
    flag[stock_name]['target_06_flag'], flag[stock_name]['target_09_flag'] = False, False
    flag[stock_name]['target_1_flag'] = False
  return transactions