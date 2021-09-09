import os
import json
import pandas as pd
from time import sleep
from datetime import datetime, time
from kiteconnect import KiteConnect

from . import serializers
from . import check_ltp
from . import check_ltp_slfema
from . import check_ltp_ca_atr_s30
from celery import shared_task
from .BB_5_MIN.utils import backbone as backbone_BB_5
from .TH_CA_15_MIN.utils import backbone as backbone_TH_CA
from .CA_SLFEMA_15_MIN.utils import backbone as backbone_CA_SLFEMA
from .CA_ATR_S30_15_MIN.utils import backbone as backbone_CA_ATR_S30

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

    # LTP CA
    transactions, stock = check_ltp.get_stock_ltp(kite_conn_var)
    if len(transactions) != 0:
      for trans in transactions:
        serializer = serializers.TH_CA_15_Min_Serializer(data=trans)
        if serializer.is_valid():
          serializer.save()
        else:
          response['TH_CA_SERIALIZER'] = serializer.errors
      response.update({'LTP': True, 'STATUS': 'DONE.','STOCKS':stock})
    else:
      transactions = 'NO CHANGE'
      response.update({'LTP': True, 'STATUS': transactions,'STOCKS':stock})
    
    # LTP SLFEMA
    transactions, stock = check_ltp_slfema.get_stock_ltp(kite_conn_var)
    if len(transactions) != 0:
      for trans in transactions:
        serializer = serializers.CA_SLFEMA_15_MIN_Serializer(data=trans)
        if serializer.is_valid():
          serializer.save()
        else:
          response['CA_SLFEMA_SERIALIZER'] = serializer.errors
      response.update({'LTP_SLFEMA': True, 'STATUS_SLFEMA': 'DONE.','STOCKS_SLFEMA':stock})
    else:
      transactions = 'NO CHANGE'
      response.update({'LTP_SLFEMA': True, 'STATUS_SLFEMA': transactions,'STOCKS_SLFEMA':stock})

    # LTP CA_ATR_S30
    transactions, stock = check_ltp_ca_atr_s30.get_stock_ltp(kite_conn_var)
    if len(transactions) != 0:
      for trans in transactions:
        serializer = serializers.CA_ATR_S30_15_MIN_Serializer(data=trans)
        if serializer.is_valid():
          serializer.save()
        else:
          response['CA_ATR_S30_SERIALIZER'] = serializer.errors
      response.update({'LTP_CA_ATR_S30': True, 'STATUS_CA_ATR_S30': 'DONE.','STOCKS_CA_ATR_S30':stock})
    else:
      transactions = 'NO CHANGE'
      response.update({'LTP_CA_ATR_S30': True, 'STATUS_CA_ATR_S30': transactions,'STOCKS_CA_ATR_S30':stock})

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
def TH_CA_RUNS_15_MIN(self):
  response = {'TH_CA': False, 'STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list_lowprice.xlsx")
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_Sheet['SYMBOL']
  kite_conn_var = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15m','5d',60,55,18,8,'30m','1mo',8,8,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''

  # Workbook Path
  flag_config            = 'algo/config/th_ca_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'selling_price':0,'stoploss':0,'target':0,'target_per':0,'order_id':0,'order_status':None,'exit_id':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_TH_CA.model(intervals, companies_symbol, flag, curr_time,kite_conn_var)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.TH_CA_15_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['TH_CA_SERIALIZER'] = serializer.errors
    response.update({'TH_CA': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'TH_CA': True, 'STATUS': data_frame})
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response

@shared_task(bind=True,max_retries=3)
def CA_SLFEMA_RUNS_15_MIN(self):
  response = {'CA_SLFEMA': False, 'STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list_lowprice.xlsx")
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_Sheet['SYMBOL']
  kite_conn_var = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15m','5d',60,55,18,8,'30m','1mo',8,8,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  # Workbook Path
  flag_config            = 'algo/config/ca_slfema_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'selling_price':0,'stoploss':0,'target':0,'target_per':0,'order_id':0,'order_status':None,'exit_id':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_CA_SLFEMA.model(intervals, companies_symbol, flag, curr_time,kite_conn_var)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.CA_SLFEMA_15_MIN_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['CA_SLFEMA_SERIALIZER'] = serializer.errors
    response.update({'CA_SLFEMA': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'CA_SLFEMA': True, 'STATUS': data_frame})
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response

@shared_task(bind=True,max_retries=3)
def CA_ATR_S30_RUNS_15_MIN(self):
  response = {'CA_ATR_S30': False, 'STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list_lowprice.xlsx")
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_Sheet['SYMBOL']
  kite_conn_var = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15m','5d',60,55,18,8,'30m','1mo',8,8,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  # Workbook Path
  flag_config            = 'algo/config/ca_atr_s30_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'selling_price':0,'stoploss':0,'target':0,'target_per':0,'order_id':0,'order_status':None,'exit_id':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_CA_ATR_S30.model(intervals, companies_symbol, flag, curr_time,kite_conn_var)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.CA_ATR_S30_15_MIN_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['TH_PACA_T2_SERIALIZER'] = serializer.errors
    response.update({'CA_ATR_S30': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'CA_ATR_S30': True, 'STATUS': data_frame})
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response
