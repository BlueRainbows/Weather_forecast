from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from main.models import WeatherForecast
from main.services import search_city, get_weather, WEATHER_CODE, get_context_for_home_page
from users.models import History


class HomeTemplateView(TemplateView):
    """
    Контроллер для главной страницы.
    """
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет новые объекты контекста:
        погоду, историю и города по которым велся поиск.
        """
        context_data = super().get_context_data(**kwargs)
        weather, history, city = get_context_for_home_page(self.request.user.pk)
        context_data['weather'] = weather
        context_data['history'] = history
        context_data['city'] = city
        return context_data


@login_required(login_url=reverse_lazy('users:login'))
def search_weather(request):
    """
    Функция по обработке поиска запросов.
    Если город не найден, возвращает сообщение.
    Если город найден в базе данных, обновляет и возвращает данные по нему.
    Если город не найден в базе данных, создает его в базе данных.
    При каждом запросе формируется история поиковых запросов пользователей.
    """
    if request.method == "POST":
        search = request.POST.get("search", None)
        if search_city(search):
            city, latitude, longitude = search_city(search)
            weather_code, temperature, tm_max, tm_min = get_weather(latitude, longitude)
            weather = WEATHER_CODE[int(weather_code[0][0])]
            temp = round(temperature[0][0])
            temp_max = round(tm_max[0][0])
            temp_min = round(tm_min[0][0])
            if WeatherForecast.objects.filter(city__icontains=city).exists():
                WeatherForecast.objects.filter(city__icontains=city).update(
                    weather=weather,
                    time_create=datetime.now().time(),
                    temperature=temp,
                    temperature_max=temp_max,
                    temperature_min=temp_min
                )
            else:
                WeatherForecast.objects.create(
                    city=city,
                    weather=weather,
                    time_create=datetime.now().time(),
                    temperature=temp,
                    temperature_max=temp_max,
                    temperature_min=temp_min
                )
            History.objects.create(
                city=WeatherForecast.objects.get(city=city),
                user=request.user,
            )
            return render(request, 'main/search.html',
                          {'search_content': WeatherForecast.objects.get(city=city)})
        else:
            search_content_text = f"К сожалению мы не нашли город {search}"
            return render(request, 'main/search.html',
                          {'text': search_content_text})
