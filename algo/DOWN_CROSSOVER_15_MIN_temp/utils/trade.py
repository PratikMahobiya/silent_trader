from algo import serializers
from Model_15_temp_down import models
from algo import models as models_a
import talib
from . import zerodha_action

def place_ord(kite_conn_var,stock, zerodha_flag_obj):
  # Place Order in ZERODHA.
  # -------------------------------------------
  order_id, order_status, price, quantity = zerodha_action.place_regular_buy_order(kite_conn_var,stock, zerodha_flag_obj)
  # -------------------------------------------
  return order_id, order_status, price, quantity

def stockrsi(fastk, fastd):
  flag = []
  if fastd[-1] >= 80:
    flag.append(0)
  else:
    flag.append(1)
  if fastk[-1] >= 80:
    flag.append(0)
  else:
    flag.append(1)
  if flag.count(0) == 2:
    return False
  else:
    return True

def checking_close_ema_diff(stock,data_frame,ema_max):
  per = ((data_frame[stock]['Close'].iloc[-2] - ema_max[-1])/ema_max[-1])*100
  if per >= 0.7:
    return True
  else:
    return False

def checking_stoploss_fixed(price):
  stoploss_val = price + price*0.004
  return round(stoploss_val,2)

def checking_stoploss_ot(price, atr):
  stoploss_val = price + atr[-1]*0.5
  return round(stoploss_val,2)

def checking_stoploss_tu(price):
  stoploss_val = price + price*0.005
  return round(stoploss_val,2)

def trade_execution(data_frame, for_trade_stocks, intervals, kite_conn_var):
  zerodha_flag_obj = models_a.PROFIT_CONFIG.objects.get(model_name = 'CRS_TEMP')
  for stock in for_trade_stocks:
    ema_max     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[4])
    ema_min     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[5])
    rsi         = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[9])
    atr         = talib.ATR(data_frame[stock]['High'].iloc[:-1],data_frame[stock]['Low'].iloc[:-1],data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[10])
    fastk, fastd = talib.STOCHRSI(data_frame[stock]['Close'].iloc[:-1], timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
    stock_config_obj = models.CONFIG_15M_TEMP_DOWN.objects.get(symbol = stock)
    if stock_config_obj.buy is False:
      buys(stock, data_frame, ema_max, ema_min, rsi, atr, fastk, fastd, kite_conn_var, zerodha_flag_obj)
    else:
      updatestoploss(stock, data_frame, atr)
  return 0

# UPDATE STOPLOSS
def updatestoploss(stock, data_frame, atr):
  stock_config_obj = models.CONFIG_15M_TEMP_DOWN.objects.get(symbol = stock)
  if data_frame[stock]['Close'].iloc[-2] < stock_config_obj.last_top:
    stock_config_obj.last_top = data_frame[stock]['Close'].iloc[-2]
    stock_config_obj.stoploss = checking_stoploss_ot(data_frame[stock]['Close'].iloc[-2],atr)
    if stock_config_obj.d_sl_flag is True:
      stock_config_obj.d_stoploss = checking_stoploss_tu(data_frame[stock]['Close'].iloc[-2])
      stock_config_obj.count        += 1
    stock_config_obj.save()
  return 0

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, ema_max, ema_min, rsi, atr, fastk, fastd, kite_conn_var, zerodha_flag_obj):
  # Difference btw ema-max-min is less or equal to 0.2 and price is above ema-min-max
  if ema_max[-1] < ema_min[-1]:
    # if stockrsi(fastk, fastd):
      if data_frame[stock]['Close'].iloc[-2] < ema_min[-1]:
        if data_frame[stock]['Close'].iloc[-2] < ema_max[-1]:
          if data_frame[stock]['Close'].iloc[-3] < ema_min[-2]:
            if data_frame[stock]['Close'].iloc[-3] < ema_max[-2]:
              if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.25):
                # Place Order in ZERODHA.
                order_id, order_status, price, quantity = place_ord(kite_conn_var,stock, zerodha_flag_obj)
                # UPDATE CONFIG
                type_str         = 'BF_{}'.format(round((((data_frame[stock]['Close'].iloc[-2] - ema_max[-1])/ema_max[-1])*100),2))
                stock_config_obj = models.CONFIG_15M_TEMP_DOWN.objects.get(symbol = stock)
                stock_config_obj.buy            = True
                stock_config_obj.f_stoploss     = checking_stoploss_fixed(price)
                stock_config_obj.stoploss       = checking_stoploss_ot(price,atr)
                stock_config_obj.target         = price - price * 0.006
                stock_config_obj.quantity       = quantity
                stock_config_obj.buy_price      = price
                stock_config_obj.last_top       = price
                stock_config_obj.order_id       = order_id
                stock_config_obj.order_status   = order_status
                if checking_close_ema_diff(stock,data_frame,ema_max):
                  stock_config_obj.fixed_target       = price - price * 0.005
                  stock_config_obj.fixed_target_flag  = True
                stock_config_obj.save()
                # TRANSACTION TABLE UPDATE
                trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price':price,'quantity':quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':None,'profit':None,'order_id':order_id,'order_status':order_status}
                transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
                if transaction.is_valid():
                  transaction.save()
                # UPDATE CURRENT ENTRY TABLE
                models.ENTRY_15M_TEMP_DOWN(symbol = stock, reference_id = transaction.data['id']).save()

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.2, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] < ema_max[-1]:
    if ema_min[-2] > ema_max[-2]:
      # if stockrsi(fastk, fastd):
        if data_frame[stock]['Close'].iloc[-2] < ema_min[-1]:
          if data_frame[stock]['Close'].iloc[-2] < ema_max[-1]:
            if data_frame[stock]['Close'].iloc[-3] < ema_min[-2]:
              if data_frame[stock]['Close'].iloc[-3] < ema_max[-2]:
                if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.25):
                  if rsi[-1] < rsi[-2] and rsi[-1] < rsi[-3]:
                    # Place Order in ZERODHA.
                    order_id, order_status, price, quantity = place_ord(kite_conn_var,stock, zerodha_flag_obj)
                    # UPDATE CONFIG
                    type_str         = 'AF_{}'.format(round((((data_frame[stock]['Close'].iloc[-2] - ema_max[-1])/ema_max[-1])*100),2))
                    stock_config_obj = models.CONFIG_15M_TEMP_DOWN.objects.get(symbol = stock)
                    stock_config_obj.buy            = True
                    stock_config_obj.f_stoploss     = checking_stoploss_fixed(price)
                    stock_config_obj.stoploss       = checking_stoploss_ot(price,atr)
                    stock_config_obj.target         = price - price * 0.006
                    stock_config_obj.quantity       = quantity
                    stock_config_obj.buy_price      = price
                    stock_config_obj.last_top       = price
                    stock_config_obj.order_id       = order_id
                    stock_config_obj.order_status   = order_status
                    if checking_close_ema_diff(stock,data_frame,ema_max):
                      stock_config_obj.fixed_target       = price - price * 0.005
                      stock_config_obj.fixed_target_flag  = True
                    stock_config_obj.save()
                    # TRANSACTION TABLE UPDATE
                    trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price':price,'quantity':quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':None,'profit':None,'order_id':order_id,'order_status':order_status}
                    transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN(data=trans_data)
                    if transaction.is_valid():
                      transaction.save()
                    # UPDATE CURRENT ENTRY TABLE
                    models.ENTRY_15M_TEMP_DOWN(symbol = stock, reference_id = transaction.data['id']).save()

