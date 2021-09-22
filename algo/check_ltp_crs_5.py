import json

from . import exit_action_crs_5
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  curr_time = datetime.now()
  transactions = []
  # Workbook Path
  flag_config_5            = 'algo/config/crs_5_min_flag.json'
  with open(flag_config_5, "r") as outfile:
    flag_5 = json.load(outfile)

  # GET ACTIVE STOCK LIST
  stock_list = flag_5['Entry']
  active_stocks = []
  for stock in stock_list:
    active_stocks.append('NSE:'+stock)
  if len(active_stocks) != 0:
    stocks_ltp = kite_conn_var.ltp(active_stocks)
    for stock_key in stocks_ltp:
      price = stocks_ltp[stock_key]['last_price']
      stock_name = stock_key.split(':')[-1]
      try:
        if datetime.now().time() >= time(9,16,00) and datetime.now().time() < time(15,15,00):
          if stock_name in flag_5['Entry']:
            exit_action_crs_5.sell(stock_name, price, flag_5, transactions, curr_time, kite_conn_var)
        elif datetime.now().time() >= time(15,15,00) and datetime.now().time() <= time(15,30,00):
          if stock_name in flag_5['Entry']:
            exit_action_crs_5.square_off(stock_name, price, flag_5, transactions, curr_time, kite_conn_var)
      except Exception as e:
        pass
    # Update config File:
    with open(flag_config_5, "w") as outfile:
      json.dump(flag_5, outfile)
    active_stocks_ltp = []
    for i in stock_list:
      if flag_5[i]['trend'] == False:
        active_stocks_ltp.append(i.split(':')[-1])
    return transactions, active_stocks_ltp, stock_list

  # Update config File:
  with open(flag_config_5, "w") as outfile:
    json.dump(flag_5, outfile)
  return transactions, active_stocks, stock_list