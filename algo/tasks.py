from datetime import date, datetime, time, timedelta
from kiteconnect import KiteConnect
from fyers_api import fyersModel,accessToken
from smartapi import SmartConnect
from time import sleep
import pandas as pd
import requests
import random
import talib
from urllib.parse import urlparse, parse_qs
from django.db.models import Q

from Model_15M import models
from Model_30M import models as models_30
from . import models as models_a
from . import freeze_all_15
from . import freeze_all_15_temp
from . import freeze_all_30
from . import freeze_all_15_down
from . import check_ltp
from . import check_ltp_crs_30
from celery import shared_task
from .CROSSOVER_15_MIN.utils import backbone as backbone_CRS_15_MIN
from .CROSSOVER_30_MIN.utils import backbone as backbone_CRS_30_MIN

# -------------------- Not ------------------
from Model_15_temp import models as models_temp
from Model_15_temp_down import models as models_temp_down
from . import check_ltp_temp
from . import check_ltp_temp_down
from .CROSSOVER_15_MIN_temp.utils import backbone as backbone_CRS_temp
from .DOWN_CROSSOVER_15_MIN_temp.utils import backbone as backbone_DOWN_CRS_temp

@shared_task(bind=True,max_retries=3)
def GENERATE_FYERS_TOKEN(self):
  username = open('./algo/config/fyers_username.txt','r').read()
  password = open('./algo/config/fyers_password.txt','r').read()
  pin = open('./algo/config/fyers_pin.txt','r').read()
  client_id = open('./algo/config/app_id.txt','r').read()
  secret_key = open('./algo/config/app_secret.txt','r').read()
  redirect_uri = "https://www.google.co.in/"
  app_id = client_id[:-4]  # '##########'
  session = accessToken.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code",
    )
  headers = {
        "accept": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "accept-language": "en-US,en;q=0.9",
    }
  s = requests.Session()
  s.headers.update(headers)
  data1 = f'{{"fy_id":"{username}","password":"{password}","app_id":"2","imei":"","recaptcha_token":""}}'
  r1 = s.post("https://api.fyers.in/vagator/v1/login", data=data1)
  assert r1.status_code == 200, f"Error in r1:\n {r1.json()}"
  request_key = r1.json()["request_key"]
  data2 = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{pin}","recaptcha_token":""}}'
  r2 = s.post("https://api.fyers.in/vagator/v1/verify_pin", data=data2)
  assert r2.status_code == 200, f"Error in r2:\n {r2.json()}"
  headers = {"authorization": f"Bearer {r2.json()['data']['access_token']}", "content-type": "application/json; charset=UTF-8"}
  data3 = f'{{"fyers_id":"{username}","app_id":"{app_id}","redirect_uri":"{redirect_uri}","appType":"100","code_challenge":"","state":"abcdefg","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
  r3 = s.post("https://api.fyers.in/api/v2/token", headers=headers, data=data3)
  assert r3.status_code == 308, f"Error in r3:\n {r3.json()}"
  parsed = urlparse(r3.json()["Url"])
  auth_code = parse_qs(parsed.query)["auth_code"][0]
  session.set_token(auth_code)
  response = session.generate_token()
  access_token = response["access_token"]
  models_a.FYERS_KEYS.objects.all().delete()
  access_token_obj = models_a.FYERS_KEYS(app_id=client_id, app_secret=secret_key,access_token=access_token)
  access_token_obj.save()
  fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
  profile_name = fyers.get_profile()['data']['name']
  return {'success': True,'profile_name': profile_name}

def angelbroking_conn():
    obj=SmartConnect(api_key="MWxz7OCW",)
    obj.generateSession("P567723","Qwerty@12")
    return obj

def fyers_conn():
  app_id = open('algo/config/app_id.txt','r').read()
  access_token = models_a.FYERS_KEYS.objects.get(app_id=app_id).access_token
  try:
    fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)
  except Exception as  e:
    pass
  return fyers

