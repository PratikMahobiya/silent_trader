from smartapi import SmartConnect
from algo import models as models_a
from datetime import date, datetime, time, timedelta
from time import sleep
import pandas as pd

def angelbroking_conn():
    obj=SmartConnect(api_key="MWxz7OCW",)
    obj.generateSession("P567723","Qwerty@12")
    return obj

def in_nifty_range(kite_conn_var):
  stock_list = []
  key_val = {'NSE:NIFTY 50': 'nifty','NSE:NIFTY NEXT 50': 'nxt50','NSE:NIFTY MIDCAP 50': 'mid50'}
  nifty_ltp = kite_conn_var.ltp(['NSE:NIFTY 50','NSE:NIFTY NEXT 50','NSE:NIFTY MIDCAP 50'])
  for nif in nifty_ltp:
    if nifty_ltp[nif]['last_price'] < models_a.STOCK.objects.get(symbol = nif).lower_lim:
      stock_list += list(models_a.STOCK.objects.filter(active_15 = True, nifty_flag = False, niftytype = key_val[nif]).values_list('symbol', flat=True))
  return stock_list


def download_trend_data_30(intervals,kite_conn_var):
  now = datetime.now()
  from_day = now - timedelta(days=intervals[7])
  df_list = []
  df_key  = []
  if time(9,14,00) <= datetime.now().time() <= time(9,25,00):
    sleep(300)
  angelbroking_conn_val = angelbroking_conn()
  # for_trend = in_nifty_range(kite_conn_var)
  for_trend = models_a.STOCK.objects.filter(active_15 = True, nifty_flag = False).values_list('symbol', flat=True)
  for stock_name in for_trend:
    sleep(0.3)
    historicParam={
                  "exchange": "NSE",
                  "symboltoken": models_a.STOCK.objects.get(symbol = stock_name).token,
                  "interval": intervals[6],
                  "fromdate": from_day.strftime("%Y-%m-%d %H:%M"), 
                  "todate": now.strftime("%Y-%m-%d %H:%M")
                  }
    data=pd.DataFrame(angelbroking_conn_val.getCandleData(historicParam)['data'])
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
  now = datetime.now()
  from_day = now - timedelta(days=intervals[1])
  df_list = []
  df_key  = []
  angelbroking_conn_val = angelbroking_conn()
  for stock_name in for_trade:
    sleep(0.3)
    historicParam={
                  "exchange": "NSE",
                  "symboltoken": models_a.STOCK.objects.get(symbol = stock_name).token,
                  "interval": intervals[0],
                  "fromdate": from_day.strftime("%Y-%m-%d %H:%M"), 
                  "todate": now.strftime("%Y-%m-%d %H:%M")
                  }
    data=pd.DataFrame(angelbroking_conn_val.getCandleData(historicParam)['data'])
    data_frame = data.set_index(data[0], drop=False, append=False, inplace=False, verify_integrity=False).drop(0, 1)
    data_frame.rename(columns = {0:'date',1:'Open',2:'High',3:'Low',4:'Close',5:'Volume'}, inplace = True)
    data_frame.index.names = ['date']
    df_list.append(data_frame)
    df_key.append(stock_name)
  merged_data_frame = pd.concat(df_list,axis=1,keys=df_key)
  return merged_data_frame