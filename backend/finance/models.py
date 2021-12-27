from django.db import models


class LogModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
    name = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=20, default='success')
    type = models.CharField(max_length=20, default='cron')

    class Meta:
        db_table = 'log'


class CronTask(models.Model):
    name = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True)
    schedule = models.CharField(max_length=200)
    days = models.IntegerField(default=30)

    class Meta:
        db_table = 'cron_task'


class Server(models.Model):
    ip = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'server'


def get_db_server() -> Server:
    return Server.objects.get(type='database')
