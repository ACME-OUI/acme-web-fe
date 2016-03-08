from django.db import models
from jsonfield import JSONField

class UserRuns(models.Model):
    user_id = models.IntegerField()
    json = JSONField()
    status = models.CharField(max_length=15)