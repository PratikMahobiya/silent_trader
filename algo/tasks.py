import os
import json
from django.db import models
import pandas as pd
from time import sleep
from datetime import datetime, time
from kiteconnect import KiteConnect

from . import models
from . import serializers
from . import check_ltp
from . import check_ltp_crs_5
from . import check_ltp_db
from celery import shared_task
from .CROSSOVER_15_MIN.utils import backbone as backbone_CRS
from .CROSSOVER_15_MIN_db.utils import backbone as backbone_CRS_db
from .CROSSOVER_5_MIN.utils import backbone as backbone_CRS_5_MIN

def get_stocks():
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
  return stock_dict

def connect_to_kite_connection():
  api_key = open('algo/config/api_key.txt','r').read()
  # access_token = open('algo/config/access_token.txt','r').read()
  access_token = models.ZERODHA_KEYS.objects.get(api_key=api_key).access_token
  try:
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
  except Exception as  e:
    pass
  return kite

@shared_task(bind=True,max_retries=3)
def ltp_of_entries(self):
  response = {'LTP': False, 'STATUS': 'NONE','OUT_TREND':None,'IN_TREND_ENTRY_STOCK':None,'LTP_5_MIN': False, 'STATUS_5_MIN': 'NONE','OUT_TREND_5_MIN':None,'IN_TREND_ENTRY_STOCK_5_MIN':None,'LTP_DB': False, 'STATUS_DB': 'NONE','ACTIVE_STOCKS_DB':None}
  if datetime.now().time() >= time(9,16,00) and datetime.now().time() < time(15,25,00):
    kite_conn_var = connect_to_kite_connection()
    
    # LTP CRS
    try:
      transactions, out_trend_stock, in_trend_entry_stock = check_ltp.get_stock_ltp(kite_conn_var)
      if len(transactions) != 0:
        for trans in transactions:
          serializer = serializers.CROSSOVER_15_Min_Serializer(data=trans)
          if serializer.is_valid():
            serializer.save()
          else:
            response['CRS_SERIALIZER'] = serializer.errors
        response.update({'LTP': True, 'STATUS': 'DONE.','OUT_TREND':out_trend_stock,'IN_TREND_ENTRY_STOCK':in_trend_entry_stock})
      else:
        transactions = 'NO CHANGE'
        response.update({'LTP': True, 'STATUS': transactions,'OUT_TREND':out_trend_stock,'IN_TREND_ENTRY_STOCK':in_trend_entry_stock})
    except Exception as e:
      pass

    # LTP CRS_5MIN
    try:
      transactions, out_trend_stock, in_trend_entry_stock = check_ltp_crs_5.get_stock_ltp(kite_conn_var)
      if len(transactions) != 0:
        for trans in transactions:
          serializer = serializers.CROSSOVER_5_MIN_Serializer(data=trans)
          if serializer.is_valid():
            serializer.save()
          else:
            response['CRS_5_MIN_SERIALIZER'] = serializer.errors
        response.update({'LTP_5_MIN': True, 'STATUS_5_MIN': 'DONE.','OUT_TREND_5_MIN':out_trend_stock,'IN_TREND_ENTRY_STOCK_5_MIN':in_trend_entry_stock})
      else:
        transactions = 'NO CHANGE'
        response.update({'LTP_5_MIN': True, 'STATUS_5_MIN': transactions,'OUT_TREND_5_MIN':out_trend_stock,'IN_TREND_ENTRY_STOCK_5_MIN':in_trend_entry_stock})
    except Exception as e:
      pass

    # LTP CRS
    try:
      status, active_stocks = check_ltp_db.get_stock_ltp(kite_conn_var)
      response.update({'LTP_DB': True, 'STATUS_DB': status,'ACTIVE_STOCKS_DB':active_stocks})
    except Exception as e:
      pass

  elif datetime.now().time() >= time(15,25,00) and datetime.now().time() < time(15,30,00):
    response.update({'LTP': True, 'STATUS': 'ALL STOCKS ARE SQUARED OFF.','LTP_5_MIN': True, 'STATUS_5_MIN': 'ALL STOCKS ARE SQUARED OFF.','LTP_DB': True, 'STATUS_DB': 'SQUARED OFF'})
  else:
    response.update({'LTP': True, 'STATUS': 'MARKET IS CLOSED.','LTP_5_MIN': True, 'STATUS_5_MIN': 'MARKET IS CLOSED.','LTP_DB': True, 'STATUS_DB': 'MARKET IS CLOSED'})
  return response

