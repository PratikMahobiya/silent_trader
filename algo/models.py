from django.db import models

# Create your models here.
class STOCK(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    instrument_key          = models.BigIntegerField(verbose_name='INSTRUMENT KEY')
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    active_15               = models.BooleanField(verbose_name='ACTIVE 15 Minute',default=True)
    active_30               = models.BooleanField(verbose_name='ACTIVE 30 Minute',default=True)
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

class PROFIT(models.Model):
    date                    = models.DateField(verbose_name='DATE',null=True, blank=True)
    model_name              = models.CharField(max_length=100, verbose_name='MODEL NAME')
    max_entry       		= models.BigIntegerField(verbose_name='MAX ENTRY',default=0)
    top_gain  				= models.FloatField(verbose_name='TOP GAIN',default=0)
    top_gain_time           = models.TimeField(verbose_name='TOP GAIN TIME',null=True, blank=True)
    top_gain_entry			= models.BigIntegerField(verbose_name='TOP GAIN ENTRY',default=0)
    top_loss  				= models.FloatField(verbose_name='TOP LOSS',default=0)
    top_loss_time           = models.TimeField(verbose_name='TOP LOSS TIME',null=True, blank=True)
    top_loss_entry			= models.BigIntegerField(verbose_name='TOP LOSS ENTRY',default=0)
    current_gain            = models.FloatField(verbose_name='CURRENT GAIN',default=0)
    current_gain_time       = models.TimeField(verbose_name='CURRENT GAIN TIME',null=True, blank=True)
    current_gain_entry		= models.BigIntegerField(verbose_name='TOTAL ENTRY',default=0)
    p_l                     = models.FloatField(verbose_name='P/L(%)',default=0)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'PROFIT'

class PROFIT_CONFIG(models.Model):
    model_name              = models.CharField(max_length=100, verbose_name='MODEL NAME')
    active                  = models.BooleanField(verbose_name='ACTIVE',default=False)
    count                   = models.BigIntegerField(verbose_name='HIT_COUNT',default=0)
    day_hit                 = models.BigIntegerField(verbose_name='DAY_HIT',default=1)
    target                  = models.FloatField(verbose_name='TARGET',default=0)
    stoploss                = models.FloatField(verbose_name='STOPLOSS',default=0)
    entry                   = models.BigIntegerField(verbose_name='NUM. OF ENT',default=0)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'PROFIT_CONFIG'

class FREEZE_PROFIT(models.Model):
    date                    = models.DateField(auto_now_add=True)
    model_name              = models.CharField(max_length=100, verbose_name='MODEL NAME')
    time                    = models.TimeField(auto_now_add=True)
    indicate                = models.CharField(max_length=100, verbose_name='INDICATE')
    price                   = models.FloatField(verbose_name='PRICE')
    p_l                     = models.FloatField(verbose_name='PROFIT')
    entry                   = models.BigIntegerField(verbose_name='NUM. OF ENT')
    day_hit                 = models.CharField(max_length=100, verbose_name='DAY_HIT')
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'FREEZE_PROFIT'
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
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_15_MIN'

class CROSSOVER_30_MIN(models.Model):
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
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_30_MIN'

# -------------------------------------- Not Active ---------------------------------------
class CROSSOVER_15_MIN_TEMP(models.Model):
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
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_15_MIN_TEMP'

class CROSSOVER_30_MIN_TEMP(models.Model):
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
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_30_MIN_TEMP'