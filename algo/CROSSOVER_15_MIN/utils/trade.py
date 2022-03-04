from datetime import date, timedelta
import pandas as pd
from algo import serializers
from Model_15M import models
from algo import models as models_a
import talib
from time import sleep
from . import zerodha_action

def place_ord_buy(kite_conn_var,stock, zerodha_flag_obj):
  # Place Order in ZERODHA.
  # -------------------------------------------
  order_id, order_status, price, quantity = zerodha_action.place_regular_buy_order(kite_conn_var,stock, zerodha_flag_obj)
  # -------------------------------------------
  return order_id, order_status, price, quantity

def place_ord_sell(kite_conn_var,stock, stock_config_obj):
  # Place Order in ZERODHA.
  # -------------------------------------------
  order_id, order_status, price = zerodha_action.place_regular_sell_order(kite_conn_var,stock, stock_config_obj)
  # -------------------------------------------
  return order_id, order_status, price

def check_15_min(stock_name,kite_conn_var):
  now = date.today()
  from_day = now - timedelta(days=30)
  data = {"symbol":"NSE:{}-EQ".format(stock_name),"resolution":"15","date_format":"1","range_from":from_day,"range_to":now,"cont_flag":"0"}
  data = kite_conn_var.history(data)['candles']
  data=pd.DataFrame(data)
  data[0] = pd.to_datetime(data[0],unit = 's')
  data_frame = data.set_index(data[0], drop=False, append=False, inplace=False, verify_integrity=False).drop(0, 1)
  data_frame.rename(columns = {0:'date',1:'Open',2:'High',3:'Low',4:'Close',5:'Volume'}, inplace = True)
  data_frame.index.names = ['date']
  macd, macdsignal, macdhist = talib.MACD(data_frame['Close'], fastperiod=9, slowperiod=23, signalperiod=9)
  if macd[-1] < macdsignal[-1]:
    return True
  else:
    return False

def trade_execution(data_frame, for_trade_stocks, intervals, kite_conn_var):
  zerodha_flag_obj = models_a.PROFIT_CONFIG.objects.get(model_name = 'CRS_MAIN')
  for stock in for_trade_stocks:
    ema           = talib.EMA(data_frame[stock]['Close'], timeperiod=intervals[5])
    adx           = talib.ADX(data_frame[stock]['High'],data_frame[stock]['Low'],data_frame[stock]['Close'], timeperiod=11)
    macd, macdsignal, macdhist = talib.MACD(data_frame[stock]['Close'], fastperiod=intervals[2], slowperiod=intervals[3], signalperiod=intervals[4])
    stock_config_obj = models.CONFIG_15M.objects.get(symbol = stock)
    if stock_config_obj.buy is False:
      buys(stock, data_frame, macd, macdsignal, macdhist, ema, adx, kite_conn_var, zerodha_flag_obj)
    else:
      sell(stock, data_frame, macd, macdsignal, macdhist, adx, kite_conn_var, zerodha_flag_obj)
  return 0

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, macd, macdsignal, macdhist, ema, adx, kite_conn_var, zerodha_flag_obj):
  stock_config_obj = models.CONFIG_15M.objects.get(symbol = stock)
  # After CrossOver MACD AND MACDSIGNAL
  if macd[-1] < macdsignal[-1]:
    if macd[-2] > macdsignal[-2]:
      if data_frame[stock]['Close'].iloc[-2] < ema[-1]:
        if macdhist[-1] < macdhist[-2]:
          if macdhist[-2] < macdhist[-3]:
            if adx[-1] <= 40:
              # if check_15_min(stock,kite_conn_var):
                # Place Order in ZERODHA.
                order_id, order_status, price, quantity = place_ord_buy(kite_conn_var,stock, zerodha_flag_obj)
                if order_id != 0:
                  stock_config_obj.placed       = True
                # UPDATE CONFIG
                type_str         = 'AF_SELL'
                stock_config_obj.buy            = True
                stock_config_obj.stoploss       = price + price * 0.006
                stock_config_obj.target         = price - price * 0.041
                stock_config_obj.quantity       = quantity
                stock_config_obj.buy_price      = price
                stock_config_obj.order_id       = order_id
                stock_config_obj.order_status   = order_status
                stock_config_obj.save()
                # TRANSACTION TABLE UPDATE
                trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price':price,'quantity':quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':None,'profit':None,'order_id':order_id,'order_status':order_status}
                transaction   = serializers.CROSSOVER_15_Min_Serializer(data=trans_data)
                if transaction.is_valid():
                  transaction.save()
                # UPDATE CURRENT ENTRY TABLE
                models.ENTRY_15M(symbol = stock, reference_id = transaction.data['id']).save()

