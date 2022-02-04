from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.ENTRY_15M_TEMP_DOWN)
class ENTRY_15M_TEMP_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','reference_id','time')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.CONFIG_15M_TEMP_DOWN)
class CONFIG_15M_TEMP_Admin_DOWN(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','buy','placed','count','buy_price','stoploss','target','sector','niftytype','quantity','return_price','order_id','order_status')
    list_per_page = 10
    search_fields = ['symbol',]
