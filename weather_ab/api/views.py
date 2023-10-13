from django.shortcuts import render


def weather(request):
    return render(
        request,
        "weather.txt",
        {'city': 'Иркутск', 'temp': 7, 'pressure': 712, 'wind': 5},
        content_type='text/plain; charset=utf-8'
    )
