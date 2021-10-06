import os
import json
from datetime import datetime, time
from kiteconnect import KiteConnect

from Model_15M import models
from Model_5M import models as models_5
from . import models as models_a
from . import serializers
from . import check_ltp
from . import check_ltp_crs_5
from celery import shared_task
from .CROSSOVER_15_MIN.utils import backbone as backbone_CRS
from .CROSSOVER_5_MIN.utils import backbone as backbone_CRS_5_MIN

# -------------------- Not ------------------
from Model_15_temp import models_temp
from . import check_ltp_temp
from .CROSSOVER_15_MIN_temp.utils import backbone as backbone_CRS_temp

@shared_task(bind=True,max_retries=3)
# initial_setup on DATABASE -------------------------------------
def get_stocks_configs(self):
  response = {'stock_table': False, 'config_table_15': False, 'config_table_5': False}
  # Stock dict
  stock_dict = {
    'AUROPHARMA':70401,
    'AARTIIND':1793,
    'ADANIENT':6401,
    'ADANIPORTS':3861249,
    'AMBUJACEM':325121,
    'APLLTD':6483969,
    'APOLLOTYRE':41729,
    'ASHOKLEY':54273,
    'AXISBANK':1510401,
    'BEL' :98049,
    'BERGEPAINT' :103425,
    'BHARATFORG' :108033,
    'BHEL' :112129,
    'BIOCON' :2911489,
    'CADILAHC' :2029825,
    'CHOLAFIN' :175361,
    'COALINDIA' :5215745,
    'CONCOR' :1215745,
    'CUMMINSIND' :486657,
    'BANKBARODA' :1195009,
    'CANBK' :2763265,
    'COLPAL' :3876097,
    'DLF' :	3771393,
    'FEDERALBNK' :261889,
    'ESCORTS' :245249,
    'GAIL' :1207553,
    'GODREJCP' :2585345,
    'GODREJPROP':4576001,
    'GRANULES':3039233,
    'HCLTECH' :1850625,
    'HDFCBANK':341249,
    'HINDALCO':348929,
    'HINDPETRO':359937,
    'ICICIBANK':1270529,
    'INDUSTOWER':7458561,
    'IOC':415745,
    'ITC':424961,
    'JINDALSTEL':1723649,
    'JSWSTEEL':3001089,
    'LT':2939649,
    'M&M':519937,
    'M&MFIN':3400961,
    'MANAPPURAM':4879617,
    'MCDOWELL-N':2674433,
    'MFSL':548353,
    'MOTHERSUMI':1076225,
    'NAM-INDIA':91393,
    'NTPC':2977281,
    'ONGC':633601,
    'PETRONET':2905857,
    'PVR':3365633,
    'SAIL':758529,
    'SBIN':779521,
    'SUNPHARMA':857857,
    'SUNTV':3431425,
    'TATACHEM':871681,
    'TATAMOTORS':884737,
    'TATAPOWER':877057,
    'TECHM':3465729,
    'UBL':4278529,
    'WIPRO':969473,
    'BANDHANBNK' :579329,
    'BATAINDIA' :94977,
    'BHARTIARTL' :2714625,
    'HDFCLIFE' :119553,
    'CUB' :1459457,
    'IDFCFIRSTB' :2863105,
    'IGL' :2883073,
    'INDUSINDBK' :1346049,
    'LUPIN' :2672641,
    'MARICO' :1041153,
    'LICHSGFIN' :511233,
    'NATIONALUM' :1629185,
    'MUTHOOTFIN' :6054401,
    'NMDC' :3924993,
    'RAMCOCEM' :523009,
    'SBILIFE' :5582849,
    'TATASTEEL' :895745,
    'TVSMOTOR' :2170625,
    'CIPLA' :177665,
    'HAVELLS' :2513665,
    'INFY' :408065,
    'ZEEL' :975873,
    'PNB' :2730497,
    'POWERGRID' :3834113,
    'TORNTPOWER' :3529217,
    'VEDL' :784129,
    'GMRINFRA':3463169,
    'VOLTAS':951809,
    'BPCL':134657,
    'DABUR':197633,
    'IBULHSGFIN':7712001,
    'ABFRL':7707649,
    'INDHOTEL':387073,
    'ADANIGREEN':912129,
    'ADANITRANS':2615553,
    'GRASIM':315393,
    'ICICIGI':5573121,
    'ICICIPRULI':4774913,
    'SBICARD':4600577,
    'TATACONSUM':878593,
    'UPL':2889473
  }
  # Create stocks and config's for trade in stock and config table
  for stock_sym in stock_dict:
    # STORE IN STOCK TABLE
    if not models_a.STOCK.objects.filter(symbol = stock_sym).exists():
      models_a.STOCK(symbol = stock_sym, instrument_key = stock_dict[stock_sym]).save()
    # CREATE CONFIG IN FOR 15 MIN
    if not models.CONFIG_15M.objects.filter(symbol = stock_sym).exists():
      models.CONFIG_15M(symbol = stock_sym).save()
    # CREATE CONFIG IN FOR 5 MIN
    if not models_5.CONFIG_5M.objects.filter(symbol = stock_sym).exists():
      models_5.CONFIG_5M(symbol = stock_sym).save()
    
    # ----------------------------------- Not Ative ------------------------------------
    # CREATE CONFIG IN FOR 15 MIN TEMP
    if not models_temp.CONFIG_15M.objects.filter(symbol = stock_sym).exists():
      models_temp.CONFIG_15M(symbol = stock_sym).save()
    

  # Update Responce as per Stock Dict
  if len(models_a.STOCK.objects.all()) == len(stock_dict):
    response.update({'stock_table': True, 'stock_len': len(models_a.STOCK.objects.all())})
  else:
    response.update({'stock_table': False, 'stock_len': len(models_a.STOCK.objects.all())})

  # Update Responce as per Data in 15 Minute
  if len(models.CONFIG_15M.objects.all()) == len(stock_dict):
    response.update({'config_table_15': True, 'config_len_15': len(models.CONFIG_15M.objects.all())})
  else:
    response.update({'config_table_15': False, 'config_len_15': len(models.CONFIG_15M.objects.all())})

  # Update Responce as per Data in 5 Minute
  if len(models_5.CONFIG_5M.objects.all()) == len(stock_dict):
    response.update({'config_table_5': True, 'config_len_5': len(models_5.CONFIG_5M.objects.all())})
  else:
    response.update({'config_table_5': False, 'config_len_5': len(models_5.CONFIG_5M.objects.all())})
  return response

