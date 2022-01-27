from algo import serializers
from Model_15_temp import models
from . import ltp_zerodha_action_temp
from time import sleep

# place a sell order for exit
def place_ord(kite_conn_var,stock,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_temp.place_regular_sell_order(kite_conn_var,stock,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# place a cancel order for exit
def cancel_ord(kite_conn_var,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_temp.exit_order(kite_conn_var,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

def order_status_FLAG(order_id):
  from smartapi import SmartConnect
  obj=SmartConnect(api_key="MWxz7OCW",)
  obj.generateSession("P567723","Qwerty@12")
  book = obj.orderBook()['data']
  obj.terminateSession("P567723")
  for ord in book:
    if ord['orderid'] == order_id and ord['status'] == 'completed':
      return True
  return False

# SELL STOCK ; EXIT
def freeze_all(stock_list, kite_conn_var):
  active_stocks = {}
  active_stocks_str = ''
  gain = [0,]
  p_l  = [0,]
  for stock in stock_list:
    active_stocks_str += 'NSE:'+stock+'-EQ,'
  active_stocks = {"symbols":active_stocks_str[:-1]}
  if len(active_stocks_str) != 0:
    stocks_ltp = kite_conn_var.quotes(active_stocks)['d']
    for stock_key in stocks_ltp:
      sleep(0.3)
      price = stock_key['v']['lp']
      stock = stock_key['v']['short_name'].split('-')[0]
      stock_config_obj = models.CONFIG_15M_TEMP.objects.get(symbol = stock)
      if stock_config_obj.order_id != 0:
        if stock_config_obj.buy is True:
          if order_status_FLAG(stock_config_obj.order_id):
            # CALL PLACE ORDER ----
            order_id, order_status = place_ord(kite_conn_var,stock,stock_config_obj)
            # ---------------------
          else:
            # CALL CANCEL ORDER ----
            order_id, order_status = cancel_ord(kite_conn_var,stock_config_obj)
            # ----------------------

      diff          = price - stock_config_obj.buy_price
      profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
      diff          = round((diff * stock_config_obj.quantity),2) - 100
      gain.append(diff)
      p_l.append(profit)

      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'FREEZE','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status,'placed' : True}
      transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_15M_TEMP.objects.filter(symbol = stock).delete()
      models.TREND_15M_A_TEMP.objects.filter(symbol = stock).delete()
      stock_config_obj.buy                  = False
      stock_config_obj.placed               = False
      stock_config_obj.d_sl_flag            = False
      stock_config_obj.fixed_target_flag    = False
      stock_config_obj.trend                = False
      stock_config_obj.count                = 0
      stock_config_obj.order_id             = 0
      stock_config_obj.save()
  return gain, p_l