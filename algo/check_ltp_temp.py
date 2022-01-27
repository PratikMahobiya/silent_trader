from Model_15_temp import models

from . import exit_action_temp
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  # GET ACTIVE STOCK LIST
  stock_list = models.ENTRY_15M_TEMP.objects.all().values_list('symbol', flat=True)
  active_stocks = []
  gain = [(0,0),]
  active_stocks = {}
  active_stocks_str = ''
  gain = [(0,0),]
  for stock in stock_list:
    active_stocks_str += 'NSE:'+stock+'-EQ,'
  active_stocks = {"symbols":active_stocks_str[:-1]}
  if len(active_stocks_str) != 0:
    stocks_ltp = kite_conn_var.quotes(active_stocks)['d']
    for stock_key in stocks_ltp:
      price = stock_key['v']['lp']
      stock_name = stock_key['v']['short_name'].split('-')[0]
      try:
        if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(15,15,5):
          if stock_name in stock_list:
            exit_action_temp.sell(stock_name, price, gain, kite_conn_var)
        elif datetime.now().time() >= time(15,15,5) and datetime.now().time() <= time(15,30,00):
          if stock_name in stock_list:
            exit_action_temp.square_off(stock_name, price, kite_conn_var)
      except Exception as e:
        pass
    return 'TRUE',list(stock_list), gain
  return 'NO ENTRY',list(stock_list), gain