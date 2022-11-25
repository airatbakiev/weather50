from django.http import HttpResponse
# from weather import tasks


def get_cities(request):
    # tasks.get_cities.delay()
    return HttpResponse('Города загружаются')


def get_weather(request):
    # tasks.get_weather.delay()
    return HttpResponse('Погода загружается')


def main_page(request):
    return HttpResponse('Главная')
