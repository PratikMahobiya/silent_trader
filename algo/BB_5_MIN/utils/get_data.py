import yfinance as yf
from pandas_datareader import data as pdr

def download_trade_data(trade_stock_list,intervals):
    yf.pdr_override()
    # download dataframe
    data = pdr.get_data_yahoo(tickers=trade_stock_list, period = intervals[1], interval=intervals[0], progress=False).tz_localize(None)
    return data