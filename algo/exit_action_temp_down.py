from algo import serializers
from Model_15_temp_down import models
from . import ltp_zerodha_action_temp_down

# place a sell order for exit
def place_ord(kite_conn_var,stock,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_temp_down.place_regular_sell_order(kite_conn_var,stock,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# place a cancel order for exit
def cancel_ord(kite_conn_var,stock_config_obj):
  # -----------------------------------------------
  order_id, order_status = ltp_zerodha_action_temp_down.exit_order(kite_conn_var,stock_config_obj)
  # -----------------------------------------------
  return order_id, order_status

# SELL STOCK ; EXIT
def sell(stock, price, gain, kite_conn_var):
  order_id      = 0
  order_status  = 'NOT ACTIVE'
  stock_config_obj = models.CONFIG_15M_TEMP_DOWN.objects.get(symbol = stock)
  # get the p&l
  gain_val = round(((stock_config_obj.buy_price - price) * stock_config_obj.quantity),2)
  gain_percent = round((((stock_config_obj.buy_price - price)/stock_config_obj.buy_price)*100),2)
  gain.append((gain_val, gain_percent))
  models.CONFIG_15M_TEMP_DOWN.objects.filter(symbol = stock).update(return_price = gain_val)

  # if gap_up entry of 0.7 or above, Exit
  if stock_config_obj.fixed_target_flag is True:
    # if price hits Fixed Target, Exit
    if price <= stock_config_obj.fixed_target:
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

        diff          = stock_config_obj.buy_price - price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2) - 100

        trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'HIT_0.5','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
        models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
        stock_config_obj.buy                  = False
        stock_config_obj.placed               = False
        stock_config_obj.d_sl_flag            = False
        stock_config_obj.fixed_target_flag    = False
        stock_config_obj.trend                = False
        stock_config_obj.count                = 0
        stock_config_obj.order_id             = 0
        stock_config_obj.save()

    # if price hits Fixed StopLoss, Exit
    elif price >= stock_config_obj.f_stoploss:
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

        diff          = stock_config_obj.buy_price - price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2) + 100

        trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'FIXED SL','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
        models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
        stock_config_obj.buy                  = False
        stock_config_obj.placed               = False
        stock_config_obj.d_sl_flag            = False
        stock_config_obj.fixed_target_flag    = False
        stock_config_obj.trend                = False
        stock_config_obj.count                = 0
        stock_config_obj.order_id             = 0
        stock_config_obj.save()

    # if price hits outoftrend exit StopLoss, Exit
    elif stock_config_obj.trend is False:
      if price >= stock_config_obj.stoploss:
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

          diff          = stock_config_obj.buy_price - price
          profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
          diff          = round((diff * stock_config_obj.quantity),2) + 100

          trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'OT_SL','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
          transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
          if transaction.is_valid():
            transaction.save()
          models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
          models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
          stock_config_obj.buy                  = False
          stock_config_obj.placed               = False
          stock_config_obj.d_sl_flag            = False
          stock_config_obj.fixed_target_flag    = False
          stock_config_obj.trend                = False
          stock_config_obj.count                = 0
          stock_config_obj.order_id             = 0
          stock_config_obj.save()

  # if price hits First Target Starts TU.
  elif ((price <= stock_config_obj.target) and (stock_config_obj.d_sl_flag is False)):
    if stock_config_obj.buy is True:
      if stock_config_obj.count == 0:
        stock_config_obj.last_top     = price
        stock_config_obj.d_stoploss   = price + price*0.005
        stock_config_obj.d_sl_flag    = True
        stock_config_obj.count        += 1
        stock_config_obj.save()
  # elif price <= stock_config_obj.target:
  #   if stock_config_obj.buy is True:
  #     if stock_config_obj.count == 0:
  #       stock_config_obj.target       = price - price*0.0025
  #       stock_config_obj.d_stoploss   = stock_config_obj.buy_price
  #       stock_config_obj.d_sl_flag    = True
  #       stock_config_obj.count        += 1
  #       stock_config_obj.save()
  #     else:
  #       stock_config_obj.target       = price - price*0.0025
  #       stock_config_obj.d_stoploss   = price + price*0.005
  #       stock_config_obj.d_sl_flag    = True
  #       stock_config_obj.count        += 1
  #       stock_config_obj.save()

  # if price hits dynamic StopLoss, Exit
  elif stock_config_obj.d_sl_flag is True:
    if price >= stock_config_obj.d_stoploss:
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

        diff          = stock_config_obj.buy_price - price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2) - 100

        type_str = 'HIT'
        if 0 < stock_config_obj.count < 8:
          type_str = 'HIT_{}'.format(stock_config_obj.count)
        else:
          type_str = 'JACKPOT_{}'.format(stock_config_obj.count)
        trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':type_str,'price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.d_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
        models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
        stock_config_obj.buy                  = False
        stock_config_obj.placed               = False
        stock_config_obj.d_sl_flag            = False
        stock_config_obj.fixed_target_flag    = False
        stock_config_obj.trend                = False
        stock_config_obj.count                = 0
        stock_config_obj.order_id             = 0
        stock_config_obj.save()

  # if price hits Fixed StopLoss, Exit
  elif price >= stock_config_obj.f_stoploss:
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

      diff          = stock_config_obj.buy_price - price
      profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
      diff          = round((diff * stock_config_obj.quantity),2) + 100

      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'FIXED SL','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
      transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
      models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
      stock_config_obj.buy                  = False
      stock_config_obj.placed               = False
      stock_config_obj.d_sl_flag            = False
      stock_config_obj.fixed_target_flag    = False
      stock_config_obj.trend                = False
      stock_config_obj.count                = 0
      stock_config_obj.order_id             = 0
      stock_config_obj.save()

  # if price hits outoftrend exit StopLoss, Exit
  elif stock_config_obj.trend is False:
    if price >= stock_config_obj.stoploss:
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

        diff          = stock_config_obj.buy_price - price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2) + 100

        trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'OT_SL','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
        models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
        stock_config_obj.buy                  = False
        stock_config_obj.placed               = False
        stock_config_obj.d_sl_flag            = False
        stock_config_obj.fixed_target_flag    = False
        stock_config_obj.trend                = False
        stock_config_obj.count                = 0
        stock_config_obj.order_id             = 0
        stock_config_obj.save()
  return 0

