from smartapi import SmartConnect
from algo import models as models_a

def angelbroking_conn():
    obj=SmartConnect(api_key="MWxz7OCW",)
    obj.generateSession("P567723","Qwerty@12")
    return obj


def place_regular_sell_order(kite_conn_var,symbol,stock_config_obj):
  # Place an order
  order_id = 0
  error_status = 'NOT_PLACED'
  try:
    ang_conn = angelbroking_conn()
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": symbol+'-EQ',
        "symboltoken": models_a.STOCK.objects.get(symbol = symbol).token,
        "transactiontype": "BUY",
        "exchange": "NSE",
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "quantity": '{}'.format(stock_config_obj.quantity)
        }
    order_id = ang_conn.placeOrder(orderparams)
    error_status = 'SUCCESSFULLY_PLACED_EXIT'
    ang_conn.terminateSession("P567723")
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  return order_id, error_status

def exit_order(kite_conn_var,stock_config_obj):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    ang_conn = angelbroking_conn()
    cancel_id = ang_conn.cancelOrder(order_id=stock_config_obj.order_id,
                                  variety="NORMAL")
    error_status = 'REJECTED_CANCELLED'
    ang_conn.terminateSession("P567723")
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END OR STOPLOSS HITTED.'
  return cancel_id, error_status
