from django.db import models
from jsonfield import JSONField

class UserRuns(models.Model):
    user = models.CharField(max_length=30)
    runspec = models.TextField(default='')
    status = models.CharField(max_length=15)