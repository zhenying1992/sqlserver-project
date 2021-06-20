from django.http import JsonResponse
from .base import login_require
import json
import os


@login_require
def serverTestView(request):
    data = json.loads(request.body)
    ip = data['ip']
    res = not bool(os.system(f'ping -c 2 -t 1 {ip}'))
    if res:
        return JsonResponse({'msg': '连接成功', 'status': True})
    return JsonResponse({'msg': '失败', 'status': False})


@login_require
def databaseTestView(request):
    data = json.loads(request.body)
    res = True
    if res:
        return JsonResponse({'msg': '连接成功', 'status': True})
    return JsonResponse({'msg': '失败', 'status': False})
