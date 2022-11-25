from django.urls import path

from weather import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name='weather'),
]