@shared_task(bind=True,max_retries=3)
def REMOVE_CONFIG_FILES(self):
  directory = './algo/config'
  files_in_directory = os.listdir(directory)
  filtered_files = [file for file in files_in_directory if file.endswith(".json")]
  for file in filtered_files:
    try:
      path_to_file = os.path.join(directory, file)
      os.remove(path_to_file)
    except Exception as e:
      pass
  files_in_directory = os.listdir(directory)
  return {'success': True, 'Files_in_config':files_in_directory}

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_15_MIN(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # Stock List in dict
  stock_dict          = get_stocks()
  # Extract Symbols in list
  stock_symbol        = stock_dict.keys()
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15minute',5,60,55,18,8,'30minute',30,14,14,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  # Workbook Path
  flag_config            = 'algo/config/crs_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    flag['Trend'] = []
    for symb in stock_symbol:
      flag[symb] = {'buy':False,'trend':False,'d_sl_flag':False,'buying_price':0,'selling_price':0,'stoploss':0,'f_stoploss':0,'d_stoploss':0,'quantity':0,'count':0,'target':0,'order_id':0,'order_status':None}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_CRS.model(intervals, stock_dict, flag, curr_time,kite_conn_var)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.CROSSOVER_15_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['CRS_SERIALIZER'] = serializer.errors
    response.update({'CRS': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'CRS': True, 'STATUS': data_frame})
  response['Trending Stocks'] = flag['Trend']
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_5_MIN(self):
  response = {'CRS_5MIN': False, 'STATUS': 'NONE'}

  # Stock List in dict
  stock_dict          = get_stocks()
  # Extract Symbols in list
  stock_symbol        = stock_dict.keys()
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['5minute',5,60,55,18,8,'30minute',30,14,14,14,'15minute',5]
  # intervals      = ['15minute',5,60,55,18,8,'30minute',30,14,14,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  # Workbook Path
  flag_config            = 'algo/config/crs_5_min_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    flag['Trend'] = []
    flag['Trend_15'] = []
    flag['Trend_30'] = []
    for symb in stock_symbol:
      flag[symb] = {'buy':False,'trend':False,'d_sl_flag':False,'buying_price':0,'selling_price':0,'stoploss':0,'f_stoploss':0,'d_stoploss':0,'quantity':0,'count':0,'target':0,'order_id':0,'order_status':None}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_CRS_5_MIN.model(intervals, stock_dict, flag, curr_time,kite_conn_var)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.CROSSOVER_5_MIN_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['TH_PACA_T2_SERIALIZER'] = serializer.errors
    response.update({'CRS_5MIN': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'CRS_5MIN': True, 'STATUS': data_frame})
  response['Trending Stocks'] = flag['Trend']
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_15_MIN_DB(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # initial_setup on DATABASE -------------------------------------
  if time(9,00,00) <= datetime.now().time() <= time(9,3,00):
    # Stock List in dict
    stock_dict          = get_stocks()
    # Create stocks and config's for trade in stock and config table
    for stock_sym in stock_dict:
      try:
        if not models.STOCK.objects.filter(symbol = stock_sym).exists():
          models.STOCK(symbol = stock_sym, instrument_key = stock_dict[stock_sym]).save()
        if not models.CONFIG_15M.objects.filter(symbol = stock_sym).exists():
          models.CONFIG_15M(symbol = stock_sym).save()
      except Exception as e:
        pass
  
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
  status = backbone_CRS_db.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'TREND': models.TREND_15M.objects.all().values_list('symbol',flat=True), 'ENTRY':models.ENTRY_15M.objects.all().values_list('symbol',flat=True)})
  return response