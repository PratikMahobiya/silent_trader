import json

from . import exit_action_slfema
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  curr_time = datetime.now()
  transactions = []
  # Workbook Path
  flag_config_SLFEMA            = 'algo/config/th_paca_t2_flag.json'
  with open(flag_config_SLFEMA, "r") as outfile:
    flag_SLFEMA = json.load(outfile)

  # GET ACTIVE STOCK LIST
  stock_list = flag_SLFEMA['Entry']
  active_stocks = []
  for stock in stock_list:
    active_stocks.append('NSE:'+stock.split('.')[0])
  if len(active_stocks) != 0:
    stocks_ltp = kite_conn_var.ltp(active_stocks)
    for stock_key in stocks_ltp:
      price = stocks_ltp[stock_key]['last_price']
      stock_name = stock_key.split(':')[-1] + '.NS'
      if datetime.now().time() >= time(9,16,00) and datetime.now().time() < time(15,14,00):
        if stock_name in flag_SLFEMA['Entry']:
          exit_action_slfema.sell(stock_name, price, flag_SLFEMA, transactions, curr_time, kite_conn_var)
      elif datetime.now().time() >= time(15,14,00) and datetime.now().time() <= time(15,30,00):
        if stock_name in flag_SLFEMA['Entry']:
          exit_action_slfema.square_off(stock_name, price, flag_SLFEMA, transactions, curr_time, kite_conn_var)
    # Update config File:
    with open(flag_config_SLFEMA, "w") as outfile:
      json.dump(flag_SLFEMA, outfile)
    return transactions, stocks_ltp

  # Update config File:
  with open(flag_config_SLFEMA, "w") as outfile:
    json.dump(flag_SLFEMA, outfile)
  return transactions, active_stocks