from Model_5M import models
from algo import models as models_a
from datetime import datetime
import talib

def trending_30(data_frame,intervals):
  models.TREND_5M_C.objects.all().delete()
  for_trend_stocks = models_a.STOCK.objects.filter(active_15 = True).values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] >= 50:
      models.TREND_5M_C(symbol = stock, rsi = rsi[-1]).save()
      conf_obj = models.CONFIG_5M.objects.get(symbol = stock)
      conf_obj.trend = True
      conf_obj.save()
    else:
      conf_obj = models.CONFIG_5M.objects.get(symbol = stock)
      conf_obj.trend = False
      conf_obj.save()

def trending_15(data_frame,intervals):
  models.TREND_5M_A.objects.all().delete()
  models.TREND_5M_B.objects.all().delete()
  for_trend_stocks = models.TREND_5M_C.objects.all().values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] >= 50:
      models.TREND_5M_A(symbol = stock, rsi = rsi[-1]).save()
      models.TREND_5M_B(symbol = stock, rsi = rsi[-1]).save()
      conf_obj = models.CONFIG_5M.objects.get(symbol = stock)
      conf_obj.trend = True
      conf_obj.save()
    else:
      conf_obj = models.CONFIG_5M.objects.get(symbol = stock)
      conf_obj.trend = False
      conf_obj.save()

def trending_5(data_frame,intervals):
  models.TREND_5M_A.objects.all().delete()
  for_trend_stocks = models.TREND_5M_B.objects.all().values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] >= 50:
      models.TREND_5M_A(symbol = stock, rsi = rsi[-1]).save()
      conf_obj = models.CONFIG_5M.objects.get(symbol = stock)
      conf_obj.trend = True
      conf_obj.save()
    else:
      conf_obj = models.CONFIG_5M.objects.get(symbol = stock)
      conf_obj.trend = False
      conf_obj.save()