def connect_to_kite_connection():
  api_key = open('algo/config/api_key.txt','r').read()
  access_token = models_a.ZERODHA_KEYS.objects.get(api_key=api_key).access_token
  try:
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
  except Exception as  e:
    pass
  return kite

@shared_task(bind=True,max_retries=3)
def ltp_of_entries(self):
  response = {'LTP': False, 'STATUS': 'NONE','ACTIVE_STOCKS': None,'LTP_5': False, 'STATUS_5': 'NONE','ACTIVE_STOCKS_5': None}
  if datetime.now().time() >= time(9,16,00) and datetime.now().time() < time(15,25,00):
    kite_conn_var = connect_to_kite_connection()
    
    # LTP CRS
    try:
      status, active_stocks = check_ltp.get_stock_ltp(kite_conn_var)
      response.update({'LTP': True, 'STATUS': status,'ACTIVE_STOCKS':active_stocks})
    except Exception as e:
      pass

    # LTP CRS_5MIN
    try:
      status, active_stocks = check_ltp_crs_5.get_stock_ltp(kite_conn_var)
      response.update({'LTP_5': True, 'STATUS_5': status,'ACTIVE_STOCKS_5':active_stocks})
    except Exception as e:
      pass

    # ----------------------------------------- NOT ACTIVE ---------------------------------
    # LTP CRS
    try:
      status, active_stocks = check_ltp_temp.get_stock_ltp(kite_conn_var)
      response.update({'LTP_TEMP': True, 'STATUS_TEMP': status,'ACTIVE_STOCKS_TEMP':active_stocks})
    except Exception as e:
      pass


  elif datetime.now().time() >= time(15,25,00) and datetime.now().time() < time(15,30,00):
    response.update({'LTP': True, 'STATUS': 'SQUARED OFF','LTP_5_MIN': True, 'STATUS_5_MIN': 'ALL STOCKS ARE SQUARED OFF.'})
  else:
    response.update({'LTP': True, 'STATUS': 'MARKET IS CLOSED','LTP': True, 'STATUS': 'MARKET IS CLOSED.','LTP_5_MIN': True, 'STATUS_5_MIN': 'MARKET IS CLOSED.'})
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_15_MIN(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # Initialize Kite Connections
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15minute',5,60,55,18,8,'30minute',30,14,14,14]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_CRS.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))})
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_5_MIN(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # Initialize Kite Connections
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['5minute',5,60,55,21,10,'30minute',30,14,14,14,'15minute',5]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_CRS_5_MIN.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_5.ENTRY_5M.objects.all().values_list('symbol',flat=True))})
  return response

# ------------------------------------------- Not Active ---------------------------------------
@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_15_MIN_TEMP(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # Initialize Kite Connections
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15minute',5,60,55,18,8,'30minute',30,14,14,14]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_CRS_temp.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_temp.ENTRY_15M.objects.all().values_list('symbol',flat=True))})
  return response