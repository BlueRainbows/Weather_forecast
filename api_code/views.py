from rest_framework.generics import ListAPIView

from api_code.serializers import WeatherForecastSerializer
from main.models import WeatherForecast


class WeatherForecastAPIView(ListAPIView):
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer
