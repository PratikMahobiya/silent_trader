from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.

@admin.register(models.CONFIG_15M)
class CONFIG_15M_Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('symbol','buy_nse','buy_bse','placed_nse','placed_bse','count_nse','count_bse','buy_price_nse','buy_price_bse','sector','niftytype','quantity','return_price_nse','return_price_bse','order_id_nse','order_id_bse','order_status_nse','order_status_bse')
    list_per_page = 10
    search_fields = ['symbol',]
