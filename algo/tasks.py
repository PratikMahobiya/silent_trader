from datetime import date, datetime, time
from kiteconnect import KiteConnect

from Model_15M import models
from Model_30M import models as models_30
from . import models as models_a
from . import check_ltp
from . import check_ltp_crs_30
from celery import shared_task
from .CROSSOVER_15_MIN.utils import backbone as backbone_CRS_15_MIN
from .CROSSOVER_30_MIN.utils import backbone as backbone_CRS_30_MIN

# -------------------- Not ------------------
from Model_15_temp import models as models_temp
from Model_30M_temp import models as models_30_temp
from . import check_ltp_temp
from . import check_ltp_crs_30_temp
from .CROSSOVER_15_MIN_temp.utils import backbone as backbone_CRS_temp
from .CROSSOVER_30_MIN_temp.utils import backbone as backbone_CRS_30_temp

@shared_task(bind=True,max_retries=3)
# initial_setup on DATABASE -------------------------------------
def get_stocks_configs(self):
  response = {'stock_table': False, 'config_table_15': False, 'config_table_5': False}
  # Stock dict
  stock_dict = {
    'AARTIIND':	[1793,		'COMMODITY'],
    'ABFRL':	[7707649,	'nill'],
    'ACC':		[5633,		'INFRA,COMMODITY'],
    'ADANIENT':	[6401,		'METAL'],
    'ADANIGREEN':	[912129,	'ENERGY,COMMODITY'],
    'ADANIPORTS':	[3861249,	'INFRA'],
    'AMBUJACEM':	[325121,	'INFRA,MNC,COMMODITY'],
    'APLLTD':	[6483969,	'nill'],
    'APOLLOTYRE':	[41729,		'nill'],
    'ASHOKLEY':	[54273,		'AUTO,INFRA,MNC'],
    'ASIANPAINT':	[60417,		'CONSUMPTION'],
    'AUROPHARMA':	[70401,		'PHARMA'],
    'AXISBANK':	[1510401,	'BANK,FINN'],
    'BAJAJ-AUTO':	[4267265,	'AUTO,CONSUMPTION'],
    'BANDHANBNK':	[579329,	'BANK'],
    'BANKBARODA':	[1195009,	'BANK'],
    'BANKINDIA':	[1214721,	'BANK'],
    'BATAINDIA':	[94977,		'MNC'],
    'BEL':		[98049,		'PSE'],
    'BERGEPAINT':	[103425,	'CONSUMPTION'],
    'BHARATFORG':	[108033,	'AUTO'],
    'BHARTIARTL':	[2714625,	'INFRA,CONSUMPTION'],
    'BHEL':		[112129,	'PSE'],
    'BIOCON':	[2911489,	'PHARMA'],
    'BPCL':		[134657,	'ENERGY,INFRA,PSE,COMMODITY'],
    'BRITANNIA':	[140033,	'FMCG,MNC,CONSUMPTION'],
    'CADILAHC':	[2029825,	'PHARMA'],
    'CANBK':	[2763265,	'BANK'],
    'CASTROLIND':	[320001,	'MNC'],
    'CHOLAFIN':	[175361,	'FINN'],
    'CIPLA':	[177665,	'PHARMA'],
    'COALINDIA':	[5215745,	'METAL,PSE,COMMODITY'],
    'COFORGE':	[2955009,	'IT'],
    'COLPAL':	[3876097,	'FMCG,MNC,CONSUMPTION'],
    'CONCOR':	[1215745,	'INFRA,PSE'],
    'CUB':		[1459457,	'nill'],
    'CUMMINSIND':	[486657,	'MNC'],
    'DABUR':	[197633,	'FMCG,CONSUMPTION'],
    'DIVISLAB':	[2800641,	'PHARMA'],
    'DLF':		[3771393,	'INFRA'],
    'DMART':	[5097729,	'CONSUMPTION'],
    'DRREDDY':	[225537,	'PHARMA'],
    'EMAMILTD':	[3460353,	'FMCG'],
    'ESCORTS':	[245249,	'nill'],
    'EXIDEIND':	[173057,	'AUTO,INFRA'],
    'FEDERALBNK':	[261889,	'BANK'],
    'GAIL':		[1207553,	'ENERGY,INFRA,PSE'],
    'GMRINFRA':	[3463169,	'nill'],
    'GODREJCP':	[2585345,	'FMCG,CONSUMPTION'],
    'GODREJPROP':	[4576001,	'nill'],
    'GRANULES':	[3039233,	'nill'],
    'GRASIM':	[315393,	'INFRA,COMMODITY'],
    'HAVELLS':	[2513665,	'CONSUMPTION'],
    'HCLTECH':	[1850625,	'IT'],
    'HDFC':		[340481,	'FINN'],
    'HDFCBANK':	[341249,	'BANK,FINN'],
    'HDFCLIFE':	[119553,	'FINN'],
    'HINDALCO':	[348929,	'METAL'],
    'HINDPETRO':	[359937,	'ENERGY,INFRA,PSE,COMMODITY'],
    'HINDUNILVR':	[356865,	'FMCG,MNC,CONSUMPTION'],
    'HINDZINC':	[364545,	'METAL,COMMODITY'],
    'IBULHSGFIN':	[7712001,	'nill'],
    'ICICIBANK':	[1270529,	'BANK,FINN'],
    'IDFCFIRSTB':	[2863105,	'BANK'],
    'IGL':		[2883073,	'INFRA'],
    'INDIANB':	[3663105,	'BANK'],
    'INDUSINDBK':	[1346049,	'BANK'],
    'INDUSTOWER':	[7458561,	'INFRA'],
    'INFY':		[408065,	'IT'],
    'IOC':		[415745,	'ENERGY,INFRA,PSE,COMMODITY'],
    'IRCTC':	[3484417,	'PSE'],
    'ITC':		[424961,	'FMCG,CONSUMPTION'],
    'JINDALSTEL':	[1723649,	'METAL,COMMODITY'],
    'JSWSTEEL':	[3001089,	'METAL,COMMODITY'],
    'JUBLFOOD':	[4632577,	'FMCG,CONSUMPTION'],
    'KOTAKBANK':	[492033,	'BANK,FINN'],
    'LICHSGFIN':	[511233,	'nill'],
    'LT':		[2939649,	'INFRA'],
    'LUPIN':	[2672641,	'PHARMA'],
    'M&M':		[519937,	'AUTO,CONSUMPTION'],
    'M&MFIN':	[3400961,	'FINN'],
    'MANAPPURAM':	[4879617,	'nill'],
    'MARICO':	[1041153,	'FMCG,CONSUMPTION'],
    'MCDOWELL-N':	[2674433,	'FMCG,MNC,CONSUMPTION'],
    'MINDTREE':	[3675137,	'IT'],
    'MUTHOOTFIN':	[6054401,	'FINN'],
    'NAM-INDIA':	[91393,		'nill'],
    'NATIONALUM':	[1629185,	'METAL,PSE'],
    'NETWORK18':	[3612417,	'MEDIA'],
    'NMDC':		[3924993,	'METAL,PSE,COMMODITY'],
    'NTPC':		[2977281,	'ENERGY,INFRA,PSE,COMMODITY'],
    'ONGC':		[633601,	'ENERGY,INFRA,PSE,COMMODITY'],
    'PETRONET':	[2905857,	'INFRA'],
    'PFC':		[3660545,	'PSE'],
    'PNB':		[2730497,	'BANK'],
    'POWERGRID':	[3834113,	'ENERGY,INFRA,PSE'],
    'PVR':		[3365633,	'MEDIA'],
    'RBLBANK':	[4708097,	'BANK'],
    'RELIANCE':	[738561,	'ENERGY,INFRA,COMMODITY'],
    'SAIL':		[758529,	'METAL,PSE'],
    'SBICARD':	[4600577,	'nill'],
    'SBILIFE':	[5582849,	'FINN'],
    'SBIN':		[779521,	'BANK,FINN'],
    'SUNPHARMA':	[857857,	'PHARMA'],
    'SUNTV':	[3431425,	'MEDIA'],
    'TATACHEM':	[871681,	'nill'],
    'TATACONSUM':	[878593,	'FMCG,CONSUMPTION'],
    'TATAMOTORS':	[884737,	'AUTO'],
    'TATAPOWER':	[877057,	'ENERGY,INFRA,COMMODITY'],
    'TATASTEEL':	[895745,	'METAL,COMMODITY'],
    'TCS':		[2953217,	'IT'],
    'TECHM':	[3465729,	'IT'],
    'TITAN':	[897537,	'CONSUMPTION'],
    'TORNTPOWER':	[3529217,	'COMMODITY'],
    'TRENT':	[502785,	'CONSUMPTION'],
    'TVSMOTOR':	[2170625,	'AUTO'],
    'ULTRACEMCO':	[2952193,	'INFRA,COMMODITY'],
    'UNIONBANK':	[2752769,	'BANK'],
    'UPL':		[2889473,	'COMMODITY'],
    'VEDL':		[784129,	'METAL,MNC,COMMODITY'],
    'VOLTAS':	[951809,	'CONSUMPTION'],
    'WELCORP':	[3026177,	'METAL'],
    'WIPRO':	[969473,	'IT'],
    'ZEEL':		[975873,	'MEDIA,CONSUMPTION'],
  }
  # Create stocks and config's for trade in stock and config table
  for stock_sym in stock_dict:
    # STORE IN STOCK TABLE
    if not models_a.STOCK.objects.filter(symbol = stock_sym).exists():
      models_a.STOCK(symbol = stock_sym, instrument_key = stock_dict[stock_sym][0], sector = stock_dict[stock_sym][1]).save()
    # CREATE CONFIG IN FOR 15 MIN
    if not models.CONFIG_15M.objects.filter(symbol = stock_sym).exists():
      models.CONFIG_15M(symbol = stock_sym, sector = stock_dict[stock_sym][1]).save()
    # CREATE CONFIG IN FOR 30 MIN
    if not models_30.CONFIG_30M.objects.filter(symbol = stock_sym).exists():
      models_30.CONFIG_30M(symbol = stock_sym, sector = stock_dict[stock_sym][1]).save()
    
    # ----------------------------------- Not Ative ------------------------------------
    # CREATE CONFIG IN FOR 15 MIN TEMP
    if not models_temp.CONFIG_15M_TEMP.objects.filter(symbol = stock_sym).exists():
      models_temp.CONFIG_15M_TEMP(symbol = stock_sym, sector = stock_dict[stock_sym][1]).save()
    # CREATE CONFIG IN FOR 30 MIN TEMP
    if not models_30_temp.CONFIG_30M_TEMP.objects.filter(symbol = stock_sym).exists():
      models_30_temp.CONFIG_30M_TEMP(symbol = stock_sym, sector = stock_dict[stock_sym][1]).save()

  # Config Model to Profit Tables
  model_name_list = ['CRS_MAIN', 'CRS_TEMP', 'CRS_30_MIN', 'CRS_30_MIN_TEMP']
  for model_name in model_name_list:
    # if model not configure in Profit Table
    if not models_a.PROFIT.objects.filter(model_name = model_name, date = datetime.now().date()).exists():
      models_a.PROFIT(model_name = model_name, date = datetime.now().date()).save()
    # else:
    #   model_config_obj = models_a.PROFIT.objects.filter(model_name = model_name, date = datetime.now().date())
    #   model_config_obj.top_gain = 0
    #   model_config_obj.top_gain_time = datetime.now()
    #   model_config_obj.top_loss = 0
    #   model_config_obj.top_loss_time = datetime.now()
    #   model_config_obj.current_gain = 0
    #   model_config_obj.current_gain_time = datetime.now()
    #   model_config_obj.save()

  # empty the trend list
  models.TREND_15M_A.objects.all().delete()
  models_temp.TREND_15M_A_TEMP.objects.all().delete()
  model_30_entry_list = models_30.ENTRY_30M.objects.all().values_list('symbol', flat=True)
  model_30_trend_list = models_30.TREND_30M_A.objects.all().values_list('symbol', flat=True)
  for stock in model_30_trend_list:
    if stock not in model_30_entry_list:
      models_30.TREND_30M_A.objects.filter(symbol = stock).delete()
  model_30_temp_entry_list = models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol', flat=True)
  model_30_temp_trend_list = models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol', flat=True)
  for stock in model_30_temp_trend_list:
    if stock not in model_30_temp_entry_list:
      models_30_temp.TREND_30M_A_TEMP.objects.filter(symbol = stock).delete()

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
def Clear_Transactions(self):
  response = {'TRANSACTION': True, 'STATUS': 'NONE'}
  models_a.CROSSOVER_15_MIN.objects.all().delete()
  models_a.CROSSOVER_15_MIN_TEMP.objects.all().delete()
  Number_of_trans = []
  Number_of_trans.append(len(models_a.CROSSOVER_15_MIN.objects.all()))
  Number_of_trans.append(len(models_a.CROSSOVER_15_MIN_TEMP.objects.all()))
  response.update({'N0_of_trans':Number_of_trans,'STATUS':'CLEARED'})
  return response

