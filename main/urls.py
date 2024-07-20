from django.urls import path

from main.apps import MainConfig
from main import views

app_name = MainConfig.name

urlpatterns = [
    # Главная страница
    path('', views.HomeTemplateView.as_view(), name='index'),
    # Страница результатов поиска
    path('search/', views.search_weather, name='search')
]
