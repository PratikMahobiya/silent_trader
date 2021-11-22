from django.urls import path, include
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('dashboard/', views.CRS_VIEW, name='CRS_MAIN'),
	path('transactions/', views.Transactions, name='transactions'),
	path('active_stocks/', views.Active_Stocks, name='Active Stocks'),
	path('place_order/', views.PLACE_ORDER, name='Place Order'),
	path('exit_order/', views.EXIT_ORDER, name='Exit Order'),

	path('dashboard_btst/', views.CRS_BTST_VIEW, name='CRS_MAIN_btst'),
	path('transactions_btst/', views.Transactions_BTST, name='transactions_btst'),
	path('active_stocks_btst/', views.Active_Stocks_BTST, name='Active Stocks_btst'),
	path('place_order_btst/', views.PLACE_ORDER_BTST, name='Place Order_btst'),
	path('exit_order_btst/', views.EXIT_ORDER_BTST, name='Exit Order_btst'),
]