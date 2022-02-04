from django.urls import path, include
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('', views.Index_FYERS, name='index'),
	path('check_fyers/', views.check_fyers, name='check_fyers'),
	path('generate_token_fyers/', views.generate_fyers_acc_token, name='generate_token_fyers'),
	

	path('model_status/', views.MODEL_STATUS, name='Model Status'),
	path('exit_all/', views.FREEZE_ALL, name='Freeze All'),
]