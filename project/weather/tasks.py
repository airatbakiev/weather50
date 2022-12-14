from celery import shared_task
import csv
from django.conf import settings
import json
from logging import handlers
import logging
from requests.adapters import HTTPAdapter
import requests
import urllib3

from weather import models
from weather import serializers

CSV_PATH = getattr(settings, 'BASE_DIR', {}) / 'data' / 'cities.csv'
DADATA_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/country'
DADATA_TOKEN = 'Token ' + getattr(settings, 'TOKEN', {})
DADATA_HEADERS = {
        'Authorization': DADATA_TOKEN,
        'Content-Type': 'application/json'
}
BASE_GEO_URL = 'http://api.openweathermap.org/geo/1.0/direct'
BASE_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
APPID = '&appid=' + getattr(settings, 'APPID', {})

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = handlers.RotatingFileHandler(
    'weather50_logger.log', maxBytes=50000000, backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

retry_strategy = urllib3.Retry(
    total=5,
    status_forcelist=[413, 429, 500, 502, 503, 504],
    method_whitelist=['GET', 'POST'],
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


@shared_task
def get_cities():
    if models.City.objects.all().count() >= 50:
        return
    cities = []
    try:
        with open(
            CSV_PATH, newline='', encoding='utf-8'
        ) as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                json_data = json.dumps({'query': row['country']})
                response = http.post(
                    DADATA_URL, data=json_data, headers=DADATA_HEADERS, timeout=5
                ).json()
                if not response['suggestions']:
                    break
                suggestion = response.get('suggestions')[0]
                country = suggestion['data']['alfa2']
                params = '?q= ' + row['name'] + ',' + country + '&limit=1'
                geo_url = BASE_GEO_URL + params + APPID
                response = http.get(geo_url, timeout=5).json()[0]
                cities.append(
                    models.City(
                        name=row['name'],
                        country=country,
                        country_name=row['country'],
                        lat=response['lat'],
                        lon=response['lon']
                    )
                )
    except EOFError as file_error:
        logger.error(file_error)
    except FileNotFoundError as path_error:
        raise path_error
    except requests.ConnectionError as crash:
        msg = f'?????? ?????????? ?? ?????????????? ????????????????. ????????????: {crash}'
        logger.error(msg)
    else:
        models.City.objects.bulk_create(cities, ignore_conflicts=True)
        logger.info('???????????????? ???????????????? 50 ?????????????? ?? ????')
    return


@shared_task
def get_weather():
    iteration = 0
    if models.WeatherCollect.objects.count() > 0:
        iteration = models.WeatherCollect.objects.latest('iter_id').iter_id
    cities = models.City.objects.values()
    for city in cities:
        params = ('?lat=' + str(city['lat']) + '&lon=' + str(city['lon'])
                  + '&lang=ru&units=metric')
        weather_url = BASE_WEATHER_URL + params + APPID
        try:
            response = http.get(weather_url, timeout=5).json()
            response['city'] = city
            response['iter_id'] = iteration + 1
            serializer = serializers.WeatherSerializer(data=response)
            if serializer.is_valid():
                serializer.save()
            else:
                error_msg = ('????????????, ???????????????????????? ?? ????????????????????????, ??????????????????.'
                             f'???????????? ???? {city["name"]} ?? ???? ???? ????????????????.'
                             '?????????????????? ???????? ???????????? ???? ???????????????? API.')
                logger.error(error_msg)
        except requests.ConnectionError as crash:
            msg = f'?????? ?????????? ?? ?????????????? ????????????????. ????????????: {crash}'
            logger.error(msg)
        except Exception as error:
            logger.error(f'???????????????????????????? ????????????: {error}')
    return
