# Погодное API и телеграм бот на Django (в одном флаконе)

Это шаблон, на основе которого можно начать разрабатывать API на Джанго, и одновременно
использовать Django как обработчик веб-хуков Telegram. Т.к. популярные решения для разработки
телеграм-ботов, например
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot), используют свой
веб-сервер, это усложняет интеграцию бота в проект.

## Компромиссы
**Правильным решением** было бы интегрировать готовую библиотеку для телеграм-ботов, например
([customwebhookboot.py](https://docs.python-telegram-bot.org/en/v20.6/examples.customwebhookbot.html)),
а не изобретать колесо и обрабатывать сообщения "руками". Однако хотелось показать идею минимальным
количеством кода.

## Python
Версия Python - **3.10+**, т.к. используется [Structural Pattern
Matching](https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching).

## Структура файлов
В шаблоне не используется стандартная для Django структура файлов. Вместо этого проект оформлен как
Python package, из которого можно собрать distribution package (`.whl` или `.tar.gz`).

## Файл настроек (local_settings.py)
Скопируйте файл `local_settings.py.tmpl` в `local_settings.py` и сделайте нужные настройки.

В коде используется API Яндекс.Погоды, и соответственно нужен ключ для доступа к API, который можно
получить в [Кабинете разработчика](https://developer.tech.yandex.ru/). Впишите его в `YANDEX_API_KEY`.

Также потребуется ключ для BotAPI - его можно получить у
[BotFather](https://core.telegram.org/bots/features#botfather). Впишите его в `BOT_TOKEN`.

При разработке можно использовать [Local Bot API
Server](https://core.telegram.org/bots/api#using-a-local-bot-api-server), который позволяет
использовать `http` вместо `https` для обработчика запросов от телеграма. Установите значение
`TG_API_BASE_URL` в нужное значение.

`INSTANCE_DIR` - это директория, где лежат файлы, не входящие в пакет - файл настроек, файлы
кеша. По-умолчанию выставляется в папку, в которой лежит `manage.py`. [Идея заимствована из
Flask](https://flask.palletsprojects.com/en/3.0.x/config/#instance-folders). 

## Запуск локально
```
$ python -m venv path/to/env/dir
$ source path/to/env/dir/bin/activate

$ mv local_settings.py.tmpl local_settings.py
$ пропишите нужные настройки

$ pip install -e .
$ ./manage.py runserver
```

## Запуск тестов
```
$ pytest -v tests/
```

## Развертывание на сервере
```
$ pip install -U build
$ python -m build

$ scp dist/weather_ab-1.0.0-py2.py3-none-any.whl my_server:/some/path
$ scp prod_settings.py wsgi.py my_server:/some/path

$ ssh my_server
$ cd /some/path

$ python -m venv .venv
$ source .venv/bin/activate

$ pip install weather_ab-1.0.0-py2.py3-none-any.whl
$ pip install gunicorn

$ gunicorn wsgi
```
