from rest_framework import serializers

from main.models import WeatherForecast
from users.models import History


class WeatherForecastSerializer(serializers.ModelSerializer):
    count_city = serializers.SerializerMethodField(read_only=True)

    def get_count_city(self, weather_forecast):
        count_city = History.objects.filter(city__pk=weather_forecast.pk).count()
        return count_city

    class Meta:
        model = WeatherForecast
        fields = ('pk', 'city', 'count_city',)
