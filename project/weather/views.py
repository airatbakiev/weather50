from django.shortcuts import HttpResponse


def main(request):
    return HttpResponse('http://127.0.0.1:8000/admin')
