import datetime
import os
import json

from datetime import datetime, time

from . import trade

def model(trade_data,intervals,company_sheet, flag_config, curr_time):
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
      flag[symb] = {'buy':False,'buying_price':0,'lowerband':0,'upperband':0,'atr':0,'selling_price':0,'stoploss':0,'selling_val':0,'upper_val':0}
    with open(flag_config, "w") as outfile:
      json.dump(flag, outfile)
  # Load The Last Updated Flag Config
  else:
    # print("Loaded Flag Config File For all Stocks.")
    with open(flag_config, "r") as outfile:
      flag = json.load(outfile)

  # Regular Trades Execution
  if datetime.now().time() >= time(9,15,00) and datetime.now().time() < time(15,15,00):
    # Initiating trades
    transactions = trade.trade_execution(trade_data, intervals, flag, transactions, curr_time)
    if len(transactions) == 0:
      return 'NOT GETTING ENTRY IN ANY OF THE STOCK', False
  # Square off
  elif datetime.now().time() >= time(15,15,00) and datetime.now().time() <= time(15,30,59):
    if len(flag['Entry']) != 0:
      # Convert dataframe to List of Companies
      trade_stock_list  = flag['Entry']

      # Initiating trades
      transactions = trade.square_off(trade_stock_list,trade_data, intervals, flag, transactions, curr_time)
    else:
      return 'ALL TRADES ARE ENDED.', False

  # Update config File:
  with open(flag_config, "w") as outfile:
    json.dump(flag, outfile)
  return transactions, True