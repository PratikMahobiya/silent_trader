from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.TREND_5M_A)
class TREND_5M_A_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','rsi')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.TREND_5M_B)
class TREND_5M_B_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','rsi')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.TREND_5M_C)
class TREND_5M_C_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','rsi')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.ENTRY_5M)
class ENTRY_5M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol',)
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.CONFIG_5M)
class CONFIG_5M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','buy','trend','d_sl_flag','buy_price','stoploss','target','f_stoploss','d_stoploss','quantity','count','order_id','order_status')
    list_per_page = 10
    search_fields = ['symbol',]