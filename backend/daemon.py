import os
import django
import time
import datetime
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "backend.settings")

django.setup()
from finance.models import CronTask, LogModel, get_db_server
from django.db import transaction
from finance.utils import copy_file, delete_local_file
from finance.config import DEST_PATH, LOCAL_PATH

fh = logging.FileHandler(filename="daemon.log")
fh.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(fmt)

logger = logging.getLogger(__name__)
logger.addHandler(fh)


def is_schedule_in_range(schedule):
    return datetime.datetime.now().strftime('%H:%M') == schedule


@transaction.atomic
def get_schedule_task():
    task_list = CronTask.objects.all()
    for task in task_list:
        if is_schedule_in_range(task.schedule):
            return task


def schedule(task):
    logger.info(f'执行任务: {task.name}')
    server = get_db_server()
    try:
        if task.id == 1:
            copy_file(
                ip=server.ip,
                dest_path=DEST_PATH,
                local_path=LOCAL_PATH,
                username=server.username,
                password=server.password,
            )
        else:
            delete_local_file(
                local_path=LOCAL_PATH,
                days=task.days
            )

        LogModel.objects.create(
            content='执行成功',
            name=task.name,
        )
        logger.info("执行完成")
    except Exception as ex:
        logger.error(f"执行发生错误{ex}")
        LogModel.objects.create(
            content=str(ex),
            name=task.name,
            status='failed'
        )


while True:
    logger.info("任务启动")
    task = get_schedule_task()
    if task:
        schedule(task)

    logger.info("等待下次轮询\n")
    time.sleep(60)
