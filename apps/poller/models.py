from django.db import models
from jsonfield import JSONField


class UserRuns(models.Model):
    user = models.CharField(max_length=30)
    runspec = models.TextField(default='')
    status = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    destination = models.TextField(default='')
    # The following fields use arbitrary max_lengths based on an example data set. Adjustment may be necessary
    casename = models.TextField(max_length=50)     # Ex. F1850C5.ne30.6mos
    mppwidth = models.IntegerField()               # Ex. 144
    stop_option = models.TextField(max_length=12)  # Ex. ndays
    stop_n = models.TextField(max_length=15)       # Ex. 60, 60  use .split(',')
    walltime = models.TextField(max_length=15)     # Ex. 60, 60
    mach = models.TextField(max_length=12)         # Ex. titan
    compset = models.TextField(max_length=10)      # Ex. F1850C5
    res = models.TextField(max_length=12)          # Ex. ne30_g16
    project = models.TextField(max_length=12)      # Ex. cli115
    compiler = models.TextField(max_length=10)     # Ex. intel
