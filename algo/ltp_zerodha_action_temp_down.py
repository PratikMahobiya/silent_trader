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
    order_id = kite_conn_var.placeOrder(orderparams)
    error_status = 'SUCCESSFULLY_PLACED_EXIT'
  except Exception as e:
    error_status = e.args[0]
  return order_id, error_status

def exit_order(kite_conn_var,stock_config_obj):
  # Place an order for exit
  cancel_id = 0
  error_status = 'NOT_EXIT'
  try:
    cancel_id = kite_conn_var.cancelOrder(order_id=stock_config_obj.order_id,
                                  variety="NORMAL")
    error_status = 'REJECTED_CANCELLED'
  except Exception as e:
    error_status = e.args[0]
  return cancel_id, error_status
