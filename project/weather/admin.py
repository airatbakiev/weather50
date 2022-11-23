from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import TextInput, Textarea

from . import models


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country_name', 'country', 'lat', 'lon')


class ConditionInLine(admin.TabularInline):
    model = models.WeatherCondition


class ConditionAdmin(admin.ModelAdmin):
    list_display = ('condition_id', 'main', 'description', 'icon')


class WeatherConditionAdmin(admin.ModelAdmin):
    list_display = ('weather', 'condition')


class MainParamsInLine(admin.TabularInline):
    model = models.MainParams


class MainParamsAdmin(admin.ModelAdmin):
    list_display = ('weather_collect', 'temp', 'feels_like', 'pressure',
                    'humidity', 'temp_min', 'temp_max', 'sea_level',
                    'grnd_level')


class WindInLine(admin.TabularInline):
    model = models.Wind


class WindAdmin(admin.ModelAdmin):
    list_display = ('weather_collect', 'speed', 'deg', 'gust')


class CloudsInLine(admin.TabularInline):
    model = models.Clouds


class CloudsAdmin(admin.ModelAdmin):
    list_display = ('weather_collect', 'all')


class RainInLine(admin.TabularInline):
    model = models.Rain


class RainAdmin(admin.ModelAdmin):
    list_display = ('weather_collect', 'one_h', 'three_h')


class SnowInLine(admin.TabularInline):
    model = models.Snow


class SnowAdmin(admin.ModelAdmin):
    list_display = ('weather_collect', 'one_h', 'three_h')


class WeatherCollectAdmin(admin.ModelAdmin):
    list_display = ('city', 'created', 'iter_id')
    inlines = [ConditionInLine, MainParamsInLine, WindInLine, CloudsInLine,
               RainInLine, SnowInLine]
    search_fields = ('iter_id', )
    list_filter = ('created', 'city')


admin.site.register(models.City, CityAdmin)
admin.site.register(models.MainParams, MainParamsAdmin)
admin.site.register(models.Wind, WindAdmin)
admin.site.register(models.Clouds, CloudsAdmin)
admin.site.register(models.Rain, RainAdmin)
admin.site.register(models.Snow, SnowAdmin)
admin.site.register(models.WeatherCollect, WeatherCollectAdmin)
admin.site.register(models.Condition, ConditionAdmin)
admin.site.register(models.WeatherCondition, WeatherConditionAdmin)
