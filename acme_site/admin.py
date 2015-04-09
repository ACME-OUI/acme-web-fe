from django.contrib import admin
from acme_site.models import Organizations, Repos, Tags, Issues
# Register your models here.

admin.site.register(Organizations)
admin.site.register(Repos)
admin.site.register(Tags)
admin.site.register(Issues)
