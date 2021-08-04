from django.db import models

# Create your models here.
class RSI_55_5_MIN(models.Model):
    date                    = models.DateTimeField()
    symbol 					= models.CharField(max_length=100, verbose_name='SYMBOL')
    indicate    			= models.CharField(max_length=100, verbose_name='INDICATE')
    type           			= models.CharField(max_length=100, verbose_name='TYPE')
    close    				= models.FloatField(verbose_name='PRICE')
    stoploss   				= models.FloatField(verbose_name='STOPLOSS')
    rsi   			    	= models.FloatField(verbose_name='RSI')
    rsi_exit_target			= models.FloatField(verbose_name='RSI_TARGET', blank=True, null=True, default=None)
    difference 				= models.FloatField(verbose_name='PRICE DIFFERENCE', blank=True, null=True,default=None)
    profit 				    = models.FloatField(verbose_name='PROFIT (%)',blank=True,null=True,default=None)
    def __int__(self):
    	return self.id
    class Meta:
        db_table = 'RSI_55_5_MIN'