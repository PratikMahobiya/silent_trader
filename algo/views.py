from django.http.response import HttpResponse
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from . import serializers
from . import models

from . import tasks

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.RSI_55_5_MIN.objects.all()
    serializer_class = serializers.TransactionSerializer

def Model_55(request):
  tasks.RSI_55_RUNS_5_MIN.delay()
  return HttpResponse("STARTED:--")
