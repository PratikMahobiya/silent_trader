from Model_5M import models
from algo import models as models_a
from datetime import date, datetime, time, timedelta
from time import sleep
import pandas as pd

def download_trend_data_60(intervals,kite_conn_var):
  now = date.today()
  from_day = now - timedelta(days=intervals[7])
  df_list = []
  df_key  = []
  if time(9,14,00) <= datetime.now().time() <= time(9,18,00):
    sleep(10)
  for_trend = models_a.STOCK.objects.filter(active_5 = True).values_list('symbol', flat=True)
  for stock_name in for_trend:
    sleep(0.3)
    data = kite_conn_var.historical_data(instrument_token=models_a.STOCK.objects.get(symbol = stock_name).instrument_key, from_date=from_day, to_date=now, interval=intervals[6])
    data=pd.DataFrame(data)
    data_frame = data.set_index(data['date'], drop=False, append=False, inplace=False, verify_integrity=False).drop('date', 1)
    data_frame.rename(columns = {'open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}, inplace = True)
    df_list.append(data_frame)
    df_key.append(stock_name)
  merged_data_frame = pd.concat(df_list,axis=1,keys=df_key).tz_localize(None)
  return merged_data_frame

def download_trade_data(for_trade,intervals,kite_conn_var):
  now = date.today()
  from_day = now - timedelta(days=intervals[1])
  df_list = []
  df_key  = []
  for stock_name in for_trade:
    sleep(0.3)
    data = kite_conn_var.historical_data(instrument_token=models_a.STOCK.objects.get(symbol = stock_name).instrument_key, from_date=from_day, to_date=now, interval=intervals[0])
    data=pd.DataFrame(data)
    data_frame = data.set_index(data['date'], drop=False, append=False, inplace=False, verify_integrity=False).drop('date', 1)
    data_frame.rename(columns = {'open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}, inplace = True)
    df_list.append(data_frame)
    df_key.append(stock_name)
  merged_data_frame = pd.concat(df_list,axis=1,keys=df_key).tz_localize(None)
  return merged_data_frame