from datetime import timedelta
from django_celery_beat.models import ClockedSchedule, IntervalSchedule
from django_celery_beat.models import PeriodicTask, HOURS
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Создание стартового расписания задач'

    def handle(self, *args, **options):
        # create clocked schedule for 'get_cities' task
        t_delta = timedelta(seconds=10)
        the_time = timezone.now() + t_delta
        get_cities_clocked = ClockedSchedule.objects.create(clocked_time=the_time)
        get_cities, created = PeriodicTask.objects.get_or_create(
            name='get_cities',
            task='weather.tasks.get_cities',
            clocked=get_cities_clocked,
            one_off=True,
        )
        # create clocked schedule for start 'get_weather'
        t_delta = timedelta(seconds=30)
        the_time = timezone.now() + t_delta
        get_weather_clocked = ClockedSchedule.objects.create(clocked_time=the_time)
        get_cities, created = PeriodicTask.objects.get_or_create(
            name='get_weather_clocked',
            task='weather.tasks.get_weather',
            clocked=get_weather_clocked,
            one_off=True,
        )
        # create interval schedule for 'get_weather' task
        the_interval = IntervalSchedule.objects.create(every=1, period=HOURS)
        get_weather, created = PeriodicTask.objects.get_or_create(
            name='get_weather_interval',
            task='weather.tasks.get_weather',
            interval=the_interval,
            start_time=the_time,
        )
        return
