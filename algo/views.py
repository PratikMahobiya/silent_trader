from algo import models, serializers
from django.http import JsonResponse, response
from django.shortcuts import render
from kiteconnect import KiteConnect
from datetime import datetime, date, timedelta

from Model_15M import models as models_15_MAIN

from rest_framework.decorators import api_view

# Create your views here.
def Index(request):
  api_key = open('./algo/config/api_key.txt','r').read()
  try:
    kite = KiteConnect(api_key=api_key)
    kite_url = kite.login_url()
  except Exception as  e:
    pass
  context = {'kite_url': kite_url}
  return render(request, 'index.html', context)

def generate_acc_token(request):
  api_key = open('./algo/config/api_key.txt','r').read()
  api_secret = open('./algo/config/api_secret.txt','r').read()
  if request.method == 'POST':
    request_token 		= request.POST.get('request_token','')
    try:
      kite = KiteConnect(api_key=api_key)
      data = kite.generate_session(request_token, api_secret=api_secret)
      kite.set_access_token(data["access_token"])
      models.ZERODHA_KEYS.objects.all().delete()
      access_token_obj = models.ZERODHA_KEYS(api_key=api_key, api_secret=api_secret,access_token=data["access_token"])
      access_token_obj.save()
      ltp = kite.ltp(['NSE:SBIN'])
      context = {'access_token': data["access_token"], 'SBI_ltp': ltp['NSE:SBIN']['last_price'],'status':'Now you can "REST IN PEACE".'}
    except Exception as  e:
      context = {'success':'ERROR','status':e}
    return render(request, 'success.html', context)
  else:
    context = {'success':'ERROR','status':'Please, Do it once again, My Lord. My Creater. My LUCIFER...','error':'WORNG METHOD APPLID.'}
    return render(request, 'success.html', context)

def check(request):
  api_key = open('./algo/config/api_key.txt','r').read()
  try:
    access_token = models.ZERODHA_KEYS.objects.get(api_key=api_key).access_token
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    ltp = kite.ltp(['NSE:SBIN'])
    context = {'access_token': access_token, 'SBI_ltp': ltp['NSE:SBIN']['last_price'],'status':'Now you can "REST IN PEACE".'}
  except Exception as  e:
    context = {'success':'ERROR','status':'Please, Do it once again, My Lord. My Creater. My LUCIFER...','error':e}
  return render(request, 'check.html', context)

@api_view(['GET',])
def PLACE_ORDER(request):
  response = {'success': True, 'status': 'Your Order is PLACED.'}
  return JsonResponse(response)


@api_view(['GET',])
def Active_Stocks(request):
  response = {'success': False, 'data': None}
  if request.method == 'GET':
    queryset      = models.CROSSOVER_15_MIN.objects.filter(created_on = (date.today() - timedelta(days=1)), indicate = 'Entry')
    # serializer    = serializers.CROSSOVER_15_Min_Serializer(queryset, many = True)
    # response.update({'success': True, 'data': serializer.data})
    response.update({'success': True, 'data': list(queryset)})
    return JsonResponse(response)
  return JsonResponse(response)

@api_view(['GET',])
def Transactions(request):
  response = {'success': False, 'data': None}
  if request.method == 'GET':
    queryset      = models.CROSSOVER_15_MIN.objects.filter(created_on = (date.today() - timedelta(days=1)))
    serializer    = serializers.CROSSOVER_15_Min_Serializer(queryset, many = True)
    response.update({'success': True, 'data': serializer.data})
    return JsonResponse(response)
  return JsonResponse(response)
