from Model_15_temp import models

from . import exit_action_temp
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  # GET ACTIVE STOCK LIST
  stock_list = models.ENTRY_15M_TEMP.objects.all().values_list('symbol', flat=True)
  stocks_ltp = {}
  gain = [(0,0),]
  from algo import models as models_a
  for stock in stock_list:
    stocks_ltp[stock] = kite_conn_var.ltpData("NSE",stock+'-EQ',models_a.STOCK.objects.get(symbol = stock).token)['data']['ltp']
  if len(stock_list) != 0:
    for stock_key in stocks_ltp:
      price = stocks_ltp[stock_key]
      stock_name = stock_key
      try:
        if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(15,30,5):
          if stock_name in stock_list:
            exit_action_temp.sell(stock_name, price, gain, kite_conn_var)
      except Exception as e:
        pass
    return 'TRUE',list(stock_list), gain
  return 'NO ENTRY',list(stock_list), gain