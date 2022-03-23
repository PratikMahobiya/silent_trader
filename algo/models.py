from django.db import models

# Create your models here.
class STOCK(models.Model):
    symbol                  = models.CharField(max_length=100, verbose_name='SYMBOL',unique=True)
    instrument_key          = models.BigIntegerField(verbose_name='INSTRUMENT KEY')
    token                   = models.CharField(max_length=100, verbose_name='TOKEN')
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    active_15               = models.BooleanField(verbose_name='15 Minute',default=False)
    active_5_up             = models.BooleanField(verbose_name='5(UP) Minute',default=False)
    active_5_down           = models.BooleanField(verbose_name='5(DOWN) Minute',default=False)
    nifty_flag              = models.BooleanField(verbose_name='NIFTY FLAG',default=False)
    volatility				= models.FloatField(verbose_name='VOLATILITY(%)',default=0)
    vol_volatility			= models.FloatField(verbose_name='VOLUME VOLATILITY(%)',default=0)
    upper_lim				= models.FloatField(verbose_name='UPPER LIMIT',default=0)
    lower_lim				= models.FloatField(verbose_name='LOWER LIMIT',default=0)
    def __str__(self):
        return self.symbol
    class Meta:
        db_table = 'STOCK'

class FYERS_KEYS(models.Model):
    access_token 					= models.TextField(verbose_name='access_token',)
    app_id                          = models.CharField(max_length=100, verbose_name='app_id')
    app_secret                      = models.CharField(max_length=100, verbose_name='app_secret')
    def __int__(self):
        return self.id
    class Meta:
        db_table = 'FYERS_KEYS'

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
    entry_count       		= models.BigIntegerField(verbose_name='Entry Count',default=0)
    def __int__(self):
        return self.id
    class Meta:
        db_table = 'PROFIT'

class PROFIT_CONFIG(models.Model):
    model_name              = models.CharField(max_length=100, verbose_name='MODEL NAME')
    zerodha_entry           = models.BooleanField(verbose_name='ZERODHA ENTRY',default=False)
    stock_amount            = models.BigIntegerField(verbose_name='STOCK_AMOUNT',default=100000)
    active                  = models.BooleanField(verbose_name='ACTIVE',default=False)
    count                   = models.BigIntegerField(verbose_name='HIT_COUNT',default=0)
    day_hit                 = models.BigIntegerField(verbose_name='DAY_HIT',default=1)
    target                  = models.FloatField(verbose_name='TARGET',default=5000)
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
    top_price               = models.FloatField(verbose_name='TOP PRICE',default=0)
    stoploss                = models.FloatField(verbose_name='STOPLOSS',default=0)
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
    order_status            = models.TextField(verbose_name='ORDER_STATUS')
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    placed                  = models.BooleanField(verbose_name='PLACED',default=False)
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
    order_status            = models.TextField(verbose_name='ORDER_STATUS')
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    placed                  = models.BooleanField(verbose_name='PLACED',default=False)
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
    order_status            = models.TextField(verbose_name='ORDER_STATUS')
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    placed                  = models.BooleanField(verbose_name='PLACED',default=False)
    def __int__(self):
        return self.id
    class Meta:
        db_table = 'CROSSOVER_15_MIN_TEMP'

class CROSSOVER_15_MIN_TEMP_DOWN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField(auto_now_add=True)
    price    				= models.FloatField(verbose_name='PRICE')
    target   				= models.FloatField(verbose_name='TARGET')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    order_id                = models.BigIntegerField(verbose_name='ORDER_ID',blank=True,null=True,default=None)
    order_status            = models.TextField(verbose_name='ORDER_STATUS')
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    sector                  = models.CharField(max_length=100, verbose_name='SECTOR')
    niftytype               = models.CharField(max_length=100, verbose_name='NiftyType',null=True, blank=True)
    created_on              = models.DateField(auto_now_add=True,null=True,blank=True)
    placed                  = models.BooleanField(verbose_name='PLACED',default=False)
    def __int__(self):
        return self.id
    class Meta:
        db_table = 'CROSSOVER_15_MIN_TEMP_DOWN'
