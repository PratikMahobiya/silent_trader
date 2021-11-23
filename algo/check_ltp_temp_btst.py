from Model_15_temp import models

from . import exit_action_temp_btst
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  # GET ACTIVE STOCK LIST
  stock_list = models.ENTRY_15M_TEMP_BTST.objects.all().values_list('symbol', flat=True)
  active_stocks = []
  gain = [[0,][0,]]
  for stock in stock_list:
    active_stocks.append('NSE:'+stock)
  if len(active_stocks) != 0:
    stocks_ltp = kite_conn_var.ltp(active_stocks)
    for stock_key in stocks_ltp:
      price = stocks_ltp[stock_key]['last_price']
      stock_name = stock_key.split(':')[-1]
      try:
        if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(9,40,00):
          if stock_name in stock_list:
            exit_action_temp_btst.sell(stock_name, price, gain, kite_conn_var)
        elif datetime.now().time() >= time(9,40,00) and datetime.now().time() <= time(9,45,00):
          if stock_name in stock_list:
            exit_action_temp_btst.square_off(stock_name, price, kite_conn_var)
      except Exception as e:
        pass
    return 'TRUE',list(stock_list), gain
  return 'NO ENTRY',list(stock_list), gain