from Model_15_temp import models
from algo import models as models_a
from datetime import datetime, time
import talib

def trending_30(data_frame,intervals):
  if datetime.now().time() >= time(9,44,00) and datetime.now().time() < time(15,00,00):
    models.TREND_15M_A_TEMP.objects.all().delete()
    for_trend_stocks = models_a.STOCK.objects.filter(active_15 = True).values_list('symbol', flat=True)
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
      if rsi[-1] >= 50:
        models.TREND_15M_A_TEMP(symbol = stock, rsi = rsi[-1]).save()
        conf_obj = models.CONFIG_15M_TEMP.objects.get(symbol = stock)
        conf_obj.trend = True
        conf_obj.save()
      else:
        conf_obj = models.CONFIG_15M_TEMP.objects.get(symbol = stock)
        conf_obj.trend = False
        conf_obj.save()
  else:
    models.TREND_15M_A_TEMP_BTST.objects.all().delete()
    for_trend_stocks = models_a.STOCK.objects.filter(active_15 = True).values_list('symbol', flat=True)
    for stock in for_trend_stocks:
      rsi = talib.RSI(data_frame[stock]['Close'].iloc[:-1], timeperiod = intervals[8])
      if rsi[-1] >= 50:
        models.TREND_15M_A_TEMP_BTST(symbol = stock, rsi = rsi[-1]).save()
        conf_obj = models.CONFIG_15M_TEMP_BTST.objects.get(symbol = stock)
        conf_obj.trend = True
        conf_obj.save()
      else:
        conf_obj = models.CONFIG_15M_TEMP_BTST.objects.get(symbol = stock)
        conf_obj.trend = False
        conf_obj.save()