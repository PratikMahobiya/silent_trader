from NSE_BSE import models
from algo import models as models_a
from . import serializers
import nse_action
import bse_action

def entry(stock_config_obj, symbol, nse_p, bse_p, kite_conn_var, zerodha_flag_obj):
  if (abs(nse_p - bse_p)/100 > 0.5) and stock_config_obj.entry_sec > 10:
    if nse_p > bse_p:
      order_id_bse, order_status_bse, price_bse, quantity = bse_action.place_regular_buy_order_ENT(kite_conn_var,symbol, bse_p, zerodha_flag_obj)
      order_id_nse, order_status_nse, price_nse, quantity = nse_action.place_regular_sell_order_ENT(kite_conn_var,symbol, nse_p, zerodha_flag_obj)
      if order_id_bse != 0:
        stock_config_obj.placed_bse       = True
      if order_id_nse != 0:
        stock_config_obj.placed_nse       = True
      # UPDATE CONFIG
      type_str         = 'AF_SELL'
      stock_config_obj.buy            = True
      stock_config_obj.counter_flag            = True
      stock_config_obj.quantity       = quantity
      stock_config_obj.buy_price_bse      = price_bse
      stock_config_obj.buy_price_nse      = price_nse
      stock_config_obj.order_id_bse       = order_id_bse
      stock_config_obj.order_id_nse       = order_id_nse
      stock_config_obj.order_status_bse   = order_status_bse
      stock_config_obj.order_status_nse   = order_status_nse
      stock_config_obj.save()
      # TRANSACTION TABLE UPDATE
      trans_data = {'symbol':symbol,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price_bse':price_bse,'price_nse':price_nse,'quantity':quantity,'difference':None,'profit':None,'order_id_bse':order_id_bse,'order_id_nse':order_id_nse,'order_status_bse':order_status_bse,'order_status_nse':order_status_nse}
      transaction   = serializers.NSE_BSE_SERIALIZER(data=trans_data)
      if transaction.is_valid():
        transaction.save()
    else:
      order_id_bse, order_status_bse, price_bse, quantity = bse_action.place_regular_sell_order_ENT(kite_conn_var,symbol, bse_p, zerodha_flag_obj)
      order_id_nse, order_status_nse, price_nse, quantity =  nse_action.place_regular_buy_order_ENT(kite_conn_var,symbol, nse_p, zerodha_flag_obj)
      if order_id_bse != 0:
        stock_config_obj.placed_bse       = True
      if order_id_nse != 0:
        stock_config_obj.placed_nse       = True
      # UPDATE CONFIG
      type_str         = 'AF_SELL'
      stock_config_obj.buy            = True
      stock_config_obj.counter_flag            = True
      stock_config_obj.quantity       = quantity
      stock_config_obj.buy_price_bse      = price_bse
      stock_config_obj.buy_price_nse      = price_nse
      stock_config_obj.order_id_bse       = order_id_bse
      stock_config_obj.order_id_nse       = order_id_nse
      stock_config_obj.order_status_bse   = order_status_bse
      stock_config_obj.order_status_nse   = order_status_nse
      stock_config_obj.save()
      # TRANSACTION TABLE UPDATE
      trans_data = {'symbol':symbol,'sector':stock_config_obj.sector,'niftytype':stock_config_obj.niftytype,'indicate':'Entry','type':type_str,'price_bse':price_bse,'price_nse':price_nse,'quantity':quantity,'difference':None,'profit':None,'order_id_bse':order_id_bse,'order_id_nse':order_id_nse,'order_status_bse':order_status_bse,'order_status_nse':order_status_nse}
      transaction   = serializers.NSE_BSE_SERIALIZER(data=trans_data)
      if transaction.is_valid():
        transaction.save()

def exit(stock_config_obj,nse_p, bse_p, kite_conn_var):
  pass