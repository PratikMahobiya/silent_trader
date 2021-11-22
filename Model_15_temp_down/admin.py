from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.TREND_15M_A_TEMP_DOWN)
class TREND_15M_A_TEMP_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','rsi','time')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.TREND_15M_A_TEMP_BTST_DOWN)
class TREND_15M_A_TEMP_BTST_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','rsi','time')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.ENTRY_15M_TEMP_DOWN)
class ENTRY_15M_TEMP_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','reference_id','time')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.ENTRY_15M_TEMP_BTST_DOWN)
class ENTRY_15M_TEMP_BTST_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','reference_id','time')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.CONFIG_15M_TEMP_DOWN)
class CONFIG_15M_TEMP_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','buy','trend','fixed_target_flag','d_sl_flag','placed','count','buy_price','stoploss','target','fixed_target','f_stoploss','d_stoploss','sector','niftytype','last_top','quantity','order_id','order_status')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.CONFIG_15M_TEMP_BTST_DOWN)
class CONFIG_15M_TEMP_BTST_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','buy','trend','fixed_target_flag','d_sl_flag','placed','count','buy_price','stoploss','target','fixed_target','f_stoploss','d_stoploss','sector','niftytype','last_top','quantity','order_id','order_status')
    list_per_page = 10
    search_fields = ['symbol',]