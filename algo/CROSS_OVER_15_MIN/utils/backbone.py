from datetime import datetime, time

from . import trade
from . import get_data
from . import trending_stocks

def model(intervals,companies_symbol, flag, curr_time):
  '''
    intervals          = Intervals for Trading and Trend Analysis
    companies_symbol   = List of Companies with their Symbol
    flag_config        = flag config file
    curr_time          = time of execution
  '''
  transactions = []

  # Regular Trades Execution
  if datetime.now().time() >= time(9,14,00) and datetime.now().time() < time(15,15,00):
    # Convert dataframe to List of Companies
    comp_list   = companies_symbol.to_list()
    stock_list  = [stock for stock in comp_list if stock not in flag['Entry']]

    # DownLoad data for trend analysis
    data_frame = get_data.download_trend_data(stock_list,intervals)

    # Get the list of Trending Stocks
    trending_stocks_list  = trending_stocks.trending(data_frame,intervals, flag)
    trade_stock_list      = flag['Entry'] + trending_stocks_list
    
    if len(trade_stock_list) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(trade_stock_list,intervals)

      # Initiating trades
      transactions = trade.trade_execution(trade_data_frame, intervals, flag, transactions, curr_time)
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.', False
  # Square off
  elif datetime.now().time() >= time(15,15,00) and datetime.now().time() < time(15,30,00):
    if len(flag['Entry']) >= 2:
      # Convert dataframe to List of Companies
      trade_stock_list  = flag['Entry']

      # DownLoad data for Square Off Trades
      trade_data_frame = get_data.download_trade_data(trade_stock_list,intervals)

      # Initiating trades
      stock_name = None
      transactions = trade.square_off(stock_name,trade_data_frame, intervals, flag, transactions, curr_time)

    elif len(flag['Entry']) == 1:
      # Convert dataframe to List of Companies
      trade_stock_list  = flag['Entry']

      # DownLoad data for Square Off Trades
      trade_data_frame = get_data.download_trade_data(trade_stock_list,intervals)

      # Initiating trades
      stock_name = flag['Entry'][0]
      transactions = trade.square_off(stock_name,trade_data_frame, intervals, flag, transactions, curr_time)

    else:
      return 'ALL TRADES ARE ENDED.', False

  return transactions, True