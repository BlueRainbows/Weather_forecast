# Generated by Django 5.1b1 on 2024-07-19 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=250, verbose_name='Город')),
                ('time_create', models.TimeField(auto_now=True, verbose_name='Время создания')),
                ('temperature', models.PositiveSmallIntegerField(verbose_name='Температура на ближайшее время')),
                ('temperature_max', models.PositiveSmallIntegerField(verbose_name='Максимальная температура')),
                ('temperature_min', models.PositiveSmallIntegerField(verbose_name='Минимальная температура')),
                ('weather', models.CharField(max_length=50, verbose_name='Погода')),
            ],
            options={
                'verbose_name': 'Погода',
                'verbose_name_plural': 'Погода',
            },
        ),
    ]
