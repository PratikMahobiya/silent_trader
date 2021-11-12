from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.STOCK)
class STOCK_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','instrument_key','sector','active_15','active_30')
    search_fields = ['symbol',]

@admin.register(models.ZERODHA_KEYS)
class ZERODHA_KEYS_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('access_token','api_key','api_secret')
    list_per_page = 10
    readonly_fields = ('access_token','api_key','api_secret')

@admin.register(models.PROFIT)
class PROFIT_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','model_name','current_gain','current_gain_time','current_gain_entry','top_gain','top_gain_time','top_gain_entry','top_loss','top_loss_time','top_loss_entry','max_entry','p_l')
    list_filter = ("date",)

@admin.register(models.PROFIT_CONFIG)
class PROFIT_CONFIG_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('model_name','zerodha_entry','stock_amount','active','count','day_hit','target','stoploss','entry')

@admin.register(models.FREEZE_PROFIT)
class FREEZE_PROFIT_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','model_name','time','indicate','price','p_l','top_price','stoploss','day_hit','entry')
    list_filter = ("date",'model_name')

@admin.register(models.CROSSOVER_15_MIN)
class CROSSOVER_15_Min_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','sector','order_status')
    list_filter = ("created_on",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_15_MIN_BTST)
class CROSSOVER_15_Min_BTST_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','sector','order_status')
    list_filter = ("created_on",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_30_MIN)
class CROSSOVER_30_MIN_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','sector','order_status')
    list_filter = ("created_on",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_30_MIN_BTST)
class CROSSOVER_30_MIN_BTST_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','sector','order_status')
    list_filter = ("created_on",)
    list_per_page = 10
    search_fields = ['symbol','date']

# -------------------------------------- Not Active ---------------------------------------
@admin.register(models.CROSSOVER_15_MIN_TEMP)
class CROSSOVER_15_Min_TEMP_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','sector','order_status')
    list_filter = ("created_on",)
    list_per_page = 10
    search_fields = ['symbol','date']

@admin.register(models.CROSSOVER_15_MIN_TEMP_BTST)
class CROSSOVER_15_Min_TEMP_BTST_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('date','symbol','indicate','type','price','target','stoploss','profit','order_id','difference','quantity','sector','order_status')
    list_filter = ("created_on",)
    list_per_page = 10
    search_fields = ['symbol','date']