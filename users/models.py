from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import WeatherForecast


class User(AbstractUser):
    """ Модель пользователя """
    username = None
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    avatar = models.ImageField(
        upload_to='users/',
        verbose_name='Аватар',
        default='/users/796d02684eadafba407faf81a4fd697d.png'
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name}. Электронная почта: {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class History(models.Model):
    city = models.ForeignKey(
        WeatherForecast,
        on_delete=models.CASCADE,
        verbose_name="Город"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    data = models.DateTimeField(
        verbose_name="Дата запроса",
        auto_now=True
    )

    class Meta:
        ordering = ["-data"]
        verbose_name = "История"
        verbose_name_plural = "История"
