from rest_framework import serializers
from . import models

class ZERODHA_KEYS_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.ZERODHA_KEYS
		fields 	= ('access_token','api_key','api_secret')

class CROSSOVER_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN
		fields 	= ('date','symbol','indicate','type','close','quantity','stoploss','target','difference','profit','stoploss_percent','order_id','order_status')

class CROSSOVER_5_MIN_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_5_MIN
		fields 	= ('date','symbol','indicate','type','close','quantity','stoploss','target','difference','profit','stoploss_percent','order_id','order_status')

class CROSSOVER_15_Min_Serializer_db(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_db
		fields 	= ('date','symbol','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status')