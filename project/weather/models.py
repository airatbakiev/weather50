from django.db import models
from django.db.models import UniqueConstraint


class City(models.Model):
    api_id = models.IntegerField('ID во внешнем API')
    name = models.CharField('Название города', max_length=150)
    country = models.CharField('Код страны', max_length=150)
    lat = models.DecimalField('Широта', max_digits=11, decimal_places=7)
    lon = models.DecimalField('Долгота', max_digits=11, decimal_places=7)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        constraints = [
            UniqueConstraint(
                fields=['api_id', 'name'], name='unique_cities'
            ),
        ]

    def __str__(self):
        return self.name


class Condition(models.Model):
    api_id = models.IntegerField('ID во внешнем API')
    name = models.CharField('Группа погодных параметров', max_length=150)
    description = models.CharField('Описание погодных условий', max_length=150)

    class Meta:
        verbose_name = 'Погодное состояние'
        verbose_name_plural = 'Погодные условия'

    def __str__(self):
        return self.description


class MainParams(models.Model):
    temp = models.FloatField('Температура, C', blank=True, null=True)
    feels_like = models.FloatField('Ощущается как, С', blank=True, null=True)
    pressure = models.FloatField('Атмосферное давление, ГПа', blank=True, null=True)
    humidity = models.FloatField('Влажность, %', blank=True, null=True)
    temp_min = models.FloatField('Минимальная температура, С', blank=True, null=True)
    temp_max = models.FloatField('Максимальная температура, С', blank=True, null=True)
    sea_level = models.FloatField('АД на уровне моря, ГПа', blank=True, null=True)
    grnd_level = models.FloatField('АД на уровне земли, ГПа', blank=True, null=True)


class Wind(models.Model):
    speed = models.FloatField('Скорость ветра, метр/сек.', blank=True, null=True)
    deg = models.FloatField('Направление ветра, град.(метеоролог.)', blank=True, null=True)
    gust = models.FloatField('Порыв ветра, метр/сек.', blank=True, null=True)


class Clouds(models.Model):
    all = models.FloatField('Облачность, %', blank=True, null=True)


class Rain(models.Model):
    one_h = models.FloatField('Осадки за последний 1 час, мм', blank=True, null=True)
    three_h = models.FloatField('Осадки за последние 3 часа, мм', blank=True, null=True)


class Snow(models.Model):
    one_h = models.FloatField('Снег за последний 1 час, мм', blank=True, null=True)
    three_h = models.FloatField('Снег за последние 3 часа, мм', blank=True, null=True)


class Weather(models.Model):
    weather = models.ForeignKey(Condition, on_delete=models.CASCADE)
    main = models.OneToOneField(MainParams, on_delete=models.CASCADE)
    visibility = models.FloatField('Видимость, метр', blank=True, null=True)
    wind = models.OneToOneField(Wind, on_delete=models.CASCADE)
    clouds = models.OneToOneField(Clouds, on_delete=models.CASCADE)
    rain = models.OneToOneField(Rain, on_delete=models.CASCADE)
    snow = models.OneToOneField(Snow, on_delete=models.CASCADE)
    dt = models.IntegerField('Время вычисления данных, unix, UTC')
    timezone = models.IntegerField('Сдвиг от UTC, секунды')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
