from django.urls import path

from weather import views

app_name = 'main'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('cities/', views.get_cities, name='cities'),
    path('weather/', views.get_weather, name='weather')
]
