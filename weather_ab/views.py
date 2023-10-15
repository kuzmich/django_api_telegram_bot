from django.http import HttpResponseNotFound
from django.conf import settings
from django.shortcuts import render
import requests



def request_yandex_weather(coords):
    lat, lon = coords

    resp = requests.get(
        'https://api.weather.yandex.ru/v2/forecast',
        dict(lat=lat, lon=lon),
        headers={'X-Yandex-API-Key': settings.YANDEX_API_KEY}
    )
    curr_weather = resp.json()['fact']
    return {'temp': curr_weather['temp'], 'wind': curr_weather['wind_speed'], 'pressure': curr_weather['pressure_mm']}


def weather(request):
    city = request.GET.get('city').lower()
    all_coords = settings.CITIES_COORDS

    if city in all_coords:
        coords = all_coords[city]

        weather = request_yandex_weather(coords)
        weather['city'] = city

        return render(
            request,
            "weather.txt",
            weather,
            # {'city': city, 'temp': 7, 'pressure': 712, 'wind': 5},
            content_type='text/plain; charset=utf-8'
        )
    else:
        return render(request, "unknown.txt", content_type='text/plain; charset=utf-8')
