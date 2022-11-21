from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls', namespace='weather')),
    path('users/', include('users.urls', namespace='users'))
]