def cal_volatility(dt):
  dt['Return'] = 100 * (dt['Close'].pct_change())
  daily_volatility = dt['Return'].std()
  return round(daily_volatility,4)

def cal_volatility_VOL(dt):
  # dt['Return'] = 100 * (dt['Volume'].pct_change())
  # daily_volatility = dt['Volume'].std()
  daily_volatility = dt['Volume'].iloc[-1]
  return round(daily_volatility,4)

def checkrsiup(rsi):
  if rsi[-1] < rsi[-2]:# and rsi[-1] > 60:
    return False
  elif rsi[-1] > 60:
    return True
  for i in range(-1,-14,-1):
    if rsi[i] <= 40:
      return True
  return False

def checkrsidown(rsi):
  if rsi[-1] > rsi[-2]:# and rsi[-1] < 40:
    return False
  elif rsi[-1] < 40:
    return True
  for i in range(-1,-14,-1):
    if rsi[i] >= 60:
      return True
  return False

def stockselection(stock_sym,data_frame):
  rsi           = talib.RSI(data_frame['Close'], timeperiod=14)
  macd, macdsignal, macdhist = talib.MACD(data_frame['Close'], fastperiod=9, slowperiod=13, signalperiod=9)
  if cal_volatility(data_frame) > 2.5:
    if checkrsiup(rsi):
      if macd[-1] > macdsignal[-1]:
        if macd[-1] > macd[-2]:
          if macd[-2] > macd[-3]:
            # models_a.STOCK.objects.filter(symbol = stock_sym).update(active_5_up = True,active_5_down = True)
            return True

    if checkrsidown(rsi):
      if macd[-1] < macdsignal[-1]:
        if macd[-1] < macd[-2]:
          if macd[-2] < macd[-3]:
            # models_a.STOCK.objects.filter(symbol = stock_sym).update(active_5_up = True,active_5_down = True)
            return True
  return False

