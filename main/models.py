from django.db import models


class WeatherForecast(models.Model):
    city = models.CharField(
        max_length=250,
        verbose_name="Город"
    )
    time_create = models.TimeField(
        verbose_name="Время создания",
        auto_now=True
    )
    temperature = models.PositiveSmallIntegerField(
        verbose_name="Температура на ближайшее время"
    )
    temperature_max = models.PositiveSmallIntegerField(
        verbose_name="Максимальная температура"
    )
    temperature_min = models.PositiveSmallIntegerField(
        verbose_name="Минимальная температура"
    )
    weather = models.CharField(
        max_length=50,
        verbose_name="Погода"
    )

    def __str__(self):
        return (f"В городе {self.city} в ближайшее время {self.weather}."
                f"Температура на ближайшее время {self.temperature}")

    class Meta:
        verbose_name = "Погода"
        verbose_name_plural = "Погода"
