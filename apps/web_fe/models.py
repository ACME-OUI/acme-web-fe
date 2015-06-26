from django.db import models
import json
from django.contrib.auth.models import User


class TileLayout(models.Model):
    user_name = models.CharField(max_length=100)
    layout_name = models.CharField(max_length=100, default='layout1')
    board_layout = models.CharField(max_length=2000)
    mode = models.CharField(max_length=10, default='day')
    default = models.BooleanField(default=0)


class Credential(models.Model):
    site_user_name = models.CharField(max_length=100, default='default_user')
    service_user_name = models.CharField(
        max_length=100, default='default_user')
    password = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
