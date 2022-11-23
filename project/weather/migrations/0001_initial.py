# Generated by Django 3.2.16 on 2022-11-23 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название города')),
                ('country', models.CharField(max_length=150, verbose_name='Код страны')),
                ('country_name', models.CharField(max_length=255, verbose_name='Название страны')),
                ('lat', models.DecimalField(decimal_places=7, max_digits=11, verbose_name='Широта')),
                ('lon', models.DecimalField(decimal_places=7, max_digits=11, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_id', models.IntegerField(verbose_name='Идентификатор погодных условий')),
                ('main', models.CharField(max_length=150, verbose_name='Группа погодных параметров')),
                ('description', models.CharField(max_length=150, verbose_name='Описание погодных условий')),
                ('icon', models.CharField(max_length=20, verbose_name='Идентификатор иконки')),
            ],
            options={
                'verbose_name': 'Вид состояния',
                'verbose_name_plural': 'Виды Погодных условий',
            },
        ),
        migrations.CreateModel(
            name='WeatherCollect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visibility', models.FloatField(blank=True, null=True, verbose_name='Видимость, метр')),
                ('dt', models.IntegerField(blank=True, null=True, verbose_name='Время вычисления данных, unix, UTC')),
                ('timezone', models.IntegerField(blank=True, null=True, verbose_name='Сдвиг от UTC, секунды')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Время создания записи')),
                ('iter_id', models.IntegerField(verbose_name='Порядковый номер итерации')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.city')),
            ],
            options={
                'verbose_name': 'Коллекция погоды',
                'verbose_name_plural': 'Коллекции погоды',
            },
        ),
        migrations.CreateModel(
            name='Wind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed', models.FloatField(blank=True, null=True, verbose_name='Скор. ветра, метр/сек.')),
                ('deg', models.FloatField(blank=True, null=True, verbose_name='Напр. ветра, град.(метеоролог.)')),
                ('gust', models.FloatField(blank=True, null=True, verbose_name='Порыв ветра, метр/сек.')),
                ('weather_collect', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.weathercollect')),
            ],
            options={
                'verbose_name': 'Показатели ветра',
                'verbose_name_plural': 'Показатели ветра',
            },
        ),
        migrations.CreateModel(
            name='WeatherCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.condition')),
                ('weather', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.weathercollect')),
            ],
            options={
                'verbose_name': 'Состояние Погоды',
                'verbose_name_plural': 'Состояния погоды',
            },
        ),
        migrations.AddField(
            model_name='weathercollect',
            name='weather',
            field=models.ManyToManyField(through='weather.WeatherCondition', to='weather.Condition'),
        ),
        migrations.CreateModel(
            name='Snow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_h', models.FloatField(blank=True, null=True, verbose_name='За посл. 1 час, мм')),
                ('three_h', models.FloatField(blank=True, null=True, verbose_name='За посл. 3 часа, мм')),
                ('weather_collect', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.weathercollect')),
            ],
            options={
                'verbose_name': 'Показатели снега',
                'verbose_name_plural': 'Показатели снега',
            },
        ),
        migrations.CreateModel(
            name='Rain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_h', models.FloatField(blank=True, null=True, verbose_name='За посл. 1 час, мм')),
                ('three_h', models.FloatField(blank=True, null=True, verbose_name='За посл. 3 часа, мм')),
                ('weather_collect', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.weathercollect')),
            ],
            options={
                'verbose_name': 'Показатели дождя',
                'verbose_name_plural': 'Показатели дождя',
            },
        ),
        migrations.CreateModel(
            name='MainParams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.FloatField(blank=True, null=True, verbose_name='Темп, C')),
                ('feels_like', models.FloatField(blank=True, null=True, verbose_name='Ощущ, С')),
                ('pressure', models.FloatField(blank=True, null=True, verbose_name='Атм.дав, ГПа')),
                ('humidity', models.FloatField(blank=True, null=True, verbose_name='Влаж, %')),
                ('temp_min', models.FloatField(blank=True, null=True, verbose_name='Мин темп, С')),
                ('temp_max', models.FloatField(blank=True, null=True, verbose_name='Макс темп, С')),
                ('sea_level', models.FloatField(blank=True, null=True, verbose_name='АД на ур моря, ГПа')),
                ('grnd_level', models.FloatField(blank=True, null=True, verbose_name='АД на ур земли, ГПа')),
                ('weather_collect', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.weathercollect')),
            ],
            options={
                'verbose_name': 'Основные показатели',
                'verbose_name_plural': 'Основные показатели',
            },
        ),
        migrations.CreateModel(
            name='Clouds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all', models.FloatField(blank=True, null=True, verbose_name='Облачность, %')),
                ('weather_collect', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.weathercollect')),
            ],
            options={
                'verbose_name': 'Показатели облачности',
                'verbose_name_plural': 'Показатели облачности',
            },
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('name', 'country'), name='unique_cities'),
        ),
        migrations.AddConstraint(
            model_name='weathercollect',
            constraint=models.UniqueConstraint(fields=('city', 'iter_id'), name='unique_collects'),
        ),
    ]
