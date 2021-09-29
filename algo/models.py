from django.db import models

# Create your models here.
class ZERODHA_KEYS(models.Model):
    access_token 					= models.CharField(max_length=100, verbose_name='access_token')
    api_key                         = models.CharField(max_length=100, verbose_name='api_key')
    api_secret                      = models.CharField(max_length=100, verbose_name='api_secret')
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'ZERODHA_KEYS'

class CROSSOVER_15_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    target   				= models.FloatField(verbose_name='TARGET')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    order_id                = models.BigIntegerField(verbose_name='ORDER_ID',blank=True,null=True,default=None)
    order_status            = models.TextField(verbose_name='ORDER_STATUS',max_length=1000)
    stoploss_percent        = models.FloatField(verbose_name='STOPLOSS (%)',blank=True,null=True,default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_15_MIN'

class CROSSOVER_5_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    target   				= models.FloatField(verbose_name='TARGET')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    order_id                = models.BigIntegerField(verbose_name='ORDER_ID',blank=True,null=True,default=None)
    order_status            = models.TextField(verbose_name='ORDER_STATUS',max_length=1000)
    stoploss_percent        = models.FloatField(verbose_name='STOPLOSS (%)',blank=True,null=True,default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_5_MIN'

# ------------------------------------------- CONFIG TABLES -------------------------------------------
class CROSSOVER_15_MIN_db(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField(auto_now_add=True)
    price    				= models.FloatField(verbose_name='PRICE')
    target   				= models.FloatField(verbose_name='TARGET')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    order_id                = models.BigIntegerField(verbose_name='ORDER_ID',blank=True,null=True,default=None)
    order_status            = models.TextField(verbose_name='ORDER_STATUS',max_length=1000)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_15_MIN_DB'

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
    sell_price              = models.FloatField(verbose_name='SELL PRICE',default=0)
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