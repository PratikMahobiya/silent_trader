
def place_regular_buy_order(kite_conn_var,symbol,flag):
  # Place an order
  order_id = 0
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
    #                             variety=kite_conn_var.VARIETY_REGULAR,
    #                             order_type=kite_conn_var.ORDER_TYPE_MARKET,
    #                             product=kite_conn_var.PRODUCT_MIS,
    #                             validity=kite_conn_var.VALIDITY_DAY,
    #                             )
    flag[symbol]['quantity'] = quantity
    flag[symbol]['buying_price'] = stocks_ltp['NSE:'+symbol.split('.')[0]]['last_price']
    error_status = 'NOT_ACTIVE'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  return order_id, error_status