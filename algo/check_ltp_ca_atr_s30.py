import json

from . import exit_action_ca_atr_s30
from datetime import datetime, time

def get_stock_ltp(kite_conn_var):
  curr_time = datetime.now()
  transactions = []
  # Workbook Path
  flag_config_CA_ATR_S30            = 'algo/config/ca_atr_s30_flag.json'
  with open(flag_config_CA_ATR_S30, "r") as outfile:
    flag_CA_ATR_S30 = json.load(outfile)

  # GET ACTIVE STOCK LIST
  stock_list = flag_CA_ATR_S30['Entry']
  active_stocks = []
  for stock in stock_list:
    active_stocks.append('NSE:'+stock.split('.')[0])
  if len(active_stocks) != 0:
    stocks_ltp = kite_conn_var.ltp(active_stocks)
    for stock_key in stocks_ltp:
      price = stocks_ltp[stock_key]['last_price']
      stock_name = stock_key.split(':')[-1] + '.NS'
      if datetime.now().time() >= time(9,16,00) and datetime.now().time() < time(15,14,00):
        if stock_name in flag_CA_ATR_S30['Entry']:
          exit_action_ca_atr_s30.sell(stock_name, price, flag_CA_ATR_S30, transactions, curr_time, kite_conn_var)
      elif datetime.now().time() >= time(15,14,00) and datetime.now().time() <= time(15,30,00):
        if stock_name in flag_CA_ATR_S30['Entry']:
          exit_action_ca_atr_s30.square_off(stock_name, price, flag_CA_ATR_S30, transactions, curr_time, kite_conn_var)
    # Update config File:
    with open(flag_config_CA_ATR_S30, "w") as outfile:
      json.dump(flag_CA_ATR_S30, outfile)
    return transactions, stocks_ltp

  # Update config File:
  with open(flag_config_CA_ATR_S30, "w") as outfile:
    json.dump(flag_CA_ATR_S30, outfile)
  return transactions, active_stocks