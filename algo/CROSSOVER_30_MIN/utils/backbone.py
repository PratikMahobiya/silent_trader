from Model_30M import models
from datetime import datetime, time
from time import sleep
from . import trade
from . import get_data
from . import trending_stocks

def model(intervals, kite_conn_var):
  '''
    intervals          = Intervals for Trading and Trend Analysis
    kite_conn_var      = to place orders in zerodha
  '''
  # Regular Trades Execution
  sleep(901)
  if datetime.now().time() >= time(9,14,00) and datetime.now().time() < time(15,00,00):
    # Trend Update i every 15 interval
    trending_stocks_list    = []
    if (15 <= datetime.now().time().minute < 19):
      # DownLoad data for trend analysis
      data_frame  = get_data.download_trend_data_60(intervals,kite_conn_var)

      # Get the list of Trending Stocks in 60 Minutes
      trending_stocks.trending_60(data_frame,intervals)
      trending_stocks_list    = models.TREND_30M_A.objects.all().values_list('symbol', flat=True)
    else:
      trending_stocks_list    = models.TREND_30M_A.objects.all().values_list('symbol', flat=True)

    if len(trending_stocks_list) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(trending_stocks_list,intervals,kite_conn_var)

      # Initiating trades
      trade.trade_execution(trade_data_frame, trending_stocks_list, intervals, kite_conn_var)
      return 'SUCCESS'
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.'

  if time(14,14,00) <= datetime.now().time() <= time(15,30,5):
    # Trend Update i every 15 interval
    trending_stocks_list    = []
    if (15 <= datetime.now().time().minute < 19):
      # DownLoad data for trend analysis
      data_frame  = get_data.download_trend_data_60(intervals,kite_conn_var)

      # Get the list of Trending Stocks in 60 Minutes
      trending_stocks.trending_60_BTST(data_frame,intervals)
      trending_stocks_list    = models.TREND_30M_A_BTST.objects.all().values_list('symbol', flat=True)
    else:
      trending_stocks_list    = models.TREND_30M_A_BTST.objects.all().values_list('symbol', flat=True)

    if len(trending_stocks_list) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(trending_stocks_list,intervals,kite_conn_var)

      # Initiating trades
      trade.trade_execution_BTST(trade_data_frame, trending_stocks_list, intervals, kite_conn_var)
      return 'SUCCESS'
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.'
    # return 'ENTRY IS CLOSED.'

  elif datetime.now().time() > time(15,30,5):
    return 'MARKET ENDED.'
  return 'MARKET NOT STARTED.'