from datetime import datetime
import pandas as pd

from . import serializers
from celery import shared_task
from .BB_5_MIN.utils import backbone as backbone_BB_5
from .CROSS_OVER_15_MIN.utils import backbone as backbone_CR_15

from .MODELS_15_MIN.utils import get_data as get_data_M1
from .MODELS_15_MIN.TH_CA.utils import backbone as backbone_TH_CA
from .MODELS_15_MIN.TH_PACA.utils import backbone as backbone_TH_PACA
from .MODELS_15_MIN.TH_PACA_T2.utils import backbone as backbone_TH_PACA_T2

@shared_task(bind=True,max_retries=3)
def TEST(self):
  print('SUCCEED YOU ARE IN RIGHT PATH.. GO ON.')
  return 'WORKING_{}'.format(datetime.now())

@shared_task(bind=True,max_retries=3)
def BB_RUNS_5_MIN(self):
  response = {'BB': False, 'STATUS': 'NONE'}
  # Workbook Path
  flag_config            = 'algo/BB_5_MIN/config/flag.json'

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")

  # [trade_min,_trade_days,sell_rsi,buy_rsi,bollingerband,rsi,atr]
  intervals      = ['5m','7d',60,40,20,8,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    [
    first two:-  trading_interval, trading_period,
    senond two:- trading_rsi_upper, trading_rsi_lower,
    third two:-  trading_ema_max, trading_ema_min,
    fourth two:- trend_interval, trend_period,
    Fifth two:-  trend_ema_timeperiod, trade_rsi_timeperiod
    ]

    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  data_frame, status = backbone_BB_5.model(intervals, company_Sheet, flag_config,curr_time)
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
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_15_MIN(self):
  response = {'CROSS_OVER': False, 'STATUS': 'NONE'}
  # Workbook Path
  flag_config            = 'algo/CROSS_OVER_15_MIN/config/flag.json'

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")

  # [trade_min,_trade_days,sell_rsi,buy_rsi,trade_ema_max,trade_ema_min,trend_min,trend_days,trend_rsi_time_period,trade_rsi_timeperiod,trade_target%_timeperiod]
  intervals      = ['15m','60d',60,55,18,8,'1h','1mo',8,8,14]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    [
    first two:-  trading_interval, trading_period,
    senond two:- trading_rsi_upper, trading_rsi_lower,
    third two:-  trading_ema_max, trading_ema_min,
    fourth two:- trend_interval, trend_period,
    Fifth two:-  trend_ema_timeperiod, trade_rsi_timeperiod
    ]

    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  data_frame, status = backbone_CR_15.model(intervals, company_Sheet, flag_config,curr_time)
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
  return response

@shared_task(bind=True,max_retries=3)
def MODELS_RUNS_15_MIN(self):
  response = {'TH_CA': False,'TH_CA_STATUS': 'NONE','TH_PACA': False,'TH_PACA_STATUS': 'NONE','TH_PACA_T2': False,'TH_PACA_T2_STATUS': 'NONE'}

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_Sheet['SYMBOL']
  comp_list = companies_symbol.to_list()

  # [trade_min,_trade_days,sell_rsi,buy_rsi,trade_ema_max,trade_ema_min,trend_min,trend_days,trend_rsi_time_period,trade_rsi_timeperiod,trade_target%_timeperiod]
  intervals      = ['15m','60d',60,55,18,8,'30m','60d',8,8,14,20,8,14,40]
  curr_time      = datetime.now()
  '''
  -> Intervals:-
    [
    first two:-  trading_interval, trading_period,
    senond two:- trading_rsi_upper, trading_rsi_lower,
    third two:-  trading_ema_max, trading_ema_min,
    fourth two:- trend_interval, trend_period,
    Fifth two:-  trend_ema_timeperiod, trade_rsi_timeperiod
    ]

    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  trend_data = get_data_M1.download_trend_data(comp_list,intervals)
  trade_data = get_data_M1.download_trade_data(comp_list,intervals)
  
  # TH_CA ------------------------------------------------------------------
  # Workbook Path
  flag_config            = 'algo/MODELS_15_MIN/TH_CA/config/flag.json'
  data_frame, status = backbone_TH_CA.model(trend_data,trade_data,intervals,company_Sheet,flag_config,curr_time)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.TH_CA_15_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
      else:
        response['TH_CA_SERIALIZER'] = serializer.errors
    response.update({'TH_CA': True,'TH_CA_STATUS': 'ALL DONE.'})    
  elif status is False:
    response.update({'TH_CA': True,'TH_CA_STATUS': data_frame})
  
  # TH_PACA ------------------------------------------------------------------
  # Workbook Path
  flag_config            = 'algo/MODELS_15_MIN/TH_PACA/config/flag.json'
  data_frame, status = backbone_TH_PACA.model(trend_data,trade_data,intervals,company_Sheet,flag_config,curr_time)
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

  # TH_PACA_T2 ------------------------------------------------------------------
  # Workbook Path
  flag_config            = 'algo/MODELS_15_MIN/TH_PACA_T2/config/flag.json'
  data_frame, status = backbone_TH_PACA_T2.model(trend_data,trade_data,intervals,company_Sheet,flag_config,curr_time)
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
  return response