def sell(stock, data_frame, macd, macdsignal, macdhist, adx, kite_conn_var, zerodha_flag_obj):
  stock_config_obj = models.CONFIG_15M.objects.get(symbol = stock)
  # ADX EXIT
  if (adx[-1] >= 40) and (adx[-1] < adx[-2]):
    # CALL PLACE ORDER ----
    order_id, order_status, price = place_ord_sell(kite_conn_var,stock, stock_config_obj)
    if (stock_config_obj.placed is True):
      if (order_id == 0):
        sleep(1)
        sell(stock, data_frame, macd, macdsignal, macdhist, adx, kite_conn_var, zerodha_flag_obj)

    diff          = stock_config_obj.buy_price - price
    profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
    diff          = round((diff * stock_config_obj.quantity),2) - 100

    type_str = 'ADX_{}'.format(stock_config_obj.count)
    trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':type_str,'price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
    transaction   = serializers.CROSSOVER_15_Min_Serializer(data=trans_data)
    if transaction.is_valid():
      transaction.save()
    models.ENTRY_15M.objects.filter(symbol = stock).delete()
    stock_config_obj.buy          = False
    stock_config_obj.placed       = False
    stock_config_obj.count        = 0
    stock_config_obj.order_id     = 0
    stock_config_obj.order_status   = order_status
    stock_config_obj.save()
    
  # After CrossOver MACD AND MACDSIGNAL
  elif macdsignal[-1] < macd[-1]:
    if macdsignal[-2] > macd[-2]:
      # CALL PLACE ORDER ----
      order_id, order_status, price = place_ord_sell(kite_conn_var,stock, stock_config_obj)
      if (stock_config_obj.placed is True):
        if (order_id == 0):
          sleep(1)
          sell(stock, data_frame, macd, macdsignal, macdhist, adx, kite_conn_var, zerodha_flag_obj)

      diff          = stock_config_obj.buy_price - price
      profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
      diff          = round((diff * stock_config_obj.quantity),2) - 100

      type_str = 'AF_BUY_{}'.format(stock_config_obj.count)
      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':type_str,'price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
      transaction   = serializers.CROSSOVER_15_Min_Serializer(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_15M.objects.filter(symbol = stock).delete()
      stock_config_obj.buy          = False
      stock_config_obj.placed       = False
      stock_config_obj.count        = 0
      stock_config_obj.order_id     = 0
      stock_config_obj.order_status   = order_status
      stock_config_obj.save()

def squareoff(kite_conn_var):
  stock_list = models.ENTRY_15M.objects.all().values_list('symbol', flat=True)
  for stock in stock_list:
    stock_config_obj = models.CONFIG_15M.objects.get(symbol = stock)
    # CALL PLACE ORDER ----
    order_id, order_status, price = place_ord_sell(kite_conn_var,stock, stock_config_obj)
    if (stock_config_obj.placed is True):
      if (order_id == 0):
        sleep(1)
        squareoff(kite_conn_var)

    diff          = stock_config_obj.buy_price - price
    profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
    diff          = round((diff * stock_config_obj.quantity),2) - 100

    type_str = 'SQUAREOFF_{}'.format(stock_config_obj.count)
    trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':type_str,'price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
    transaction   = serializers.CROSSOVER_15_Min_Serializer(data=trans_data)
    if transaction.is_valid():
      transaction.save()
    models.ENTRY_15M.objects.filter(symbol = stock).delete()
    stock_config_obj.buy          = False
    stock_config_obj.placed       = False
    stock_config_obj.count        = 0
    stock_config_obj.order_id     = 0
    stock_config_obj.order_status   = order_status
    stock_config_obj.save()
    sleep(0.3)
