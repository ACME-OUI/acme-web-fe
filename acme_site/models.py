from django.db import models

class Organizations(models.Model):
    name = models.CharField(max_length=512, unique=True, blank=False)

    def __str__(self):
        return self.name

class Repos(models.Model):
    name = models.CharField(max_length=512, unique=True, blank=False)
    organization = models.ManyToManyField(Organizations, blank=False)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=512, unique=True, blank=False)
    desc = models.CharField(max_length=2048, unique=True, blank=False)
    repo = models.ManyToManyField(Repos, blank=False)

    def __str__(self):
        return self.name

class Issues(models.Model):
    author = models.CharField(max_length=512, unique=True, blank=False)
    github = models.CharField(max_length=512, unique=True, blank=False)
    jira   = models.CharField(max_length=512, unique=True, blank=False)
    email  = models.CharField(max_length=512, unique=True, blank=False)
    issues = models.ManyToManyField(Repos, blank=False)
    comment = models.CharField(max_length=512, unique=True, blank=False)
