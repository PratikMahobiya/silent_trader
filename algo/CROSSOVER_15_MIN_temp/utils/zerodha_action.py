from smartapi import SmartConnect
from algo import models as models_a

def angelbroking_conn():
    obj=SmartConnect(api_key="MWxz7OCW",)
    obj.generateSession("P567723","Qwerty@12")
    return obj


def place_regular_buy_order(kite_conn_var,symbol, zerodha_flag_obj):
  # Place an order
  quantity  = 1
  ltp       = 0
  order_id  = 0
  order_status = 'NOT_PLACED'
  ang_conn = angelbroking_conn()
  try:
    ltp        = ang_conn.ltpData("NSE",symbol+'-EQ',models_a.STOCK.objects.get(symbol = symbol).token)['data']['ltp']
    while True:
      price = ltp * quantity
      if price >= zerodha_flag_obj.stock_amount:
        quantity = quantity - 1
        break
      quantity += 1
    if zerodha_flag_obj.zerodha_entry is True:
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
    order_status = 'SUCCESSFULLY_PLACED_EXIT'
  except Exception as e:
    order_status = 'PROBLEM AT ZERODHA END.'
  ang_conn.terminateSession("P567723")
  return order_id, order_status, ltp, quantity