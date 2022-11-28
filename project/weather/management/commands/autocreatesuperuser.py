from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User

USERNAME = getattr(settings, 'ADMIN_USERNAME', {})
PASSWORD = getattr(settings, 'ADMIN_PASSWORD', {})


class Command(BaseCommand):
    help = 'Автоматическое создание суперпользователя админки'

    def handle(self, *args, **options):
        if User.objects.filter(username=USERNAME).exists():
            return
        user = User(
            username=USERNAME,
            email='admin@weather50.org',
            first_name='firstName',
            last_name='lastName',
        )
        user.set_password(PASSWORD)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print('Superuser created')
        return
