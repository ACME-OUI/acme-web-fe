# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ESGFNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(default=b'default_node', max_length=100)),
                ('last_seen', models.DateTimeField(default=datetime.datetime(2016, 6, 27, 13, 48, 2, 541226))),
                ('available', models.BooleanField(default=False)),
                ('host', models.CharField(default=b'unknown host', max_length=100)),
                ('node_data', jsonfield.fields.JSONField()),
            ],
        ),
    ]
