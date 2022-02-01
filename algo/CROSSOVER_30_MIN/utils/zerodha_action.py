from smartapi import SmartConnect
from algo import models as models_a

def angelbroking_conn():
    obj=SmartConnect(api_key="MWxz7OCW",)
    obj.generateSession("P567723","Qwerty@12")
    return obj

def order_status_FLAG(order_id,ang_conn):
  book = ang_conn.orderBook()['data']
  for ord in book:
    if ord['orderid'] == order_id and ord['status'] == 'completed':
      return True
  return False


def exit_order(ang_conn,stock_config_obj):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    cancel_id = ang_conn.cancelOrder(order_id=stock_config_obj.order_id,
                                  variety="NORMAL")
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
    ltp        = kite_conn_var.quotes({"symbols":'NSE:{}-EQ'.format(symbol)})['d'][0]['v']['lp']
    while True:
      price = ltp * quantity
      if price >= zerodha_flag_obj.stock_amount:
        quantity = quantity - 1
        break
      quantity += 1
    if zerodha_flag_obj.zerodha_entry is True:
      ang_conn = angelbroking_conn()
      orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": symbol+'-EQ',
        "symboltoken": models_a.STOCK.objects.get(symbol = symbol).token,
        "transactiontype": "BUY",
        "exchange": "NSE",
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": ltp,
        "quantity": '{}'.format(quantity)
        }
      order_id = ang_conn.placeOrder(orderparams)
      ang_conn.terminateSession("P567723")
    order_status = 'SUCCESSFULLY_PLACED_EXIT'
  except Exception as e:
    order_status = 'PROBLEM AT ZERODHA END.'
  return order_id, order_status, ltp, quantity

def place_regular_sell_order(kite_conn_var,symbol,stock_config_obj):
  # Place an order
  order_id = 0
  order_status = 'NOT_PLACED'
  ltp        = kite_conn_var.quotes({"symbols":'NSE:{}-EQ'.format(symbol)})['d'][0]['v']['lp']
  try:
    if stock_config_obj.order_id != 0:
      ang_conn = angelbroking_conn()
      if order_status_FLAG(stock_config_obj.order_id,ang_conn):
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": symbol+'-EQ',
            "symboltoken": models_a.STOCK.objects.get(symbol = symbol).token,
            "transactiontype": "SELL",
            "exchange": "NSE",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "quantity": '{}'.format(stock_config_obj.quantity)
            }
        order_id = ang_conn.placeOrder(orderparams)
        order_status = 'SUCCESSFULLY_PLACED_EXIT'
      else:
        # CALL CANCEL ORDER ----
        order_id, order_status = exit_order(ang_conn,stock_config_obj)
        # ----------------------
      ang_conn.terminateSession("P567723")
  except Exception as e:
    order_status = 'PROBLEM AT ZERODHA END.'
  return order_id, order_status, ltp
