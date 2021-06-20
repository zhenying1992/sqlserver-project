import os
import django
import time
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "backend.settings")

django.setup()
from finance.models import CronTask, LogModel
from django.db import transaction


def is_schedule_in_range(schedule):
    return datetime.datetime.now().strftime('%H:%M') == schedule


def run_bak_database(task):
    pass


def run_copy_file(task):
    pass


def run_delete_file(task):
    pass


task_mapping = {
    '备份数据库到本地': run_bak_database,
    '传输文件到远程': run_copy_file,
    '删除文件': run_delete_file,
}


def run(task):
    print(task.name)
    func = task_mapping[task.name]
    func(task)

    LogModel.objects.create(
        content='aaaaa',
        name=task.name
    )


while True:
    with transaction.atomic():
        task_list = CronTask.objects.all()
        for task in task_list:
            if is_schedule_in_range(task.schedule):
                run(task)

        print('等待下次轮询\n\n')
    time.sleep(60)
