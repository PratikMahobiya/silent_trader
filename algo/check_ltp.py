import json

from . import exit_action
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  curr_time = datetime.now()
  transactions = []
  # Workbook Path
  flag_config_CA            = 'algo/config/th_ca_flag.json'
  with open(flag_config_CA, "r") as outfile:
    flag_CA = json.load(outfile)

  # GET ACTIVE STOCK LIST
  stock_list = flag_CA['Entry']
  active_stocks = []
  for stock in stock_list:
    active_stocks.append('NSE:'+stock)
  if len(active_stocks) != 0:
    stocks_ltp = kite_conn_var.ltp(active_stocks)
    for stock_key in stocks_ltp:
      price = stocks_ltp[stock_key]['last_price']
      stock_name = stock_key.split(':')[-1]
      if datetime.now().time() >= time(9,18,00) and datetime.now().time() < time(15,15,00):
        if stock_name in flag_CA['Entry']:
          exit_action.sell(stock_name, price, flag_CA, transactions, curr_time, kite_conn_var)
      elif datetime.now().time() >= time(15,15,00) and datetime.now().time() <= time(15,40,00):
        if stock_name in flag_CA['Entry']:
          exit_action.square_off(stock_name, price, flag_CA, transactions, curr_time, kite_conn_var)

  # Update config File:
  with open(flag_config_CA, "w") as outfile:
    json.dump(flag_CA, outfile)
  return transactions