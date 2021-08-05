from django.http.response import HttpResponse
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from . import serializers
from . import models

from . import tasks

# Create your views here.
class RSI_55_5_MIN_ViewSet(viewsets.ModelViewSet):
    queryset = models.RSI_55_5_MIN.objects.all()
    serializer_class = serializers.RSI_55_5_Min_Serializer

class RSI_55_15_MIN_ViewSet(viewsets.ModelViewSet):
    queryset = models.RSI_55_15_MIN.objects.all()
    serializer_class = serializers.RSI_55_15_Min_Serializer

def RSI_55_5_MIN(request):
  tasks.RSI_55_RUNS_5_MIN.delay()
  return HttpResponse("RSI_55_5_MIN_STARTED:--")

def RSI_55_15_MIN(request):
  tasks.RSI_55_RUNS_15_MIN.delay()
  return HttpResponse("RSI_55_15_MIN_STARTED:--")
