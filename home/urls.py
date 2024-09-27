# home/urls.py
from django.urls import path
from . import views  # Importamos las vistas desde el archivo views.py

urlpatterns = [
    path('', views.home, name = 'home')
]
