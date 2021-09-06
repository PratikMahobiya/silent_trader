
def exit_cover_order(kite_conn_var,exit_id):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    cancel_id = kite_conn_var.cancel_order(order_id=exit_id,
                                variety=kite_conn_var.VARIETY_CO)
    error_status = 'SUCCESSFULLY_EXITED'
  except Exception as e:
    error_status = e
  return cancel_id, error_status
