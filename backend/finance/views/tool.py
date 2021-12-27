from django.http import JsonResponse
from finance.views.base import login_require
from finance.utils import ping_server, ping_sqlserver, copy_file, delete_local_file, backup_sqlserver
from finance.models import get_db_server
import datetime
import json
from finance.config import DEST_PATH, LOCAL_PATH, DB_NAME


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
        dest_path=DEST_PATH,
        local_path=LOCAL_PATH,
        username=db_server.username,
        password=db_server.password
    )

    if res:
        return JsonResponse({'msg': '执行成功', 'status': True})
    return JsonResponse({'msg': "执行失败", 'status': False})


@login_require
def deleteLocalFileView(request):
    res = delete_local_file(local_path=LOCAL_PATH)
    if res:
        return JsonResponse({'msg': '执行成功', 'status': True})
    return JsonResponse({'msg': "执行失败", 'status': False})


@login_require
def backupDatabaseView(request):
    db_server = get_db_server()
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    name = f'{DB_NAME}_{now}.bak'
    res = backup_sqlserver(
        ip=db_server.ip,
        username=db_server.username,
        password=db_server.password,
        database=DB_NAME,
        local_path=rf'e:\backup\{name}'
    )

    if res:
        return JsonResponse({'msg': '执行成功', 'status': True})
    return JsonResponse({'msg': "执行失败", 'status': False})
