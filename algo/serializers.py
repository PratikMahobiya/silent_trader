from rest_framework import serializers
from . import models

class BB_5_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.BB_5_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','lowerband','upperband','rsi','atr','difference','profit')

class CROSS_OVER_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.CROSS_OVER_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')

class TD_CA_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.TD_CA_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')

class TD_PACA_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.TD_PACA_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')

class TH_CA_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.TH_CA_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')

class TH_PACA_15_Min_Serializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.TH_PACA_15_MIN
		fields 	= ('date','symbol','indicate','type','close','stoploss','target','rsi','emamin','emamax','difference','profit','target_percent','trend_rsi','target_hit')