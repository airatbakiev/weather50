from django.urls import path

from . import views

app_name = 'weather'

urlpatterns = [
    path('cities/', views.get_cities, name='cities'),
    path('data/', views.get_weather, name='data')
]
