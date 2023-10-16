import json

from django.http import HttpResponse, HttpResponseNotFound
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render
from django.test import RequestFactory
from django.views.decorators.csrf import csrf_exempt

import requests


def weather(request):
    # TODO Что делать, если город не указан, timeout, город неизвестен, нет данных?

    city = request.GET.get('city').strip().lower()
    all_coords = settings.CITIES_COORDS

    if city in all_coords:
        coords = all_coords[city]

        if not (weather := cache.get(city)):
            weather = request_yandex_weather(coords)
            weather['city'] = city.title()
            cache.set(city, weather)

        weather['temp_icon'] = '\U0001f321'
        weather['wind_icon'] = '\U0001f32c'
        weather['press_icon'] = '\U0001f5dc'

        return render(
            request,
            "weather.txt",
            weather,
            content_type='text/plain; charset=utf-8'
        )
    else:
        return render(request, "unknown.txt", content_type='text/plain; charset=utf-8')


@csrf_exempt
def tg_update_hook(request):
    if request.method == 'POST':
        update = json.loads(request.body)

        text = update['message']['text']
        chat_id = update['message']['from']['id']

        match text:
            case '/start':
                send_message(
                    chat_id,
                    'Просто введите название города (например Москва), и я пришлю текущую погоду'
                )
            case _:
                weather = get_weather(text)
                send_message(chat_id, weather)

    return HttpResponse()


def request_yandex_weather(coords):
    lat, lon = coords
    resp = requests.get(
        'https://api.weather.yandex.ru/v2/forecast',
        dict(lat=lat, lon=lon),
        headers={'X-Yandex-API-Key': settings.YANDEX_API_KEY}
    )
    curr_weather = resp.json()['fact']
    return {'temp': curr_weather['temp'], 'wind': curr_weather['wind_speed'], 'pressure': curr_weather['pressure_mm']}


def get_weather(city):
    rf = RequestFactory()
    req = rf.get(f'/weather?city={city}')
    resp = weather(req)
    return resp.content.decode(resp.charset)


def send_message(chat_id, text):
    s = settings
    resp = requests.post(
        f'{s.TG_API_BASE_URL}/bot{s.BOT_TOKEN}/sendMessage',
        json=dict(chat_id=chat_id, text=text)
    )
    return resp
