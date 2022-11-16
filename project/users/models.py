from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[RegexValidator(r'^[\w.@+-]')],
        verbose_name='Ник пользователя',
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия',
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        constraints = [
            UniqueConstraint(fields=['username', ], name='username')
        ]

    def __str__(self):
        return self.username
