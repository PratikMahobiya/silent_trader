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
    for_trend_stocks  = {}
    for stock in stock_dict.keys():
      if stock not in flag['Entry']:
        for_trend_stocks[stock] = stock_dict[stock]

    if (15 <= datetime.now().time().minute < 30) or (45 <= datetime.now().time().minute < 59):
      # DownLoad data for trend analysis
      data_frame = get_data.download_trend_data(for_trend_stocks,intervals,kite_conn_var)

      # Get the list of Trending Stocks
      trending_stocks_list  = trending_stocks.trending(data_frame,for_trend_stocks,intervals, flag)
    else:
      trending_stocks_list  = flag['Trend']

    trade_stock_list = []
    for stock in trending_stocks_list:
      if stock not in flag['Entry']:
        trade_stock_list.append(stock)

    for_trade_stocks  = {}
    for stock in stock_dict.keys():
      if stock in trade_stock_list:
        for_trade_stocks[stock] = stock_dict[stock]
    
    if len(trade_stock_list) != 0:
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