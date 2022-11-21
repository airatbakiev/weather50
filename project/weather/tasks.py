from celery import shared_task
import csv
from django.conf import settings
import json
import requests

from . import models


@shared_task
def task_get_cities():
    dadata_url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/country'
    token = 'Token ' + getattr(settings, 'TOKEN', {})
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    csv_path = getattr(settings, 'BASE_DIR', {}) / 'data' / 'cities.csv'
    pk = 1
    with open(
            csv_path, newline='', encoding='utf-8'
    ) as csvfile:
        datareader = csv.DictReader(csvfile, delimiter=',')
        for row in datareader:
            json_data = json.dumps({'query': row['country']})
            response = requests.post(dadata_url, data=json_data, headers=headers)
            suggestions = response.json().get('suggestions')

            ingredient = models.City(
                id=pk,
                name=row['name'],
                country=row['country'],
            )
            ingredient.save()
            pk += 1

    return True


@shared_task
def task_get_weather():
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    appid = '&appid=' + getattr(settings, 'APPID', {})
    # TODO: add params
    params = '?'
    api_url = base_url + params + appid
    response = requests.get(api_url)
    return True