@shared_task(bind=True,max_retries=3)
def ltp_of_entries(self):
  response = {'LTP': False, 'STATUS': 'NONE','ACTIVE_STOCKS': None,'LTP_30': False, 'STATUS_30': 'NONE','ACTIVE_STOCKS_30': None}
  model_name_dict = {}
  if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(15,17,00):
    kite_conn_var = connect_to_kite_connection()
    
    # LTP CRS
    try:
      status, active_stocks, gain = check_ltp.get_stock_ltp(kite_conn_var)
      model_name_dict.update({'CRS_MAIN': gain})
      response.update({'LTP': True, 'STATUS': status,'ACTIVE_STOCKS':active_stocks})
    except Exception as e:
      pass

    # LTP CRS 30 MIN
    try:
      status, active_stocks, gain = check_ltp_crs_30.get_stock_ltp(kite_conn_var)
      model_name_dict.update({'CRS_30_MIN': gain})
      response.update({'LTP_30': True, 'STATUS_30': status,'ACTIVE_STOCKS_30':active_stocks})
    except Exception as e:
      pass

    # ----------------------------------------- NOT ACTIVE ---------------------------------
    # LTP CRS TEMP
    try:
      status, active_stocks, gain = check_ltp_temp.get_stock_ltp(kite_conn_var)
      model_name_dict.update({'CRS_TEMP': gain})
      response.update({'LTP_TEMP': True, 'STATUS_TEMP': status,'ACTIVE_STOCKS_TEMP':active_stocks})
    except Exception as e:
      pass

    # LTP CRS 30 MIN TEMP
    try:
      status, active_stocks, gain = check_ltp_crs_30_temp.get_stock_ltp(kite_conn_var)
      model_name_dict.update({'CRS_30_MIN_TEMP': gain})
      response.update({'LTP_30_TEMP': True, 'STATUS_30_TEMP': status,'ACTIVE_STOCKS_30_TEMP':active_stocks})
    except Exception as e:
      pass
    
    # --------------------------------- Calculate Profit at each LTP ------------------------
    for index, model_name in enumerate(model_name_dict):
      model_config_obj = models_a.PROFIT.objects.get(model_name = model_name, date = datetime.now().date())
      # -------------------------------- CURRENT/ACTUAL LIVE GAIN -------------------------
      if index == 0:
        actual_gain_list  = models_a.CROSSOVER_15_MIN.objects.filter(indicate = 'Exit').values_list('difference', flat=True)
        total_sum = sum(actual_gain_list) + sum(model_name_dict[model_name])
        model_config_obj.current_gain           = round(total_sum,2)
        model_config_obj.current_gain_time      = datetime.now()
        model_config_obj.current_gain_entry     = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
        if len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
          model_config_obj.max_entry     = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
        if total_sum > model_config_obj.top_gain:
          model_config_obj.top_gain       = round(total_sum,2)
          model_config_obj.top_gain_time  = datetime.now()
          model_config_obj.top_gain_entry = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
        if total_sum < model_config_obj.top_loss:
          model_config_obj.top_loss       = round(total_sum,2)
          model_config_obj.top_loss_time  = datetime.now()
          model_config_obj.top_loss_entry = len(models.ENTRY_15M.objects.all().values_list('symbol',flat=True))
      if index == 1:
        actual_gain_list  = models_a.CROSSOVER_30_MIN.objects.filter(indicate = 'Exit').values_list('difference', flat=True)
        total_sum = sum(actual_gain_list) + sum(model_name_dict[model_name])
        model_config_obj.current_gain           = round(total_sum,2)
        model_config_obj.current_gain_time      = datetime.now()
        model_config_obj.current_gain_entry     = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
        if len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
          model_config_obj.max_entry     = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
        if total_sum > model_config_obj.top_gain:
          model_config_obj.top_gain       = round(total_sum,2)
          model_config_obj.top_gain_time  = datetime.now()
          model_config_obj.top_gain_entry = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
        if total_sum < model_config_obj.top_loss:
          model_config_obj.top_loss       = round(total_sum,2)
          model_config_obj.top_loss_time  = datetime.now()
          model_config_obj.top_loss_entry = len(models_30.ENTRY_30M.objects.all().values_list('symbol',flat=True))
      if index == 2:
        actual_gain_list  = models_a.CROSSOVER_15_MIN_TEMP.objects.filter(indicate = 'Exit').values_list('difference', flat=True)
        total_sum = sum(actual_gain_list) + sum(model_name_dict[model_name])
        model_config_obj.current_gain           = round(total_sum,2)
        model_config_obj.current_gain_time      = datetime.now()
        model_config_obj.current_gain_entry     = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
        if len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
          model_config_obj.max_entry     = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
        if total_sum > model_config_obj.top_gain:
          model_config_obj.top_gain       = round(total_sum,2)
          model_config_obj.top_gain_time  = datetime.now()
          model_config_obj.top_gain_entry = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
        if total_sum < model_config_obj.top_loss:
          model_config_obj.top_loss       = round(total_sum,2)
          model_config_obj.top_loss_time  = datetime.now()
          model_config_obj.top_loss_entry = len(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))
      if index == 3:
        actual_gain_list  = models_a.CROSSOVER_30_MIN_TEMP.objects.filter(indicate = 'Exit').values_list('difference', flat=True)
        total_sum = sum(actual_gain_list) + sum(model_name_dict[model_name])
        model_config_obj.current_gain           = round(total_sum,2)
        model_config_obj.current_gain_time      = datetime.now()
        model_config_obj.current_gain_entry     = len(models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol',flat=True))
        if len(models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol',flat=True)) > model_config_obj.max_entry:
          model_config_obj.max_entry     = len(models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol',flat=True))
        if total_sum > model_config_obj.top_gain:
          model_config_obj.top_gain       = round(total_sum,2)
          model_config_obj.top_gain_time  = datetime.now()
          model_config_obj.top_gain_entry = len(models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol',flat=True))
        if total_sum < model_config_obj.top_loss:
          model_config_obj.top_loss       = round(total_sum,2)
          model_config_obj.top_loss_time  = datetime.now()
          model_config_obj.top_loss_entry = len(models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol',flat=True))
      model_config_obj.save()

  elif datetime.now().time() >= time(15,17,00) and datetime.now().time() < time(15,30,00):
    model_name_list = ['CRS_MAIN', 'CRS_TEMP', 'CRS_30_MIN', 'CRS_30_MIN_TEMP']
    for ind, m_name in enumerate(model_name_list):
      model_config_obj = models_a.PROFIT.objects.get(model_name = m_name, date = datetime.now().date())
      if ind == 0:
        profit = models_a.CROSSOVER_15_MIN.objects.filter(indicate = 'Exit').values_list('profit',flat=True)
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = sum(profit)
      if ind == 1:
        profit = models_a.CROSSOVER_15_MIN_TEMP.objects.filter(indicate = 'Exit').values_list('profit',flat=True)
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = sum(profit)
      if ind == 2:
        profit = models_a.CROSSOVER_30_MIN.objects.filter(indicate = 'Exit').values_list('profit',flat=True)
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = sum(profit)
      if ind == 3:
        profit = models_a.CROSSOVER_30_MIN_TEMP.objects.filter(indicate = 'Exit').values_list('profit',flat=True)
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = sum(profit)
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
  intervals      = ['15minute',5,60,55,18,8,'30minute',30,14,14,14]
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
  intervals      = ['15minute',5,60,55,18,8,'30minute',30,14,14,14]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_CRS_temp.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_temp.ENTRY_15M_TEMP.objects.all().values_list('symbol',flat=True))})
  return response

@shared_task(bind=True,max_retries=3)
def CROSS_OVER_RUNS_30_MIN_TEMP(self):
  response = {'CRS': False, 'STATUS': 'NONE'}

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
  status = backbone_CRS_30_temp.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_30_temp.ENTRY_30M_TEMP.objects.all().values_list('symbol',flat=True))})
  return response