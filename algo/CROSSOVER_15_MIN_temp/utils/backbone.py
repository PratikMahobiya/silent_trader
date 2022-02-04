from algo.models import PROFIT_CONFIG
from datetime import datetime, time
from . import trade
from . import get_data

def model(intervals, kite_conn_var):
  '''
    intervals          = Intervals for Trading and Trend Analysis
    kite_conn_var      = to place orders in zerodha
  '''
  # Regular Trades Execution
  if datetime.now().time() >= time(9,14,00) and datetime.now().time() < time(15,25,00):
    # if (datetime.now().time() >= time(10,30,00) and datetime.now().time() < time(13,58,00)) and (PROFIT_CONFIG.objects.get(model_name = 'CRS_TEMP').zerodha_entry is True):
    #   PROFIT_CONFIG.objects.get(model_name = 'CRS_TEMP').update(zerodha_entry = False)
    # if (datetime.now().time() >= time(13,58,00)) and (PROFIT_CONFIG.objects.get(model_name = 'CRS_TEMP').zerodha_entry is False):
    #   PROFIT_CONFIG.objects.get(model_name = 'CRS_TEMP').update(zerodha_entry = True)
    # DownLoad data for initiating Trades
    trade_data_frame, trading_stocks_list = get_data.download_trade_data(intervals,kite_conn_var)

    # Initiating trades
    trade.trade_execution(trade_data_frame, trading_stocks_list, intervals, kite_conn_var)
    return 'SUCCESS'

  # # SQUARE OFF EXECUTIONS
  # elif time(15,12,00) <= datetime.now().time() < time(15,30,00):
  #   trade.squareoff(kite_conn_var)
  #   return 'SUCCESS'

  elif datetime.now().time() > time(15,30,5):
    return 'MARKET ENDED.'
  return 'MARKET NOT STARTED.'