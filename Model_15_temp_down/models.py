from django.db import models

# Create your models here.
class ENTRY_15M_TEMP_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    time                    = models.DateTimeField(auto_now_add=True,verbose_name='TIME',null=True,blank=True)
    reference_id            = models.BigIntegerField(verbose_name='REFERENCE ID',default=0)
    class Meta:
        db_table = 'ENTRY_15M_TEMP_DOWN'

class CONFIG_15M_TEMP_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    buy                     = models.BooleanField(verbose_name='BUY',default=False)
    placed                  = models.BooleanField(verbose_name='PLACED',default=False)
    buy_price               = models.FloatField(verbose_name='BUY PRICE',default=0)
    stoploss                = models.FloatField(verbose_name='STOPLOSS',default=0)
    target                  = models.FloatField(verbose_name='TARGET',default=0)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY',default=0)
    count                   = models.FloatField(verbose_name='COUNT',default=0)
    return_price            = models.FloatField(verbose_name='RET_PRICE',default=0)
    ltp                     = models.FloatField(verbose_name='LTP',default=0)
    order_id                = models.BigIntegerField(verbose_name='ORDER ID',default=0)
    order_status            = models.TextField( verbose_name='ORDER STATUS',default='NONE')
    class Meta:
        db_table = 'CONFIG_15M_TEMP_DOWN'