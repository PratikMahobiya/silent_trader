from django.urls import path, include
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('', views.Index, name='index'),
	path('/generate_token/', views.generate_acc_token, name='index'),
]