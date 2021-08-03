import datetime
import os
import json
import pandas as pd

from datetime import datetime, time

from . import trade
from . import get_data
from . import trending_stocks

def model_ema_rsi(intervals,company_sheet, flag_config):
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
      flag[symb] = {'buy':False,'buying_price':0,'selling_val':0,'upper_val':0,'selling_price':0,'stoploss':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)

  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  # Regular Trades Execution
  if datetime.now().time() >= time(9,15,00) and datetime.now().time() < time(15,20,00):
    # Convert dataframe to List of Companies
    comp_list   = companies_symbol.to_list()
    stock_list  = [stock for stock in comp_list if stock not in flag['Entry']]

    # DownLoad data for trend analysis
    data_frame = get_data.download_trend_data(stock_list,intervals)

    # Get the list of Trending Stocks
    trending_stocks_list  = trending_stocks.trending(data_frame,intervals)
    trade_stock_list      = flag['Entry'] + trending_stocks_list
    
    if len(trade_stock_list) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(trade_stock_list,intervals)

      # Initiating trades
      transactions = trade.trade_execution(trade_data_frame, intervals, flag, transactions)
    else:
      # print('None of them is in Trending.')
      return 'Done', False
  # Square off
  elif datetime.now().time() >= time(15,20,00) and datetime.now().time() < time(15,30,00):
    if len(flag['Entry']) >= 2:
      # Convert dataframe to List of Companies
      trade_stock_list  = flag['Entry']

      # DownLoad data for Square Off Trades
      trade_data_frame = get_data.download_trade_data(trade_stock_list,intervals)

      # Initiating trades
      stock_name = None
      transactions = trade.square_off(stock_name,trade_data_frame, intervals, flag, transactions)

    elif len(flag['Entry']) == 1:
      # Convert dataframe to List of Companies
      trade_stock_list  = flag['Entry']

      # DownLoad data for Square Off Trades
      trade_data_frame = get_data.download_trade_data(trade_stock_list,intervals)

      # Initiating trades
      stock_name = flag['Entry'][0]
      transactions = trade.square_off(stock_name,trade_data_frame, intervals, flag, transactions)

    else:
      return 'Done', False

  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return transactions, True