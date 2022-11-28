from django.shortcuts import HttpResponse


def main(request):
    return HttpResponse(
        '<a href="http://127.0.0.1:8000/admin">http://127.0.0.1:8000/admin<a>'
    )
