from Model_15_temp import models
from algo import models as models_a
from datetime import datetime
import talib

def trending_30(data_frame,intervals):
  models.TREND_15M_A.objects.all().delete()
  for_trend_stocks = models_a.STOCK.objects.filter(active_15 = True).values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] >= 50:
      models.TREND_15M_A(symbol = stock, rsi = rsi[-1]).save()
      conf_obj = models.CONFIG_15M.objects.get(symbol = stock)
      conf_obj.trend = True
      conf_obj.save()
    else:
      conf_obj = models.CONFIG_15M.objects.get(symbol = stock)
      conf_obj.trend = False
      conf_obj.save()