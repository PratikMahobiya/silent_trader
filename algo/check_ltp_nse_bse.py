from algo import models as models_a
from NSE_BSE import models

from . import nse_bse_trade
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  # GET ACTIVE STOCK LIST
  stock_list = models_a.STOCK.objects.filter(active_5_down = True, nifty_flag = False).values_list('symbol', flat=True)
  stocks_ltp = {}
  gain = [(0,0),]
  for stock in stock_list:
    stocks_ltp[stock] = (kite_conn_var.ltpData("NSE",stock+'-EQ',models_a.STOCK.objects.get(symbol = stock).token)['data']['ltp'],kite_conn_var.ltpData("BSE",stock,models_a.STOCK.objects.get(symbol = stock).bse_token)['data']['ltp'])
  if len(stock_list) != 0:
    for stock_key in stocks_ltp:
      nse_p, bse_p = stocks_ltp[stock_key]
      stock_config_obj = models.CONFIG_NSE_BSE.objects.get(symbol = stock)
      zerodha_flag_obj = models_a.PROFIT_CONFIG.objects.get(model_name = 'NSE_BSE')
      try:
        if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(15,15,5):
          if stock_config_obj.buy is False:
            nse_bse_trade.entry(stock_config_obj, stock_key, nse_p, bse_p, kite_conn_var,zerodha_flag_obj)
          else:
            pass #POORA BACHA HAI
      except Exception as e:
        pass
    return 'TRUE',list(stock_list), gain
  return 'NO ENTRY',list(stock_list), gain