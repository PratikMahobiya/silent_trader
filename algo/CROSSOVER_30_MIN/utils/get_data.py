from fyers_api import fyersModel
from algo import models as models_a
from datetime import date, datetime, time, timedelta
from time import sleep
import pandas as pd

def fyers_conn():
  app_id = open('algo/config/app_id.txt','r').read()
  access_token = models_a.FYERS_KEYS.objects.get(app_id=app_id).access_token
  try:
    fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)
  except Exception as  e:
    pass
  return fyers

def download_trade_data(intervals,kite_conn_var):
  now = date.today()
  from_day = now - timedelta(days=intervals[1])
  df_list = []
  df_key  = []
  if time(9,14,00) <= datetime.now().time() <= time(9,18,00):
    sleep(30)
  fyers_conn_val = fyers_conn()
  for_trade = models_a.STOCK.objects.filter(active_5 = True, nifty_flag = False).values_list('symbol', flat=True)
  for stock_name in for_trade:
    sleep(0.3)
    data = {"symbol":"NSE:{}-EQ".format(stock_name),"resolution":intervals[0],"date_format":"1","range_from":from_day,"range_to":now,"cont_flag":"0"}
    data = fyers_conn_val.history(data)['candles']
    data=pd.DataFrame(data)
    data[0] = pd.to_datetime(data[0],unit = 's')
    data_frame = data.set_index(data[0], drop=False, append=False, inplace=False, verify_integrity=False).drop(0, 1)
    data_frame.rename(columns = {0:'date',1:'Open',2:'High',3:'Low',4:'Close',5:'Volume'}, inplace = True)
    data_frame.index.names = ['date']
    df_list.append(data_frame)
    df_key.append(stock_name)
  merged_data_frame = pd.concat(df_list,axis=1,keys=df_key)
  return merged_data_frame, for_trade