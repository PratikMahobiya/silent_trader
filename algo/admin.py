from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.STOCK)
class STOCK_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','instrument_key','active_15','active_5')
    search_fields = ['symbol',]

@admin.register(models.ZERODHA_KEYS)
class ZERODHA_KEYS_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('access_token','api_key','api_secret')
    list_per_page = 10
    readonly_fields = ('access_token','api_key','api_secret')

@admin.register(models.CROSSOVER_15_MIN)
class CROSSOVER_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','order_status')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_5_MIN)
class CROSSOVER_5_MIN_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','order_status')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']