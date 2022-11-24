from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Автоматическое создание суперпользователя админки'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            return
        user = User(
            username='admin',
            email='admin@weather50.org',
            first_name='firstName',
            last_name='lastName',
        )
        user.set_password('adminpassword')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print('Superuser created')
        return
