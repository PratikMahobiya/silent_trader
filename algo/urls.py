from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'TransactionView', views.TransactionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('', include(router.urls)),
    path(r'model_55', views.Model_55, name = 'RSI_55'),
]