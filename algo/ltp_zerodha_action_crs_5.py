from time import sleep

def place_regular_sell_order(kite_conn_var,symbol,flag):
  # Place an order
  order_id = 0
  error_status = 'NOT_PLACED'
  try:
    if flag[symbol]['order_id'] != 0:
      # order_id = kite_conn_var.place_order(tradingsymbol=symbol.split('.')[0],
      #                             exchange=kite_conn_var.EXCHANGE_NSE,
      #                             transaction_type=kite_conn_var.TRANSACTION_TYPE_SELL,
      #                             quantity=flag[symbol]['quantity'],
      #                             variety=kite_conn_var.VARIETY_REGULAR,
      #                             order_type=kite_conn_var.ORDER_TYPE_MARKET,
      #                             product=kite_conn_var.PRODUCT_MIS,
      #                             validity=kite_conn_var.VALIDITY_DAY,
      #                             )
      order_id = 2
    sleep(0.3)
    error_status = 'NOT ACTIVE'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  return order_id, error_status

def exit_order(kite_conn_var,symbol,flag):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    # cancel_id = kite_conn_var.cancel_order(order_id=flag[symbol]['order_id'],
    #                             variety=kite_conn_var.VARIETY_REGULAR)
    cancel_id = 2
    error_status = 'NOT ACTIVE'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END OR STOPLOSS HITTED.'
  return cancel_id, error_status