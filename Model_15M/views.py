from algo import models, serializers
from django.http import JsonResponse
from django.shortcuts import render
from kiteconnect import KiteConnect
from datetime import datetime, date, timedelta

from Model_15M import models as models_15_MAIN

from rest_framework.decorators import api_view

# Create your views here.
def CRS_MAIN_VIEW(request):
  return render(request, 'dashboard_15_main.html')

def connect_to_kite_connection():
  api_key = open('../algo/config/api_key.txt','r').read()
  access_token = models.ZERODHA_KEYS.objects.get(api_key=api_key).access_token
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
    kite_conn_var = connect_to_kite_connection()
    order_id = kite_conn_var.place_order(tradingsymbol=symbol,
                                exchange=kite_conn_var.EXCHANGE_NSE,
                                transaction_type=kite_conn_var.TRANSACTION_TYPE_BUY,
                                quantity=quantity,
                                variety=kite_conn_var.VARIETY_REGULAR,
                                order_type=kite_conn_var.ORDER_TYPE_LIMIT,
                                product=kite_conn_var.PRODUCT_MIS,
                                validity=kite_conn_var.VALIDITY_DAY,
                                price=price,
                                )
    order_status = 'SUCCESSFULLY_PLACED_ENTRY'
  except Exception as e:
    order_status = 'PROBLEM AT ZERODHA END.'
  return order_id, order_status

def place_regular_sell_order(symbol, stock_config_obj):
  # Place an order
  order_id = 0
  error_status = 'NOT_PLACED'
  try:
    kite_conn_var = connect_to_kite_connection()
    stocks_ltp = kite_conn_var.ltp('NSE:'+symbol)
    ltp        = stocks_ltp['NSE:'+symbol]['last_price']
    order_id = kite_conn_var.place_order(tradingsymbol=symbol,
                                exchange=kite_conn_var.EXCHANGE_NSE,
                                transaction_type=kite_conn_var.TRANSACTION_TYPE_SELL,
                                quantity=stock_config_obj.quantity,
                                variety=kite_conn_var.VARIETY_REGULAR,
                                order_type=kite_conn_var.ORDER_TYPE_MARKET,
                                product=kite_conn_var.PRODUCT_MIS,
                                validity=kite_conn_var.VALIDITY_DAY,
                                )
    error_status = 'SUCCESSFULLY_PLACED_EXIT'
  except Exception as e:
    error_status = 'PROBLEM AT ZERODHA END.'
  return order_id, error_status, ltp

@api_view(['GET','POST'])
def PLACE_ORDER(request):
  if request.method == 'POST':
    reference_id  = int(request.data['reference_id'])
    symbol        = request.data['symbol']
    price         = int(request.data['price'])
    quantity      = int(request.data['quantity'])
    # order_id, order_status = place_regular_buy_order(symbol, price, quantity)
    order_id, order_status = 1 , 'NOT ACTIVE'
    if order_id != 0:
      models_15_MAIN.CONFIG_15M.objects.filter(symbol = symbol).update(placed = True, buy_price = price, quantity = quantity, order_id = order_id, order_status = order_status)
      models.CROSSOVER_15_MIN.objects.filter(symbol = symbol, id = reference_id).update(order_id = order_id, order_status = order_status, price = price, quantity = quantity)
      response      = {'success': True, 'status': '"{}" is PLACED. ORDER ID:- {}'.format(symbol,order_id)}
      return JsonResponse(response)
    response = {'success': False, 'status': '"{}" is NOT PLACED. ..TRY AGAIN..'.format(symbol)}
    return JsonResponse(response)
  response = {'success': False, 'status': 'WORNG METHOD {}.'.format(request.method)}
  return JsonResponse(response)

@api_view(['GET','POST'])
def EXIT_ORDER(request):
  if request.method == 'POST':
    symbol        = request.data['symbol']
    stock_config_obj = models_15_MAIN.CONFIG_15M.objects.get(symbol = symbol)
    if stock_config_obj.buy is True:
      # order_id, order_status, price = place_regular_sell_order(symbol, stock_config_obj)
      order_id, order_status, price  = 1 , 'NOT ACTIVE', 200
      if order_id != 0:
        diff          = price - stock_config_obj.buy_price
        profit        = round((((diff/stock_config_obj.buy_price) * 100)),2)
        diff          = round((diff * stock_config_obj.quantity),2) - 100
        trans_data = {'symbol':symbol,'sector':stock_config_obj.sector,'indicate':'Exit','type':'M_Exit','price':price,'quantity':stock_config_obj.quantity,'stoploss':stock_config_obj.stoploss,'target':stock_config_obj.target,'difference':diff,'profit':profit,'order_id':order_id,'order_status':order_status}
        transaction   = serializers.CROSSOVER_15_Min_Serializer(data=trans_data)
        if transaction.is_valid():
          transaction.save()
        models.ENTRY_15M.objects.filter(symbol = symbol).delete()
        models.TREND_15M_A.objects.filter(symbol = symbol).delete()
        stock_config_obj.buy          = False
        stock_config_obj.placed       = False
        stock_config_obj.d_sl_flag    = False
        stock_config_obj.trend        = False
        stock_config_obj.count        = 0
        stock_config_obj.order_id     = 0
        stock_config_obj.save()
        response      = {'success': True, 'status': '"{}" is EXITED. ORDER ID:- {}'.format(symbol,order_id)}
        return JsonResponse(response)
      response = {'success': False, 'status': '"{}" is NOT EXITED. ..TRY AGAIN..'.format(symbol)}
      return JsonResponse(response)
    response = {'success': False, 'status': 'WORNG METHOD {}.'.format(request.method)}
    return JsonResponse(response)

@api_view(['GET',])
def Active_Stocks(request):
  response = {'success': False, 'data': None}
  if request.method == 'GET':
    queryset      = models.CROSSOVER_15_MIN.objects.filter(created_on = (date.today() - timedelta(days=4)), indicate = 'Entry')
    serializer    = serializers.CROSSOVER_15_Min_Serializer(queryset, many = True)
    response.update({'success': True, 'data': serializer.data})
    
    # active_entry  = models_15_MAIN.ENTRY_15M.objects.all().values_list('symbol', 'reference_id', flat=True)
    # active_entry_list = []
    # for sym_list in active_entry:
    #   stock_config_obj = models_15_MAIN.CONFIG_15M.objects.get(symbol = sym_list[0])
    #   active_entry_list.append({"symbol": sym_list[0], "sector": stock_config_obj.sector,"price": stock_config_obj.buy_price, "quantity": stock_config_obj.quantity, "date": models.CROSSOVER_15_MIN.objects.get(id = sym_list[1]).date,"placed": stock_config_obj.placed,"reference_id": sym_list[1]})
    # response.update({'success': True, 'data': active_entry_list})

    return JsonResponse(response)
  return JsonResponse(response)

@api_view(['GET',])
def Transactions(request):
  response = {'success': False, 'data': None}
  if request.method == 'GET':
    queryset      = models.CROSSOVER_15_MIN.objects.filter(created_on = (date.today() - timedelta(days=4)))
    serializer    = serializers.CROSSOVER_15_Min_Serializer(queryset, many = True)
    response.update({'success': True, 'data': serializer.data})
    return JsonResponse(response)
  return JsonResponse(response)
