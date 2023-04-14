from django.db import models
from datetime import datetime
import pytz


class ServiceOrder(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=128)
    hardware = models.CharField(max_length=256)
    start_date = models.DateTimeField(auto_now = datetime.now(pytz.timezone('America/Sao_Paulo')))
    end_date = models.DateField()
    status = models.SmallIntegerField()
    active = models.BooleanField(default=1)

    class Meta:
        managed = True