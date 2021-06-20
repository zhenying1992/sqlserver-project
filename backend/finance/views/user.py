from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
from .base import login_require
from django.contrib.auth.models import User


def loginView(request):
    data = json.loads(request.body)
    user = authenticate(
        username=data['username'],
        password=data['password']
    )
    if user is not None:
        login(request, user)
        return JsonResponse(data={'msg': '登陆成功', 'status': True})
    else:
        return JsonResponse(data={'msg': '登陆失败', 'status': False})


def logoutView(request):
    logout(request)
    return JsonResponse(data={'msg': '登出成功', 'status': True})


@login_require
def changePasswordView(request):
    data = json.loads(request.body)
    user = User.objects.get(username=request.user.username)
    user.set_password(data['password'])
    user.save()
    return JsonResponse(data={'msg': '修改成功', 'status': True})
