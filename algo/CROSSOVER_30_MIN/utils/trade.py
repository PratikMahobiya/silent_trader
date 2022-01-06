from algo import serializers
from Model_30M import models
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
  order_id, order_status, price, quantity = zerodha_action.place_regular_sell_order(kite_conn_var,stock, stock_config_obj)
  # -------------------------------------------
  return order_id, order_status, price, quantity


def trade_execution(data_frame, for_trade_stocks, intervals, kite_conn_var):
  zerodha_flag_obj = models_a.PROFIT_CONFIG.objects.get(model_name = 'CRS_30_MIN')
  for stock in for_trade_stocks:
    macd, macdsignal, macdhist = talib.MACD(data_frame[stock]['Close'], fastperiod=intervals[2], slowperiod=intervals[3], signalperiod=intervals[4])
    stock_config_obj = models.CONFIG_30M.objects.get(symbol = stock)
    if stock_config_obj.buy == False:
      buys(stock, data_frame, macd, macdsignal, macdhist, kite_conn_var, zerodha_flag_obj)
    else:
      sell(stock, data_frame, macd, macdsignal, macdhist, kite_conn_var, zerodha_flag_obj)
  return 0

# BUYS STOCKS ; ENTRY
def buys(stock, data_frame, macd, macdsignal, macdhist, kite_conn_var, zerodha_flag_obj):
  stock_config_obj = models.CONFIG_30M.objects.get(symbol = stock)
  # After CrossOver MACD AND MACDSIGNAL
  if macd[-1] > macdsignal[-1]:
    if macd[-2] < macdsignal[-2]:
      # Place Order in ZERODHA.
      order_id, order_status, price, quantity = place_ord_buy(kite_conn_var,stock, zerodha_flag_obj)
      # UPDATE CONFIG
      type_str         = 'AF_BUY'
      stock_config_obj.buy            = True
      stock_config_obj.stoploss       = price - price * 0.006
      stock_config_obj.target         = price + price * 0.006
      stock_config_obj.quantity       = quantity
      stock_config_obj.buy_price      = price
      stock_config_obj.order_id       = order_id
      stock_config_obj.order_status   = order_status
      stock_config_obj.save()
      # TRANSACTION TABLE UPDATE
      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price':price,'quantity':quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':None,'profit':None,'order_id':order_id,'order_status':order_status}
      transaction   = serializers.CROSSOVER_30_MIN_Serializer(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      # UPDATE CURRENT ENTRY TABLE
      models.ENTRY_30M(symbol = stock, reference_id = transaction.data['id']).save()

def sell(stock, data_frame, macd, macdsignal, macdhist, kite_conn_var, zerodha_flag_obj):
  stock_config_obj = models.CONFIG_30M.objects.get(symbol = stock)
  # After CrossOver MACD AND MACDSIGNAL
  if macdsignal[-1] > macd[-1]:
    if macdsignal[-2] < macd[-2]:
      # CALL PLACE ORDER ----
      order_id, order_status, price = place_ord_sell(kite_conn_var,stock, stock_config_obj)

      diff          = price - stock_config_obj.buy_price 
      profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
      diff          = round((diff * stock_config_obj.quantity),2) - 100

      type_str = 'AF_SELL'
      trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':type_str,'price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
      transaction   = serializers.CROSSOVER_30_MIN_Serializer(data=trans_data)
      if transaction.is_valid():
        transaction.save()
      models.ENTRY_30M.objects.filter(symbol = stock).delete()
      stock_config_obj.buy          = False
      stock_config_obj.placed       = False
      stock_config_obj.count        = 0
      stock_config_obj.order_id     = 0
      stock_config_obj.save()

def squareoff(kite_conn_var):
  stock_list = models.ENTRY_30M.objects.all().values_list('symbol', flat=True)
  for stock in stock_list:
    stock_config_obj = models.CONFIG_30M.objects.get(symbol = stock)
    # CALL PLACE ORDER ----
    order_id, order_status, price = place_ord_sell(kite_conn_var,stock, stock_config_obj)

    diff          = price - stock_config_obj.buy_price 
    profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
    diff          = round((diff * stock_config_obj.quantity),2) - 100

    type_str = 'SQUAREOFF'
    trans_data = {'symbol':stock,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':type_str,'price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
    transaction   = serializers.CROSSOVER_30_MIN_Serializer(data=trans_data)
    if transaction.is_valid():
      transaction.save()
    models.ENTRY_30M.objects.filter(symbol = stock).delete()
    stock_config_obj.buy          = False
    stock_config_obj.placed       = False
    stock_config_obj.count        = 0
    stock_config_obj.order_id     = 0
    stock_config_obj.save()
    sleep(0.3)