@shared_task(bind=True,max_retries=3)
# initial_setup on DATABASE -------------------------------------
def get_stocks_configs(self):
  response = {'stock_table': False, 'config_table_15': False, 'config_table_30': False}
  now = date.today()
  last_6_days       = now - timedelta(days=360)
  fyers_conn_val = fyers_conn()
  for_intraday = []
  # Stock dict
  stock_dict = {
      'AARTIIND':	[1793,		'COMMODITY','mid50','7'],
      'ABFRL':	[7707649,	'nill','nifty','30108'],
      'ACC':		[5633,		'INFRA,COMMODITY','nxt50','4421'],
      'ADANIENT':	[6401,		'METAL','nxt50','25'],
      'ADANIGREEN':	[912129,	'ENERGY,COMMODITY','nxt50','3563'],
      'ADANIPORTS':	[3861249,	'INFRA','nify','15083'],
      'AMBUJACEM':	[325121,	'INFRA,MNC,COMMODITY','nxt50','1270'],
      'APLLTD':	[6483969,	'nill','nifty','25328'],
      'ASHOKLEY':	[54273,		'AUTO,INFRA,MNC','mid50','212'],
      'ASIANPAINT':	[60417,		'CONSUMPTION','nify','236'],
      'AUROPHARMA':	[70401,		'PHARMA','nxt50','275'],
      'AXISBANK':	[1510401,	'BANK,FINN','nify','5900'],
      'BAJAJ-AUTO':	[4267265,	'AUTO,CONSUMPTION','nify','16669'],
      'BANDHANBNK':	[579329,	'BANK','nxt50','2263'],
      'BANKBARODA':	[1195009,	'BANK','nxt50','4668'],
      'BANKINDIA':	[1214721,	'BANK','mid50','4745'],
      'BATAINDIA':	[94977,		'MNC','mid50','371'],
      'BEL':		[98049,		'PSE','mid50','383'],
      'BERGEPAINT':	[103425,	'CONSUMPTION','nxt50','404'],
      'BHARATFORG':	[108033,	'AUTO','mid50','422'],
      'BHARTIARTL':	[2714625,	'INFRA,CONSUMPTION','nify','10604'],
      'BHEL':		[112129,	'PSE','mid50','438'],
      'BIOCON':	[2911489,	'PHARMA','nxt50','11373'],
      'BPCL':		[134657,	'INFRA,PSE,COMMODITY','nify','526'],
      'BRITANNIA':	[140033,	'FMCG,MNC,CONSUMPTION','nify','547'],
      'CADILAHC':	[2029825,	'PHARMA','nxt50','7929'],
      'CANBK':	[2763265,	'BANK','mid50','10794'],
      'CASTROLIND':	[320001,	'MNC','nifty','1250'],
      'CHOLAFIN':	[175361,	'FINN','nxt50','685'],
      'CIPLA':	[177665,	'PHARMA','nify','694'],
      'COALINDIA':	[5215745,	'METAL,PSE,COMMODITY','nify','20374'],
      'COFORGE':	[2955009,	'IT','mid50','11543'],
      'COLPAL':	[3876097,	'FMCG,MNC,CONSUMPTION','nxt50','15141'],
      'CONCOR':	[1215745,	'INFRA,PSE','mid50','4749'],
      'CUB':		[1459457,	'nill','nifty','5701'],
      'CUMMINSIND':	[486657,	'MNC','mid50','1901'],
      'DABUR':	[197633,	'FMCG,CONSUMPTION','nxt50','772'],
      'DIVISLAB':	[2800641,	'PHARMA','nify','10940'],
      'DLF':		[3771393,	'INFRA','nxt50','14732'],
      'DMART':	[5097729,	'CONSUMPTION','nxt50','19913'],
      'DRREDDY':	[225537,	'PHARMA','nify','881'],
      'EMAMILTD':	[3460353,	'FMCG','nifty','13517'],
      'ESCORTS':	[245249,	'nill','mid50','958'],
      'EICHERMOT':	[232961,	'AUTO','nify','910'],
      'EXIDEIND':	[173057,	'AUTO,INFRA','mid50','676'],
      'FEDERALBNK':	[261889,	'BANK','mid50','1023'],
      'GAIL':		[1207553,	'INFRA,PSE','nxt50','4717'],
      'GMRINFRA':	[3463169,	'nill','nifty','13528'],
      'GODREJCP':	[2585345,	'FMCG,CONSUMPTION','nxt50','10099'],
      'GODREJPROP':	[4576001,	'nill','mid50','17875'],
      'GRANULES':	[3039233,	'nill','nifty','11872'],
      'GRASIM':	[315393,	'INFRA,COMMODITY','nify','1232'],
      'HAVELLS':	[2513665,	'CONSUMPTION','nxt50','9819'],
      'HCLTECH':	[1850625,	'IT','nify','7229'],
      'HDFC':		[340481,	'FINN','nify','1330'],
      'HDFCBANK':	[341249,	'BANK,FINN','nify','1333'],
      'HDFCLIFE':	[119553,	'FINN','nify','467'],
      'HEROMOTOCO':	[345089,	'AUTO','nify','1348'],
      'HINDALCO':	[348929,	'METAL','nify','1363'],
      'HINDPETRO':	[359937,	'INFRA,PSE,COMMODITY','nxt50','1406'],
      'HINDUNILVR':	[356865,	'FMCG,MNC,CONSUMPTION','nify','1394'],
      'HINDZINC':	[364545,	'METAL,COMMODITY','nifty','1424'],
      'IBULHSGFIN':	[7712001,	'nill','nifty','30125'],
      'ICICIBANK':	[1270529,	'BANK,FINN','nify','4963'],
      'IDFCFIRSTB':	[2863105,	'BANK','mid50','11184'],
      'IGL':		[2883073,	'INFRA','nxt50','11262'],
      'INDIANB':	[3663105,	'BANK','nifty','14309'],
      'INDIGO': [2865921,'nill','nifty','11195'],
      'INDUSINDBK':	[1346049,	'BANK','nify','5258'],
      'INDUSTOWER':	[7458561,	'INFRA','nxt50','29135'],
      'INFY':		[408065,	'IT','nify','1594'],
      'IOC':		[415745,	'INFRA,PSE,COMMODITY','nify','1624'],
      'IRCTC':	[3484417,	'PSE','mid50','13611'],
      'ITC':		[424961,	'FMCG,CONSUMPTION','nify','1660'],
      'JINDALSTEL':	[1723649,	'METAL,COMMODITY','nxt50','6733'],
      'JSWSTEEL':	[3001089,	'METAL,COMMODITY','nify','11723'],
      'JUBLFOOD':	[4632577,	'FMCG,CONSUMPTION','nxt50','18096'],
      'KOTAKBANK':	[492033,	'BANK,FINN','nify','1922'],
      'LICHSGFIN':	[511233,	'nill','mid50','1997'],
      'LT':		[2939649,	'INFRA','nify','11483'],
      'LUPIN':	[2672641,	'PHARMA','nxt50','10440'],
      'M&M':		[519937,	'AUTO,CONSUMPTION','nify','2031'],
      'MARUTI':	[2815745,	'AUTO','nify','10999'],
      'M&MFIN':	[3400961,	'FINN','mid50','13285'],
      'MANAPPURAM':	[4879617,	'nill','mid50','19061'],
      'MARICO':	[1041153,	'FMCG,CONSUMPTION','nxt50','4067'],
      'MINDTREE':	[3675137,	'IT','mid50','14356'],
      'MUTHOOTFIN':	[6054401,	'FINN','nxt50','23650'],
      'NAM-INDIA':	[91393,		'nill','nifty','357'],
      'NATIONALUM':	[1629185,	'METAL,PSE','nifty','6364'],
      'NMDC':		[3924993,	'METAL,PSE,COMMODITY','nxt50','15332'],
      'NTPC':		[2977281,	'INFRA,PSE,COMMODITY','nify','11630'],
      'ONGC':		[633601,	'INFRA,PSE,COMMODITY','nify','2475'],
      'PETRONET':	[2905857,	'INFRA','mid50','11351'],
      'PFC':		[3660545,	'PSE','mid50','14299'],
      'PNB':		[2730497,	'BANK','nxt50','10666'],
      'POWERGRID':	[3834113,	'INFRA,PSE','nify','14977'],
      'PVR':		[3365633,	'MEDIA','nifty','13147'],
      'RBLBANK':	[4708097,	'BANK','nifty','18391'],
      'RELIANCE':	[738561,	'INFRA,COMMODITY','nify','2885'],
      'SAIL':		[758529,	'METAL,PSE','nxt50','2963'],
      'SBICARD':	[4600577,	'nill','nxt50','17971'],
      'SBILIFE':	[5582849,	'FINN','nify','21808'],
      'SBIN':		[779521,	'BANK,FINN','nify','3045'],
      'SUNPHARMA':	[857857,	'PHARMA','nify','3351'],
      'SUNTV':	[3431425,	'MEDIA','mid50','13404'],
      'TATACHEM':	[871681,	'nill','nifty','3405'],
      'TATACONSUM':	[878593,	'FMCG,CONSUMPTION','nify','3432'],
      'TATAMOTORS':	[884737,	'AUTO','nify','3456'],
      'TATAPOWER':	[877057,	'ENERGY,INFRA,COMMODITY','mid50','3426'],
      'TATASTEEL':	[895745,	'METAL,COMMODITY','nify','3499'],
      'TCS':		[2953217,	'IT','nify','11536'],
      'TECHM':	[3465729,	'IT','nify','13538'],
      'TITAN':	[897537,	'CONSUMPTION','nify','3506'],
      'TORNTPOWER':	[3529217,	'COMMODITY','mid50','13786'],
      'TRENT':	[502785,	'CONSUMPTION','mid50','1964'],
      'TVSMOTOR':	[2170625,	'AUTO','mid50','8479'],
      'ULTRACEMCO':	[2952193,	'INFRA,COMMODITY','nify','11532'],
      'UNIONBANK':	[2752769,	'BANK','nifty','10753'],
      'UPL':		[2889473,	'COMMODITY','nify','11287'],
      'VEDL':		[784129,	'METAL,MNC,COMMODITY','nxt50','3063'],
      'VOLTAS':	[951809,	'CONSUMPTION','mid50','3718'],
      'WELCORP':	[3026177,	'METAL','nifty','11821'],
      'WIPRO':	[969473,	'IT','nify','3787'],
      'ZEEL':		[975873,	'MEDIA,CONSUMPTION','mid50','3812']
      }
  # Create stocks and config's for trade in stock and config table
  for stock_sym in stock_dict:
    # STORE IN STOCK TABLE
    if not models_a.STOCK.objects.filter(symbol = stock_sym).exists():
      models_a.STOCK(symbol = stock_sym, instrument_key = stock_dict[stock_sym][0], sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2], token=stock_dict[stock_sym][3]).save()
    # CREATE CONFIG IN FOR 15 MIN
    if not models.CONFIG_15M.objects.filter(symbol = stock_sym).exists():
      models.CONFIG_15M(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()
    # CREATE CONFIG IN FOR 30 MIN
    if not models_30.CONFIG_30M.objects.filter(symbol = stock_sym).exists():
      models_30.CONFIG_30M(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()

    
    # ----------------------------------- Not Ative ------------------------------------
    # CREATE CONFIG IN FOR 15 MIN TEMP
    if not models_temp.CONFIG_15M_TEMP.objects.filter(symbol = stock_sym).exists():
      models_temp.CONFIG_15M_TEMP(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()

    # CREATE CONFIG IN FOR 15 MIN TEMP DOWN
    if not models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(symbol = stock_sym).exists():
      models_temp_down.CONFIG_15M_TEMP_DOWN(symbol = stock_sym, sector = stock_dict[stock_sym][1],niftytype = stock_dict[stock_sym][2]).save()

    # GET THE VOLATILITY OF EACH STK IN DICT
    sleep(0.3)
    data = {"symbol":"NSE:{}-EQ".format(stock_sym),"resolution":'D',"date_format":"1","range_from":last_6_days,"range_to":now,"cont_flag":"0"}
    data = fyers_conn_val.history(data)['candles']
    data=pd.DataFrame(data)
    data[0] = pd.to_datetime(data[0],unit = 's')
    data_frame = data.set_index(data[0], drop=False, append=False, inplace=False, verify_integrity=False).drop(0, 1)
    data_frame.rename(columns = {0:'date',1:'Open',2:'High',3:'Low',4:'Close',5:'Volume'}, inplace = True)
    data_frame.index.names = ['date']
    models_a.STOCK.objects.filter(symbol = stock_sym).update(volatility = cal_volatility(data_frame), vol_volatility = cal_volatility_VOL(data_frame))
    macd, macdsignal, macdhist = talib.MACD(data_frame['Close'], fastperiod=9, slowperiod=15, signalperiod=9)
    # cut_off_volatility = sum(volatile_stocks.values())/len(volatile_stocks)
    cut_off_volatility = 2.8
    if cal_volatility(data_frame) > cut_off_volatility:
      models_a.STOCK.objects.filter(symbol = stock_sym).update(active_15 = True)
    else:
      models_a.STOCK.objects.filter(symbol = stock_sym).update(active_15 = False)
    
    if stockselection(stock_sym,data_frame):
      for_intraday.append(stock_sym)
    else:
      models_a.STOCK.objects.filter(symbol = stock_sym).update(active_5_up = False, active_5_down = False)

  if len(for_intraday) <= 5:
    for stock_sym in for_intraday:
      models_a.STOCK.objects.filter(symbol = stock_sym).update(active_5_up = True, active_5_down = True)
  else:
    random.shuffle(for_intraday)
    for stock_sym in for_intraday[:5]:
      models_a.STOCK.objects.filter(symbol = stock_sym).update(active_5_up = True, active_5_down = True)
    for stock_sym in for_intraday[5:]:
      models_a.STOCK.objects.filter(symbol = stock_sym).update(active_5_up = False, active_5_down = False)

  # Config Model to Profit Tables
  model_name_list = ['CRS_MAIN', 'CRS_TEMP', 'CRS_TEMP_DOWN', 'CRS_30_MIN','OVER_ALL_PLACED']
  for model_name in model_name_list:
    # if model not configure in Profit Table
    if not models_a.PROFIT.objects.filter(model_name = model_name, date = datetime.now().date()).exists():
      models_a.PROFIT(model_name = model_name, date = datetime.now().date()).save()
    if not models_a.PROFIT_CONFIG.objects.filter(model_name = model_name).exists():
      models_a.PROFIT_CONFIG(model_name = model_name).save()
    else:
      model_profit_config_obj = models_a.PROFIT_CONFIG.objects.get(model_name = model_name)
      model_profit_config_obj.day_hit   = 1
      model_profit_config_obj.target    = 10000
      model_profit_config_obj.stoploss  = 0
      model_profit_config_obj.count     = 0
      model_profit_config_obj.active    = False
      model_profit_config_obj.entry     = 0
      model_profit_config_obj.save()

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
  response.update({'STOCKS_SELECTION':for_intraday})
  return response

@shared_task(bind=True,max_retries=3)
def UPDATE_LIMIT(self):
  now = date.today()
  from_day = now - timedelta(days=20)
  # Initialize Kite Connections
  fyers_conn_val = fyers_conn()
  stocks = models_a.STOCK.objects.all().values_list('symbol', flat=True)
  for stock_name in stocks:
    sleep(0.3)
    data = {"symbol":"NSE:{}-EQ".format(stock_name),"resolution":'15',"date_format":"1","range_from":from_day,"range_to":now,"cont_flag":"0"}
    data = fyers_conn_val.history(data)['candles']
    data=pd.DataFrame(data)
    data[0] = pd.to_datetime(data[0],unit = 's')
    data_frame = data.set_index(data[0], drop=False, append=False, inplace=False, verify_integrity=False).drop(0, 1)
    data_frame.rename(columns = {0:'date',1:'Open',2:'High',3:'Low',4:'Close',5:'Volume'}, inplace = True)
    data_frame.index.names = ['date']
    data_frame = data_frame[now:]
    if (data_frame['Close'].iloc[0] > data_frame['Open'].iloc[0]):
      up_l = data_frame['Close'].iloc[0]
      lower_l = data_frame['Open'].iloc[0]
      models_a.STOCK.objects.filter(symbol = stock_name).update(upper_lim = up_l, lower_lim = lower_l)
    elif (data_frame['Close'].iloc[0] < data_frame['Open'].iloc[0]):
      up_l = data_frame['Open'].iloc[0]
      lower_l = data_frame['Close'].iloc[0]
      models_a.STOCK.objects.filter(symbol = stock_name).update(upper_lim = up_l, lower_lim = lower_l)
  return 'TRUE'

@shared_task(bind=True,max_retries=3)
def ltp_of_entries(self):
  response = {'LTP': False, 'STATUS': 'NONE','ACTIVE_STOCKS': None,'LTP_30': False, 'STATUS_30': 'NONE','ACTIVE_STOCKS_30': None}
  gain_placed_price = 0
  active_placed_entry = 0

  # CALCULATE CURRENT RETURN OF ALL ACTIVE STOCKS
  if datetime.now().time() > time(9,15,00) and datetime.now().time() < time(15,17,00):
    kite_conn_var = angelbroking_conn()

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
    gain_placed_price += sum(models.CONFIG_15M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    active_placed_entry += len(models.CONFIG_15M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))

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
    gain_placed_price += sum(models_30.CONFIG_30M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    active_placed_entry += len(models_30.CONFIG_30M.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))

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
    gain_placed_price += sum(models_temp.CONFIG_15M_TEMP.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    active_placed_entry += len(models_temp.CONFIG_15M_TEMP.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))

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
    gain_placed_price += sum(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))
    active_placed_entry += len(models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True,placed = True).values_list('return_price', flat=True))

    # OVER_ALL MODEL UPDATES ----------------------------------------
    model_config_obj   = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
    if active_placed_entry != 0:
      model_config_obj.current_gain           = round(gain_placed_price,2)
      model_config_obj.current_gain_time      = datetime.now().time()
      if active_placed_entry > model_config_obj.max_entry:
        model_config_obj.max_entry     = active_placed_entry
      if gain_placed_price > model_config_obj.top_gain:
        model_config_obj.top_gain       = round(gain_placed_price,2)
        model_config_obj.top_gain_time  = datetime.now().time()
        model_config_obj.top_gain_entry = active_placed_entry
      if gain_placed_price < model_config_obj.top_loss:
        model_config_obj.top_loss       = round(gain_placed_price,2)
        model_config_obj.top_loss_time  = datetime.now().time()
        model_config_obj.top_loss_entry = active_placed_entry
    else:
      # PROFIT TABLE
      model_config_obj.current_gain           = 0
      model_config_obj.top_gain               = 0
      model_config_obj.top_loss               = 0
      model_config_obj.p_l                    = 0
      # PROFIT CONFIG
      model_profit_config_obj           = models_a.PROFIT_CONFIG.objects.get(model_name = 'OVER_ALL_PLACED')
      model_profit_config_obj.target    = 10000
      model_profit_config_obj.stoploss  = 0
      model_profit_config_obj.count     = 0
      model_profit_config_obj.active    = False
      model_profit_config_obj.entry     = 0
      model_profit_config_obj.save()
    model_config_obj.save()

    # # --------------------------------- FREEZE Profit at each LTP ------------------------
    # crs_main_entry_list = models.CONFIG_15M.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    # crs_temp_entry_list = models_temp.CONFIG_15M_TEMP.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    # crs_30_entry_list   = models_30.CONFIG_30M.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    # crs_down_entry_list = models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
    # total_placed_entry = len(crs_main_entry_list) + len(crs_temp_entry_list) + len(crs_30_entry_list) + len(crs_down_entry_list)

    # model_config_obj               = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
    # model_profit_config_obj        = models_a.PROFIT_CONFIG.objects.get(model_name = 'OVER_ALL_PLACED')
    # if model_config_obj.current_gain > model_profit_config_obj.target:
    #   model_profit_config_obj.stoploss  = model_profit_config_obj.target - 500
    #   model_profit_config_obj.target    = model_profit_config_obj.target + 200
    #   model_profit_config_obj.count     += 1
    #   model_profit_config_obj.active    = True
    # elif model_profit_config_obj.active is True:
    #   if model_config_obj.current_gain < model_profit_config_obj.stoploss:
    #     # FREEZE PROFIT
    #     gain_main, p_l_main = freeze_all_15.freeze_all(crs_main_entry_list,kite_conn_var)
    #     gain_temp, p_l_temp = freeze_all_15_temp.freeze_all(crs_temp_entry_list,kite_conn_var)
    #     gain_30, p_l_30 = freeze_all_30.freeze_all(crs_30_entry_list,kite_conn_var)
    #     gain_down, p_l_down = freeze_all_15_down.freeze_all(crs_down_entry_list,kite_conn_var)
    #     gain = gain_main + gain_temp + gain_30 + gain_down
    #     p_l  = p_l_main + p_l_temp + p_l_30 + p_l_down
    #     models_a.FREEZE_PROFIT(model_name = 'OVER_ALL_PLACED', indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = total_placed_entry, day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
    #     model_profit_config_obj.day_hit   += 1
    #     model_profit_config_obj.target    = 10000
    #     model_profit_config_obj.stoploss  = 0
    #     model_profit_config_obj.count     = 0
    #     model_profit_config_obj.active    = False
    #     model_profit_config_obj.entry     = 0
    #     # PROFIT TABLE
    #     model_config_obj.current_gain           = 0
    #     model_config_obj.top_gain               = 0
    #     model_config_obj.top_loss               = 0
    #     model_config_obj.p_l                    = 0
    # model_profit_config_obj.save()
    # model_config_obj.save()
    kite_conn_var.terminateSession("P567723")
  # CALCULATE THE RETURN OF ALL MODELS
  elif datetime.now().time() >= time(15,17,00) and datetime.now().time() < time(15,30,00):
    model_name_list = ['CRS_MAIN', 'CRS_TEMP', 'CRS_30_MIN', 'CRS_TEMP_DOWN','OVER_ALL_PLACED']
    for ind, m_name in enumerate(model_name_list):
      # models_a.PROFIT_CONFIG.objects.filter(model_name = m_name).update(zerodha_entry = False)
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
        profit = models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True)
        total_sum = models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True)
        model_config_obj.current_gain            = round(sum(total_sum),2)
        model_config_obj.current_gain_time       = datetime.now().time()
        model_config_obj.current_gain_entry      = len(profit)
        model_config_obj.p_l                     = round(sum(profit),2)
      if ind == 4:
        profit_main = list(models_a.CROSSOVER_15_MIN.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True))
        total_sum_main = list(models_a.CROSSOVER_15_MIN.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True))
        profit_temp = list(models_a.CROSSOVER_15_MIN_TEMP.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True))
        total_sum_temp = list(models_a.CROSSOVER_15_MIN_TEMP.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True))
        profit_30 = list(models_a.CROSSOVER_30_MIN.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True))
        total_sum_30 = list(models_a.CROSSOVER_30_MIN.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True))
        profit_down = list(models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('profit',flat=True))
        total_sum_down = list(models_a.CROSSOVER_15_MIN_TEMP_DOWN.objects.filter(~Q(order_id = 0),indicate = 'Exit',created_on = datetime.now().date()).values_list('difference',flat=True))
        # merge all--
        total_sum = total_sum_main + total_sum_temp + total_sum_30 + total_sum_down
        profit    = profit_main + profit_temp + profit_30 + profit_down
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
  kite_conn_var       = fyers_conn()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['5',20,9,23,20,100]
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
  kite_conn_var       = fyers_conn()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['5',20,9,23,20,100]
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
  sleep(901)
  # Initialize Kite Connections
  kite_conn_var       = fyers_conn()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['30',90,9,15,9,100]
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
  sleep(901)
  # Initialize Kite Connections
  kite_conn_var       = fyers_conn()
  '''
    -> intervals = [trade_time_period, Num_Of_Days, Upper_rsi, Lower_rsi, EMA_max, EMA_min, trend_time_period, Num_Of_Days, Trend_rsi, Trade_rsi, Num_of_Candles_for_Target]
  '''
  intervals      = ['30',90,9,15,9,100]
  '''
  -> Intervals:-
    ** Make Sure Don't change the Index, Otherwise You Are Responsible for the Disasters.. **
  '''
  status = backbone_DOWN_CRS_temp.model(intervals, kite_conn_var)
  response.update({'CRS': True, 'STATUS': status, 'ENTRY':list(models_temp_down.ENTRY_15M_TEMP_DOWN.objects.all().values_list('symbol',flat=True))})
  return response
