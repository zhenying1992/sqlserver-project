from django.db import models


class LogModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
    name = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'log'


class CronTask(models.Model):
    name = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True)
    schedule = models.CharField(max_length=200)
    params = models.TextField(default='')

    class Meta:
        db_table = 'cron_task'


class Server(models.Model):
    ip = models.CharField(max_length=100)

    class Meta:
        db_table = 'server'
