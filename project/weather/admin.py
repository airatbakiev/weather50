from django.contrib import admin

from . import models


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country_name', 'country', 'lat', 'lon')


class WeatherAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')


admin.site.register(models.City, CityAdmin)
admin.site.register(models.WeatherCollect, WeatherAdmin)