# BTST TARDES
def trade_execution_BTST(data_frame, for_trade_stocks, intervals, kite_conn_var):
  zerodha_flag_obj = models_a.PROFIT_CONFIG.objects.get(model_name = 'CRS_15_TEMP_BTST')
  for stock in for_trade_stocks:
    ema_max     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[4])
    ema_min     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[5])
    rsi         = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[9])
    atr         = talib.ATR(data_frame[stock]['High'].iloc[:-1],data_frame[stock]['Low'].iloc[:-1],data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[10])
    fastk, fastd = talib.STOCHRSI(data_frame[stock]['Close'].iloc[:-1], timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
    stock_config_obj = models.CONFIG_15M_TEMP_BTST_DOWN.objects.get(symbol = stock)
    if stock_config_obj.buy is False:
      buys_BTST(stock, data_frame, ema_max, ema_min, rsi, atr, fastk, fastd, kite_conn_var, zerodha_flag_obj)
    else:
      updatestoploss(stock, data_frame, atr)
  return 0

# BUYS STOCKS ; ENTRY
def buys_BTST(stock, data_frame, ema_max, ema_min, rsi, atr, fastk, fastd, kite_conn_var, zerodha_flag_obj):
  # Difference btw ema-max-min is less or equal to 0.2 and price is above ema-min-max
  if ema_max[-1] < ema_min[-1]:
    # if stockrsi(fastk, fastd):
      if data_frame[stock]['Close'].iloc[-2] < ema_min[-1]:
        if data_frame[stock]['Close'].iloc[-2] < ema_max[-1]:
          if data_frame[stock]['Close'].iloc[-3] < ema_min[-2]:
            if data_frame[stock]['Close'].iloc[-3] < ema_max[-2]:
              if ((((ema_max[-1]-ema_min[-1])/ema_max[-1])*100) <= 0.25):
                # Place Order in ZERODHA.
                order_id, order_status, price, quantity = place_ord(kite_conn_var,stock, zerodha_flag_obj)
                # UPDATE CONFIG
                type_str         = 'BF_{}'.format(round((((data_frame[stock]['Close'].iloc[-2] - ema_max[-1])/ema_max[-1])*100),2))
                stock_config_obj = models.CONFIG_15M_TEMP_BTST_DOWN.objects.get(symbol = stock)
                stock_config_obj.buy            = True
                stock_config_obj.f_stoploss     = checking_stoploss_fixed(price)
                stock_config_obj.stoploss       = checking_stoploss_ot(price,atr)
                stock_config_obj.target         = price - price * 0.006
                stock_config_obj.quantity       = quantity
                stock_config_obj.buy_price      = price
                stock_config_obj.last_top       = price
                stock_config_obj.order_id       = order_id
                stock_config_obj.order_status   = order_status
                if checking_close_ema_diff(stock,data_frame,ema_max):
                  stock_config_obj.fixed_target       = price - price * 0.005
                  stock_config_obj.fixed_target_flag  = True
                stock_config_obj.save()
                # TRANSACTION TABLE UPDATE
                trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price':price,'quantity':quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':None,'profit':None,'order_id':order_id,'order_status':order_status}
                transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN_BTST(data=trans_data)
                if transaction.is_valid():
                  transaction.save()
                # UPDATE CURRENT ENTRY TABLE
                models.ENTRY_15M_TEMP_BTST_DOWN(symbol = stock, reference_id = transaction.data['id']).save()

  # After CrossOver ema-min greater than ema-max and pema-min less than pema-max, diff is less than 0.2, curr_rsi is greater than its prev_2_rsi's
  elif ema_min[-1] < ema_max[-1]:
    if ema_min[-2] > ema_max[-2]:
      # if stockrsi(fastk, fastd):
        if data_frame[stock]['Close'].iloc[-2] < ema_min[-1]:
          if data_frame[stock]['Close'].iloc[-2] < ema_max[-1]:
            if data_frame[stock]['Close'].iloc[-3] < ema_min[-2]:
              if data_frame[stock]['Close'].iloc[-3] < ema_max[-2]:
                if ((((ema_min[-1]-ema_max[-1])/ema_min[-1])*100) <= 0.25):
                  if rsi[-1] < rsi[-2] and rsi[-1] < rsi[-3]:
                    # Place Order in ZERODHA.
                    order_id, order_status, price, quantity = place_ord(kite_conn_var,stock, zerodha_flag_obj)
                    # UPDATE CONFIG
                    type_str         = 'AF_{}'.format(round((((data_frame[stock]['Close'].iloc[-2] - ema_max[-1])/ema_max[-1])*100),2))
                    stock_config_obj = models.CONFIG_15M_TEMP_BTST_DOWN.objects.get(symbol = stock)
                    stock_config_obj.buy            = True
                    stock_config_obj.f_stoploss     = checking_stoploss_fixed(price)
                    stock_config_obj.stoploss       = checking_stoploss_ot(price,atr)
                    stock_config_obj.target         = price - price * 0.006
                    stock_config_obj.quantity       = quantity
                    stock_config_obj.buy_price      = price
                    stock_config_obj.last_top       = price
                    stock_config_obj.order_id       = order_id
                    stock_config_obj.order_status   = order_status
                    if checking_close_ema_diff(stock,data_frame,ema_max):
                      stock_config_obj.fixed_target       = price - price * 0.005
                      stock_config_obj.fixed_target_flag  = True
                    stock_config_obj.save()
                    # TRANSACTION TABLE UPDATE
                    trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price':price,'quantity':quantity,'stoploss':stock_config_obj.f_stoploss,'target':stock_config_obj.target,'difference':None,'profit':None,'order_id':order_id,'order_status':order_status}
                    transaction   = serializers.CROSSOVER_15_Min_Serializer_TEMP_DOWN_BTST(data=trans_data)
                    if transaction.is_valid():
                      transaction.save()
                    # UPDATE CURRENT ENTRY TABLE
                    models.ENTRY_15M_TEMP_BTST_DOWN(symbol = stock, reference_id = transaction.data['id']).save()