from datetime import datetime, time

from . import trade
from . import get_data
from . import trending_stocks

def model(intervals,stock_dict, flag, curr_time, kite_conn_var):
  '''
    intervals          = Intervals for Trading and Trend Analysis
    stock_dict         = List of Companies with their Symbol
    flag_config        = flag config file
    curr_time          = time of execution
    kite_conn_var      = to place orders in zerodha
  '''
  transactions = []

  # Regular Trades Execution
  if datetime.now().time() >= time(9,14,00) and datetime.now().time() < time(15,15,00):
    # Convert dataframe to List of Companies
    for_trend_stocks_30  = {}
    for stock in stock_dict.keys():
      if stock not in flag['Entry']:
        for_trend_stocks_30[stock] = stock_dict[stock]

    # DownLoad data for trend analysis 30 MIN
    data_frame = get_data.download_trend_data(for_trend_stocks_30,intervals,kite_conn_var)

    # Get the list of Trending Stocks 30 MIN
    trending_stocks_list_30  = trending_stocks.trending_30(data_frame,for_trend_stocks_30,intervals, flag)
    for_trend_stocks_15      = {}
    for stock in trending_stocks_list_30:
      for_trend_stocks_15[stock] = stock_dict[stock]

    # DownLoad data for trend analysis 15 MIN
    data_frame = get_data.download_trend_data(for_trend_stocks_15,intervals,kite_conn_var)

    # Get the list of Trending Stocks 15 MIN
    trending_stocks_list_15  = trending_stocks.trending_15(data_frame,for_trend_stocks_15,intervals, flag)
    for_trade_stocks  = {}
    for stock in stock_dict.keys():
      if stock in trending_stocks_list_15:
        for_trade_stocks[stock] = stock_dict[stock]
    
    if len(trending_stocks_list_15) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(for_trade_stocks,intervals,kite_conn_var)

      # Initiating trades
      transactions = trade.trade_execution(trade_data_frame, for_trade_stocks, intervals, flag, transactions, curr_time, kite_conn_var)
      return transactions, True
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.', False

  elif datetime.now().time() >= time(15,31,00):
    return 'MARKET ENDED.', False
  return 'MARKET NOT STARTED.', False