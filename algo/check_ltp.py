import json

from . import exit_action
from datetime import datetime

def get_stock_ltp(kite_conn_var):
  curr_time = datetime.now()
  transactions = []
  # Workbook Path
  flag_config_15            = 'algo/config/th_paca_t2_flag.json'
  with open(flag_config_15, "r") as outfile:
    flag_15 = json.load(outfile)

  # GET ACTIVE STOCK LIST
  stock_list = flag_15['Entry']
  active_stocks = []
  for stock in stock_list:
    active_stocks.append('NSE:'+stock)
  if len(active_stocks) != 0:
    stocks_ltp = kite_conn_var.ltp(active_stocks)
    for stock_key in stocks_ltp:
      price = stocks_ltp[stock_key]['last_price']
      stock_name = stock_key.split(':')[-1]
      if stock_name in flag_15['Entry']:
        exit_action.sell(stock_name, price, flag_15, transactions, curr_time, kite_conn_var)

  # Update config File:
  with open(flag_config_15, "w") as outfile:
    json.dump(flag_15, outfile)
  return transactions