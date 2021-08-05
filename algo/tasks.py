from datetime import datetime
import pandas as pd

from . import serializers
from celery import shared_task
from .RSI_55_5_MIN.utils import backbone as backbone_5_55
from .RSI_55_15_MIN.utils import backbone as backbone_15_55

@shared_task(bind=True,max_retries=3)
def TEST(self):
  print('SUCCEED YOU ARE IN RIGHT PATH.. GO ON.')
  return 'WORKING_{}'.format(datetime.now())

@shared_task(bind=True,max_retries=3)
def RSI_55_RUNS_5_MIN(self):
  response = {'success': False,'ALL': []}
  # Workbook Path
  flag_config            = 'algo/RSI_55_5_MIN/config/flag.json'

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")

  intervals      = ['5m','7d',60,55,40,15,'1h','1mo',8,14]
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
  data_frame, status = backbone_5_55.model_ema_rsi(intervals, company_Sheet, flag_config,curr_time)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.RSI_55_5_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
        response['ALL'].append(1)
      else:
        response['ERROR'] = serializer.errors
        response['ALL'].append(0)
    if response['ALL'].count(0) == 0:
      response.update({'success' : True})
      return response
    else:
      return response
  elif data_frame == 'Done' and status is False:
    response.update({'success' : True})
    response['SquareOff'] = True
    return response
  else:
    return response

@shared_task(bind=True,max_retries=3)
def RSI_55_RUNS_15_MIN(self):
  response = {'success': False,'ALL': []}
  # Workbook Path
  flag_config            = 'algo/RSI_55_15_MIN/config/flag.json'

  # Companies List
  company_Sheet          = pd.read_excel("algo/company/yf_stock_list.xlsx")

  intervals      = ['15m','60d',60,55,30,12,'1h','1mo',8,8]
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
  data_frame, status = backbone_15_55.model_ema_rsi(intervals, company_Sheet, flag_config,curr_time)
  if status is True:
    for data_f in data_frame:
      serializer = serializers.RSI_55_15_Min_Serializer(data=data_f)
      if serializer.is_valid():
        serializer.save()
        response['ALL'].append(1)
      else:
        response['ERROR'] = serializer.errors
        response['ALL'].append(0)
    if response['ALL'].count(0) == 0:
      response.update({'success' : True})
      return response
    else:
      return response
  elif data_frame == 'Done' and status is False:
    response.update({'success' : True})
    response['SquareOff'] = True
    return response
  else:
    return response