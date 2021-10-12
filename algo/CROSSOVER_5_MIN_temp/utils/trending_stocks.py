from Model_5_temp import models
from algo import models as models_a
from datetime import datetime
import talib

def trending_30(data_frame,intervals):
  models.TREND_5M_A_TEMP.objects.all().delete()
  models.TREND_5M_C_TEMP.objects.all().delete()
  for_trend_stocks = models_a.STOCK.objects.filter(active_15 = True).values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] >= 50:
      models.TREND_5M_C_TEMP(symbol = stock, rsi = rsi[-1]).save()
      models.TREND_5M_A_TEMP(symbol = stock, rsi = rsi[-1]).save()
      conf_obj = models.CONFIG_5M_TEMP.objects.get(symbol = stock)
      conf_obj.trend = True
      conf_obj.save()
    else:
      conf_obj = models.CONFIG_5M_TEMP.objects.get(symbol = stock)
      conf_obj.trend = False
      conf_obj.save()

def trending_15(data_frame,intervals):
  models.TREND_5M_A_TEMP.objects.all().delete()
  models.TREND_5M_B_TEMP.objects.all().delete()
  for_trend_stocks = models.TREND_5M_C_TEMP.objects.all().values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] >= 50:
      models.TREND_5M_A_TEMP(symbol = stock, rsi = rsi[-1]).save()
      models.TREND_5M_B_TEMP(symbol = stock, rsi = rsi[-1]).save()
      conf_obj = models.CONFIG_5M_TEMP.objects.get(symbol = stock)
      conf_obj.trend = True
      conf_obj.save()
    else:
      conf_obj = models.CONFIG_5M_TEMP.objects.get(symbol = stock)
      conf_obj.trend = False
      conf_obj.save()

def trending_5(data_frame,intervals):
  models.TREND_5M_A_TEMP.objects.all().delete()
  for_trend_stocks = models.TREND_5M_B_TEMP.objects.all().values_list('symbol', flat=True)
  for stock in for_trend_stocks:
    rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
    if rsi[-1] >= 50:
      models.TREND_5M_A_TEMP(symbol = stock, rsi = rsi[-1]).save()
      conf_obj = models.CONFIG_5M_TEMP.objects.get(symbol = stock)
      conf_obj.trend = True
      conf_obj.save()