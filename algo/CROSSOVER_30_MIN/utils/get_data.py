from smartapi import SmartConnect
from algo import models as models_a
from datetime import date, datetime, time, timedelta
from time import sleep
import pandas as pd

def angelbroking_conn():
    obj=SmartConnect(api_key="MWxz7OCW",)
    obj.generateSession("P567723","Qwerty@12")
    return obj

def download_trade_data(intervals,kite_conn_var):
  now = datetime.now()
  from_day = now - timedelta(days=intervals[1])
  df_list = []
  df_key  = []
  if time(9,14,00) <= datetime.now().time() <= time(9,18,00):
    sleep(30)
  angelbroking_conn_val = angelbroking_conn()
  for_trade = models_a.STOCK.objects.filter(active_5 = True, nifty_flag = False).values_list('symbol', flat=True)
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
  return merged_data_frame, for_trade