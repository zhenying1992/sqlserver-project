from django.http import JsonResponse
from finance.views.base import login_require
from finance.utils import ping_server, ping_sqlserver, copy_file, delete_local_file
from finance.models import get_db_server
import json


@login_require
def serverTestView(request):
    db_server = get_db_server()
    res = ping_server(db_server.ip)
    if res:
        return JsonResponse({'msg': '连接成功', 'status': True})
    return JsonResponse({'msg': '失败', 'status': False})


@login_require
def databaseTestView(request):
    data = json.loads(request.body)
    db_server = get_db_server()

    res = ping_sqlserver(ip=db_server.ip, dbuser=data['username'], password=data['password'])
    if res:
        return JsonResponse({'msg': '连接成功', 'status': True})
    return JsonResponse({'msg': '失败', 'status': False})


@login_require
def copyFileView(request):

    db_server = get_db_server()
    res = copy_file(
        ip=db_server.ip,
        dest_path=r'\E$\GXCW30',
        local_path=r'e:\199GXCW30',
        username=db_server.username,
        password=db_server.password
    )

    if res:
        return JsonResponse({'msg': '执行成功', 'status': True})
    return JsonResponse({'msg': "执行失败", 'status': False})


@login_require
def deleteDestFileView(request):
    pass


@login_require
def deleteLocalFileView(request):
    res = delete_local_file(local_path=r'E:\199GXCW30')
    if res:
        return JsonResponse({'msg': '执行成功', 'status': True})
    return JsonResponse({'msg': "执行失败", 'status': False})
