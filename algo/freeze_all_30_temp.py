from algo import serializers
from Model_30M_temp import models
from . import ltp_zerodha_action_crs_30_temp

# place a sell order for exit
def place_ord(kite_conn_var,stock,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_crs_30_temp.place_regular_sell_order(kite_conn_var,stock,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# place a cancel order for exit
def cancel_ord(kite_conn_var,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_crs_30_temp.exit_order(kite_conn_var,stock_config_obj)
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
      price = stocks_ltp[stock_key]['last_price']
      gain.append(price)
      stock = stock_key.split(':')[-1]
      stock_config_obj = models.CONFIG_30M_TEMP.objects.get(symbol = stock)
      if stock_config_obj.order_id != 0:
        if stock_config_obj.buy is True:
          ord_det = kite_conn_var.order_history(order_id=stock_config_obj.order_id)
          if ord_det[-1]['status'] == 'COMPLETE':
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
          p_l.append(profit)

          trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Exit','type':'FREEZE','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
          transaction   = serializers.CROSSOVER_30_MIN_Serializer_TEMP(data=trans_data)
          if transaction.is_valid():
            transaction.save()
          models.ENTRY_30M_TEMP.objects.filter(symbol = stock).delete()
          models.TREND_30M_A_TEMP.objects.filter(symbol = stock).delete()
          stock_config_obj.buy          = False
          stock_config_obj.d_sl_flag    = False
          stock_config_obj.trend        = False
          stock_config_obj.count        = 0
          stock_config_obj.order_id     = 0
          stock_config_obj.save()
      else:
        order_id       = '0'
        order_status   = 'NOT PLACED'
        diff          = price - stock_config_obj.buy_price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2)
        p_l.append(profit)

        trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Exit','type':'FREEZE','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.d_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_30_MIN_Serializer_TEMP(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_30M_TEMP.objects.filter(symbol = stock).delete()
        models.TREND_30M_A_TEMP.objects.filter(symbol = stock).delete()
        stock_config_obj.buy          = False
        stock_config_obj.d_sl_flag    = False
        stock_config_obj.trend        = False
        stock_config_obj.count        = 0
        stock_config_obj.order_id     = 0
        stock_config_obj.save()
  return gain, p_l