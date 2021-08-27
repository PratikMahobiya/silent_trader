from rest_framework import serializers
from . import models

class BB_5_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.BB_5_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','difference','profit')

class TH_CA_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.TH_CA_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','difference','profit','target_percent')

class TH_PACA_T2_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.TH_PACA_T2_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','difference','profit','target_percent','order_id','exit_id','order_status')
