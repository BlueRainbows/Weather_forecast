import pandas as pd
from geopy.geocoders import Nominatim
import openmeteo_requests
from openmeteo_sdk.Aggregation import Aggregation
from openmeteo_sdk.Variable import Variable

from main.models import WeatherForecast
from users.models import History

# Константна погодного кода
WEATHER_CODE = {
    0: 'чистое небо',
    1: 'ясно',
    2: 'переменная облачность',
    3: 'облачно',
    45: 'туманно',
    48: 'туман и иней',
    51: 'небольшая морось',
    53: 'морось',
    55: 'сильная морось',
    56: 'слабый моросящий дождь',
    57: 'сильный моросящий дождь',
    61: 'Слабый дождь',
    63: 'Умеренный дождь',
    65: 'Сильный дождь',
    66: 'Слабый ледяной дождь',
    67: 'Сильный ледяной дождь',
    71: 'Слабый снег',
    73: 'Умеренный снегопад',
    75: 'Сильный снегопад',
    77: 'Град',
    80: 'Слабый ливень',
    81: 'Умеренный ливень',
    82: 'Сильный ливень',
    85: 'Дождь со снегом',
    86: 'Сильный дождь со снегом',
    95: 'Гроза',
    96: 'Гроза с небольшим градом',
    99: 'Гроза с сильным градом',
}


def get_context_for_home_page(user):
    """
    Сервисная функция для получения контекста для главной страницы.
    Возвращает данные о 5 случайных городах из бд.
    Возвращает данные о 5 последних запросах пользователя.
    Возвращает данные о последнем запроса пользователя.
    """
    city = WeatherForecast.objects.all().order_by('?')[:5]
    data_weather = History.objects.filter(user=user)[:5]
    data_history = History.objects.filter(user=user).first()
    if data_history:
        data_city = WeatherForecast.objects.get(
            pk=data_history.city.pk
        )
    else:
        data_city = None
    return data_weather, data_city, city


def search_city(city):
    """
    Сервисная функция для поиска города по его названию.
    Если функция находит город, то возвращает название города и его координаты.
    """
    # Осуществление поиска широты и долготы по городу введенным пользователем
    geolocator = Nominatim(user_agent="geo").geocode(city)
    # Условие при удачном поиске города
    if geolocator:
        return geolocator.raw['name'], geolocator.latitude, geolocator.longitude
    else:
        return None


def get_weather(latitude, longitude):
    """
    Сервисная функция для получения погоды по городу.
    Возвращает код погоды, темпаратуру на ближайший час,
    Максимальную и минимальную температуру на сегодня.
    """
    # Создаем объект клиента
    client = openmeteo_requests.Client()
    # Указываем параметры запроса
    params = {
        'latitude': latitude,
        'longitude': longitude,
        "forecast_days": 1,
        'hourly': ['temperature_2m', 'weather_code'],
        'daily': ['temperature_2m_max', 'temperature_2m_min'],
        'timezone': 'auto',
        'forecast_hours': 1,
    }
    # Выполняем запрос к API Open-Meteo
    responses = client.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    # Вызываем полученные данные
    hourly = responses[0].Hourly()
    daily = responses[0].Daily()
    # Делаем перебор данных и формируем список
    daily_variables = list(map(lambda i: daily.Variables(i), range(0, daily.VariablesLength())))
    hourly_variables = list(map(lambda i: hourly.Variables(i), range(0, hourly.VariablesLength())))
    # Вытаскиваем погодные осадки
    weather_code = next(filter(lambda x: x.Variable() == Variable.weather_code, hourly_variables))
    # Вытаскиваем температуру на ближайший час
    temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature, hourly_variables))
    # Вытаскиваем максимальную температуру за сутки
    temperature_2m_max = next(filter(
        lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2 and x.Aggregation() == Aggregation.maximum,
        daily_variables))
    # Вытаскиваем минимальную температуру за сутки
    temperature_2m_min = next(filter(
        lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2 and x.Aggregation() == Aggregation.minimum,
        daily_variables))
    # Выполняем приведение типов данных коллекций в словарь
    weather_code_data = pd.DataFrame(data=weather_code.ValuesAsNumpy()).to_dict()
    temperature_2m_data = pd.DataFrame(data=temperature_2m.ValuesAsNumpy()).to_dict()
    temperature_2m_max_data = pd.DataFrame(data=temperature_2m_max.ValuesAsNumpy()).to_dict()
    temperature_2m_min_data = pd.DataFrame(data=temperature_2m_min.ValuesAsNumpy()).to_dict()
    return weather_code_data, temperature_2m_data, temperature_2m_max_data, temperature_2m_min_data
