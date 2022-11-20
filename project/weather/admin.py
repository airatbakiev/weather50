from django.contrib import admin

from .models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country_name', 'country', 'lat', 'lon')


admin.site.register(City, CityAdmin)
