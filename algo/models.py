from django.db import models

# Create your models here.
class STOCK(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    instrument_key          = models.BigIntegerField(verbose_name='INSTRUMENT KEY')
    active_15               = models.BooleanField(verbose_name='ACTIVE 15 Minute',default=True)
    active_5                = models.BooleanField(verbose_name='ACTIVE 5 Minute',default=True)
    def __str__(self):
        return self.symbol
    class Meta:
        db_table = 'STOCK'

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