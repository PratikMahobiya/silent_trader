"""silent_trader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from algo import urls as aurls
from Model_15M import urls as MODEL_15M_urls
from Model_15_temp import urls as MODEL_15M_TEMP_urls
from Model_30M import urls as MODEL_30M_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(aurls)),
    path('crs15m/', include(MODEL_15M_urls)),
    path('crs15mtemp/', include(MODEL_15M_TEMP_urls)),
    path('crs30m/', include(MODEL_30M_urls)),
]
