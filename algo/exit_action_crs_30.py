from algo import serializers
from Model_30M import models
from . import ltp_zerodha_action_crs_30

# place a sell order for exit
def place_ord(kite_conn_var,stock,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_crs_30.place_regular_sell_order(kite_conn_var,stock,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# place a cancel order for exit
def cancel_ord(kite_conn_var,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_crs_30.exit_order(kite_conn_var,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# SELL STOCK ; EXIT
def sell(stock, price, gain, kite_conn_var):
  order_id      = 0
  order_status  = 'NOT ACTIVE'
  stock_config_obj = models.CONFIG_30M.objects.get(symbol = stock)
  # get the p&l
  gain_val = round(((price - stock_config_obj.buy_price) * stock_config_obj.quantity),2)
  gain_percent = round((((price - stock_config_obj.buy_price)/stock_config_obj.buy_price)*100),2)
  gain.append((gain_val, gain_percent))
  models.CONFIG_30M.objects.filter(symbol = stock).update(return_price = gain_val)
  
  # if price hits Fixed StopLoss, Exit
  # if price <= stock_config_obj.stoploss:
  #   if stock_config_obj.buy is True:
  #     if stock_config_obj.order_id != 0:
  #       ord_det = kite_conn_var.order_history(order_id=stock_config_obj.order_id)
  #       if ord_det[-1]['status'] == 'COMPLETE':
  #         # CALL PLACE ORDER ----
  #         order_id, order_status = place_ord(kite_conn_var,stock,stock_config_obj)
  #         # ---------------------
  #       else:
  #         # CALL CANCEL ORDER ----
  #         order_id, order_status = cancel_ord(kite_conn_var,stock_config_obj)
  #         # ----------------------

  #     diff          = price - stock_config_obj.buy_price
  #     profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
  #     diff          = round((diff * stock_config_obj.quantity),2) - 100

  #     trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'FIXED SL','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
  #     transaction   = serializers.CROSSOVER_30_MIN_Serializer(data=trans_data)
  #     if transaction.is_valid():
  #       transaction.save()
  #     models.ENTRY_30M.objects.filter(symbol = stock).delete()
  #     stock_config_obj.buy          = False
  #     stock_config_obj.placed       = False
  #     stock_config_obj.count        = 0
  #     stock_config_obj.order_id     = 0
  #     stock_config_obj.save()

  return 0