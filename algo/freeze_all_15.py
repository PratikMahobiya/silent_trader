from algo import serializers
from Model_15M import models
from . import ltp_zerodha_action
from time import sleep

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

# SELL STOCK ; EXIT
def freeze_all(stock_list, kite_conn_var):
  active_stocks = []
  gain = [0,]
  p_l  = [0,]
  for stock in stock_list:
    active_stocks.append('NSE:'+stock)
  if len(active_stocks) != 0:
    stocks_ltp = kite_conn_var.ltp(active_stocks)
    for stock_key in stocks_ltp:
      sleep(0.3)
      price = stocks_ltp[stock_key]['last_price']
      stock = stock_key.split(':')[-1]
      stock_config_obj = models.CONFIG_15M.objects.get(symbol = stock)
      if stock_config_obj.order_id != 0:
        ord_det = kite_conn_var.order_history(order_id=stock_config_obj.order_id)
        if ord_det[-1]['status'] == 'COMPLETE':
          # CALL PLACE ORDER ----
          order_id, order_status = place_ord(kite_conn_var,stock,stock_config_obj)
          # ---------------------
        else:
          # CALL CANCEL ORDER ----
          order_id, order_status = cancel_ord(kite_conn_var,stock_config_obj)
          # ----------------------

      diff          = stock_config_obj.buy_price - price
      profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
      diff          = round((diff * stock_config_obj.quantity),2) - 100
      gain.append(diff)
      p_l.append(profit)

      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'FREEZE','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status,'placed' : True}
      transaction   = serializers.CROSSOVER_15_Min_Serializer(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_15M.objects.filter(symbol = stock).delete()
      stock_config_obj.buy          = False
      stock_config_obj.placed       = False
      stock_config_obj.count        = 0
      stock_config_obj.order_id     = 0
      stock_config_obj.save()
  return gain, p_l