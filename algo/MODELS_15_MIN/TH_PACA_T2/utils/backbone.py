import datetime
import os
import json

from datetime import datetime, time

from . import trade
from . import trending_stocks

def model(trend_data,trade_data,intervals,company_sheet,flag_config,curr_time):
  '''
    intervals       = Intervals for Trading and Trend Analysis
    company_sheet   = List of Companies with their Symbol
    flag_config     = flag config file
  '''
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_sheet['SYMBOL']
  transactions = []

  # Create Flag config for each company
  if not os.path.exists(flag_config):
    # print("Created Flag Config File For all STOCKS.")
    flag = {}
    flag['Entry'] = []
    for symb in companies_symbol:
      flag[symb] = {'buy':False,'buying_price':0,'ema_min':0,'ema_max':0,'selling_price':0,'stoploss':0,'target':0,'target_per':0,'trend_rsi':0,'target_hit':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)

  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

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
    # Update config File:
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
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
    # Update config File:
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
    return transactions, True

  elif datetime.now().time() >= time(15,30,00):
    return 'MARKET CLOSED', False