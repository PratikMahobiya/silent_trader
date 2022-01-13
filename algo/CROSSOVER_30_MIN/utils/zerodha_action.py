
def exit_order(kite_conn_var,stock_config_obj):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    cancel_id = kite_conn_var.cancel_order(order_id=stock_config_obj.order_id,
                                  variety=kite_conn_var.VARIETY_REGULAR)
    error_status = 'REJECTED_CANCELLED'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END OR STOPLOSS HITTED.'
  return cancel_id, error_status

def place_regular_buy_order(kite_conn_var,symbol, zerodha_flag_obj):
  # Place an order
  quantity  = 1
  ltp       = 0
  order_id  = 0
  order_status = 'NOT_PLACED'
  try:
    stocks_ltp = kite_conn_var.ltp('NSE:'+symbol)
    ltp        = stocks_ltp['NSE:'+symbol]['last_price']
    while True:
      price = ltp * quantity
      if price >= zerodha_flag_obj.stock_amount:
        quantity = quantity - 1
        break
      quantity += 1
    if zerodha_flag_obj.zerodha_entry is True:
      order_id = kite_conn_var.place_order(tradingsymbol=symbol,
                                  exchange=kite_conn_var.EXCHANGE_NSE,
                                  transaction_type=kite_conn_var.TRANSACTION_TYPE_BUY,
                                  quantity=quantity,
                                  variety=kite_conn_var.VARIETY_REGULAR,
                                  order_type=kite_conn_var.ORDER_TYPE_LIMIT,
                                  product=kite_conn_var.PRODUCT_MIS,
                                  validity=kite_conn_var.VALIDITY_DAY,
                                  price=ltp,
                                  )
    order_status = 'SUCCESSFULLY_PLACED_ENTRY'
  except Exception as e:
    order_status = 'PROBLEM AT ZERODHA END.'
  return order_id, order_status, ltp, quantity

def place_regular_sell_order(kite_conn_var,symbol,stock_config_obj):
  # Place an order
  order_id = 0
  order_status = 'NOT_PLACED'
  stocks_ltp = kite_conn_var.ltp('NSE:'+symbol)
  ltp        = stocks_ltp['NSE:'+symbol]['last_price']
  try:
    if stock_config_obj.order_id != 0:
      ord_det = kite_conn_var.order_history(order_id=stock_config_obj.order_id)
      if ord_det[-1]['status'] == 'COMPLETE':
        order_id = kite_conn_var.place_order(tradingsymbol=symbol,
                                      exchange=kite_conn_var.EXCHANGE_NSE,
                                      transaction_type=kite_conn_var.TRANSACTION_TYPE_SELL,
                                      quantity=stock_config_obj.quantity,
                                      variety=kite_conn_var.VARIETY_REGULAR,
                                      order_type=kite_conn_var.ORDER_TYPE_MARKET,
                                      product=kite_conn_var.PRODUCT_MIS,
                                      validity=kite_conn_var.VALIDITY_DAY,
                                      )
        order_status = 'SUCCESSFULLY_PLACED_EXIT'
      else:
        # CALL CANCEL ORDER ----
        order_id, order_status = exit_order(kite_conn_var,stock_config_obj)
        # ----------------------
  except Exception as e:
    order_status = 'PROBLEM AT ZERODHA END.'
  return order_id, order_status, ltp
