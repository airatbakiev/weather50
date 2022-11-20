# Generated by Django 3.2.16 on 2022-11-20 17:35

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
                ('api_id', models.IntegerField(blank=True, null=True, verbose_name='ID во внешнем API')),
                ('name', models.CharField(max_length=150, verbose_name='Название города')),
                ('country', models.CharField(max_length=150, verbose_name='Код страны')),
                ('country_name', models.CharField(max_length=255, verbose_name='Название страны')),
                ('lat', models.DecimalField(blank=True, decimal_places=7, max_digits=11, null=True, verbose_name='Широта')),
                ('lon', models.DecimalField(blank=True, decimal_places=7, max_digits=11, null=True, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Clouds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all', models.FloatField(blank=True, null=True, verbose_name='Облачность, %')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.IntegerField(verbose_name='ID во внешнем API')),
                ('name', models.CharField(max_length=150, verbose_name='Группа погодных параметров')),
                ('description', models.CharField(max_length=150, verbose_name='Описание погодных условий')),
            ],
            options={
                'verbose_name': 'Погодное состояние',
                'verbose_name_plural': 'Погодные условия',
            },
        ),
        migrations.CreateModel(
            name='MainParams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.FloatField(blank=True, null=True, verbose_name='Температура, C')),
                ('feels_like', models.FloatField(blank=True, null=True, verbose_name='Ощущается как, С')),
                ('pressure', models.FloatField(blank=True, null=True, verbose_name='Атмосферное давление, ГПа')),
                ('humidity', models.FloatField(blank=True, null=True, verbose_name='Влажность, %')),
                ('temp_min', models.FloatField(blank=True, null=True, verbose_name='Минимальная температура, С')),
                ('temp_max', models.FloatField(blank=True, null=True, verbose_name='Максимальная температура, С')),
                ('sea_level', models.FloatField(blank=True, null=True, verbose_name='АД на уровне моря, ГПа')),
                ('grnd_level', models.FloatField(blank=True, null=True, verbose_name='АД на уровне земли, ГПа')),
            ],
        ),
        migrations.CreateModel(
            name='Rain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_h', models.FloatField(blank=True, null=True, verbose_name='Осадки за последний 1 час, мм')),
                ('three_h', models.FloatField(blank=True, null=True, verbose_name='Осадки за последние 3 часа, мм')),
            ],
        ),
        migrations.CreateModel(
            name='Snow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_h', models.FloatField(blank=True, null=True, verbose_name='Снег за последний 1 час, мм')),
                ('three_h', models.FloatField(blank=True, null=True, verbose_name='Снег за последние 3 часа, мм')),
            ],
        ),
        migrations.CreateModel(
            name='Wind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed', models.FloatField(blank=True, null=True, verbose_name='Скорость ветра, метр/сек.')),
                ('deg', models.FloatField(blank=True, null=True, verbose_name='Направление ветра, град.(метеоролог.)')),
                ('gust', models.FloatField(blank=True, null=True, verbose_name='Порыв ветра, метр/сек.')),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visibility', models.FloatField(blank=True, null=True, verbose_name='Видимость, метр')),
                ('dt', models.IntegerField(verbose_name='Время вычисления данных, unix, UTC')),
                ('timezone', models.IntegerField(verbose_name='Сдвиг от UTC, секунды')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.city')),
                ('clouds', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.clouds')),
                ('main', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.mainparams')),
                ('rain', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.rain')),
                ('snow', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.snow')),
                ('weather', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.condition')),
                ('wind', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.wind')),
            ],
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('name', 'country'), name='unique_cities'),
        ),
    ]
