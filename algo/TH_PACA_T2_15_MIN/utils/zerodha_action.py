
def place_cover_order(kite_conn_var,symbol,stoploss_val,target_val):
  # Place an order
  order_id = 0
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
                                # stoploss=stoploss_val,
                                # trigger_price=target_val
                                )
    error_status = 'SUCCESSFULLY_PLACED'
  except Exception as e:
    error_status = e
  return order_id, error_status


def exit_cover_order(kite_conn_var,symbol):
  # Place an order for exit
  order_id = 0
  error_status = 'NOT_EXIT'
  try:
    order_id = kite_conn_var.place_order(tradingsymbol=symbol.split('.')[0],
                                exchange=kite_conn_var.EXCHANGE_NSE,
                                transaction_type=kite_conn_var.TRANSACTION_TYPE_SELL,
                                quantity=1,
                                variety=kite_conn_var.VARIETY_CO,
                                order_type=kite_conn_var.ORDER_TYPE_MARKET,
                                product=kite_conn_var.PRODUCT_CO,
                                validity=kite_conn_var.VALIDITY_DAY,
                                # stoploss=stoploss_val,
                                # trigger_price=target_val
                                )
    error_status = 'SUCCESSFULLY_EXITED'
  except Exception as e:
    error_status = e
  return order_id, error_status
