from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('delete/<path:place_name>/', views.delete, name="delete"),
    path('', views.home, name="home"),

]