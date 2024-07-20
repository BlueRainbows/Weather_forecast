from django.contrib import admin

from main.models import WeatherForecast


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'weather')
    search_fields = ('city',)
