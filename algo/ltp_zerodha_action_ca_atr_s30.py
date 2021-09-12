def exit_cover_order(kite_conn_var,symbol,flag):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    if flag[symbol]['order_id'] != 0:
      cancel_id = kite_conn_var.cancel_order(order_id=flag[symbol]['exit_id'],
                                  variety=kite_conn_var.VARIETY_CO)
    error_status = 'SUCCESSFULLY_EXITED'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END OR STOPLOSS HITTED.'
  return cancel_id, error_status