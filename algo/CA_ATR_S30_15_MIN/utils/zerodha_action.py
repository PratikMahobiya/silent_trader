
def place_cover_order(kite_conn_var,symbol,stoploss_val,flag):
  # Place an order
  order_id = 0
  exit_id  = 0
  error_status = 'NOT_PLACED'
  try:
    stocks_ltp = kite_conn_var.ltp('NSE:'+symbol.split('.')[0])
    quantity = 1
    while True:
      price = stocks_ltp['NSE:'+symbol.split('.')[0]]['last_price'] * quantity
      if price >= 2000:
        quantity = quantity - 1
        break
      quantity += 1
    # order_id = kite_conn_var.place_order(tradingsymbol=symbol.split('.')[0],
    #                             exchange=kite_conn_var.EXCHANGE_NSE,
    #                             transaction_type=kite_conn_var.TRANSACTION_TYPE_BUY,
    #                             quantity=1,
    #                             variety=kite_conn_var.VARIETY_CO,
    #                             order_type=kite_conn_var.ORDER_TYPE_MARKET,
    #                             product=kite_conn_var.PRODUCT_CO,
    #                             validity=kite_conn_var.VALIDITY_DAY,
    #                             trigger_price=round(stoploss_val,1)
    #                             )
    flag[symbol]['quantity'] = quantity
    error_status = 'SUCCESSFULLY_PLACED'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  if order_id != 0:
    order_list = kite_conn_var.orders()
    for i in range(len(order_list)):
      if order_list[i]['parent_order_id'] == order_id:
        exit_id = order_list[i]['order_id']
  return order_id, error_status, exit_id
