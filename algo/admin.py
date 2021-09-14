from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.BB_5_MIN)
class BB_5_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','difference','profit')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_15_MIN)
class CROSSOVER_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','quantity','stoploss','target','stoploss_percent','difference','profit','order_id','order_status')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_SLFEMA_15_MIN)
class CROSSOVER_SLFEMA_15_MIN_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','quantity','stoploss','target_05','target_075','target_1','target_2','difference','profit','stoploss_percent','order_id','order_status')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CA_ATR_S30_15_MIN)
class CA_ATR_S30_15_MIN_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','quantity','stoploss','target','difference','profit','target_percent','order_id','exit_id','order_status','stoploss_percent')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']
