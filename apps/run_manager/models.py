from django.db import models


class ModelRun(models.Model):
    user = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.TextField()
