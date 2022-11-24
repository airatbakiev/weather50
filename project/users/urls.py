from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.users_def, name='users'),
]