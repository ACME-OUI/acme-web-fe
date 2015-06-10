from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings


class Command(BaseCommand):
    help = "Sync groups out of settings.py"

    def handle(self, *args, **options):
        groups = settings.DEFAULT_GROUPS
        for groupname in groups:

            try:
                g = Group.objects.get(name=groupname)
            except Group.DoesNotExist:
                g = Group()
                g.name = groupname
                g.save()

            if g.name == "Default":
                g.users = User.objects.all()

            g.permissions = []
            for permission in groups[groupname]:
                try:
                    p = Permission.objects.get(codename=permission)
                    g.permissions.add(p)
                except Permission.DoesNotExist:
                    if permission[0] == "*":
                        permissions = Permission.objects.filter(content_type__model=permission.split("_")[1])
                        for p in permissions:
                            g.permissions.add(p)
            g.save()
