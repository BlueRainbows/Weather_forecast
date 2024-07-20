from django.urls import path
from api_code.views import WeatherForecastAPIView
from api_code.apps import ApiCodeConfig

app_name = ApiCodeConfig.name

urlpatterns = [
    path('', WeatherForecastAPIView.as_view(), name='api-code'),
]
