from datetime import date, datetime, time
from kiteconnect import KiteConnect
from time import sleep

from Model_15M import models
from Model_30M import models as models_30
from algo import check_ltp_temp_btst
from algo import check_ltp_crs_30_btst
from . import models as models_a
from . import freeze_all_15
from . import freeze_all_15_btst
from . import freeze_all_15_temp
from . import freeze_all_15_temp_btst
from . import freeze_all_30
from . import freeze_all_30_btst
from . import freeze_all_15_down
from . import check_ltp
from . import check_ltp_btst
from . import check_ltp_crs_30
from celery import shared_task
from .CROSSOVER_15_MIN.utils import backbone as backbone_CRS_15_MIN
from .CROSSOVER_30_MIN.utils import backbone as backbone_CRS_30_MIN

# -------------------- Not ------------------
from Model_15_temp import models as models_temp
from Model_15_temp_down import models as models_temp_down
from . import check_ltp_temp
from . import check_ltp_temp_btst
from . import check_ltp_temp_down
from . import check_ltp_temp_btst_down
from .CROSSOVER_15_MIN_temp.utils import backbone as backbone_CRS_temp
from .DOWN_CROSSOVER_15_MIN_temp.utils import backbone as backbone_DOWN_CRS_temp

@shared_task(bind=True,max_retries=3)
# initial_setup on DATABASE -------------------------------------
def get_stocks_configs(self):
  response = {'stock_table': False, 'config_table_15': False, 'config_table_30': False}
  # Stock dict
  stock_dict = {
      'AARTIIND':	[1793,		'COMMODITY','mid50'],
      'ABFRL':	[7707649,	'nill','NA'],
      'ACC':		[5633,		'INFRA,COMMODITY','nxt50'],
      'ADANIENT':	[6401,		'METAL','nxt50'],
      'ADANIGREEN':	[912129,	'ENERGY,COMMODITY','nxt50'],
      'ADANIPORTS':	[3861249,	'INFRA','nify'],
      'AMBUJACEM':	[325121,	'INFRA,MNC,COMMODITY','nxt50'],
      'APLLTD':	[6483969,	'nill','NA'],
      'APOLLOTYRE':	[41729,		'nill','mid50'],
      'ASHOKLEY':	[54273,		'AUTO,INFRA,MNC','mid50'],
      'ASIANPAINT':	[60417,		'CONSUMPTION','nify'],
      'AUROPHARMA':	[70401,		'PHARMA','nxt50'],
      'AXISBANK':	[1510401,	'BANK,FINN','nify'],
      'BAJAJ-AUTO':	[4267265,	'AUTO,CONSUMPTION','nify'],
      'BANDHANBNK':	[579329,	'BANK','nxt50'],
      'BANKBARODA':	[1195009,	'BANK','nxt50'],
      'BANKINDIA':	[1214721,	'BANK','mid50'],
      'BATAINDIA':	[94977,		'MNC','mid50'],
      'BEL':		[98049,		'PSE','mid50'],
      'BERGEPAINT':	[103425,	'CONSUMPTION','nxt50'],
      'BHARATFORG':	[108033,	'AUTO','mid50'],
      'BHARTIARTL':	[2714625,	'INFRA,CONSUMPTION','nify'],
      'BHEL':		[112129,	'PSE','mid50'],
      'BIOCON':	[2911489,	'PHARMA','nxt50'],
      'BPCL':		[134657,	'INFRA,PSE,COMMODITY','nify'],
      'BRITANNIA':	[140033,	'FMCG,MNC,CONSUMPTION','nify'],
      'CADILAHC':	[2029825,	'PHARMA','nxt50'],
      'CANBK':	[2763265,	'BANK','mid50'],
      'CASTROLIND':	[320001,	'MNC','NA'],
      'CHOLAFIN':	[175361,	'FINN','nxt50'],
      'CIPLA':	[177665,	'PHARMA','nify'],
      'COALINDIA':	[5215745,	'METAL,PSE,COMMODITY','nify'],
      'COFORGE':	[2955009,	'IT','mid50'],
      'COLPAL':	[3876097,	'FMCG,MNC,CONSUMPTION','nxt50'],
      'CONCOR':	[1215745,	'INFRA,PSE','mid50'],
      'CUB':		[1459457,	'nill','NA'],
      'CUMMINSIND':	[486657,	'MNC','mid50'],
      'DABUR':	[197633,	'FMCG,CONSUMPTION','nxt50'],
      'DIVISLAB':	[2800641,	'PHARMA','nify'],
      'DLF':		[3771393,	'INFRA','nxt50'],
      'DMART':	[5097729,	'CONSUMPTION','nxt50'],
      'DRREDDY':	[225537,	'PHARMA','nify'],
      'EMAMILTD':	[3460353,	'FMCG','NA'],
      'ESCORTS':	[245249,	'nill','mid50'],
      'EICHERMOT':	[232961,	'AUTO','nify'],
      'EXIDEIND':	[173057,	'AUTO,INFRA','mid50'],
      'FEDERALBNK':	[261889,	'BANK','mid50'],
      'GAIL':		[1207553,	'INFRA,PSE','nxt50'],
      'GMRINFRA':	[3463169,	'nill','NA'],
      'GODREJCP':	[2585345,	'FMCG,CONSUMPTION','nxt50'],
      'GODREJPROP':	[4576001,	'nill','mid50'],
      'GRANULES':	[3039233,	'nill','NA'],
      'GRASIM':	[315393,	'INFRA,COMMODITY','nify'],
      'HAVELLS':	[2513665,	'CONSUMPTION','nxt50'],
      'HCLTECH':	[1850625,	'IT','nify'],
      'HDFC':		[340481,	'FINN','nify'],
      'HDFCBANK':	[341249,	'BANK,FINN','nify'],
      'HDFCLIFE':	[119553,	'FINN','nify'],
      'HEROMOTOCO':	[345089,	'AUTO','nify'],
      'HINDALCO':	[348929,	'METAL','nify'],
      'HINDPETRO':	[359937,	'INFRA,PSE,COMMODITY','nxt50'],
      'HINDUNILVR':	[356865,	'FMCG,MNC,CONSUMPTION','nify'],
      'HINDZINC':	[364545,	'METAL,COMMODITY','NA'],
      'IBULHSGFIN':	[7712001,	'nill','NA'],
      'ICICIBANK':	[1270529,	'BANK,FINN','nify'],
      'IDFCFIRSTB':	[2863105,	'BANK','mid50'],
      'IGL':		[2883073,	'INFRA','nxt50'],
      'INDIANB':	[3663105,	'BANK','NA'],
      'INDIGO': [2865921,'nill','NA'],
      'INDUSINDBK':	[1346049,	'BANK','nify'],
      'INDUSTOWER':	[7458561,	'INFRA','nxt50'],
      'INFY':		[408065,	'IT','nify'],
      'IOC':		[415745,	'INFRA,PSE,COMMODITY','nify'],
      'IRCTC':	[3484417,	'PSE','mid50'],
      'ITC':		[424961,	'FMCG,CONSUMPTION','nify'],
      'JINDALSTEL':	[1723649,	'METAL,COMMODITY','nxt50'],
      'JSWSTEEL':	[3001089,	'METAL,COMMODITY','nify'],
      'JUBLFOOD':	[4632577,	'FMCG,CONSUMPTION','nxt50'],
      'KOTAKBANK':	[492033,	'BANK,FINN','nify'],
      'LICHSGFIN':	[511233,	'nill','mid50'],
      'LT':		[2939649,	'INFRA','nify'],
      'LUPIN':	[2672641,	'PHARMA','nxt50'],
      'M&M':		[519937,	'AUTO,CONSUMPTION','nify'],
      'MARUTI':	[2815745,	'AUTO','nify'],
      'M&MFIN':	[3400961,	'FINN','mid50'],
      'MANAPPURAM':	[4879617,	'nill','mid50'],
      'MARICO':	[1041153,	'FMCG,CONSUMPTION','nxt50'],
      'MCDOWELL-N':	[2674433,	'FMCG,MNC,CONSUMPTION','nxt50'],
      'MINDTREE':	[3675137,	'IT','mid50'],
      'MUTHOOTFIN':	[6054401,	'FINN','nxt50'],
      'NAM-INDIA':	[91393,		'nill','NA'],
      'NATIONALUM':	[1629185,	'METAL,PSE','NA'],
      'NMDC':		[3924993,	'METAL,PSE,COMMODITY','nxt50'],
      'NTPC':		[2977281,	'INFRA,PSE,COMMODITY','nify'],
      'ONGC':		[633601,	'INFRA,PSE,COMMODITY','nify'],
      'PETRONET':	[2905857,	'INFRA','mid50'],
      'PFC':		[3660545,	'PSE','mid50'],
      'PNB':		[2730497,	'BANK','nxt50'],
      'POWERGRID':	[3834113,	'INFRA,PSE','nify'],
      'PVR':		[3365633,	'MEDIA','NA'],
      'RBLBANK':	[4708097,	'BANK','NA'],
      'RELIANCE':	[738561,	'INFRA,COMMODITY','nify'],
      'SAIL':		[758529,	'METAL,PSE','nxt50'],
      'SBICARD':	[4600577,	'nill','nxt50'],
      'SBILIFE':	[5582849,	'FINN','nify'],
      'SBIN':		[779521,	'BANK,FINN','nify'],
      'SUNPHARMA':	[857857,	'PHARMA','nify'],
      'SUNTV':	[3431425,	'MEDIA','mid50'],
      'TATACHEM':	[871681,	'nill','NA'],
      'TATACONSUM':	[878593,	'FMCG,CONSUMPTION','nify'],
      'TATAMOTORS':	[884737,	'AUTO','nify'],
      'TATAPOWER':	[877057,	'ENERGY,INFRA,COMMODITY','mid50'],
      'TATASTEEL':	[895745,	'METAL,COMMODITY','nify'],
      'TCS':		[2953217,	'IT','nify'],
      'TECHM':	[3465729,	'IT','nify'],
      'TITAN':	[897537,	'CONSUMPTION','nify'],
      'TORNTPOWER':	[3529217,	'COMMODITY','mid50'],
      'TRENT':	[502785,	'CONSUMPTION','mid50'],
      'TVSMOTOR':	[2170625,	'AUTO','mid50'],
      'ULTRACEMCO':	[2952193,	'INFRA,COMMODITY','nify'],
      'UNIONBANK':	[2752769,	'BANK','NA'],
      'UPL':		[2889473,	'COMMODITY','nify'],
      'VEDL':		[784129,	'METAL,MNC,COMMODITY','nxt50'],
      'VOLTAS':	[951809,	'CONSUMPTION','mid50'],
      'WELCORP':	[3026177,	'METAL','NA'],
      'WIPRO':	[969473,	'IT','nify'],
      'ZEEL':		[975873,	'MEDIA,CONSUMPTION','mid50']
      }
  # Create stocks and config's for trade in stock and config table
  for stock_sym in stock_dict:
    # STORE IN STOCK TABLE
    if not models_a.STOCK.objects.filter(symbol = stock_sym).exists():
      models_a.STOCK(symbol = stock_sym, instrument_key = stock_dict[stock_sym][0], sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    # CREATE CONFIG IN FOR 15 MIN
    if not models.CONFIG_15M.objects.filter(symbol = stock_sym).exists():
      models.CONFIG_15M(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    # 15 MIN BTST
    if not models.CONFIG_15M_BTST.objects.filter(symbol = stock_sym).exists():
      models.CONFIG_15M_BTST(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    # CREATE CONFIG IN FOR 30 MIN
    if not models_30.CONFIG_30M.objects.filter(symbol = stock_sym).exists():
      models_30.CONFIG_30M(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    # 30 MIN BTST
    if not models_30.CONFIG_30M_BTST.objects.filter(symbol = stock_sym).exists():
      models_30.CONFIG_30M_BTST(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    
    # ----------------------------------- Not Ative ------------------------------------
    # CREATE CONFIG IN FOR 15 MIN TEMP
    if not models_temp.CONFIG_15M_TEMP.objects.filter(symbol = stock_sym).exists():
      models_temp.CONFIG_15M_TEMP(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    # CREATE CONFIG IN FOR 15 MIN TEMP BTST
    if not models_temp.CONFIG_15M_TEMP_BTST.objects.filter(symbol = stock_sym).exists():
      models_temp.CONFIG_15M_TEMP_BTST(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()

    # CREATE CONFIG IN FOR 15 MIN TEMP DOWN
    if not models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(symbol = stock_sym).exists():
      models_temp_down.CONFIG_15M_TEMP_DOWN(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    # CREATE CONFIG IN FOR 15 MIN TEMP BTST DOWN
    if not models_temp_down.CONFIG_15M_TEMP_BTST_DOWN.objects.filter(symbol = stock_sym).exists():
      models_temp_down.CONFIG_15M_TEMP_BTST_DOWN(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()

  # Config Model to Profit Tables
  model_name_list = ['CRS_MAIN', 'CRS_TEMP', 'CRS_TEMP_DOWN', 'CRS_30_MIN','CRS_15_MAIN_BTST','CRS_15_TEMP_BTST','CRS_30_MIN_BTST','CRS_15_TEMP_BTST_DOWN','OVER_ALL_PLACED']
  for model_name in model_name_list:
    # if model not configure in Profit Table
    if not models_a.PROFIT.objects.filter(model_name = model_name, date = datetime.now().date()).exists():
      models_a.PROFIT(model_name = model_name, date = datetime.now().date()).save()
    if not models_a.PROFIT_CONFIG.objects.filter(model_name = model_name).exists():
      models_a.PROFIT_CONFIG(model_name = model_name).save()
    else:
      model_profit_config_obj = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
      model_profit_config_obj.day_hit   = 1
      model_profit_config_obj.target    = 4000
      model_profit_config_obj.stoploss  = 0
      model_profit_config_obj.count     = 0
      model_profit_config_obj.active    = False
      model_profit_config_obj.entry     = 0
      model_profit_config_obj.save()

  # empty the trend list
  models.TREND_15M_A.objects.all().delete()
  models_temp.TREND_15M_A_TEMP.objects.all().delete()
  models_30.TREND_30M_A.objects.all().delete()
  models_temp_down.TREND_15M_A_TEMP_DOWN.objects.all().delete()

  # Update Responce as per Stock Dict
  if len(models_a.STOCK.objects.all()) == len(stock_dict):
    response.update({'stock_table': True, 'stock_len': len(models_a.STOCK.objects.all())})
  else:
    response.update({'stock_table': False, 'stock_len': len(models_a.STOCK.objects.all())})

  # Update Responce as per Data in 15 Minute
  if len(models.CONFIG_15M.objects.all()) == len(stock_dict):
    response.update({'config_table_15': True, 'config_len_15': len(models.CONFIG_15M.objects.all())})
  else:
    response.update({'config_table_15': False, 'config_len_15': len(models.CONFIG_15M.objects.all())})

  # Update Responce as per Data in 30 Minute
  if len(models_30.CONFIG_30M.objects.all()) == len(stock_dict):
    response.update({'config_table_30': True, 'config_len_30': len(models_30.CONFIG_30M.objects.all())})
  else:
    response.update({'config_table_30': False, 'config_len_30': len(models_30.CONFIG_30M.objects.all())})
  return response

def connect_to_kite_connection():
  api_key = open('algo/config/api_key.txt','r').read()
  access_token = models_a.ZERODHA_KEYS.objects.get(api_key=api_key).access_token
  try:
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
  except Exception as  e:
    pass
  return kite

@shared_task(bind=True,max_retries=3)
def ltp_of_entries(self):
  response = {'LTP': False, 'STATUS': 'NONE','ACTIVE_STOCKS': None,'LTP_30': False, 'STATUS_30': 'NONE','ACTIVE_STOCKS_30': None}
  # CALCULATE CURRENT RETURN OF ALL ACTIVE STOCKS
  if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(15,17,00):
    kite_conn_var = connect_to_kite_connection()

    # LTP CRS BTST
    if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(9,43,00):
      try:
        status, active_stocks, gain = check_ltp_btst.get_stock_ltp(kite_conn_var)
        response.update({'LTP_BTST': True, 'STATUS_BTST': status,'ACTIVE_STOCKS_BTST':active_stocks})
      except Exception as e:
        pass
      # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
      model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_15_MAIN_BTST', date = datetime.now().date())
      gain_val = []
      gain_per = []
      for val, per in gain:
        gain_val.append(val)
        gain_per.append(per)
      total_sum = sum(gain_val) + sum(models_a.CROSSOVER_15_MIN_BTST.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
      model_config_obj.current_gain           = round(total_sum,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models.ENTRY_15M_BTST.objects.all().values_list('symbol',flat=True))
      if len(models.ENTRY_15M_BTST.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models.ENTRY_15M_BTST.objects.all().values_list('symbol',flat=True))
      if total_sum > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(total_sum,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models.ENTRY_15M_BTST.objects.all().values_list('symbol',flat=True))
      if total_sum < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(total_sum,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models.ENTRY_15M_BTST.objects.all().values_list('symbol',flat=True))
      model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_15_MIN_BTST.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
      model_config_obj.save()

    # LTP CRS TEMP BTST
    if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(9,43,00):
      try:
        status, active_stocks, gain = check_ltp_temp_btst.get_stock_ltp(kite_conn_var)
        response.update({'LTP_BTST': True, 'STATUS_BTST': status,'ACTIVE_STOCKS_BTST':active_stocks})
      except Exception as e:
        pass
      # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
      model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_15_TEMP_BTST', date = datetime.now().date())
      gain_val = []
      gain_per = []
      for val, per in gain:
        gain_val.append(val)
        gain_per.append(per)
      total_sum = sum(gain_val) + sum(models_a.CROSSOVER_15_MIN_TEMP_BTST.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
      model_config_obj.current_gain           = round(total_sum,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models_temp.ENTRY_15M_TEMP_BTST.objects.all().values_list('symbol',flat=True))
      if len(models_temp.ENTRY_15M_TEMP_BTST.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models_temp.ENTRY_15M_TEMP_BTST.objects.all().values_list('symbol',flat=True))
      if total_sum > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(total_sum,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models_temp.ENTRY_15M_TEMP_BTST.objects.all().values_list('symbol',flat=True))
      if total_sum < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(total_sum,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models_temp.ENTRY_15M_TEMP_BTST.objects.all().values_list('symbol',flat=True))
      model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_15_MIN_TEMP_BTST.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
      model_config_obj.save()

    # LTP CRS TEMP BTST DOWN
    if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(9,43,00):
      try:
        status, active_stocks, gain = check_ltp_temp_btst_down.get_stock_ltp(kite_conn_var)
        response.update({'LTP_BTST_DOWN': True, 'STATUS_BTST_DOWN': status,'ACTIVE_STOCKS_BTST_DOWN':active_stocks})
      except Exception as e:
        pass
      # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
      model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_15_TEMP_BTST_DOWN', date = datetime.now().date())
      gain_val = []
      gain_per = []
      for val, per in gain:
        gain_val.append(val)
        gain_per.append(per)
      total_sum = sum(gain_val) + sum(models_a.CROSSOVER_15_MIN_TEMP_BTST_DOWN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
      model_config_obj.current_gain           = round(total_sum,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models_temp_down.ENTRY_15M_TEMP_BTST_DOWN.objects.all().values_list('symbol',flat=True))
      if len(models_temp_down.ENTRY_15M_TEMP_BTST_DOWN.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models_temp_down.ENTRY_15M_TEMP_BTST_DOWN.objects.all().values_list('symbol',flat=True))
      if total_sum > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(total_sum,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models_temp_down.ENTRY_15M_TEMP_BTST_DOWN.objects.all().values_list('symbol',flat=True))
      if total_sum < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(total_sum,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models_temp_down.ENTRY_15M_TEMP_BTST_DOWN.objects.all().values_list('symbol',flat=True))
      model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_15_MIN_TEMP_BTST_DOWN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
      model_config_obj.save()

    # LTP CRS 30 MIN BTST
    if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(9,43,00):
      try:
        status, active_stocks, gain = check_ltp_crs_30_btst.get_stock_ltp(kite_conn_var)
        response.update({'LTP_BTST': True, 'STATUS_BTST': status,'ACTIVE_STOCKS_BTST':active_stocks})
      except Exception as e:
        pass
      # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
      model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_30_MIN_BTST', date = datetime.now().date())
      gain_val = []
      gain_per = []
      for val, per in gain:
        gain_val.append(val)
        gain_per.append(per)
      total_sum = sum(gain_val) + sum(models_a.CROSSOVER_30_MIN_BTST.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
      model_config_obj.current_gain           = round(total_sum,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models_30.ENTRY_30M_BTST.objects.all().values_list('symbol',flat=True))
      if len(models_30.ENTRY_30M_BTST.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models_30.ENTRY_30M_BTST.objects.all().values_list('symbol',flat=True))
      if total_sum > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(total_sum,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models_30.ENTRY_30M_BTST.objects.all().values_list('symbol',flat=True))
      if total_sum < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(total_sum,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models_30.ENTRY_30M_BTST.objects.all().values_list('symbol',flat=True))
      model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_30_MIN_BTST.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
      model_config_obj.save()
        
    # LTP CRS
    try:
      status, active_stocks, gain = check_ltp.get_stock_ltp(kite_conn_var)
      response.update({'LTP': True, 'STATUS': status,'ACTIVE_STOCKS':active_stocks})
    except Exception as e:
      pass
    # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
    model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_MAIN', date = datetime.now().date())
    gain_val = []
    gain_per = []
    for val, per in gain:
      gain_val.append(val)
      gain_per.append(per)
    total_sum = sum(gain_val) + sum(models_a.CROSSOVER_15_MIN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
    model_config_obj.current_gain           = round(total_sum,2)
    model_config_obj.current_gain_time      = datetime.now().time()
    model_config_obj.current_gain_entry     = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
    if len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
      model_config_obj.max_entry     = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
    if total_sum > model_config_obj.top_gain:
      model_config_obj.top_gain       = round(total_sum,2)
      model_config_obj.top_gain_time  = datetime.now().time()
      model_config_obj.top_gain_entry = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
    if total_sum < model_config_obj.top_loss:
      model_config_obj.top_loss       = round(total_sum,2)
      model_config_obj.top_loss_time  = datetime.now().time()
      model_config_obj.top_loss_entry = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
    model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_15_MIN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
    model_config_obj.save()
    gain_placed_price = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date()).current_gain + sum(models.CONFIG_15M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    if len(models.CONFIG_15M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True)) != 0:
      model_config_obj   = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
      model_config_obj.current_gain           = round(gain_placed_price,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models.CONFIG_15M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if len(models.CONFIG_15M.filter(buy = True, placed = True).values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models.CONFIG_15M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(gain_placed_price,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models.CONFIG_15M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(gain_placed_price,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models.CONFIG_15M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      model_config_obj.save()

    # LTP CRS 30 MIN
    try:
      status, active_stocks, gain = check_ltp_crs_30.get_stock_ltp(kite_conn_var)
      response.update({'LTP_30': True, 'STATUS_30': status,'ACTIVE_STOCKS_30':active_stocks})
    except Exception as e:
      pass
    # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
    model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_30_MIN', date = datetime.now().date())
    gain_val = []
    gain_per = []
    for val, per in gain:
      gain_val.append(val)
      gain_per.append(per)
    total_sum = sum(gain_val) + sum(models_a.CROSSOVER_30_MIN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
    model_config_obj.current_gain           = round(total_sum,2)
    model_config_obj.current_gain_time      = datetime.now().time()
    model_config_obj.current_gain_entry     = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
    if len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
      model_config_obj.max_entry     = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
    if total_sum > model_config_obj.top_gain:
      model_config_obj.top_gain       = round(total_sum,2)
      model_config_obj.top_gain_time  = datetime.now().time()
      model_config_obj.top_gain_entry = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
    if total_sum < model_config_obj.top_loss:
      model_config_obj.top_loss       = round(total_sum,2)
      model_config_obj.top_loss_time  = datetime.now().time()
      model_config_obj.top_loss_entry = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
    model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_30_MIN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
    model_config_obj.save()
    gain_placed_price = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date()).current_gain + sum(models_30.CONFIG_30M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    if len(models_30.CONFIG_30M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True)) != 0:
      model_config_obj   = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
      model_config_obj.current_gain           = round(gain_placed_price,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models_30.CONFIG_30M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if len(models_30.CONFIG_30M.filter(buy = True, placed = True).values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models_30.CONFIG_30M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(gain_placed_price,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models_30.CONFIG_30M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(gain_placed_price,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models_30.CONFIG_30M.filter(buy = True, placed = True).values_list('symbol',flat=True))
      model_config_obj.save()

    # ----------------------------------------- NOT ACTIVE ---------------------------------
    # LTP CRS TEMP
    try:
      status, active_stocks, gain = check_ltp_temp.get_stock_ltp(kite_conn_var)
      response.update({'LTP_TEMP': True, 'STATUS_TEMP': status,'ACTIVE_STOCKS_TEMP':active_stocks})
    except Exception as e:
      pass
    # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
    model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_TEMP', date = datetime.now().date())
    gain_val = []
    gain_per = []
    for val, per in gain:
      gain_val.append(val)
      gain_per.append(per)
    total_sum = sum(gain_val) + sum(models_a.CROSSOVER_15_MIN_TEMP.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
    model_config_obj.current_gain           = round(total_sum,2)
    model_config_obj.current_gain_time      = datetime.now().time()
    model_config_obj.current_gain_entry     = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
    if len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
      model_config_obj.max_entry     = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
    if total_sum > model_config_obj.top_gain:
      model_config_obj.top_gain       = round(total_sum,2)
      model_config_obj.top_gain_time  = datetime.now().time()
      model_config_obj.top_gain_entry = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
    if total_sum < model_config_obj.top_loss:
      model_config_obj.top_loss       = round(total_sum,2)
      model_config_obj.top_loss_time  = datetime.now().time()
      model_config_obj.top_loss_entry = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
    model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_15_MIN_TEMP.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
    model_config_obj.save()
    gain_placed_price = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date()).current_gain + sum(models_temp.CONFIG_15M_TEMP.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    if len(models_temp.CONFIG_15M_TEMP.objects.filter(buy = True,placed = True).values_list('return_price', flat=True)) != 0:
      model_config_obj   = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
      model_config_obj.current_gain           = round(gain_placed_price,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models_temp.CONFIG_15M_TEMP.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if len(models_temp.CONFIG_15M_TEMP.filter(buy = True, placed = True).values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models_temp.CONFIG_15M_TEMP.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(gain_placed_price,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models_temp.CONFIG_15M_TEMP.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(gain_placed_price,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models_temp.CONFIG_15M_TEMP.filter(buy = True, placed = True).values_list('symbol',flat=True))
      model_config_obj.save()

    # LTP CRS TEMP DOWN
    try:
      status, active_stocks, gain = check_ltp_temp_down.get_stock_ltp(kite_conn_var)
      response.update({'LTP_TEMP_DOWN': True, 'STATUS_TEMP_DOWN': status,'ACTIVE_STOCKS_TEMP_DOWN':active_stocks})
    except Exception as e:
      pass
    # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
    model_config_obj = models_a.PROFIT.objects.get(model_name = 'CRS_TEMP_DOWN', date = datetime.now().date())
    gain_val = []
    gain_per = []
    for val, per in gain:
      gain_val.append(val)
      gain_per.append(per)
    total_sum = sum(gain_val) + sum(models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('difference', flat=True))
    model_config_obj.current_gain           = round(total_sum,2)
    model_config_obj.current_gain_time      = datetime.now().time()
    model_config_obj.current_gain_entry     = len(models_temp_down.ENTRY_15M_TEMP_DOWN.objects.all().values_list('symbol',flat=True))
    if len(models_temp_down.ENTRY_15M_TEMP_DOWN.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
      model_config_obj.max_entry     = len(models_temp_down.ENTRY_15M_TEMP_DOWN.objects.all().values_list('symbol',flat=True))
    if total_sum > model_config_obj.top_gain:
      model_config_obj.top_gain       = round(total_sum,2)
      model_config_obj.top_gain_time  = datetime.now().time()
      model_config_obj.top_gain_entry = len(models_temp_down.ENTRY_15M_TEMP_DOWN.objects.all().values_list('symbol',flat=True))
    if total_sum < model_config_obj.top_loss:
      model_config_obj.top_loss       = round(total_sum,2)
      model_config_obj.top_loss_time  = datetime.now().time()
      model_config_obj.top_loss_entry = len(models_temp_down.ENTRY_15M_TEMP_DOWN.objects.all().values_list('symbol',flat=True))
    model_config_obj.p_l = sum(gain_per) + sum(models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(created_on = date.today(),indicate = 'Exit').values_list('profit', flat=True))
    model_config_obj.save()
    gain_placed_price = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date()).current_gain + sum(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    if len(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True,placed = True).values_list('return_price', flat=True)) != 0:
      model_config_obj   = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
      model_config_obj.current_gain           = round(gain_placed_price,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      model_config_obj.current_gain_entry     = len(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if len(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol',flat=True)) > model_config_obj.max_entry:
        model_config_obj.max_entry     = len(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(gain_placed_price,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = len(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol',flat=True))
      if gain_placed_price < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(gain_placed_price,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = len(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol',flat=True))
      model_config_obj.save()

    # --------------------------------- FREEZE Profit at each LTP ------------------------
    crs_main_entry_list = models.CONFIG_15M.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    crs_temp_entry_list = models_temp.CONFIG_15M_TEMP.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    crs_30_entry_list   = models_30.CONFIG_30M.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    crs_down_entry_list = models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    total_placed_entry = len(crs_main_entry_list) + len(crs_temp_entry_list) + len(crs_30_entry_list) + len(crs_down_entry_list)

    model_config_obj               = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
    model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = 'OVER_ALL_PLACED')
    if model_config_obj.current_gain > model_profit_config_obj.target:
      model_profit_config_obj.stoploss  = model_profit_config_obj.target - 500
      model_profit_config_obj.target    = model_profit_config_obj.target + 500
      model_profit_config_obj.count     += 1
      model_profit_config_obj.active    = True
    elif model_profit_config_obj.active is True:
      if model_config_obj.current_gain < model_profit_config_obj.stoploss:
        # FREEZE PROFIT
        gain_main, p_l_main = freeze_all_15.freeze_all(crs_main_entry_list,kite_conn_var)
        gain_temp, p_l_temp = freeze_all_15_temp.freeze_all(crs_temp_entry_list,kite_conn_var)
        gain_30, p_l_30 = freeze_all_30.freeze_all(crs_30_entry_list,kite_conn_var)
        gain_down, p_l_down = freeze_all_15_down.freeze_all(crs_down_entry_list,kite_conn_var)
        gain = gain_main + gain_temp + gain_30 + gain_down
        p_l  = p_l_main + p_l_temp + p_l_30 + p_l_down
        models_a.FREEZE_PROFIT(model_name = 'OVER_ALL_PLACED', indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = total_placed_entry, day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
        model_profit_config_obj.day_hit   += 1
        model_profit_config_obj.target    = 4000
        model_profit_config_obj.stoploss  = 0
        model_profit_config_obj.count     = 0
        model_profit_config_obj.active    = False
        model_profit_config_obj.entry     = 0
        # PROFIT TABLE
        model_config_obj.current_gain           = 0
        model_config_obj.current_gain_entry     = 0
        model_config_obj.top_gain               = 0
        model_config_obj.top_gain_entry         = 0
        model_config_obj.top_loss               = 0
        model_config_obj.top_loss_entry         = 0
        model_config_obj.p_l                    = 0
    model_profit_config_obj.save()
    model_config_obj.save()

    # model_name_list = ['CRS_MAIN', 'CRS_30_MIN', 'CRS_TEMP','CRS_15_MAIN_BTST','CRS_15_TEMP_BTST','CRS_30_MIN_BTST']
    # for index, model_name in enumerate(model_name_list):
    #   # ---------------------------- FREEZE THE STOCK AT IT LIVE GAIN --------------------
    #   if index == 0:
    #     model_config_obj               = models_a.PROFIT.objects.get(model_name = model_name, date = datetime.now().date())
    #     model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
    #     entry_list                     = models.ENTRY_15M.objects.all().values_list('symbol',flat=True)
    #     if model_config_obj.current_gain > model_profit_config_obj.target:
    #       model_profit_config_obj.stoploss  = model_profit_config_obj.target - 500
    #       model_profit_config_obj.target    = model_profit_config_obj.target + 500
    #       model_profit_config_obj.count     += 1
    #       model_profit_config_obj.active    = True
    #     elif model_profit_config_obj.active is True:
    #       if model_config_obj.current_gain < model_profit_config_obj.stoploss:
    #         # FREEZE PROFIT
    #         gain, p_l = freeze_all_15.freeze_all(entry_list,kite_conn_var)
    #         models_a.FREEZE_PROFIT(model_name = model_name, indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = len(entry_list), day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
    #         model_profit_config_obj.day_hit   += 1
    #         model_profit_config_obj.target    = 3000
    #         model_profit_config_obj.stoploss  = 0
    #         model_profit_config_obj.count     = 0
    #         model_profit_config_obj.active    = False
    #         model_profit_config_obj.entry     = 0
    #         # PROFIT TABLE
    #         model_config_obj.current_gain           = 0
    #         model_config_obj.current_gain_entry     = 0
    #         model_config_obj.top_gain               = 0
    #         model_config_obj.top_gain_entry         = 0
    #         model_config_obj.top_loss               = 0
    #         model_config_obj.top_loss_entry         = 0
    #     model_profit_config_obj.save()
    #     model_config_obj.save()
    #   if index == 1:
    #     model_config_obj               = models_a.PROFIT.objects.get(model_name = model_name, date = datetime.now().date())
    #     model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
    #     entry_list                     = models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True)
    #     if model_config_obj.current_gain > model_profit_config_obj.target:
    #       model_profit_config_obj.stoploss  = model_profit_config_obj.target - 400
    #       model_profit_config_obj.target    = model_profit_config_obj.target + 500
    #       model_profit_config_obj.count     += 1
    #       model_profit_config_obj.active    = True
    #     elif model_profit_config_obj.active is True:
    #       if model_config_obj.current_gain < model_profit_config_obj.stoploss:
    #         # FREEZE PROFIT
    #         gain, p_l = freeze_all_30.freeze_all(entry_list,kite_conn_var)
    #         models_a.FREEZE_PROFIT(model_name = model_name, indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = len(entry_list), day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
    #         model_profit_config_obj.day_hit   += 1
    #         model_profit_config_obj.target    = 5000
    #         model_profit_config_obj.stoploss  = 0
    #         model_profit_config_obj.count     = 0
    #         model_profit_config_obj.active    = False
    #         model_profit_config_obj.entry     = 0
    #         # PROFIT TABLE
    #         model_config_obj.current_gain           = 0
    #         model_config_obj.current_gain_entry     = 0
    #         model_config_obj.top_gain               = 0
    #         model_config_obj.top_gain_entry         = 0
    #         model_config_obj.top_loss               = 0
    #         model_config_obj.top_loss_entry         = 0
    #     model_profit_config_obj.save()
    #     model_config_obj.save()
    #   if index == 2:
    #     model_config_obj               = models_a.PROFIT.objects.get(model_name = model_name, date = datetime.now().date())
    #     model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
    #     entry_list                     = models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True)
    #     if model_config_obj.current_gain > model_profit_config_obj.target:
    #       model_profit_config_obj.stoploss  = model_profit_config_obj.target - 400
    #       model_profit_config_obj.target    = model_profit_config_obj.target + 500
    #       model_profit_config_obj.count     += 1
    #       model_profit_config_obj.active    = True
    #     elif model_profit_config_obj.active is True:
    #       if model_config_obj.current_gain < model_profit_config_obj.stoploss:
    #         # FREEZE PROFIT
    #         gain, p_l = freeze_all_15_temp.freeze_all(entry_list,kite_conn_var)
    #         models_a.FREEZE_PROFIT(model_name = model_name, indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = len(entry_list), day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
    #         model_profit_config_obj.day_hit   += 1
    #         model_profit_config_obj.target    = 5000
    #         model_profit_config_obj.stoploss  = 0
    #         model_profit_config_obj.count     = 0
    #         model_profit_config_obj.active    = False
    #         model_profit_config_obj.entry     = 0
    #         # PROFIT TABLE
    #         model_config_obj.current_gain           = 0
    #         model_config_obj.current_gain_entry     = 0
    #         model_config_obj.top_gain               = 0
    #         model_config_obj.top_gain_entry         = 0
    #         model_config_obj.top_loss               = 0
    #         model_config_obj.top_loss_entry         = 0
    #     model_profit_config_obj.save()
    #     model_config_obj.save()
    #   if index == 3:
    #     model_config_obj               = models_a.PROFIT.objects.get(model_name = model_name, date = datetime.now().date())
    #     model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
    #     entry_list                     = models.ENTRY_15M_BTST.objects.all().values_list('symbol',flat=True)
    #     if model_config_obj.current_gain > model_profit_config_obj.target:
    #       model_profit_config_obj.stoploss  = model_profit_config_obj.target - 400
    #       model_profit_config_obj.target    = model_profit_config_obj.target + 500
    #       model_profit_config_obj.count     += 1
    #       model_profit_config_obj.active    = True
    #     elif model_profit_config_obj.active is True:
    #       if model_config_obj.current_gain < model_profit_config_obj.stoploss:
    #         # FREEZE PROFIT
    #         gain, p_l = freeze_all_15_btst.freeze_all(entry_list,kite_conn_var)
    #         models_a.FREEZE_PROFIT(model_name = model_name, indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = len(entry_list), day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
    #         model_profit_config_obj.day_hit   += 1
    #         model_profit_config_obj.target    = 5000
    #         model_profit_config_obj.stoploss  = 0
    #         model_profit_config_obj.count     = 0
    #         model_profit_config_obj.active    = False
    #         model_profit_config_obj.entry     = 0
    #         # PROFIT TABLE
    #         model_config_obj.current_gain           = 0
    #         model_config_obj.current_gain_entry     = 0
    #         model_config_obj.top_gain               = 0
    #         model_config_obj.top_gain_entry         = 0
    #         model_config_obj.top_loss               = 0
    #         model_config_obj.top_loss_entry         = 0
    #     model_profit_config_obj.save()
    #     model_config_obj.save()
    #   if index == 4:
    #     model_config_obj               = models_a.PROFIT.objects.get(model_name = model_name, date = datetime.now().date())
    #     model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
    #     entry_list                     = models_temp.ENTRY_15M_TEMP_BTST.objects.all().values_list('symbol',flat=True)
    #     if model_config_obj.current_gain > model_profit_config_obj.target:
    #       model_profit_config_obj.stoploss  = model_profit_config_obj.target - 400
    #       model_profit_config_obj.target    = model_profit_config_obj.target + 500
    #       model_profit_config_obj.count     += 1
    #       model_profit_config_obj.active    = True
    #     elif model_profit_config_obj.active is True:
    #       if model_config_obj.current_gain < model_profit_config_obj.stoploss:
    #         # FREEZE PROFIT
    #         gain, p_l = freeze_all_15_temp_btst.freeze_all(entry_list,kite_conn_var)
    #         models_a.FREEZE_PROFIT(model_name = model_name, indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = len(entry_list), day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
    #         model_profit_config_obj.day_hit   += 1
    #         model_profit_config_obj.target    = 5000
    #         model_profit_config_obj.stoploss  = 0
    #         model_profit_config_obj.count     = 0
    #         model_profit_config_obj.active    = False
    #         model_profit_config_obj.entry     = 0
    #         # PROFIT TABLE
    #         model_config_obj.current_gain           = 0
    #         model_config_obj.current_gain_entry     = 0
    #         model_config_obj.top_gain               = 0
    #         model_config_obj.top_gain_entry         = 0
    #         model_config_obj.top_loss               = 0
    #         model_config_obj.top_loss_entry         = 0
    #     model_profit_config_obj.save()
    #     model_config_obj.save()
    #   if index == 5:
    #     model_config_obj               = models_a.PROFIT.objects.get(model_name = model_name, date = datetime.now().date())
    #     model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
    #     entry_list                     = models_30.ENTRY_30M_BTST.objects.all().values_list('symbol',flat=True)
    #     if model_config_obj.current_gain > model_profit_config_obj.target:
    #       model_profit_config_obj.stoploss  = model_profit_config_obj.target - 400
    #       model_profit_config_obj.target    = model_profit_config_obj.target + 500
    #       model_profit_config_obj.count     += 1
    #       model_profit_config_obj.active    = True
    #     elif model_profit_config_obj.active is True:
    #       if model_config_obj.current_gain < model_profit_config_obj.stoploss:
    #         # FREEZE PROFIT
    #         gain, p_l = freeze_all_30_btst.freeze_all(entry_list,kite_conn_var)
    #         models_a.FREEZE_PROFIT(model_name = model_name, indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = len(entry_list), day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
    #         model_profit_config_obj.day_hit   += 1
    #         model_profit_config_obj.target    = 5000
    #         model_profit_config_obj.stoploss  = 0
    #         model_profit_config_obj.count     = 0
    #         model_profit_config_obj.active    = False
    #         model_profit_config_obj.entry     = 0
    #         # PROFIT TABLE
    #         model_config_obj.current_gain           = 0
    #         model_config_obj.current_gain_entry     = 0
    #         model_config_obj.top_gain               = 0
    #         model_config_obj.top_gain_entry         = 0
    #         model_config_obj.top_loss               = 0
    #         model_config_obj.top_loss_entry         = 0
    #     model_profit_config_obj.save()
    #     model_config_obj.save()

  # CALCULATE THE RETURN OF ALL MODELS
  elif datetime.now().time() >= time(15,17,00) and datetime.now().time() < time(15,30,00):
    model_name_list = ['CRS_MAIN', 'CRS_TEMP', 'CRS_30_MIN','CRS_15_MAIN_BTST','CRS_15_TEMP_BTST','CRS_30_MIN_BTST', 'CRS_TEMP_DOWN','CRS_15_TEMP_BTST_DOWN']
    for ind, m_name in enumerate(model_name_list):
      models_a.PROFIT_CONFIG.objects.filter(model_name = m_name).update(zerodha_entry = False)
      model_config_obj = models_a.PROFIT.objects.get(model_name = m_name, date = datetime.now().date())
      if ind == 0:
        profit = models_a.CROSSOVER_15_MIN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_15_MIN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 1:
        profit = models_a.CROSSOVER_15_MIN_TEMP.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_15_MIN_TEMP.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 2:
        profit = models_a.CROSSOVER_30_MIN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_30_MIN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 3:
        profit = models_a.CROSSOVER_15_MIN_BTST.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_15_MIN_BTST.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 4:
        profit = models_a.CROSSOVER_15_MIN_TEMP_BTST.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_15_MIN_TEMP_BTST.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 5:
        profit = models_a.CROSSOVER_30_MIN_BTST.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_30_MIN_BTST.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 6:
        profit = models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 7:
        profit = models_a.CROSSOVER_15_MIN_TEMP_BTST_DOWN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_15_MIN_TEMP_BTST_DOWN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      model_config_obj.save()

    response.update({'LTP': True, 'STATUS': 'SQUARED OFF','LTP_30_MIN': True, 'STATUS_30_MIN': 'ALL STOCKS ARE SQUARED OFF.'})

  else:
    response.update({'LTP': True, 'STATUS': 'MARKET IS CLOSED','LTP': True, 'STATUS': 'MARKET IS CLOSED.','LTP_30_MIN': True, 'STATUS_30_MIN': 'MARKET IS CLOSED.'})
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_15_MIN(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # Initialize Kite Connections
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15minute',5,60,55,16,8,'30minute',30,14,14,14]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_CRS_15_MIN.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))})
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_30_MIN(self):
  response = {'CRS': False, 'STATUS': 'NONE'}
  sleep(901)

  # Initialize Kite Connections
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['30minute',5,60,55,15,7,'60minute',30,14,14,14]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_CRS_30_MIN.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))})
  return response

# ------------------------------------------- Not Active ---------------------------------------
@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_15_MIN_TEMP(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # Initialize Kite Connections
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15minute',5,60,55,16,8,'30minute',30,14,14,14]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_CRS_temp.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))})
  return response

@shared_task(bind=True,max_retries=3)
def DOWN_CROSS_OVER_RUNS_15_MIN_TEMP(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

  # Initialize Kite Connections
  kite_conn_var       = connect_to_kite_connection()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['15minute',5,60,55,16,8,'30minute',30,14,14,14]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_DOWN_CRS_temp.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_temp_down.ENTRY_15M_TEMP_DOWN.objects.all().values_list('symbol',flat=True))})
  return response
