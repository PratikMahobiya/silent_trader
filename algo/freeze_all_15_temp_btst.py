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

def order_status_FLAG(order_id,kite_conn_var):
  book = kite_conn_var.orderBook()['data']
  for ord in book:
    if ord['orderid'] == order_id and ord['status'] == 'completed':
      return True
  return False

# SELL STOCK ; EXIT
def freeze_all(stock_list, kite_conn_var):
  stocks_ltp = {}
  from algo import models as models_a
  gain = [0,]
  p_l  = [0,]
  if len(stock_list) != 0:
    for stock in stock_list:
      stocks_ltp[stock] = kite_conn_var.ltpData("NSE",stock+'-EQ',models_a.STOCK.objects.get(symbol = stock).token)['data']['ltp']
      sleep(0.2)
    for stock_key in stocks_ltp:
      sleep(0.3)
      price = stocks_ltp[stock_key]
      stock = stock_key
      stock_config_obj = models.CONFIG_15M_TEMP_BTST.objects.get(symbol = stock)
      if stock_config_obj.order_id != 0:
        if stock_config_obj.buy is True:
          if order_status_FLAG(stock_config_obj.order_id,kite_conn_var):
            # CALL PLACE ORDER ----
            order_id, order_status = place_ord(kite_conn_var,stock,stock_config_obj)
            # ---------------------
          else:
            # CALL CANCEL ORDER ----
            order_id, order_status = cancel_ord(kite_conn_var,stock_config_obj)
            # ----------------------

          diff          = price - stock_config_obj.buy_price
          profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
          diff          = round((diff * stock_config_obj.quantity),2)
          gain.append(diff)
          p_l.append(profit)

          # trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Exit','type':'FREEZE','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
          # transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_BTST(data=trans_data)
          # if transaction.is_valid():
          #   transaction.save()
          # models.ENTRY_15M_TEMP_BTST.objects.filter(symbol = stock).delete()
          # models.TREND_15M_A_TEMP_BTST.objects.filter(symbol = stock).delete()
          # stock_config_obj.buy                  = False
          # stock_config_obj.d_sl_flag            = False
          # stock_config_obj.fixed_target_flag    = False
          # stock_config_obj.trend                = False
          # stock_config_obj.count                = 0
          # stock_config_obj.order_id             = 0
          # stock_config_obj.save()
      else:
        order_id       = '0'
        order_status   = 'NOT PLACED'
        diff          = price - stock_config_obj.buy_price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2)
        gain.append(diff)
        p_l.append(profit)

        # trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Exit','type':'FREEZE','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.d_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        # transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_BTST(data=trans_data)
        # if transaction.is_valid():
        #   transaction.save()
        # models.ENTRY_15M_TEMP_BTST.objects.filter(symbol = stock).delete()
        # models.TREND_15M_A_TEMP_BTST.objects.filter(symbol = stock).delete()
        # stock_config_obj.buy                  = False
        # stock_config_obj.d_sl_flag            = False
        # stock_config_obj.fixed_target_flag    = False
        # stock_config_obj.trend                = False
        # stock_config_obj.count                = 0
        # stock_config_obj.order_id             = 0
        # stock_config_obj.save()
  return gain, p_l