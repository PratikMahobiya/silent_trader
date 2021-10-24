from Model_15_temp import models
from datetime import datetime, time
from . import trade
from . import get_data
from . import trending_stocks

def model(intervals, kite_conn_var):
  '''
    intervals          = Intervals for Trading and Trend Analysis
    kite_conn_var      = to place orders in zerodha
  '''
  # Regular Trades Execution
  if datetime.now().time() >= time(9,44,00) and datetime.now().time() < time(15,00,00):
    # Trend Update i every 15 and 45 interval
    trending_stocks_list = []
    if (15 <= datetime.now().time().minute < 19) or (45 <= datetime.now().time().minute < 49):
      # DownLoad data for trend analysis
      data_frame  = get_data.download_trend_data_30(intervals,kite_conn_var)

      # Get the list of Trending Stocks in 30 Minutes
      trending_stocks.trending_30(data_frame,intervals)
      trending_stocks_list        = models.TREND_15M_A_TEMP.objects.all().values_list('symbol', flat=True)
    else:
      # Get the list of those Trending Stocks who are in trend in 30 Minutes
      trending_stocks_list    = models.TREND_15M_A_TEMP.objects.all().values_list('symbol', flat=True)

    if len(trending_stocks_list) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(trending_stocks_list,intervals,kite_conn_var)

      # Initiating trades
      trade.trade_execution(trade_data_frame, trending_stocks_list, intervals, kite_conn_var)
      return 'SUCCESS'
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.'

  elif time(15,00,00) <= datetime.now().time() <= time(15,30,00):
    # Trend Update i every 15 and 45 interval
    trending_stocks_list = []
    if (15 <= datetime.now().time().minute < 19) or (45 <= datetime.now().time().minute < 49):
      # DownLoad data for trend analysis
      data_frame  = get_data.download_trend_data_30(intervals,kite_conn_var)

      # Get the list of Trending Stocks in 30 Minutes
      trending_stocks.trending_30(data_frame,intervals)
      trending_stocks_list        = models.TREND_15M_A_TEMP_BTST.objects.all().values_list('symbol', flat=True)
    else:
      # Get the list of those Trending Stocks who are in trend in 30 Minutes
      trending_stocks_list    = models.TREND_15M_A_TEMP.objects.all().values_list('symbol', flat=True)

    if len(trending_stocks_list) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(trending_stocks_list,intervals,kite_conn_var)

      # Initiating trades
      trade.trade_execution_BTST(trade_data_frame, trending_stocks_list, intervals, kite_conn_var)
      return 'SUCCESS'
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.'
    return 'ENTRY IS CLOSED.'
  elif datetime.now().time() > time(15,30,00):
    return 'MARKET ENDED.'
  return 'MARKET NOT STARTED.'