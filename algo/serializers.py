from rest_framework import serializers
from . import models

class RSI_55_5_MINSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.RSI_55_5_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','rsi','rsi_exit_target','difference','profit')