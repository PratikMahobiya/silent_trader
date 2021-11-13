from django.urls import path, include
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('', views.Index, name='index'),
	path('index/', views.Index, name='index'),
	path('check/', views.check, name='check'),
	path('generate_token/', views.generate_acc_token, name='generate_token'),

	path('transactions/', views.transactions, name='transactions'),
]