from algo import models
from Model_15M import models as models_15
from Model_30M import models as models_30
from Model_15_temp import models as models_temp
from Model_15_temp_down import models as models_temp_down
from django.http import JsonResponse
from django.shortcuts import render
from kiteconnect import KiteConnect
from fyers_api import accessToken
from fyers_api import fyersModel
from datetime import date, datetime

from . import freeze_all_15
from . import freeze_all_15_temp
from . import freeze_all_30
from . import freeze_all_15_down

from rest_framework.decorators import api_view

# Create your views here.
def fyers_conn():
  app_id = open('algo/config/app_id.txt','r').read()
  access_token = models.FYERS_KEYS.objects.get(app_id=app_id).access_token
  try:
    fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)
  except Exception as  e:
    pass
  return fyers

def Index_FYERS(request):
  app_id = open('./algo/config/app_id.txt','r').read()
  app_secret = open('./algo/config/app_secret.txt','r').read()
  try:
    session=accessToken.SessionModel(client_id=app_id,
    secret_key=app_secret,redirect_uri='https://www.google.co.in/',
    response_type='code', grant_type='authorization_code')
    fyers_url = session.generate_authcode()  
  except Exception as  e:
      print(e)
  context = {'fyers_url': fyers_url}
  return render(request, 'index_fyers.html', context)

def generate_fyers_acc_token(request):
  app_id = open('./algo/config/app_id.txt','r').read()
  app_secret = open('./algo/config/app_secret.txt','r').read()
  if request.method == 'POST':
    request_token 		= request.POST.get('request_token','')
    try:
      session=accessToken.SessionModel(client_id=app_id,
      secret_key=app_secret,redirect_uri='https://www.google.com/',
      response_type='code', grant_type='authorization_code')
      session.set_token(request_token)
      response = session.generate_token()

      access_token = response["access_token"]
      models.FYERS_KEYS.objects.all().delete()
      access_token_obj = models.FYERS_KEYS(app_id=app_id, app_secret=app_secret,access_token=access_token)
      access_token_obj.save()
      fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)
      acc_name = fyers.get_profile()['data']['name']
      context = {'access_token': access_token,'fyers': '1', 'account_name': acc_name,'status':'Now you can "REST IN PEACE".'}
    except Exception as  e:
      context = {'success':'ERROR','status':e}
    return render(request, 'success.html', context)
  else:
    context = {'success':'ERROR','status':'Please, Do it once again, My Lord. My Creater. My LUCIFER...','error':'WORNG METHOD APPLID.'}
    return render(request, 'success.html', context)

def check_fyers(request):
  app_id = open('./algo/config/app_id.txt','r').read()
  try:
    access_token = models.FYERS_KEYS.objects.get(app_id=app_id).access_token
    fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)
    acc_name = fyers.get_profile()['data']['name']
    context = {'access_token': access_token,'fyers': '1', 'account_name': acc_name,'status':'Now you can "REST IN PEACE".'}
  except Exception as  e:
    context = {'success':'ERROR','status':'Please, Do it once again, My Lord. My Creater. My LUCIFER...','error':e}
  return render(request, 'check.html', context)

@api_view(['GET',])
def MODEL_STATUS(request):
  response = {'success': False, 'data': None}
  if request.method == 'GET':
    queryset      = models.PROFIT.objects.filter(date = date.today()).values_list('model_name', 'current_gain', 'date', 'p_l')
    data = []
    for query_list in queryset:
      data.append({'model_name': query_list[0],'current_gain': query_list[1],'date': query_list[2],'p_l': round(query_list[3],2)})
    response.update({'success': True, 'data': data})
    return JsonResponse(response)
  return JsonResponse(response)

@api_view(['GET','POST'])
def FREEZE_ALL(request):
  kite_conn_var = fyers_conn()
  # --------------------------------- FREEZE Profit at each LTP ------------------------
  crs_main_entry_list = models_15.CONFIG_15M.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
  # crs_temp_entry_list = models_temp.CONFIG_15M_TEMP.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
  crs_30_entry_list   = models_30.CONFIG_30M.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
  # crs_down_entry_list = models_temp_down.CONFIG_15M_TEMP_DOWN.objects.filter(buy = True, placed = True).values_list('symbol', flat=True)
  total_placed_entry = len(crs_main_entry_list) + len(crs_30_entry_list)#  + len(crs_temp_entry_list) + len(crs_down_entry_list)

  model_config_obj               = models.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
  model_profit_config_obj        = models.PROFIT_CONFIG.objects.get(model_name = 'OVER_ALL_PLACED')
  # FREEZE PROFIT
  gain_main, p_l_main = freeze_all_15.freeze_all(list(crs_main_entry_list),kite_conn_var)
  # gain_temp, p_l_temp = freeze_all_15_temp.freeze_all(list(crs_temp_entry_list),kite_conn_var)
  gain_30, p_l_30 = freeze_all_30.freeze_all(list(crs_30_entry_list),kite_conn_var)
  # gain_down, p_l_down = freeze_all_15_down.freeze_all(list(crs_down_entry_list),kite_conn_var)
  gain = gain_main + gain_30# + gain_temp + gain_down
  p_l  = p_l_main + p_l_30# + p_l_temp + p_l_down
  models.FREEZE_PROFIT(model_name = 'OVER_ALL_PLACED', indicate = 'HIT_{}'.format(model_profit_config_obj.count), price = round(sum(gain), 2), p_l = round(sum(p_l), 2), entry = total_placed_entry, day_hit = 'DAY_HIT_{}'.format(model_profit_config_obj.day_hit),top_price= model_config_obj.top_gain, stoploss = model_config_obj.top_loss).save()
  model_profit_config_obj.day_hit   += 1
  model_profit_config_obj.target    = 10000
  model_profit_config_obj.stoploss  = 0
  model_profit_config_obj.count     = 0
  model_profit_config_obj.active    = False
  model_profit_config_obj.entry     = 0
  # PROFIT TABLE
  model_config_obj.current_gain           = 0
  model_config_obj.top_gain               = 0
  model_config_obj.top_loss               = 0
  model_config_obj.p_l                    = 0
  model_profit_config_obj.save()
  model_config_obj.save()
  response = {'success': True, 'status': 'BOOKED PROFIT OF {} ₹.'.format(gain)}
  return JsonResponse(response)