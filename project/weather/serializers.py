from rest_framework import serializers

from . import models


class ConditionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='condition_id')

    class Meta:
        model = models.Condition
        fields = ('id', 'main', 'description', 'icon')


class MainParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainParams
        fields = ('temp', 'feels_like', 'pressure', 'humidity', 'temp_min',
                  'temp_max', 'sea_level', 'grnd_level')


class WindSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wind
        fields = ('speed', 'deg', 'gust')


class CloudsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clouds
        fields = ('all', )


class RainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rain
        fields = ('one_h', 'three_h')


class SnowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Snow
        fields = ('one_h', 'three_h')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    weather = ConditionSerializer(many=True)
    main = MainParamsSerializer(required=False)
    wind = WindSerializer(required=False)
    clouds = CloudsSerializer(required=False)
    rain = RainSerializer(required=False)
    snow = SnowSerializer(required=False)
    city = CitySerializer()

    class Meta:
        model = models.WeatherCollect
        fields = ('weather', 'main', 'visibility', 'wind', 'clouds', 'rain',
                  'snow', 'dt', 'timezone', 'city', 'iter_id')

    def create(self, validated_data):
        # Подготовка данных к записи
        condition_data = validated_data.pop('weather')
        main_data = validated_data.pop('main', None)
        wind_data = validated_data.pop('wind', None)
        clouds_data = validated_data.pop('clouds', None)
        rain_data = validated_data.pop('rain', None)
        if rain_data:
            one_h = rain_data.pop('1h', None)
            if one_h:
                rain_data['one_h'] = one_h
            three_h = rain_data.pop('3h', None)
            if three_h:
                rain_data['three_h'] = three_h
        snow_data = validated_data.pop('snow', None)
        if snow_data:
            one_h = snow_data.pop('1h', None)
            if one_h:
                snow_data['one_h'] = one_h
            three_h = snow_data.pop('3h', None)
            if three_h:
                snow_data['three_h'] = three_h
        city_dict = validated_data.pop('city')
        city = models.City.objects.filter(
            lat=city_dict['lat'], lon=city_dict['lon']
        ).first()
        # Запись данных в БД
        w_collect = models.WeatherCollect.objects.create(
            city=city, **validated_data
        )
        if main_data:
            models.MainParams.objects.create(
                weather_collect=w_collect, **main_data
            )
        if wind_data:
            models.Wind.objects.create(
                weather_collect=w_collect, **wind_data
            )
        if clouds_data:
            models.Clouds.objects.create(
                weather_collect=w_collect, **clouds_data
            )
        if rain_data:
            models.Rain.objects.create(
                weather_collect=w_collect, **rain_data
            )
        if snow_data:
            models.Snow.objects.create(
                weather_collect=w_collect, **snow_data
            )
        for condition in condition_data:
            current_condition, status = (
                models.Condition.objects.get_or_create(**condition)
            )
            models.WeatherCondition.objects.create(
                weather=w_collect,
                condition=current_condition
            )
        return w_collect
