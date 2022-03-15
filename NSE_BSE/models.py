from django.db import models

# Create your models here.
class CONFIG_NSE_BSE(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    buy                     = models.BooleanField(verbose_name='BUY',default=False)
    placed_nse                  = models.BooleanField(verbose_name='PLACED NSE',default=False)
    placed_bse                  = models.BooleanField(verbose_name='PLACED BSE',default=False)
    buy_price_nse               = models.FloatField(verbose_name='BP NSE',default=0)
    buy_price_bse               = models.FloatField(verbose_name='BP BSE',default=0)
    quantity                    = models.BigIntegerField(verbose_name='QUANTITY',default=0)
    count_nse                   = models.FloatField(verbose_name='COUNT NSE',default=0)
    count_bse                   = models.FloatField(verbose_name='COUNT BSE',default=0)
    return_price_nse            = models.FloatField(verbose_name='RET_PRICE NSE',default=0)
    return_price_bse            = models.FloatField(verbose_name='RET_PRICE BSE',default=0)
    ltp_nse                     = models.FloatField(verbose_name='LTP NSE',default=0)
    ltp_bse                     = models.FloatField(verbose_name='LTP BSE',default=0)
    order_id_nse                = models.BigIntegerField(verbose_name='ORDER ID NSE',default=0)
    order_id_bse                = models.BigIntegerField(verbose_name='ORDER ID BSE',default=0)
    order_status_nse            = models.TextField( verbose_name='ORDER STATUS NSE',default='NONE')
    order_status_bse            = models.TextField( verbose_name='ORDER STATUS BSE',default='NONE')
    counter_flag                = models.BooleanField(verbose_name='COUNTER FLAG',default=False)
    class Meta:
        db_table = 'CONFIG_NSE_BSE'
