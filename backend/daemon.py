import os
import django
import time
import datetime
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "backend.settings")

django.setup()
from finance.models import CronTask, LogModel, get_db_server
from django.db import transaction
from finance.utils import copy_file, delete_local_file
from finance.config import DEST_PATH, LOCAL_PATH


def is_schedule_in_range(schedule):
    return datetime.datetime.now().strftime('%H:%M') == schedule


@transaction.atomic
def get_schedule_task():
    task_list = CronTask.objects.all()
    for task in task_list:
        if is_schedule_in_range(task.schedule):
            return task


def schedule(task):
    print(f'执行任务: {task.name}')
    server = get_db_server()
    try:
        if task.id == 1:
            res = copy_file(
                ip=server.ip,
                dest_path=DEST_PATH,
                local_path=LOCAL_PATH,
                username=server.username,
                password=server.password,
            )
        else:
            res = delete_local_file(
                local_path=LOCAL_PATH
            )

        LogModel.objects.create(
            content='执行成功',
            name=task.name,
        )
        print('执行完成\n\n')
    except Exception as ex:
        print(f'执行发生错误: {ex}')
        LogModel.objects.create(
            content=str(ex),
            name=task.name,
        )


while True:
    task = get_schedule_task()
    if task:
        schedule(task)

    print('等待下次轮询\n\n')
    time.sleep(60)
