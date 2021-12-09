from django.http import JsonResponse
from finance.views.base import login_require
from finance.constant import TASK_LIST, SSH_USER
from finance.models import Server, CronTask, LogModel
from finance.utils import download_file, delete_file
import json


@login_require
def taskView(request):
    return JsonResponse({'data': TASK_LIST})


@login_require
def getCronTaskView(request):
    cron_task_list = CronTask.objects.all()
    cron_task_list = [
        {
            'id': task.id,
            'name': task.name,
            'created_time': task.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            'schedule': task.schedule,
            'params': json.dumps({k: v for k, v in json.loads(task.params).items() if v})
        }
        for task in cron_task_list
    ]
    return JsonResponse({'data': cron_task_list})


@login_require
def createCronTaskView(request):
    data = json.loads(request.body)
    task = CronTask(
        name=data.pop('task'),
        schedule=data.pop('schedule'),
        params=json.dumps(data)
    )
    task.save()
    return JsonResponse({'data': 'success'})


@login_require
def deleteCronTaskView(request):
    data = json.loads(request.body)
    task = CronTask.objects.get(id=data['id'])
    task.delete()
    return JsonResponse({'data': 'success'})


@login_require
def executeView(request):
    data = json.loads(request.body)
    task = data['task']
    try:
        if task == '备份数据库到本地':
            pass
        elif task == '传输文件到远程':
            res = download_file(
                ip=data['source_ip'],
                username=SSH_USER,
                file=data['source_path'],
                local_file=data['dest_path']
            )
        elif task == '删除文件':
            res = delete_file(data['source_file'])

        log = LogModel(
            content=res,
            name=task,
            status='success',
            type='once'
        )
        log.save()
    except Exception as ex:
        log = LogModel(
            content=str(ex),
            name=task,
            status='failed',
            type='once'
        )
        log.save()
        return JsonResponse({'data': str(ex), 'status': False})
    return JsonResponse({'data': '成功', 'status': True})


@login_require
def serverView(request):
    server_list = Server.objects.all()
    server_list = [
        {
            'id': server.id,
            'ip': server.ip
        }
        for server in server_list
    ]
    return JsonResponse({'data': server_list})


@login_require
def logView(request):
    data = json.loads(request.body)
    start, end = data
    log_list = LogModel.objects.filter(created_time__gte=start).filter(created_time__lte=end).all()
    log_list = [
        {
            'id': log.id,
            'name': log.name,
            'content': log.content,
            'created_time': log.created_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for log in log_list
    ]

    return JsonResponse({'data': log_list})
