from django.http import JsonResponse


def login_require(func):
    def wrap(request):
        if not request.user.is_authenticated:
            return JsonResponse(data={'msg': '用户未登陆', 'status': False})

        try:
            return func(request)
        except Exception as e:
            return JsonResponse(data={'msg': f"请求失败{e}", 'status': False})

    return wrap
