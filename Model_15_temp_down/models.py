from django.db import models

# Create your models here.
class TREND_15M_A_TEMP_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    rsi                     = models.FloatField(verbose_name='RSI')
    time                    = models.DateTimeField(auto_now_add=True,verbose_name='TIME',null=True,blank=True)
    class Meta:
        db_table = 'TREND_15M_A_TEMP_DOWN'

class TREND_15M_A_TEMP_BTST_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    rsi                     = models.FloatField(verbose_name='RSI')
    time                    = models.DateTimeField(auto_now_add=True,verbose_name='TIME',null=True,blank=True)
    class Meta:
        db_table = 'TREND_15M_A_TEMP_BTST_DOWN'

class ENTRY_15M_TEMP_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    time                    = models.DateTimeField(auto_now_add=True,verbose_name='TIME',null=True,blank=True)
    reference_id            = models.BigIntegerField(verbose_name='REFERENCE ID',default=0)
    class Meta:
        db_table = 'ENTRY_15M_TEMP_DOWN'

class ENTRY_15M_TEMP_BTST_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    time                    = models.DateTimeField(auto_now_add=True,verbose_name='TIME',null=True,blank=True)
    reference_id            = models.BigIntegerField(verbose_name='REFERENCE ID',default=0)
    class Meta:
        db_table = 'ENTRY_15M_TEMP_BTST_DOWN'

class CONFIG_15M_TEMP_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    buy                     = models.BooleanField(verbose_name='BUY',default=False)
    trend                   = models.BooleanField(verbose_name='IN_TREND',default=False)
    d_sl_flag               = models.BooleanField(verbose_name='D_SL_FLAG',default=False)
    placed                  = models.BooleanField(verbose_name='PLACED',default=False)
    fixed_target_flag       = models.BooleanField(verbose_name='FIXED_TR_FLAG',default=False)
    buy_price               = models.FloatField(verbose_name='BUY PRICE',default=0)
    stoploss                = models.FloatField(verbose_name='STOPLOSS',default=0)
    target                  = models.FloatField(verbose_name='TARGET',default=0)
    fixed_target            = models.FloatField(verbose_name='FIXED TARGET',default=0)
    last_top                = models.FloatField(verbose_name='LAST TOP',default=0)
    f_stoploss              = models.FloatField(verbose_name='F_SL',default=0)
    d_stoploss              = models.FloatField(verbose_name='D_SL',default=0)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY',default=0)
    count                   = models.BigIntegerField(verbose_name='COUNT',default=0)
    return_price            = models.FloatField(verbose_name='RET_PRICE',default=0)
    ltp                     = models.FloatField(verbose_name='LTP',default=0)
    order_id                = models.BigIntegerField(verbose_name='ORDER ID',default=0)
    order_status            = models.CharField(max_length=100, verbose_name='ORDER STATUS',default='NONE')
    class Meta:
        db_table = 'CONFIG_15M_TEMP_DOWN'

class CONFIG_15M_TEMP_BTST_DOWN(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    buy                     = models.BooleanField(verbose_name='BUY',default=False)
    trend                   = models.BooleanField(verbose_name='IN_TREND',default=False)
    d_sl_flag               = models.BooleanField(verbose_name='D_SL_FLAG',default=False)
    placed                  = models.BooleanField(verbose_name='PLACED',default=False)
    fixed_target_flag       = models.BooleanField(verbose_name='FIXED_TR_FLAG',default=False)
    buy_price               = models.FloatField(verbose_name='BUY PRICE',default=0)
    stoploss                = models.FloatField(verbose_name='STOPLOSS',default=0)
    target                  = models.FloatField(verbose_name='TARGET',default=0)
    fixed_target            = models.FloatField(verbose_name='FIXED TARGET',default=0)
    last_top                = models.FloatField(verbose_name='LAST TOP',default=0)
    f_stoploss              = models.FloatField(verbose_name='F_SL',default=0)
    d_stoploss              = models.FloatField(verbose_name='D_SL',default=0)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY',default=0)
    count                   = models.BigIntegerField(verbose_name='COUNT',default=0)
    return_price            = models.FloatField(verbose_name='RET_PRICE',default=0)
    ltp                     = models.FloatField(verbose_name='LTP',default=0)
    order_id                = models.BigIntegerField(verbose_name='ORDER ID',default=0)
    order_status            = models.CharField(max_length=100, verbose_name='ORDER STATUS',default='NONE')
    class Meta:
        db_table = 'CONFIG_15M_TEMP_BTST_DOWN'