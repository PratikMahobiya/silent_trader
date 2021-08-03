from rest_framework import serializers
from . import models

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.Transactions
		fields 	= ('date','symbol','indicate','type','close','stoploss','rsi','rsi_exit_target','difference','profit')