from rest_framework import serializers
from . import models

class RSI_55_5_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.RSI_55_5_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent')

class RSI_55_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.RSI_55_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent')