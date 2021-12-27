from django.http import JsonResponse
from finance.views.base import login_require
from finance.models import LogModel, CronTask
import json
import datetime
import re

p = re.compile(r'^([0-1][0-9]|2[0-3]):([0-5][0-9])-([0-1][0-9]|2[0-3]):([0-5][0-9])$')


@login_require
def updateCopyTaskView(request):
    data = json.loads(request.body)
    schedule = data['schedule']
    if not p.match(schedule):
        return JsonResponse({'data': "输入需要为00:00-01:00格式", 'status': False})

    task = CronTask.objects.get(id=1)
    task.schedule = schedule
    task.save()
    return JsonResponse({'data': "修改成功", 'status': True})


@login_require
def updateDeleteTaskView(request):
    try:
        data = json.loads(request.body)
        days = data['days']
        days = int(days)
        if days <= 0:
            raise
    except Exception:
        return JsonResponse({'data': "输入的非数字或小于0", 'status': False})

    task = CronTask.objects.get(id=2)
    task.days = days
    task.save()
    return JsonResponse({'data': "修改成功", 'status': True})


@login_require
def logView(request):
    data = json.loads(request.body)
    delta = 7 if data['week'] else 1
    start = datetime.datetime.now() - datetime.timedelta(days=delta)
    log_list = LogModel.objects.filter(created_time__gte=start).all()
    log_list = [
        {
            'id': log.id,
            'name': log.name,
            'content': log.content,
            'status': log.status,
            'created_time': log.created_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for log in log_list
    ]

    return JsonResponse({'data': log_list, 'status': True})
