"""
URL configuration for knitwits project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('stock-status/', views.stock_status, name='stock_status'),
    path('low-stock/', views.low_stock, name='low_stock'),
    path('out-of-stock/', views.out_of_stock, name='out_of_stock'),
    path('pick-list/', views.all_pick_list, name='pick_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('thresholds/', views.thresholds, name='thresholds'),
    path('threshholds/', views.thresholds, name='thresholds_legacy'),
]
