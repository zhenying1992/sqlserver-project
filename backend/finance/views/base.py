from django.http import JsonResponse


def login_require(func):
    def wrap(request):
        if request.user.is_authenticated:
            return func(request)
        return JsonResponse(data={'msg': '用户未登陆', 'status': 400})

    return wrap
