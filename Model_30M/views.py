from algo import models as models_a, serializers
from django.http import JsonResponse
from django.shortcuts import render
from kiteconnect import KiteConnect
from fyers_api import fyersModel
from smartapi import SmartConnect
from datetime import datetime, date, timedelta

from Model_30M import models as models

from rest_framework.decorators import api_view

# Create your views here.
def CRS_VIEW(request):
  return render(request, 'dashboard_30_main.html')

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

def connect_to_kite_connection():
  api_key = open('algo/config/api_key.txt','r').read()
  access_token = models_a.ZERODHA_KEYS.objects.get(api_key=api_key).access_token
  try:
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
  except Exception as  e:
    pass
  return kite

def place_regular_buy_order(symbol, price, quantity):
  # Place an order
  order_id      = 0
  order_status  = 'NOT_PLACED'
  try:
    ang_conn = angelbroking_conn()
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": symbol+'-EQ',
        "symboltoken": models_a.STOCK.objects.get(symbol = symbol).token,
        "transactiontype": "BUY",
        "exchange": "NSE",
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": price,
        "quantity": '{}'.format(quantity)
        }
    order_id = ang_conn.placeOrder(orderparams)
    order_status = 'SUCCESSFULLY_PLACED_ENTRY'
    ang_conn.terminateSession("P567723")
  except Exception as e:
    order_status = 'PROBLEM AT ZERODHA END.'
  return order_id, order_status

def place_regular_sell_order(symbol, stock_config_obj):
  # Place an order
  order_id = 0
  error_status = 'NOT_PLACED'
  try:
    ang_conn = angelbroking_conn()
    ltp        = ang_conn.ltpData("NSE",symbol+'-EQ',models_a.STOCK.objects.get(symbol = symbol).token)['data']['ltp']
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": symbol+'-EQ',
        "symboltoken": models_a.STOCK.objects.get(symbol = symbol).token,
        "transactiontype": "SELL",
        "exchange": "NSE",
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "quantity": '{}'.format(stock_config_obj.quantity)
        }
    order_id = ang_conn.placeOrder(orderparams)
    error_status = 'SUCCESSFULLY_PLACED_EXIT'
    ang_conn.terminateSession("P567723")
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  return order_id, error_status, ltp

@api_view(['GET','POST'])
def PLACE_ORDER(request):
  if request.method == 'POST':
    reference_id  = int(request.data['reference_id'])
    symbol        = request.data['symbol'].split('/')[0]
    price         = float(request.data['price'])
    quantity      = int(request.data['quantity'])
    order_id, order_status = place_regular_buy_order(symbol, price, quantity)
    # order_id, order_status = 1 , 'NOT ACTIVE'
    if order_id != 0:
      target_p = price + price * 0.01
      sl_fixed = price - price * 0.004
      models.CONFIG_30M.objects.filter(symbol = symbol).update(placed = True, buy_price = price, quantity = quantity, order_id = order_id, order_status = order_status, count = 0, target = target_p, stoploss = sl_fixed)
      models_a.CROSSOVER_30_MIN.objects.filter(symbol = symbol, id = reference_id).update(order_id = order_id, order_status = order_status, price = price, quantity = quantity)
      model_config_obj   = models_a.PROFIT.objects.get(model_name = 'OVER_ALL_PLACED', date = datetime.now().date())
      model_config_obj.current_gain_entry     += 1
      model_config_obj.save()
      response      = {'success': True, 'status': '"{}" is PLACED. ORDER ID:- {}'.format(symbol,order_id)}
      return JsonResponse(response)
    response = {'success': False, 'status': '"{}" is NOT PLACED. ..TRY AGAIN..'.format(symbol)}
    return JsonResponse(response)
  response = {'success': False, 'status': 'WORNG METHOD {}.'.format(request.method)}
  return JsonResponse(response)

@api_view(['GET','POST'])
def EXIT_ORDER(request):
  if request.method == 'POST':
    symbol        = request.data['symbol'].split('/')[0]
    stock_config_obj = models.CONFIG_30M.objects.get(symbol = symbol)
    if stock_config_obj.buy is True:
      order_id, order_status, price = place_regular_sell_order(symbol, stock_config_obj)
      # order_id, order_status, price  = 1 , 'NOT ACTIVE', 200
      if order_id != 0:
        diff          = price - stock_config_obj.buy_price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2) - 100
        trans_data = {'symbol':symbol,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Exit','type':'M_Exit','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status,'placed' : True}
        transaction   = serializers.CROSSOVER_30_MIN_Serializer(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_30M.objects.filter(symbol = symbol).delete()
        stock_config_obj.buy          = False
        stock_config_obj.placed       = False
        stock_config_obj.count        = 0
        stock_config_obj.order_id     = 0
        stock_config_obj.save()
        response      = {'success': True, 'status': '"{}" is EXITED. ORDER ID:- {}'.format(symbol,order_id)}
        return JsonResponse(response)
      response = {'success': False, 'status': '"{}" is NOT EXITED. ..TRY AGAIN..'.format(symbol)}
      return JsonResponse(response)
    response = {'success': False, 'status': 'ALREADY EXITED {}.'.format(symbol)}
    return JsonResponse(response)
  response = {'success': False, 'status': 'WORNG METHOD {}.'.format(request.method)}
  return JsonResponse(response)

@api_view(['GET',])
def Active_Stocks(request):
  response = {'success': False, 'data': None}
  if request.method == 'GET':
    active_entry  = models.ENTRY_30M.objects.all().values_list('symbol', 'reference_id')
    active_stocks = {}
    active_stocks_str = ''
    stock_ltp = {}
    for stock in active_entry:
      active_stocks_str += 'NSE:'+stock[0]+'-EQ,'
    active_stocks = {"symbols":active_stocks_str[:-1]}
    if len(active_stocks_str) != 0:
      fyers_conn_var = fyers_conn()
      stocks_ltp_res = fyers_conn_var.quotes(active_stocks)['d']
    for i in stocks_ltp_res:
        stock_ltp[i['v']['short_name'].split('-')[0]] = i['v']['lp']
    active_entry_list = []
    for sym_list in active_entry:
      stock_config_obj = models.CONFIG_30M.objects.get(symbol = sym_list[0])
      active_entry_list.append({"symbol": sym_list[0] + '/HIT_{}'.format(stock_config_obj.count), "sector": stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,"price": stock_config_obj.buy_price, "quantity": stock_config_obj.quantity, "date": models_a.CROSSOVER_30_MIN.objects.get(id = sym_list[1]).date + timedelta(hours= 5 , minutes= 30),"placed": stock_config_obj.placed,"reference_id": sym_list[1],'ltp':stock_ltp[sym_list[0]]})
    response.update({'success': True, 'data': active_entry_list})
    return JsonResponse(response)
  return JsonResponse(response)

@api_view(['GET',])
def Transactions(request):
  response = {'success': False, 'data': None}
  if request.method == 'GET':
    queryset      = models_a.CROSSOVER_30_MIN.objects.filter(created_on = date.today()).order_by('-date')
    serializer    = serializers.CROSSOVER_30_MIN_Serializer(queryset, many = True)
    response.update({'success': True, 'data': serializer.data})
    return JsonResponse(response)
  return JsonResponse(response)
