from algo import serializers
from Model_5M import models
from . import ltp_zerodha_action_crs_5

# place a sell order for exit
def place_ord(kite_conn_var,stock,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_crs_5.place_regular_sell_order(kite_conn_var,stock,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# place a cancel order for exit
def cancel_ord(kite_conn_var,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_crs_5.exit_order(kite_conn_var,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# SELL STOCK ; EXIT
def sell(stock, price, kite_conn_var):
  order_id      = 0
  order_status  = 'NOT ACTIVE'
  # if price hits First Target Starts TU.
  stock_config_obj = models.CONFIG_5M.objects.get(symbol = stock)
  if ((price >= stock_config_obj.target) and (stock_config_obj.d_sl_flag is False)):
    if stock_config_obj.buy is True:
      if stock_config_obj.count == 0:
        stock_config_obj.last_top     = price
        stock_config_obj.d_stoploss   = price - price*0.0045
        stock_config_obj.d_sl_flag    = True
        stock_config_obj.count        += 1
        stock_config_obj.save()

  # if price hits dynamic StopLoss, Exit
  elif stock_config_obj.d_sl_flag is True:
    if price <= stock_config_obj.d_stoploss:
      if stock_config_obj.buy is True:
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

        diff          = price - stock_config_obj.buy_price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2)
        type_str = 'HIT'
        if 0 < stock_config_obj.count < 8:
          type_str = 'HIT_{}'.format(stock_config_obj.count)
        else:
          type_str = 'JACKPOT_{}'.format(stock_config_obj.count)
        trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Exit','type':type_str,'price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.d_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_5_MIN_Serializer(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_5M.objects.filter(symbol = stock).delete()
        models.TREND_5M_A.objects.filter(symbol = stock).delete()
        stock_config_obj.buy          = False
        stock_config_obj.d_sl_flag    = False
        stock_config_obj.trend        = False
        stock_config_obj.count        = 0
        stock_config_obj.order_id     = 0
        stock_config_obj.save()

  # if price hits Fixed StopLoss, Exit
  elif price <= stock_config_obj.f_stoploss:
    if stock_config_obj.buy is True:
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

      diff          = price - stock_config_obj.buy_price
      profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
      diff          = round((diff * stock_config_obj.quantity),2)

      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Exit','type':'FIXED SL','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
      transaction   = serializers.CROSSOVER_5_MIN_Serializer(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_5M.objects.filter(symbol = stock).delete()
      models.TREND_5M_A.objects.filter(symbol = stock).delete()
      stock_config_obj.buy          = False
      stock_config_obj.d_sl_flag    = False
      stock_config_obj.trend        = False
      stock_config_obj.count        = 0
      stock_config_obj.order_id     = 0
      stock_config_obj.save()

  # if price hits outoftrend exit StopLoss, Exit
  elif stock_config_obj.trend is False:
    if price <= stock_config_obj.stoploss:
      if stock_config_obj.buy is True:
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

        diff          = price - stock_config_obj.buy_price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2)

        trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Exit','type':'OT_SL','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_5_MIN_Serializer(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_5M.objects.filter(symbol = stock).delete()
        models.TREND_5M_A.objects.filter(symbol = stock).delete()
        stock_config_obj.buy          = False
        stock_config_obj.d_sl_flag    = False
        stock_config_obj.trend        = False
        stock_config_obj.count        = 0
        stock_config_obj.order_id     = 0
        stock_config_obj.save()
  return 0

# SQUARE OFF, EXIT
def square_off(stock, price, kite_conn_var):
  stock_config_obj = models.CONFIG_5M.objects.get(symbol = stock)
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

      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Square_Off','type':'EOD','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
      transaction   = serializers.CROSSOVER_5_MIN_Serializer(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_5M.objects.filter(symbol = stock).delete()
      models.TREND_5M_A.objects.filter(symbol = stock).delete()
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

    trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'indicate':'Square_Off','type':'EOD','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.d_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
    transaction   = serializers.CROSSOVER_5_MIN_Serializer(data=trans_data)
    if transaction.is_valid():
      transaction.save()
    models.ENTRY_5M.objects.filter(symbol = stock).delete()
    models.TREND_5M_A.objects.filter(symbol = stock).delete()
    stock_config_obj.buy          = False
    stock_config_obj.d_sl_flag    = False
    stock_config_obj.trend        = False
    stock_config_obj.count        = 0
    stock_config_obj.order_id     = 0
    stock_config_obj.save()
  return 0