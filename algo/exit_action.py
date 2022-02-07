from algo import serializers
from Model_15M import models
from . import ltp_zerodha_action

# place a sell order for exit
def place_ord(kite_conn_var,stock,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action.place_regular_sell_order(kite_conn_var,stock,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# place a cancel order for exit
def cancel_ord(kite_conn_var,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action.exit_order(kite_conn_var,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

def order_status_FLAG(order_id,kite_conn_var):
  book = kite_conn_var.orderBook()['data']
  for ord in book:
    if ord['orderid'] == order_id and ord['status'] == 'complete':
      return True
  return False

# SELL STOCK ; EXIT
def sell(stock, price, gain, kite_conn_var):
  order_id      = 0
  order_status  = 'NOT ACTIVE'
  stock_config_obj = models.CONFIG_15M.objects.get(symbol = stock)
  # get the p&l
  gain_val = round(((stock_config_obj.buy_price - price) * stock_config_obj.quantity),2)
  gain_percent = round((((stock_config_obj.buy_price - price)/stock_config_obj.buy_price)*100),2)
  gain.append((gain_val, gain_percent))
  models.CONFIG_15M.objects.filter(symbol = stock).update(return_price = gain_val, ltp = price)

  if stock_config_obj.count > gain_percent:
    models.CONFIG_15M.objects.filter(symbol = stock).update(count = gain_percent)

  # if price hits TARGET, Exit
  # if price <= stock_config_obj.target:
  #   if stock_config_obj.buy is True:
  #     if stock_config_obj.order_id != 0:
  #       if order_status_FLAG(stock_config_obj.order_id,kite_conn_var):
  #         # CALL PLACE ORDER ----
  #         order_id, order_status = place_ord(kite_conn_var,stock,stock_config_obj)
  #         # ---------------------
  #       else:
  #         # CALL CANCEL ORDER ----
  #         order_id, order_status = cancel_ord(kite_conn_var,stock_config_obj)
  #         # ----------------------

  #       diff          = stock_config_obj.buy_price - price
  #       profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
  #       diff          = round((diff * stock_config_obj.quantity),2) - 100
  #       trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'HIT','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
  #       transaction   = serializers.CROSSOVER_15_Min_Serializer(data=trans_data)
  #       if transaction.is_valid():
  #         transaction.save()
  #       # models.ENTRY_15M.objects.filter(symbol = stock).delete()
  #       # stock_config_obj.buy          = False
  #       stock_config_obj.placed       = False
  #       stock_config_obj.count        = 0
  #       stock_config_obj.order_id     = 0
  #       stock_config_obj.save()
  return 0