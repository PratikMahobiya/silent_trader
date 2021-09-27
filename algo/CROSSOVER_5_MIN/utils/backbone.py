from datetime import datetime, time
import talib
from . import trade
from . import get_data
from . import trending_stocks

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
    # Convert dataframe to List of Companies

    # GET 30 MINUTE TRENDING STOCKS
    if (15 <= datetime.now().time().minute < 30) or (45 <= datetime.now().time().minute < 59):
      # DownLoad data for trend analysis 30 MIN
      data_frame_30 = get_data.download_trend_data_30(stock_dict,intervals,kite_conn_var)

      # Get the list of Trending Stocks 30 MIN
      trending_stocks_list_30  = trending_stocks.trending_30(data_frame_30,stock_dict,intervals, flag)
    else:
      trending_stocks_list_30  = flag['Trend_30']

    # GET 15 MINUTE TRENDING STOCKS
    if (0 <= datetime.now().time().minute < 4) or (15 <= datetime.now().time().minute < 19) or (30 <= datetime.now().time().minute < 34) or (45 <= datetime.now().time().minute < 49):
      for_trend_stocks_15      = {}
      for stock in trending_stocks_list_30:
        for_trend_stocks_15[stock] = stock_dict[stock]

      # DownLoad data for trend analysis 15 MIN
      data_frame_15 = get_data.download_trend_data_15(for_trend_stocks_15,intervals,kite_conn_var)

      # Get the list of Trending Stocks 15 MIN
      trending_stocks_list_15  = trending_stocks.trending_15(data_frame_15,for_trend_stocks_15,intervals, flag)
    else:
      trending_stocks_list_15  = flag['Trend_15']

    for_trade_stocks_temp  = {}
    for stock in trending_stocks_list_15:
      for_trade_stocks_temp[stock] = stock_dict[stock]
    
    for_trade_stocks = {}
    # GET 15 MINUTE TRENDING STOCKS
    if len(trending_stocks_list_15) != 0:
      if (0 <= datetime.now().time().minute < 4) or (15 <= datetime.now().time().minute < 19) or (30 <= datetime.now().time().minute < 34) or (45 <= datetime.now().time().minute < 49):
        for_trade_stocks = for_trade_stocks_temp
      else:
        # DownLoad data for initiating Trades
        trade_data_frame = get_data.download_trade_data(for_trade_stocks_temp,intervals,kite_conn_var)
        flag['Trend'].clear()
        for stock in trending_stocks_list_15:
          rsi = talib.RSI(trade_data_frame[stock]['Close'].iloc[:-1], timeperiod=intervals[9])
          if rsi[-1] > 50:
            for_trade_stocks[stock] = stock_dict[stock]
            flag['Trend'].append(stock)

    if len(for_trade_stocks) != 0:
      # DownLoad data for initiating Trades
      trade_data_frame = get_data.download_trade_data(for_trade_stocks,intervals,kite_conn_var)

      # Initiating trades
      transactions = trade.trade_execution(trade_data_frame, for_trade_stocks, intervals, flag, transactions, curr_time, kite_conn_var)
      return transactions, True
    else:
      # print('None of them is in Trending.')
      return 'NO STOCK IS IN TRENDING.', False

  elif datetime.now().time() >= time(15,31,00):
    return 'MARKET ENDED.', False
  return 'MARKET NOT STARTED.', False