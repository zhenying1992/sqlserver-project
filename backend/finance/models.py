from django.db import models


class LogModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
    title = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'log'


class Task(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    params = models.TextField(default='')

    class Meta:
        db_table = 'task'
