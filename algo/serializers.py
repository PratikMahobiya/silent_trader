from rest_framework import serializers
from . import models

class BB_5_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.BB_5_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','difference','profit')

class CROSSOVER_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','difference','profit','stoploss_percent','order_id','order_status')

class CA_SLFEMA_15_MIN_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CA_SLFEMA_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','difference','profit','target_percent','order_id','exit_id','order_status','stoploss_percent')

class CA_ATR_S30_15_MIN_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CA_ATR_S30_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','difference','profit','target_percent','order_id','exit_id','order_status','stoploss_percent')
