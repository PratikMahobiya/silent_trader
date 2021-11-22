from rest_framework import serializers
from . import models

class ZERODHA_KEYS_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.ZERODHA_KEYS
		fields 	= ('access_token','api_key','api_secret')

class CROSSOVER_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')

class CROSSOVER_15_Min_BTST_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_BTST
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')

class CROSSOVER_30_MIN_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_30_MIN
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')

class CROSSOVER_30_MIN_BTST_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_30_MIN_BTST
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')

# -------------------------------------- Not Active ---------------------------------------
class CROSSOVER_15_Min_Serializer_TEMP(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_TEMP
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')

class CROSSOVER_15_Min_Serializer_TEMP_BTST(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_TEMP_BTST
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')

class CROSSOVER_15_Min_Serializer_TEMP_DOWN(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_TEMP_DOWN
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')

class CROSSOVER_15_Min_Serializer_TEMP_BTST_DOWN(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_TEMP_BTST_DOWN
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date')
