from django.db import models

# Create your models here.
class STOCK(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    instrument_key          = models.BigIntegerField(verbose_name='INSTRUMENT KEY')
    active                  = models.BooleanField(verbose_name='ACTIVE',default=True)
    def __str__(self):
        return self.symbol
    class Meta:
        db_table = 'STOCK'

class TREND_15M(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    rsi                     = models.FloatField(verbose_name='RSI')
    class Meta:
        db_table = 'TREND_15M'

class ENTRY_15M(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    class Meta:
        db_table = 'ENTRY_15M'

class CONFIG_15M(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    buy                     = models.BooleanField(verbose_name='BUY',default=False)
    trend                   = models.BooleanField(verbose_name='IN_TREND',default=False)
    d_sl_flag               = models.BooleanField(verbose_name='D_SL_FLAG',default=False)
    buy_price               = models.FloatField(verbose_name='BUY PRICE',default=0)
    stoploss                = models.FloatField(verbose_name='STOPLOSS',default=0)
    target                  = models.FloatField(verbose_name='TARGET',default=0)
    f_stoploss              = models.FloatField(verbose_name='F_SL',default=0)
    d_stoploss              = models.FloatField(verbose_name='D_SL',default=0)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY',default=0)
    count                   = models.BigIntegerField(verbose_name='COUNT',default=0)
    order_id                = models.BigIntegerField(verbose_name='ORDER ID',default=0)
    order_status            = models.CharField(max_length=100, verbose_name='ORDER STATUS',default='NONE')
    class Meta:
        db_table = 'CONFIG_15M'