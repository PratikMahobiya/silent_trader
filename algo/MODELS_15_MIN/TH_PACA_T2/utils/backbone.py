from datetime import datetime, time
from . import trade
from . import trending_stocks

def model(trend_data,trade_data,intervals,flag,curr_time):
  '''
    intervals       = Intervals for Trading and Trend Analysis
    flag_config     = flag config file
  '''
  transactions = []

  # Regular Trades Execution
  if datetime.now().time() >= time(9,14,00) and datetime.now().time() < time(15,15,00):
    # Get the list of Trending Stocks
    trending_stocks_list  = trending_stocks.trending(trend_data,intervals, flag)
    trade_stock_list      = flag['Entry'] + [stock for stock in trending_stocks_list if stock not in flag['Entry']]

    if len(trade_stock_list) != 0:
      # Initiating trades
      transactions = trade.trade_execution(trade_data, trade_stock_list, intervals, flag, transactions, curr_time)
    else:
      # print('None of them is in Trending.')
      return 'No stock is in Trend and Entry', False
    return transactions, True

  # Square off
  elif datetime.now().time() >= time(15,15,00) and datetime.now().time() < time(15,30,00):
    # Convert dataframe to List of Companies
    trade_stock_list  = flag['Entry']

    if len(trade_stock_list) != 0:
      # Initiating trades
      transactions = trade.square_off(trade_data,trade_stock_list,intervals,flag,transactions,curr_time)
    else:
      # print('None of them is in Trending.')
      return 'No Stock For SquareOff', False
    return transactions, True

  elif datetime.now().time() >= time(15,30,00):
    return 'MARKET CLOSED', False
  return 'MARKET NOT STARTED.', False