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


class DiagnosticConfig(models.Model):

    class Meta:
        get_latest_by = 'version'

    # The user that created the diagnostic configuration
    user = models.CharField(max_length=50)

    # The time the config was created
    created = models.DateTimeField(auto_now_add=True)

    # The version number
    version = models.IntegerField(default=1)

    # The set of diagnostic sets, comma delimited
    diag_set = models.CharField(max_length=100, default='')

    # The path to the obs data
    obs_path = models.CharField(max_length=200, default='')

    # The path to the model data
    model_path = models.CharField(max_length=200, default='')

    # The output data path
    output_path = models.CharField(max_length=200, default='')

    # The run config name
    name = models.CharField(max_length=100, default='default')

    # The set of authorized users
    allowed_users = models.TextField()
