from rest_framework import serializers

from . import models


# class ConditionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Condition
#         fields = '__all__'


class MainParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainParams
        fields = '__all__'


class WindSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wind
        fields = '__all__'


class CloudsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clouds
        fields = '__all__'


class RainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rain
        fields = '__all__'


class SnowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Snow
        fields = '__all__'


# class CitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.City
#         fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    # weather = ConditionSerializer(many=True)
    main = MainParamsSerializer(required=False)
    wind = WindSerializer(required=False)
    clouds = CloudsSerializer(required=False)
    rain = RainSerializer(required=False)
    snow = SnowSerializer(required=False)
    # city = CitySerializer()

    class Meta:
        model = models.WeatherCollect
        fields = (
            # 'weather',
            'main',
            'visibility',
            'wind',
            'clouds',
            'rain',
            'snow',
            'dt',
            'timezone',
            # 'city',
        )

    def create(self, validated_data):
        # Подготовка данных к записи
        # condition_data = validated_data.pop('weather')
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
        # city = models.City.objects.filter(
        #     lat=coord['lat'], lon=coord['lon']
        # ).first()
        # validated_data['city'] = city
        # Запись данных в БД
        main = models.MainParams.objects.create(**main_data)
        wind = models.Wind.objects.create(**wind_data)
        clouds = models.Clouds.objects.create(**clouds_data)
        rain = models.Rain.objects.create(**rain_data)
        snow = models.Snow.objects.create(**snow_data)
        weather_collect = models.Weather.objects.create(
            main=main,
            visibility=validated_data.pop('visibility', None),
            wind=wind,
            clouds=clouds,
            rain=rain,
            snow=snow,
            dt=validated_data.pop('dt', None),
            timezone=validated_data.pop('timezone', None)
        )
        # for condition in condition_data:
        #     current_condition, status = (
        #         models.Condition.objects.get_or_create(**condition)
        #     )
        #     models.WeatherCondition.objects.create(
        #         weather=weather_collect,
        #         condition=current_condition
        #     )
        return weather_collect