# SQUARE OFF, EXIT
def square_off(stock, price, kite_conn_var):
  stock_config_obj = models.CONFIG_15M_TEMP_DOWN.objects.get(symbol = stock)
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

      diff          = stock_config_obj.buy_price - price
      profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
      diff          = round((diff * stock_config_obj.quantity),2) - 100

      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'Square_Off','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
      transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
      models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
      stock_config_obj.buy                  = False
      stock_config_obj.placed               = False
      stock_config_obj.d_sl_flag            = False
      stock_config_obj.fixed_target_flag    = False
      stock_config_obj.trend                = False
      stock_config_obj.count                = 0
      stock_config_obj.order_id             = 0
      stock_config_obj.save()
  else:
    order_id       = '0'
    order_status   = 'NOT PLACED'
    diff          = stock_config_obj.buy_price - price
    profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
    diff          = round((diff * stock_config_obj.quantity),2) - 100

    trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'Square_Off','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.d_stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
    transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
    if transaction.is_valid():
      transaction.save()
    models.ENTRY_15M_TEMP_DOWN.objects.filter(symbol = stock).delete()
    models.TREND_15M_A_TEMP_DOWN.objects.filter(symbol = stock).delete()
    stock_config_obj.buy                  = False
    stock_config_obj.placed               = False
    stock_config_obj.d_sl_flag            = False
    stock_config_obj.fixed_target_flag    = False
    stock_config_obj.trend                = False
    stock_config_obj.count                = 0
    stock_config_obj.order_id             = 0
    stock_config_obj.save()
  return 0