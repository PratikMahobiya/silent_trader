from django.db import models

# Create your models here.
class RSI_55_5_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    target   				= models.FloatField(verbose_name='TARGET_PRICE',blank=True,null=True,default=None)
    rsi   			    	= models.FloatField(verbose_name='RSI')
    emamin      			= models.FloatField(verbose_name='EMA_MAX', blank=True, null=True, default=None)
    emamax      			= models.FloatField(verbose_name='EMA_MIN', blank=True, null=True, default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    target_percent          = models.FloatField(verbose_name='TARGET (%)',blank=True,null=True,default=None)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'RSI_55_5_MIN'

class RSI_55_15_MIN(models.Model):
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    date                    = models.DateTimeField()
    close    				= models.FloatField(verbose_name='PRICE')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    target   				= models.FloatField(verbose_name='TARGET_PRICE',blank=True,null=True,default=None)
    rsi   			    	= models.FloatField(verbose_name='RSI')
    emamin      			= models.FloatField(verbose_name='EMA_MAX', blank=True, null=True, default=None)
    emamax      			= models.FloatField(verbose_name='EMA_MIN', blank=True, null=True, default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    target_percent          = models.FloatField(verbose_name='TARGET (%)',blank=True,null=True,default=None)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'RSI_55_15_MIN'