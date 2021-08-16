from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.BB_5_MIN)
class BB_5_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','lowerband','upperband','rsi','atr','difference','profit')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSS_OVER_15_MIN)
class CROSS_OVER_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.TD_CA_15_MIN)
class TD_CA_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.TD_PACA_15_MIN)
class TD_PACA_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.TH_CA_15_MIN)
class TH_CA_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.TH_PACA_15_MIN)
class TH_PACA_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']
