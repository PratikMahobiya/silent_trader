from rest_framework import serializers
from . import models

class FYERS_KEYS_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.FYERS_KEYS
		fields 	= ('access_token','app_id','app_secret')

class CROSSOVER_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date','placed')

class CROSSOVER_30_MIN_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_30_MIN
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date','placed')

# -------------------------------------- Not Active ---------------------------------------
class CROSSOVER_15_Min_Serializer_TEMP(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_TEMP
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date','placed')

class CROSSOVER_15_Min_Serializer_TEMP_DOWN(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSSOVER_15_MIN_TEMP_DOWN
		fields 	= ('id','symbol','sector','niftytype','indicate','type','price','quantity','stoploss','target','difference','profit','order_id','order_status','date','placed')
