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

def in_nifty_range(kite_conn_var):
  stock_list = []
  key_val = {'NSE:NIFTY 50': 'nifty','NSE:NIFTY NEXT 50': 'nxt50','NSE:NIFTY MIDCAP 50': 'mid50'}
  nifty_ltp = kite_conn_var.ltp(['NSE:NIFTY 50','NSE:NIFTY NEXT 50','NSE:NIFTY MIDCAP 50'])
  for nif in nifty_ltp:
    if nifty_ltp[nif]['last_price'] < models_a.STOCK.objects.get(symbol = nif).lower_lim:
      stock_list += list(models_a.STOCK.objects.filter(active_15 = True, nifty_flag = False, niftytype = key_val[nif]).values_list('symbol', flat=True))
  return stock_list


def download_trend_data_30(intervals,kite_conn_var):
  now = date.today()
  from_day = now - timedelta(days=intervals[7])
  df_list = []
  df_key  = []
  if time(9,14,00) <= datetime.now().time() <= time(9,25,00):
    sleep(300)
  fyers_conn_val = fyers_conn()
  # for_trend = in_nifty_range(kite_conn_var)
  for_trend = models_a.STOCK.objects.filter(active_15 = True, nifty_flag = False).values_list('symbol', flat=True)
  for stock_name in for_trend:
    sleep(0.3)
    data = {"symbol":"NSE:{}-EQ".format(stock_name),"resolution":intervals[6],"date_format":"1","range_from":from_day,"range_to":now,"cont_flag":"0"}
    data = fyers_conn_val.history(data)['candles']
    data=pd.DataFrame(data)
    data[0] = pd.to_datetime(data[0],unit = 's')
    data_frame = data.set_index(data[0], drop=False, append=False, inplace=False, verify_integrity=False).drop(0, 1)
    data_frame.rename(columns = {0:'date',1:'Open',2:'High',3:'Low',4:'Close',5:'Volume'}, inplace = True)
    data_frame.index.names = ['date']
    df_list.append(data_frame)
    df_key.append(stock_name)
  if len(for_trend) != 0:
    merged_data_frame = pd.concat(df_list,axis=1,keys=df_key)
  else:
    merged_data_frame = {}
  return merged_data_frame, for_trend

def download_trade_data(for_trade,intervals,kite_conn_var):
  now = date.today()
  from_day = now - timedelta(days=intervals[1])
  df_list = []
  df_key  = []
  fyers_conn_val = fyers_conn()
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
  return merged_data_frame