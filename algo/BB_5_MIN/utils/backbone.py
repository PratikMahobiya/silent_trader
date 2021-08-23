import datetime
import os
import json

from datetime import datetime, time
from time import sleep

from . import trade
from . import get_data

def model(intervals,company_sheet, flag, curr_time):
  sleep(65)
  '''
    intervals       = Intervals for Trading and Trend Analysis
    company_sheet   = List of Companies with their Symbol
    flag     = flag config file
  '''
  # Extract Symbols and Company Names from Dataframe
  companies_symbol = company_sheet['SYMBOL']
  transactions = []

  # Regular Trades Execution
  if datetime.now().time() >= time(9,15,00) and datetime.now().time() < time(15,20,00):
    # Convert dataframe to List of Companies
    comp_list   = companies_symbol.to_list()
    # DownLoad data for initiating Trades
    trade_data_frame = get_data.download_trade_data(comp_list,intervals)

    # Initiating trades
    transactions = trade.trade_execution(trade_data_frame, intervals, flag, transactions, curr_time)
    return transactions, True

  # Square off
  elif datetime.now().time() >= time(15,20,00) and datetime.now().time() <= time(15,30,59):
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
      return 'ALL STOCKS ARE SQUARED OFF', False

  elif datetime.now().time() >= time(15,31,00):
    return 'MARKET ENDED.', False  
  return 'MARKET NOT STARTED.', False