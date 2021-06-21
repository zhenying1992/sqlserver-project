from django.http import JsonResponse
from finance.views.base import login_require
from finance.utils import ping_server
import json


@login_require
def serverTestView(request):
    data = json.loads(request.body)
    res = ping_server(data['ip'])
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
