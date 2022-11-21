from django.http import HttpResponse


def users_def(request):
    return HttpResponse('View для управления пользователями')
