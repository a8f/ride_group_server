"""ridegroup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from ridegroup import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', views.connection_test, name='check_connection'),
    path('login/', views.login, name='auth_user'),
    path('register/', views.register, name='register'),
    path('create_ride/', views.create_ride, name='create_ride'),
    path('my_vehicles/', views.my_vehicles, name='my_vehicles'),
    path('create_vehicle/', views.create_vehicle, name='create_vehicle'),
    path('my_rides/', views.my_rides, name='my_rides'),
    path('ride_search/', views.ride_search, name='ride_search')
]
