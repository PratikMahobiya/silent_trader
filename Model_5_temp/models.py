from django.db import models

# Create your models here.
class TREND_5M_A_TEMP(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    rsi                     = models.FloatField(verbose_name='RSI')
    class Meta:
        db_table = 'TREND_5M_A_TEMP'

class TREND_5M_B_TEMP(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    rsi                     = models.FloatField(verbose_name='RSI')
    class Meta:
        db_table = 'TREND_5M_B_TEMP'

class TREND_5M_C_TEMP(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    rsi                     = models.FloatField(verbose_name='RSI')
    class Meta:
        db_table = 'TREND_5M_C_TEMP'

class ENTRY_5M_TEMP(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    class Meta:
        db_table = 'ENTRY_5M_TEMP'

class CONFIG_5M_TEMP(models.Model):
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
        db_table = 'CONFIG_5M_TEMP'