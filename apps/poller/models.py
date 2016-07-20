from django.db import models


class UserRuns(models.Model):
    class Meta:
        get_latest_by = 'created'

    user = models.CharField(max_length=30)
    config_options = models.TextField()
    status = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
