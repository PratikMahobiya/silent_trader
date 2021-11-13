from django.urls import path, include
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('', views.Index, name='index'),
	path('index/', views.Index, name='index'),
	path('check/', views.check, name='check'),
	path('generate_token/', views.generate_acc_token, name='generate_token'),

	path('M1/', views.CRS_MAIN_VIEW, name='CRS_MAIN'),
	path('transactions/', views.Transactions, name='transactions'),
	path('active_stocks/', views.Active_Stocks, name='Active Stocks'),
	path('place_order/', views.PLACE_ORDER, name='Place Order'),
	path('exit_order/', views.EXIT_ORDER, name='Exit Order'),
]