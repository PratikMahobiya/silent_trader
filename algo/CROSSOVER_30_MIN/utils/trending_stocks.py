from Model_30M import models
from algo import models as models_a
from datetime import datetime
import talib

def trending_60(data_frame,intervals):
  models.TREND_30M_A.objects.all().delete()
  for_trend_stocks = models_a.STOCK.objects.filter(active_30 = True).values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    ema_min     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=40)
    ema_max     = talib.EMA(data_frame[stock]['Close'].iloc[:-1], timeperiod=200)
    if rsi[-1] >= 40:
      if ema_min[-1] > ema_max[-1]:
        models.TREND_30M_A(symbol = stock, rsi = rsi[-1]).save()
        conf_obj = models.CONFIG_30M.objects.get(symbol = stock)
        conf_obj.trend = True
        conf_obj.save()
      else:
        conf_obj = models.CONFIG_30M.objects.get(symbol = stock)
        conf_obj.trend = False
        conf_obj.save()
    else:
      conf_obj = models.CONFIG_30M.objects.get(symbol = stock)
      conf_obj.trend = False
      conf_obj.save()