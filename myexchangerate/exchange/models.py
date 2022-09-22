import datetime
from django.db import models
from django.utils import timezone


class Euro(models.Model):
    iso_code = models.CharField(max_length=3, default='EUR', editable=False)
    exc_date = models.DateTimeField('Exchange rate date')
    value = models.FloatField(default=1)

    def __str__(self):
        return self.iso_code

    def is_recent(self):
        return timezone.now() >= self.exc_date >= timezone.now() - datetime.timedelta(days=7)


class Real(models.Model):
    iso_code = models.CharField(max_length=3, default='BRL', editable=False)
    exc_date = models.DateTimeField('Exchange rate date')
    value = models.FloatField(default=1)

    def __str__(self):
        return self.iso_code

    def is_recent(self):
        return timezone.now() >= self.exc_date >= timezone.now() - datetime.timedelta(days=7)


class Yen(models.Model):
    iso_code = models.CharField(max_length=3, default='JPY', editable=False)
    exc_date = models.DateTimeField('Exchange rate date')
    value = models.FloatField(default=1)

    def __str__(self):
        return self.iso_code

    def is_recent(self):
        return timezone.now() >= self.exc_date >= timezone.now() - datetime.timedelta(days=7)
