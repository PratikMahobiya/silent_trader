from django.db import models

# Create your models here.
class BB_5_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'BB_5_MIN'

class CROSSOVER_15_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    target   				= models.FloatField(verbose_name='TARGET_PRICE',blank=True,null=True,default=None)
    stoploss_percent        = models.FloatField(verbose_name='STOPLOSS (%)',blank=True,null=True,default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    order_id                = models.BigIntegerField(verbose_name='ORDER_ID',blank=True,null=True,default=None)
    order_status            = models.TextField(verbose_name='ORDER_STATUS',max_length=1000)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_15_MIN'

class CROSSOVER_SLFEMA_15_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    quantity                = models.BigIntegerField(verbose_name='QUANTITY')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    target_1   				= models.FloatField(verbose_name='TARGET_1',blank=True,null=True,default=None)
    target_2   				= models.FloatField(verbose_name='TARGET_2',blank=True,null=True,default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    stoploss_percent        = models.FloatField(verbose_name='STOPLOSS (%)',blank=True,null=True,default=None)
    order_id                = models.BigIntegerField(verbose_name='ORDER_ID',blank=True,null=True,default=None)
    order_status            = models.TextField(verbose_name='ORDER_STATUS',max_length=1000)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CROSSOVER_SLFEMA_15_MIN'

class CA_ATR_S30_15_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    target   				= models.FloatField(verbose_name='TARGET_PRICE',blank=True,null=True,default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    target_percent          = models.FloatField(verbose_name='TARGET (%)',blank=True,null=True,default=None)
    stoploss_percent        = models.FloatField(verbose_name='STOPLOSS (%)',blank=True,null=True,default=None)
    order_id                = models.BigIntegerField(verbose_name='ORDER_ID',blank=True,null=True,default=None)
    exit_id                 = models.BigIntegerField(verbose_name='EXIT_ID',blank=True,null=True,default=None)
    order_status            = models.TextField(verbose_name='ORDER_STATUS',max_length=1000)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'CA_ATR_S30_15_MIN'