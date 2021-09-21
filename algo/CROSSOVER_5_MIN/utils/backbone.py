from datetime import datetime, time
from . import trade
from . import get_data
from . import trending_stocks
import talib

def model(intervals,stock_dict, flag, curr_time, kite_conn_var):
  '''
    intervals          = Intervals for Trading and Trend Analysis
    stock_dict         = List of Companies with their Symbol
    flag_config        = flag config file
    curr_time          = time of execution
    kite_conn_var      = to place orders in zerodha
  '''
  transactions = []

  # Regular Trades Execution
  if datetime.now().time() >= time(9,14,00) and datetime.now().time() < time(15,15,00):
    # Trend Update i every 15 and 45 interval
    if (15 <= datetime.now().time().minute < 30) or (45 <= datetime.now().time().minute < 59):
      # DownLoad data for trend analysis
      data_frame = get_data.download_trend_data(stock_dict,intervals,kite_conn_var)

      # Get the list of Trending Stocks
      trending_stocks_list  = trending_stocks.trending(data_frame,stock_dict,intervals, flag)
    else:
      trending_stocks_list  = flag['Trend'] + flag['Trend_2']
      trending_stocks_list  = list(dict.fromkeys(trending_stocks_list))

    for_trade_stocks_temp  = {}
    for stock in trending_stocks_list:
      for_trade_stocks_temp[stock] = stock_dict[stock]
    
    if len(for_trade_stocks_temp) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(for_trade_stocks_temp,intervals,kite_conn_var)

      if (15 <= datetime.now().time().minute < 30) or (45 <= datetime.now().time().minute < 59):
        for_trade_stocks = for_trade_stocks_temp
      else:
        flag['Trend'].clear()
        for_trade_stocks = {}
        for stock in trending_stocks_list:
          rsi = talib.RSI(trade_data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[9])
          if rsi[-1] > 50:
            for_trade_stocks[stock] = stock_dict[stock]
            flag['Trend'].append(stock)
            flag[stock]['trend'] = True

      # Initiating trades
      transactions = trade.trade_execution(trade_data_frame, for_trade_stocks, intervals, flag, transactions, curr_time, kite_conn_var)
      return transactions, True
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.', False

  elif datetime.now().time() >= time(15,31,00):
    return 'MARKET ENDED.', False
  return 'MARKET NOT STARTED.', False