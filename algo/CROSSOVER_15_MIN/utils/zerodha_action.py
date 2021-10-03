
def place_regular_buy_order(kite_conn_var,symbol):
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
      if price >= 6000:
        quantity = quantity - 1
        break
      quantity += 1
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