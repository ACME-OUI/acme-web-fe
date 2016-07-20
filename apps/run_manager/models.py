from django.db import models


class ModelRun(models.Model):
    user = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.TextField()

class RunScript(models.Model):
    
    class Meta:
        get_latest_by = 'version'

    user = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.TextField()
    name = models.CharField(max_length=100)
    version = models.IntegerField()
    run = models.CharField(max_length=100)
