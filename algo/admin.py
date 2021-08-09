from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.RSI_55_5_MIN)
class RSI_55_5_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.RSI_55_15_MIN)
class RSI_55_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent')
    list_filter = ("date",)
    list_per_page = 10
    search_fields = ['symbol','date']
