from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.

@admin.register(models.ZERODHA_KEYS)
class ZERODHA_KEYS_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('access_token','api_key','api_secret')
    list_per_page = 10
    readonly_fields = ('access_token','api_key','api_secret')

@admin.register(models.STOCK)
class STOCK_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','instrument_key','active')

@admin.register(models.TREND_15M)
class TREND_15M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','rsi')

@admin.register(models.ENTRY_15M)
class ENTRY_15M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol',)

@admin.register(models.CONFIG_15M)
class CONFIG_15M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','buy','trend','d_sl_flag','buy_price','sell_price','stoploss','target','f_stoploss','d_stoploss','quantity','count','order_id','order_status')

@admin.register(models.CROSSOVER_15_MIN)
class CROSSOVER_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','target','stoploss','profit','order_id','stoploss_percent','difference','quantity','order_status')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_5_MIN)
class CROSSOVER_5_MIN_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','target','stoploss','profit','order_id','stoploss_percent','difference','quantity','order_status')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_15_MIN_db)
class CROSSOVER_15_Min_Admin_db(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','order_status')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']