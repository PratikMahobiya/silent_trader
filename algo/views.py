from django.http.response import HttpResponse
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from . import serializers
from . import models

from . import tasks

# Create your views here.
