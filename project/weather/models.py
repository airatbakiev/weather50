from django.db import models
from django.db.models import UniqueConstraint


class City(models.Model):
    name = models.CharField('Название города', max_length=150)
    country = models.CharField('Код страны', max_length=150)
    country_name = models.CharField('Название страны', max_length=255)
    lat = models.DecimalField('Широта', max_digits=11, decimal_places=7)
    lon = models.DecimalField('Долгота', max_digits=11, decimal_places=7)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        constraints = [
            UniqueConstraint(
                fields=['name', 'country'], name='unique_cities'
            ),
        ]

    def __str__(self):
        return self.name


class Condition(models.Model):
    condition_id = models.IntegerField('Идентификатор погодных условий')
    main = models.CharField('Группа погодных параметров', max_length=150)
    description = models.CharField('Описание погодных условий', max_length=150)
    icon = models.CharField('Идентификатор иконки', max_length=20)

    class Meta:
        verbose_name = 'Вид состояния'
        verbose_name_plural = 'Виды Погодных условий'

    def __str__(self):
        return self.description


class WeatherCollect(models.Model):
    weather = models.ManyToManyField(Condition, through='WeatherCondition')
    visibility = models.FloatField('Видимость, метр', blank=True, null=True)
    dt = models.IntegerField('Время вычисления данных, unix, UTC', blank=True, null=True)
    timezone = models.IntegerField('Сдвиг от UTC, секунды', blank=True, null=True)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    created = models.DateTimeField('Время создания записи', auto_now=True)
    iter_id = models.IntegerField('Итерация')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Коллекция погоды'
        verbose_name_plural = 'ГЛАВНАЯ ТАБЛИЦА'
        constraints = [
            UniqueConstraint(
                fields=['city', 'iter_id'], name='unique_collects'
            ),
        ]

    def __str__(self):
        return f'{str(self.created)[:16]} ({self.iter_id}) ({self.city.name})'


class WeatherCondition(models.Model):
    weather = models.ForeignKey(WeatherCollect, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Состояние Погоды'
        verbose_name_plural = 'Состояния погоды'


class MainParams(models.Model):
    temp = models.FloatField('Темп, C', blank=True, null=True)
    feels_like = models.FloatField('Ощущ, С', blank=True, null=True)
    pressure = models.FloatField('Атм.дав, ГПа', blank=True, null=True)
    humidity = models.FloatField('Влаж, %', blank=True, null=True)
    temp_min = models.FloatField('Мин темп, С', blank=True, null=True)
    temp_max = models.FloatField('Макс темп, С', blank=True, null=True)
    sea_level = models.FloatField('АД на ур моря, ГПа', blank=True, null=True)
    grnd_level = models.FloatField('АД на ур земли, ГПа', blank=True, null=True)
    weather_collect = models.OneToOneField(WeatherCollect, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Основные показатели'
        verbose_name_plural = 'Основные показатели'


class Wind(models.Model):
    speed = models.FloatField('Скор. ветра, метр/сек.', blank=True, null=True)
    deg = models.FloatField('Напр. ветра, град.(метеоролог.)', blank=True, null=True)
    gust = models.FloatField('Порыв ветра, метр/сек.', blank=True, null=True)
    weather_collect = models.OneToOneField(WeatherCollect, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Показатели ветра'
        verbose_name_plural = 'Показатели ветра'


class Clouds(models.Model):
    all = models.FloatField('Облачность, %', blank=True, null=True)
    weather_collect = models.OneToOneField(WeatherCollect, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Показатели облачности'
        verbose_name_plural = 'Показатели облачности'


class Rain(models.Model):
    one_h = models.FloatField('За посл. 1 час, мм', blank=True, null=True)
    three_h = models.FloatField('За посл. 3 часа, мм', blank=True, null=True)
    weather_collect = models.OneToOneField(WeatherCollect, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Показатели дождя'
        verbose_name_plural = 'Показатели дождя'


class Snow(models.Model):
    one_h = models.FloatField('За посл. 1 час, мм', blank=True, null=True)
    three_h = models.FloatField('За посл. 3 часа, мм', blank=True, null=True)
    weather_collect = models.OneToOneField(WeatherCollect, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Показатели снега'
        verbose_name_plural = 'Показатели снега'
