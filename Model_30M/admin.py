from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(models.ENTRY_30M)
class ENTRY_30M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','reference_id','time')
    list_per_page = 10
    search_fields = ['symbol',]

@admin.register(models.CONFIG_30M)
class CONFIG_30M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','buy''placed','count','buy_price','stoploss','target','sector','niftytype','quantity','return_price','order_id','order_status')
    list_per_page = 10
    search_fields = ['symbol',]
