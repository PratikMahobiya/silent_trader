
def place_regular_sell_order(kite_conn_var,symbol):
  # Place an order
  order_id = 0
  error_status = 'NOT_PLACED'
  try:
    # order_id = kite_conn_var.place_order(tradingsymbol=symbol.split('.')[0],
    #                             exchange=kite_conn_var.EXCHANGE_NSE,
    #                             transaction_type=kite_conn_var.TRANSACTION_TYPE_SELL,
    #                             quantity=1,
    #                             variety=kite_conn_var.VARIETY_REGULAR,
    #                             order_type=kite_conn_var.ORDER_TYPE_MARKET,
    #                             product=kite_conn_var.PRODUCT_MIS,
    #                             validity=kite_conn_var.VALIDITY_DAY,
    #                             )
    order_id = 1
    error_status = 'NOT ACTIVE'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  return order_id, error_status