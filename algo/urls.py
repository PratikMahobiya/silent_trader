from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'RSI_60_40_5_MIN', views.RSI_60_40_5_MIN_ViewSet)
router.register(r'RSI_55_15_MIN', views.RSI_55_15_MIN_ViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('', include(router.urls)),
    path(r'RSI_60_40_5_MIN', views.RSI_60_40_5_MIN, name = 'RSI_60_40_5_MIN'),
    path(r'RSI_55_15_MIN', views.RSI_55_15_MIN, name = 'RSI_55_15_MIN'),
]