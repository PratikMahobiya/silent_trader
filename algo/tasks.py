import os
import json
import pandas as pd
from time import sleep
from datetime import datetime

from . import serializers
from celery import shared_task
from .BB_5_MIN.utils import backbone as backbone_BB_5
from .CROSS_OVER_15_MIN.utils import backbone as backbone_CR_15

from .MODELS_15_MIN.utils import get_data as get_data_M1
from .MODELS_15_MIN.TH_PACA.utils import backbone as backbone_TH_PACA
from .MODELS_15_MIN.TH_PACA_T2.utils import backbone as backbone_TH_PACA_T2

@shared_task(bind=True,max_retries=3)
def TEST(self):
  print('SUCCEED YOU ARE IN RIGHT PATH.. GO ON.')
  return 'WORKING_{}'.format(datetime.now())

@shared_task(bind=True,max_retries=3)
def BB_RUNS_5_MIN(self):
  response = {'BB': False, 'STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")
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
      flag[symb] = {'buy':False,'buying_price':0,'lowerband':0,'upperband':0,'atr':0,'selling_price':0,'stoploss':0,'selling_val':0,'upper_val':0}
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
  intervals      = ['5m','7d',60,40,20,8,14]
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
  response = {'CROSS_OVER': False, 'STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_Sheet['SYMBOL']
  sleep(65)
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['5m','60d',60,55,18,8,'30m','60d',8,8,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''

  # Workbook Path
  flag_config            = 'algo/config/cro_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'ema_min':0,'ema_max':0,'selling_price':0,'stoploss':0,'target':0,'target_per':0,'trend_rsi':0,'target_hit':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_CR_15.model(intervals, companies_symbol, flag, curr_time)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.CROSS_OVER_15_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['BB_SERIALIZER'] = serializer.errors
    response.update({'CROSS_OVER': True, 'STATUS': 'ALL DONE.'})
  elif status is False:
    response.update({'CROSS_OVER': True, 'STATUS': data_frame})
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return response

@shared_task(bind=True,max_retries=3)
def MODELS_RUNS_15_MIN(self):
  response = {'TH_PACA': False,'TH_PACA_STATUS': 'NONE','TH_PACA_T2': False,'TH_PACA_T2_STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_Sheet['SYMBOL']
  comp_list = companies_symbol.to_list()
  sleep(65)
  
  '''
    -> interval = [Upper_rsi,Lower_rsi,EMA_MAX,EMA_MIN,TRADE_RSI,TREND_RSI,TRAGET_CANDLE_NUMBER]
  '''
  intervals      = ['15m','60d',60,55,18,8,'30m','60d',8,8,14,20,8,14,40]
  curr_time      = datetime.now()
  '''
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  trend_data = get_data_M1.download_trend_data(comp_list,intervals)
  trade_data = get_data_M1.download_trade_data(comp_list,intervals)

  # TH_PACA ------------------------------------------------------------------
  # Workbook Path
  flag_config            = 'algo/config/th_paca_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'ema_min':0,'ema_max':0,'selling_price':0,'stoploss':0,'target':0,'target_per':0,'trend_rsi':0,'target_hit':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_TH_PACA.model(trend_data,trade_data,intervals,flag,curr_time)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.TH_PACA_15_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['TH_PACA_SERIALIZER'] = serializer.errors
    response.update({'TH_PACA': True,'TH_PACA_STATUS': 'ALL DONE.'})    
  elif status is False:
    response.update({'TH_PACA': True,'TH_PACA_STATUS': data_frame})
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  # TH_PACA ------------------------------------------------------------------

  # TH_PACA_T2 ---------------------------------------------------------------
  # Workbook Path
  flag_config            = 'algo/config/th_paca_t2_flag.json'
  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'ema_min':0,'ema_max':0,'selling_price':0,'stoploss':0,'target':0,'target_per':0,'trend_rsi':0,'target_hit':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  data_frame, status = backbone_TH_PACA_T2.model(trend_data,trade_data,intervals,flag,curr_time)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.TH_PACA_T2_15_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['TH_PACA_T2_SERIALIZER'] = serializer.errors
    response.update({'TH_PACA_T2': True,'TH_PACA_T2_STATUS': 'ALL DONE.'})    
  elif status is False:
    response.update({'TH_PACA_T2': True,'TH_PACA_T2_STATUS': data_frame})
  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  # TH_PACA_T2 ---------------------------------------------------------------
  return response