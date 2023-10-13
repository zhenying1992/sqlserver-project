from django.db import models


class UserPropertyModel(models.Model):
    username = models.CharField(max_length=128, default='')
    permissions = models.CharField(max_length=1024, default='')
    bms = models.CharField(max_length=1024, default='')

    class Meta:
        db_table = 'user_property'
