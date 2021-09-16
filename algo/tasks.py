import os
import json
import pandas as pd
from time import sleep
from datetime import datetime, time
from kiteconnect import KiteConnect

from . import serializers
from . import check_ltp
from . import check_ltp_slfema
from . import check_ltp_crs_5
from celery import shared_task
from .BB_5_MIN.utils import backbone as backbone_BB_5
from .CROSSOVER_15_MIN.utils import backbone as backbone_CRS
from .CROSSOVER_SLFEMA_15_MIN.utils import backbone as backbone_CRS_SLFEMA
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
    'KOTAKBANK':492033,
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
  access_token = open('algo/config/access_token.txt','r').read()
  try:
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
  except Exception as  e:
    pass
  return kite

@shared_task(bind=True,max_retries=3)
def ltp_of_entries(self):
  response = {'LTP': False, 'STATUS': 'NONE','STOCKS':None,'LTP_SLFEMA': False, 'STATUS_SLFEMA': 'NONE','STOCKS_SLFEMA':None,'LTP_CA_ATR_S30': False, 'STATUS_CA_ATR_S30': 'NONE','STOCKS_CA_ATR_S30':None}
  if datetime.now().time() >= time(9,16,00) and datetime.now().time() < time(15,25,00):
    kite_conn_var = connect_to_kite_connection()

    # LTP CRS
    try:
      transactions, stock = check_ltp.get_stock_ltp(kite_conn_var)
      if len(transactions) != 0:
        for trans in transactions:
          serializer = serializers.CROSSOVER_15_Min_Serializer(data=trans)
          if serializer.is_valid():
            serializer.save()
          else:
            response['CRS_SERIALIZER'] = serializer.errors
        response.update({'LTP': True, 'STATUS': 'DONE.','STOCKS':stock})
      else:
        transactions = 'NO CHANGE'
        response.update({'LTP': True, 'STATUS': transactions,'STOCKS':stock})
    except Exception as e:
      pass
    
    # LTP SLFEMA
    try:
      transactions, stock = check_ltp_slfema.get_stock_ltp(kite_conn_var)
      if len(transactions) != 0:
        for trans in transactions:
          serializer = serializers.CROSSOVER_SLFEMA_15_MIN_Serializer(data=trans)
          if serializer.is_valid():
            serializer.save()
          else:
            response['CRS_SLFEMA_SERIALIZER'] = serializer.errors
        response.update({'LTP_SLFEMA': True, 'STATUS_SLFEMA': 'DONE.','STOCKS_SLFEMA':stock})
      else:
        transactions = 'NO CHANGE'
        response.update({'LTP_SLFEMA': True, 'STATUS_SLFEMA': transactions,'STOCKS_SLFEMA':stock})
    except Exception as e:
      pass

    # LTP CRS_5MIN
    try:
      transactions, stock = check_ltp_crs_5.get_stock_ltp(kite_conn_var)
      if len(transactions) != 0:
        for trans in transactions:
          serializer = serializers.CROSSOVER_5_MIN_Serializer(data=trans)
          if serializer.is_valid():
            serializer.save()
          else:
            response['CA_ATR_S30_SERIALIZER'] = serializer.errors
        response.update({'LTP_CA_ATR_S30': True, 'STATUS_CA_ATR_S30': 'DONE.','STOCKS_CA_ATR_S30':stock})
      else:
        transactions = 'NO CHANGE'
        response.update({'LTP_CA_ATR_S30': True, 'STATUS_CA_ATR_S30': transactions,'STOCKS_CA_ATR_S30':stock})
    except Exception as e:
      pass

  elif datetime.now().time() >= time(15,25,00) and datetime.now().time() < time(15,30,00):
    response.update({'LTP': True, 'STATUS': 'ALL STOCKS ARE SQUARED OFF.', 'STOCKS': 'I APOLOGIZE MY MASTER.','LTP_SLFEMA': True, 'STATUS_SLFEMA': 'ALL STOCKS ARE SQUARED OFF.', 'STOCKS_SLFEMA': 'I APOLOGIZE MY MASTER.','LTP_CA_ATR_S30': True, 'STATUS_CA_ATR_S30': 'ALL STOCKS ARE SQUARED OFF.', 'STOCKS_CA_ATR_S30': 'I APOLOGIZE MY MASTER.'})
  else:
    response.update({'LTP': True, 'STATUS': 'MARKET IS CLOSED.', 'STOCKS': 'SORRY.','LTP': True, 'STATUS_SLFEMA': 'MARKET IS CLOSED.', 'STOCKS_SLFEMA': 'SORRY.','LTP_CA_ATR_S30': True, 'STATUS_CA_ATR_S30': 'MARKET IS CLOSED.', 'STOCKS_CA_ATR_S30': 'SORRY.'})
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
def BB_RUNS_5_MIN(self):
  response = {'BB': False, 'STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list_lowprice.xlsx")
  companies_symbol         = company_Sheet['SYMBOL']
  sleep(65)

  # Workbook Path
  flag_config            = 'algo/config/bb_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'selling_price':0,'stoploss':0,'selling_val':0,'upper_val':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  '''
    -> intervals = [Time_period, Number_oF_Days,Upper_rsi, Lower_rsi, Bollinger_Band, RSI, ATR]
  '''
  intervals      = ['5m','2d',60,30,20,8,14]
  curr_time      = datetime.now()
  '''
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  data_frame, status = backbone_BB_5.model(intervals, companies_symbol, flag, curr_time)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.BB_5_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['BB_SERIALIZER'] = serializer.errors
    response.update({'BB': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'BB': True, 'STATUS': data_frame})
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response

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
  intervals      = ['15minute',5,60,55,18,8,'30minute',30,8,8,14]
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
      flag[symb] = {'buy':False,'buying_price':0,'selling_price':0,'stoploss':0,'target':0,'quantity':0,'order_id':0,'order_status':None}
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
def CROSS_OVER_ATR_SLFEMA_RUNS_15_MIN(self):
  response = {'CRS_SLFEMA': False, 'STATUS': 'NONE'}

  # Stock List in dict
  stock_dict          = get_stocks()
  # Extract Symbols in list
  stock_symbol        = stock_dict.keys()
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15minute',5,60,55,18,8,'30minute',30,8,8,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  # Workbook Path
  flag_config            = 'algo/config/crs_slfema_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    flag['Trend'] = []
    for symb in stock_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'selling_price':0,'stoploss':0,'target_05':0,'target_075':0,'target_1':0,'target_2':0,'atr_1':0,'atr_2':0,'target_05_flag':False,'target_075_flag':False,'target_1_flag':False,'quantity':0,'order_id':0,'order_status':None}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_CRS_SLFEMA.model(intervals, stock_dict, flag, curr_time,kite_conn_var)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.CROSSOVER_SLFEMA_15_MIN_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['CRS_SLFEMA_SERIALIZER'] = serializer.errors
    response.update({'CRS_SLFEMA': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'CRS_SLFEMA': True, 'STATUS': data_frame})
  response['Trending Stocks'] = flag['Trend']
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response

@shared_task(bind=True,max_retries=3)
def CROSSOVER_ATR_ATR30_RUNS_5_MIN(self):
  response = {'CRS_5MIN': False, 'STATUS': 'NONE'}

  # Stock List in dict
  stock_dict          = get_stocks()
  # Extract Symbols in list
  stock_symbol        = stock_dict.keys()
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['5minute',5,60,55,21,10,'30minute',30,8,8,14]
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
    for symb in stock_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'selling_price':0,'stoploss':0,'target':0,'quantity':0,'order_id':0,'order_status':None}
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
