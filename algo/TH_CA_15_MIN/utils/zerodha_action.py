
def place_cover_order(kite_conn_var,symbol,stoploss_val):
  # Place an order
  order_id = 0
  exit_id  = 0
  error_status = 'NOT_PLACED'
  try:
    order_id = kite_conn_var.place_order(tradingsymbol=symbol.split('.')[0],
                                exchange=kite_conn_var.EXCHANGE_NSE,
                                transaction_type=kite_conn_var.TRANSACTION_TYPE_BUY,
                                quantity=1,
                                variety=kite_conn_var.VARIETY_CO,
                                order_type=kite_conn_var.ORDER_TYPE_MARKET,
                                product=kite_conn_var.PRODUCT_CO,
                                validity=kite_conn_var.VALIDITY_DAY,
                                trigger_price=stoploss_val
                                )
    error_status = 'SUCCESSFULLY_PLACED'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  if order_id != 0:
    order_list = kite_conn_var.orders()
    for i in range(len(order_list)):
      if order_list[i]['parent_order_id'] == order_id:
        exit_id = order_list[i]['order_id']
  return order_id, error_status, exit_id


def exit_cover_order(kite_conn_var,exit_id):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    cancel_id = kite_conn_var.cancel_order(order_id=exit_id,
                                variety=kite_conn_var.VARIETY_CO)
    error_status = 'SUCCESSFULLY_EXITED'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END OR STOPLOSS HITTED.'
  return cancel_id, error_status
