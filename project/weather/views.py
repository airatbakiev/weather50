from django.http import HttpResponse
import csv
from django.conf import settings
import json
import requests
from rest_framework import status

from . import models, serializers

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


def get_cities(request):
    if models.City.objects.all().count() >= 50:
        return HttpResponse('Коды alfa2 стартового перечня стран загружены.')
    cities = []
    pk = 0
    with open(
        CSV_PATH, newline='', encoding='utf-8'
    ) as csvfile:
        datareader = csv.DictReader(csvfile, delimiter=',')
        for row in datareader:
            json_data = json.dumps({'query': row['country']})
            response = requests.post(
                DADATA_URL, data=json_data, headers=DADATA_HEADERS
            ).json()
            if not response['suggestions']:
                break
            suggestion = response.get('suggestions')[0]
            country = suggestion['data']['alfa2']
            params = '?q= ' + row['name'] + ',' + country + '&limit=1'
            geo_url = BASE_GEO_URL + params + APPID
            response = requests.get(geo_url).json()[0]
            cities.append(
                models.City(
                    name=row['name'],
                    country=country,
                    country_name=row['country'],
                    lat=response['lat'],
                    lon=response['lon']
                )
            )
            pk += 1
    models.City.objects.bulk_create(cities, ignore_conflicts=True)
    return HttpResponse('Загружены коды alfa2(iso) ' + str(pk) + 'стран(ы).')


def get_weather(request):
    cities = models.City.objects.all()
    for city in cities:
        params = ('?lat=' + str(city.lat) + '&lon=' + str(city.lon)
                  + '&lang=ru&units=metric')
        weather_url = BASE_WEATHER_URL + params + APPID
        response = requests.get(weather_url)
        serializer = serializers.WeatherSerializer(data=response.json())
        if serializer.is_valid():
            serializer.save()
        else:
            return HttpResponse(json.dumps(serializer.errors))
    return HttpResponse('Готово')
